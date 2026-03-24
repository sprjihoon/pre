from datetime import date
from sqlalchemy import String, Integer, Float, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class SupplierProfile(Base):
    __tablename__ = "supplier_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supplier_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    supplier_name: Mapped[str] = mapped_column(String(200))
    min_prepack_qty: Mapped[int] = mapped_column(Integer, default=5)
    combination_priority: Mapped[bool] = mapped_column(Boolean, default=False)
    recent_weight: Mapped[float] = mapped_column(Float, default=0.7)
    weekday_weight: Mapped[float] = mapped_column(Float, default=0.3)
    new_sku_exclude_days: Mapped[int] = mapped_column(Integer, default=7)
    overpredict_penalty: Mapped[float] = mapped_column(Float, default=1.0)
    conservative_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    preferred_model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    llm_review_level: Mapped[str] = mapped_column(String(20), default="light")


class ExclusionRule(Base):
    __tablename__ = "exclusion_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    target_type: Mapped[str] = mapped_column(String(20))
    target_key: Mapped[str] = mapped_column(String(500))
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    exclude_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
