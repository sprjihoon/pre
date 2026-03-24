from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class DLModel(Base):
    __tablename__ = "dl_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(200))
    model_version: Mapped[str] = mapped_column(String(50))
    model_type: Mapped[str] = mapped_column(String(50))  # 'lstm' | 'transformer'
    file_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    train_accuracy: Mapped[float | None] = mapped_column(Float, nullable=True)
    trained_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    training_params: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    backtest_results: Mapped[list["BacktestResult"]] = relationship(back_populates="model")


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("dl_models.id"))
    test_start: Mapped[date] = mapped_column(Date)
    test_end: Mapped[date] = mapped_column(Date)
    supplier_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sku_accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    combination_hit_rate: Mapped[float] = mapped_column(Float, default=0.0)
    threshold_detection_accuracy: Mapped[float] = mapped_column(Float, default=0.0)
    usage_rate: Mapped[float] = mapped_column(Float, default=0.0)
    unwrap_rate: Mapped[float] = mapped_column(Float, default=0.0)
    overpredict_rate: Mapped[float] = mapped_column(Float, default=0.0)
    underpredict_rate: Mapped[float] = mapped_column(Float, default=0.0)
    tested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    model: Mapped["DLModel"] = relationship(back_populates="backtest_results")
