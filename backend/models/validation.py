from datetime import date
from sqlalchemy import String, Integer, Float, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class ValidationResult(Base):
    __tablename__ = "validation_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_date: Mapped[date] = mapped_column(Date, index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    target_key: Mapped[str] = mapped_column(String(500))
    predicted_qty: Mapped[int] = mapped_column(Integer, default=0)
    actual_qty: Mapped[int] = mapped_column(Integer, default=0)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    usage_rate: Mapped[float] = mapped_column(Float, default=0.0)
    unwrap_rate: Mapped[float] = mapped_column(Float, default=0.0)
    is_overpredict: Mapped[bool] = mapped_column(Boolean, default=False)
    is_underpredict: Mapped[bool] = mapped_column(Boolean, default=False)
