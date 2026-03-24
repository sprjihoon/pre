from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class LLMReview(Base):
    __tablename__ = "llm_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"))
    review_type: Mapped[str] = mapped_column(String(50))
    input_summary: Mapped[str | None] = mapped_column(String(5000), nullable=True)
    output_result: Mapped[str | None] = mapped_column(String(5000), nullable=True)
    action_suggestion: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    risk_signals: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    reason_text: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    token_used: Mapped[float] = mapped_column(Float, default=0.0)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    recommendation: Mapped["Recommendation"] = relationship(back_populates="llm_reviews")


from models.recommendation import Recommendation
