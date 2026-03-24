"""LLM 검증 서비스 - API 실패 시 폴백으로 추천은 계속 진행"""

import logging
from datetime import datetime

from openai import AsyncOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.recommendation import Recommendation
from models.analysis import SkuAnalysis
from models.llm import LLMReview
from engines.llm.prompt_builder import build_review_prompt
from engines.llm.response_parser import parse_llm_response

logger = logging.getLogger(__name__)


async def review_recommendations(
    db: AsyncSession,
    recommendation_ids: list[int],
    review_level: str = "light",
) -> list[LLMReview]:
    if not settings.OPENAI_API_KEY:
        logger.warning("OpenAI API 키가 설정되지 않음. LLM 검증을 건너뜁니다.")
        return []

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    reviews = []

    for rec_id in recommendation_ids:
        rec_result = await db.execute(
            select(Recommendation).where(Recommendation.id == rec_id)
        )
        rec = rec_result.scalars().first()
        if not rec:
            continue

        analysis_data = None
        if rec.target_type == "sku":
            sa_result = await db.execute(
                select(SkuAnalysis)
                .where(SkuAnalysis.sku_code == rec.target_key, SkuAnalysis.supplier_code == rec.supplier_code)
                .order_by(SkuAnalysis.analysis_date.desc())
                .limit(1)
            )
            sa = sa_result.scalars().first()
            if sa:
                analysis_data = {
                    "avg_7d": sa.avg_7d,
                    "avg_30d": sa.avg_30d,
                    "avg_same_weekday": sa.avg_same_weekday,
                    "repetition_rate": sa.repetition_rate,
                    "volatility": sa.volatility,
                }

        rec_data = {
            "target_date": str(rec.target_date),
            "supplier_code": rec.supplier_code,
            "target_type": rec.target_type,
            "target_key": rec.target_key,
            "rule_based_qty": rec.rule_based_qty,
            "dl_predicted_qty": rec.dl_predicted_qty,
            "final_recommended_qty": rec.final_recommended_qty,
            "risk_level": rec.risk_level,
        }

        prompt = build_review_prompt(rec_data, analysis_data, review_level)

        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000,
            )
            output_text = response.choices[0].message.content or ""
            token_used = float(response.usage.total_tokens) if response.usage else 0.0
            parsed = parse_llm_response(output_text)

            rec.llm_review_result = parsed.get("action", "approve")
            rec.llm_reason = parsed.get("reason", "")[:2000]
            rec.status = "llm_reviewed"

            if parsed.get("action") == "adjust" and parsed.get("adjusted_qty"):
                rec.final_recommended_qty = int(parsed["adjusted_qty"])

            review = LLMReview(
                recommendation_id=rec_id,
                review_type=review_level,
                input_summary=prompt[:5000],
                output_result=output_text[:5000],
                action_suggestion=parsed.get("action"),
                risk_signals=str(parsed.get("risk_signals", [])),
                reason_text=parsed.get("reason", ""),
                token_used=token_used,
                reviewed_at=datetime.now(),
            )
            db.add(review)
            reviews.append(review)

        except Exception as e:
            logger.error(f"LLM 검증 실패 (rec_id={rec_id}): {e}")
            review = LLMReview(
                recommendation_id=rec_id,
                review_type=review_level,
                input_summary=prompt[:5000],
                output_result=f"API 오류: {str(e)[:500]}",
                action_suggestion="fallback",
                reason_text="LLM API 호출 실패로 규칙기반 값 유지",
                token_used=0.0,
                reviewed_at=datetime.now(),
            )
            db.add(review)
            reviews.append(review)

    await db.commit()
    return reviews
