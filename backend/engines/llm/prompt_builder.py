"""LLM 프롬프트 빌더 - 추천 검증용 프롬프트 생성"""


def build_review_prompt(
    recommendation: dict,
    analysis: dict | None = None,
    review_level: str = "light",
) -> str:
    base = f"""당신은 물류센터 프리패킹(선포장) 전문가입니다.
아래 프리패킹 추천 내용을 검토하고 의견을 제시해주세요.

## 추천 정보
- 대상 날짜: {recommendation.get('target_date')}
- 업체코드: {recommendation.get('supplier_code')}
- 대상 구분: {recommendation.get('target_type')}
- 대상: {recommendation.get('target_key')}
- 규칙기반 추천 수량: {recommendation.get('rule_based_qty')}
- 딥러닝 예측 수량: {recommendation.get('dl_predicted_qty', '없음')}
- 최종 추천 수량: {recommendation.get('final_recommended_qty')}
- 위험도: {recommendation.get('risk_level', '미평가')}
"""

    if analysis:
        base += f"""
## 분석 데이터
- 7일 평균: {analysis.get('avg_7d', 'N/A')}
- 30일 평균: {analysis.get('avg_30d', 'N/A')}
- 동일 요일 평균: {analysis.get('avg_same_weekday', 'N/A')}
- 반복률: {analysis.get('repetition_rate', 'N/A')}
- 변동성: {analysis.get('volatility', 'N/A')}
"""

    if review_level == "full":
        base += """
## 검토 요청사항
다음 항목을 모두 평가해주세요:
1. 추천 수량의 적정성 (과대/과소 예측 위험)
2. 위험 신호 (급격한 변동, 계절 영향, 이벤트 가능성)
3. 제외 대상 여부 (신규 SKU, 불규칙 패턴)
4. 개선 제안

아래 JSON 형식으로 답변해주세요:
```json
{
  "action": "approve" | "adjust" | "warn" | "exclude",
  "adjusted_qty": null 또는 조정수량,
  "risk_signals": ["위험 신호 목록"],
  "reason": "판단 사유",
  "confidence": 0.0~1.0
}
```"""
    else:
        base += """
## 검토 요청사항
추천 수량의 적정성을 간단히 평가하고, JSON으로 답변해주세요:
```json
{
  "action": "approve" | "adjust" | "warn",
  "reason": "간단한 판단 사유",
  "confidence": 0.0~1.0
}
```"""

    return base


def build_failure_analysis_prompt(validation_results: list[dict]) -> str:
    items = "\n".join(
        f"- {v['target_key']}: 예측 {v['predicted_qty']} / 실제 {v['actual_qty']} (정확도 {v['accuracy']:.1%})"
        for v in validation_results
    )

    return f"""당신은 물류센터 프리패킹 전문가입니다.
아래 예측 실패 사례를 분석하고 원인과 개선 방안을 제시해주세요.

## 실패 사례
{items}

다음 JSON 형식으로 분석해주세요:
```json
{{
  "failure_patterns": ["발견된 패턴"],
  "root_causes": ["근본 원인"],
  "recommendations": ["개선 제안"]
}}
```"""
