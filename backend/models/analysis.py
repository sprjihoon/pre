from datetime import date
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class SkuAnalysis(Base):
    __tablename__ = "sku_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sku_code: Mapped[str] = mapped_column(String(100), index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    analysis_date: Mapped[date] = mapped_column(Date)
    avg_7d: Mapped[float] = mapped_column(Float, default=0.0)
    avg_30d: Mapped[float] = mapped_column(Float, default=0.0)
    avg_same_weekday: Mapped[float] = mapped_column(Float, default=0.0)
    repetition_rate: Mapped[float] = mapped_column(Float, default=0.0)
    volatility: Mapped[float] = mapped_column(Float, default=0.0)
    total_days_appeared: Mapped[int] = mapped_column(Integer, default=0)
    consecutive_days: Mapped[int] = mapped_column(Integer, default=0)


class CombinationAnalysis(Base):
    __tablename__ = "combination_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    combination_key: Mapped[str] = mapped_column(String(500), index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    analysis_date: Mapped[date] = mapped_column(Date)
    occurrence_rate: Mapped[float] = mapped_column(Float, default=0.0)
    avg_quantity: Mapped[float] = mapped_column(Float, default=0.0)
    repetition_rate: Mapped[float] = mapped_column(Float, default=0.0)
    total_occurrences: Mapped[int] = mapped_column(Integer, default=0)
