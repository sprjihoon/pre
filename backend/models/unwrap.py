from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class UnwrapRecord(Base):
    __tablename__ = "unwrap_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("prepack_stocks.id"))
    unwrap_qty: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_returned: Mapped[bool] = mapped_column(Boolean, default=False)
    return_location: Mapped[str | None] = mapped_column(String(50), nullable=True)
    unwrapped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    stock: Mapped["PrepackStock"] = relationship(back_populates="unwrap_records")


from models.stock import PrepackStock
