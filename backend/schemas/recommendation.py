from datetime import date, datetime
from pydantic import BaseModel


class RecommendationOut(BaseModel):
    id: int
    target_date: date
    supplier_code: str
    target_type: str
    target_key: str
    rule_based_qty: int
    dl_predicted_qty: int | None
    final_recommended_qty: int
    confidence_score: float | None
    risk_level: str | None
    llm_review_result: str | None
    llm_reason: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RecommendationGenerateRequest(BaseModel):
    target_date: date
    supplier_code: str | None = None


class ApprovalRequest(BaseModel):
    action: str  # 'approved' | 'modified' | 'rejected'
    approved_qty: int | None = None
    memo: str | None = None


class ApprovalOut(BaseModel):
    id: int
    recommendation_id: int
    action: str
    approved_qty: int | None
    memo: str | None
    approved_at: datetime

    model_config = {"from_attributes": True}


class ExecutionRequest(BaseModel):
    actual_packed_qty: int


class ExecutionUpdateRequest(BaseModel):
    used_qty: int | None = None
    remaining_qty: int | None = None
    status: str | None = None


class ExecutionOut(BaseModel):
    id: int
    approval_id: int
    actual_packed_qty: int
    used_qty: int
    remaining_qty: int
    status: str
    executed_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}
