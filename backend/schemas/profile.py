from datetime import date
from pydantic import BaseModel


class SupplierProfileCreate(BaseModel):
    supplier_code: str
    supplier_name: str
    min_prepack_qty: int = 5
    combination_priority: bool = False
    recent_weight: float = 0.7
    weekday_weight: float = 0.3
    new_sku_exclude_days: int = 7
    overpredict_penalty: float = 1.0
    conservative_mode: bool = False
    preferred_model: str | None = None
    llm_review_level: str = "light"


class SupplierProfileUpdate(BaseModel):
    supplier_name: str | None = None
    min_prepack_qty: int | None = None
    combination_priority: bool | None = None
    recent_weight: float | None = None
    weekday_weight: float | None = None
    new_sku_exclude_days: int | None = None
    overpredict_penalty: float | None = None
    conservative_mode: bool | None = None
    preferred_model: str | None = None
    llm_review_level: str | None = None


class SupplierProfileOut(BaseModel):
    id: int
    supplier_code: str
    supplier_name: str
    min_prepack_qty: int
    combination_priority: bool
    recent_weight: float
    weekday_weight: float
    new_sku_exclude_days: int
    overpredict_penalty: float
    conservative_mode: bool
    preferred_model: str | None
    llm_review_level: str

    model_config = {"from_attributes": True}


class ExclusionRuleCreate(BaseModel):
    supplier_code: str
    target_type: str
    target_key: str
    reason: str | None = None
    exclude_until: date | None = None


class ExclusionRuleOut(BaseModel):
    id: int
    supplier_code: str
    target_type: str
    target_key: str
    reason: str | None
    exclude_until: date | None
    is_active: bool

    model_config = {"from_attributes": True}
