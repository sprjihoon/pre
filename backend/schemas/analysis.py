from datetime import date
from pydantic import BaseModel


class SkuAnalysisOut(BaseModel):
    id: int
    sku_code: str
    supplier_code: str
    analysis_date: date
    avg_7d: float
    avg_30d: float
    avg_same_weekday: float
    repetition_rate: float
    volatility: float
    total_days_appeared: int
    consecutive_days: int

    model_config = {"from_attributes": True}


class CombinationAnalysisOut(BaseModel):
    id: int
    combination_key: str
    supplier_code: str
    analysis_date: date
    occurrence_rate: float
    avg_quantity: float
    repetition_rate: float
    total_occurrences: int

    model_config = {"from_attributes": True}


class AnalysisRequest(BaseModel):
    supplier_code: str | None = None
    analysis_date: date | None = None
