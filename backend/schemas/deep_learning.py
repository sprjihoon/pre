from datetime import date, datetime
from pydantic import BaseModel


class DLModelOut(BaseModel):
    id: int
    model_name: str
    model_version: str
    model_type: str
    file_path: str | None
    train_accuracy: float | None
    trained_at: datetime | None
    status: str
    training_params: dict | None

    model_config = {"from_attributes": True}


class TrainRequest(BaseModel):
    model_type: str = "lstm"  # 'lstm' | 'transformer'
    supplier_code: str | None = None
    epochs: int = 50
    batch_size: int = 32
    learning_rate: float = 0.001
    lookback_days: int = 30


class PredictRequest(BaseModel):
    model_id: int
    target_date: date
    supplier_code: str | None = None


class PredictResult(BaseModel):
    target_key: str
    target_type: str
    predicted_qty: int
    confidence: float


class BacktestRequest(BaseModel):
    model_id: int
    test_start: date
    test_end: date
    supplier_code: str | None = None


class BacktestResultOut(BaseModel):
    id: int
    model_id: int
    test_start: date
    test_end: date
    supplier_code: str | None
    sku_accuracy: float
    combination_hit_rate: float
    threshold_detection_accuracy: float
    usage_rate: float
    unwrap_rate: float
    overpredict_rate: float
    underpredict_rate: float
    tested_at: datetime

    model_config = {"from_attributes": True}
