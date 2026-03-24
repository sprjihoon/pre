from datetime import date, datetime
from sqlalchemy import String, Integer, Float, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    target_date: Mapped[date] = mapped_column(Date, index=True)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    target_type: Mapped[str] = mapped_column(String(20))  # 'sku' | 'combination'
    target_key: Mapped[str] = mapped_column(String(500))
    rule_based_qty: Mapped[int] = mapped_column(Integer, default=0)
    dl_predicted_qty: Mapped[int | None] = mapped_column(Integer, nullable=True)
    final_recommended_qty: Mapped[int] = mapped_column(Integer, default=0)
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    llm_review_result: Mapped[str | None] = mapped_column(String(50), nullable=True)
    llm_reason: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    approval: Mapped["Approval | None"] = relationship(back_populates="recommendation", uselist=False)
    llm_reviews: Mapped[list["LLMReview"]] = relationship(back_populates="recommendation")


from models.approval import Approval
from models.llm import LLMReview
