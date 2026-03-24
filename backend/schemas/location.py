from datetime import datetime
from pydantic import BaseModel


class LocationMasterCreate(BaseModel):
    location_code: str
    zone: str | None = None
    description: str | None = None


class LocationMasterOut(BaseModel):
    id: int
    location_code: str
    zone: str | None
    description: str | None
    is_active: bool
    current_sku: str | None
    current_combination: str | None

    model_config = {"from_attributes": True}


class LocationHistoryOut(BaseModel):
    id: int
    location_id: int
    action: str
    target_key: str | None
    quantity: int
    action_at: datetime
    memo: str | None

    model_config = {"from_attributes": True}


class LocationAssignRequest(BaseModel):
    target_key: str
    target_type: str  # 'sku' | 'combination'
    quantity: int
    memo: str | None = None


class StockOut(BaseModel):
    id: int
    target_type: str
    target_key: str
    supplier_code: str
    current_qty: int
    location_code: str | None
    status: str
    last_updated: datetime

    model_config = {"from_attributes": True}


class UnwrapRequest(BaseModel):
    stock_id: int
    unwrap_qty: int
    reason: str | None = None
    is_returned: bool = False
    return_location: str | None = None


class UnwrapOut(BaseModel):
    id: int
    stock_id: int
    unwrap_qty: int
    reason: str | None
    is_returned: bool
    return_location: str | None
    unwrapped_at: datetime

    model_config = {"from_attributes": True}
