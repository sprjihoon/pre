from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class LocationMaster(Base):
    __tablename__ = "location_masters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_code: Mapped[str] = mapped_column(String(50), unique=True)
    zone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    current_sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    current_combination: Mapped[str | None] = mapped_column(String(500), nullable=True)

    histories: Mapped[list["LocationHistory"]] = relationship(back_populates="location")


class LocationHistory(Base):
    __tablename__ = "location_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("location_masters.id"))
    action: Mapped[str] = mapped_column(String(50))
    target_key: Mapped[str | None] = mapped_column(String(500), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    action_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    memo: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    location: Mapped["LocationMaster"] = relationship(back_populates="histories")
