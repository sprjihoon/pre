from datetime import datetime
from pydantic import BaseModel


class LLMReviewOut(BaseModel):
    id: int
    recommendation_id: int
    review_type: str
    input_summary: str | None
    output_result: str | None
    action_suggestion: str | None
    risk_signals: str | None
    reason_text: str | None
    token_used: float
    reviewed_at: datetime

    model_config = {"from_attributes": True}


class LLMReviewRequest(BaseModel):
    recommendation_ids: list[int]
    review_level: str = "light"  # 'light' | 'full'
