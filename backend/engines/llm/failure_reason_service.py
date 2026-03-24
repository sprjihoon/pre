import logging
from datetime import datetime

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from engines.llm.prompt_builder import build_failure_analysis_prompt
from engines.llm.response_parser import parse_llm_response

logger = logging.getLogger(__name__)


async def analyze_failures(
    db: AsyncSession,
    validation_results: list[dict],
) -> dict:
    if not settings.OPENAI_API_KEY:
        return {"error": "OpenAI API 키가 설정되지 않았습니다."}

    prompt = build_failure_analysis_prompt(validation_results)
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
        )
        output = response.choices[0].message.content or ""
        return parse_llm_response(output)

    except Exception as e:
        logger.error(f"실패 분석 LLM 호출 오류: {e}")
        return {"error": str(e)}
