from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.deep_learning import DLModel, BacktestResult


async def compare_models(db: AsyncSession, model_ids: list[int]) -> list[dict]:
    results = []
    for mid in model_ids:
        model_r = await db.execute(select(DLModel).where(DLModel.id == mid))
        model = model_r.scalars().first()
        if not model:
            continue

        bt_r = await db.execute(
            select(BacktestResult).where(BacktestResult.model_id == mid)
        )
        backtests = bt_r.scalars().all()

        avg_accuracy = sum(b.sku_accuracy for b in backtests) / len(backtests) if backtests else 0
        avg_usage = sum(b.usage_rate for b in backtests) / len(backtests) if backtests else 0

        results.append({
            "model_id": mid,
            "model_name": model.model_name,
            "model_type": model.model_type,
            "status": model.status,
            "train_accuracy": model.train_accuracy,
            "avg_backtest_accuracy": round(avg_accuracy, 4),
            "avg_usage_rate": round(avg_usage, 4),
            "backtest_count": len(backtests),
        })

    return results
