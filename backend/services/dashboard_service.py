from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.upload import UploadFile
from models.recommendation import Recommendation
from models.stock import PrepackStock
from models.validation import ValidationResult


async def get_dashboard_summary(db: AsyncSession) -> dict:
    uploads = await db.execute(select(func.count(UploadFile.id)).where(UploadFile.is_active == True))
    recs = await db.execute(select(func.count(Recommendation.id)))
    pending = await db.execute(select(func.count(Recommendation.id)).where(Recommendation.status == "pending"))
    stocks = await db.execute(select(func.count(PrepackStock.id)).where(PrepackStock.status == "active"))
    vals = await db.execute(select(func.avg(ValidationResult.accuracy)))

    return {
        "active_uploads": uploads.scalar() or 0,
        "total_recommendations": recs.scalar() or 0,
        "pending_recommendations": pending.scalar() or 0,
        "active_stocks": stocks.scalar() or 0,
        "avg_accuracy": round(float(vals.scalar() or 0), 4),
    }
