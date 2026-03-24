from datetime import date, datetime
from pydantic import BaseModel


class UploadRecordOut(BaseModel):
    id: int
    order_date: date
    supplier_code: str
    supplier_name: str
    sku_code: str
    sku_name: str
    option_name: str | None
    quantity: int
    combination_key: str | None

    model_config = {"from_attributes": True}


class UploadFileOut(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    date_range_start: date | None
    date_range_end: date | None
    uploaded_at: datetime
    status: str
    record_count: int
    version: int
    is_active: bool

    model_config = {"from_attributes": True}


class UploadFileDetail(UploadFileOut):
    records: list[UploadRecordOut] = []
