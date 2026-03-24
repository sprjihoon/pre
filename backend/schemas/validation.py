from datetime import date
from pydantic import BaseModel


class ValidationResultOut(BaseModel):
    id: int
    target_date: date
    supplier_code: str
    target_key: str
    predicted_qty: int
    actual_qty: int
    accuracy: float
    usage_rate: float
    unwrap_rate: float
    is_overpredict: bool
    is_underpredict: bool

    model_config = {"from_attributes": True}


class ValidationRunRequest(BaseModel):
    target_date: date
    supplier_code: str | None = None


class ReportSummary(BaseModel):
    period_start: date
    period_end: date
    supplier_code: str | None
    total_predictions: int
    avg_accuracy: float
    avg_usage_rate: float
    avg_unwrap_rate: float
    overpredict_count: int
    underpredict_count: int
