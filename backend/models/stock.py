from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class PrepackStock(Base):
    __tablename__ = "prepack_stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_type: Mapped[str] = mapped_column(String(20))
    target_key: Mapped[str] = mapped_column(String(500), index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    current_qty: Mapped[int] = mapped_column(Integer, default=0)
    location_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active")
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    unwrap_records: Mapped[list["UnwrapRecord"]] = relationship(back_populates="stock")


from models.unwrap import UnwrapRecord
