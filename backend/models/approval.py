from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), unique=True)
    action: Mapped[str] = mapped_column(String(20))  # 'approved' | 'modified' | 'rejected'
    approved_qty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    memo: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    recommendation: Mapped["Recommendation"] = relationship(back_populates="approval")
    execution: Mapped["Execution | None"] = relationship(back_populates="approval", uselist=False)


from models.recommendation import Recommendation
from models.execution import Execution
