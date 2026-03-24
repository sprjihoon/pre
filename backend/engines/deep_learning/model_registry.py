from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.deep_learning import DLModel, BacktestResult


async def get_models(db: AsyncSession, status: str | None = None) -> list[DLModel]:
    q = select(DLModel).order_by(DLModel.trained_at.desc())
    if status:
        q = q.where(DLModel.status == status)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_model(db: AsyncSession, model_id: int) -> DLModel | None:
    result = await db.execute(select(DLModel).where(DLModel.id == model_id))
    return result.scalars().first()


async def activate_model(db: AsyncSession, model_id: int) -> DLModel:
    model = await get_model(db, model_id)
    if not model:
        raise ValueError("모델을 찾을 수 없습니다.")

    bt_result = await db.execute(
        select(BacktestResult).where(BacktestResult.model_id == model_id)
    )
    backtests = bt_result.scalars().all()
    if not backtests:
        raise ValueError("백테스트 결과가 없습니다. 먼저 백테스트를 실행해주세요.")

    best = max(backtests, key=lambda b: b.sku_accuracy)
    if best.sku_accuracy < 0.5:
        raise ValueError(f"백테스트 정확도({best.sku_accuracy:.1%})가 기준(50%) 미만입니다.")

    model.status = "active"
    await db.commit()
    await db.refresh(model)
    return model


async def get_active_model(db: AsyncSession, model_type: str | None = None) -> DLModel | None:
    q = select(DLModel).where(DLModel.status == "active")
    if model_type:
        q = q.where(DLModel.model_type == model_type)
    q = q.order_by(DLModel.trained_at.desc())
    result = await db.execute(q)
    return result.scalars().first()


async def get_backtest_results(db: AsyncSession, model_id: int) -> list[BacktestResult]:
    result = await db.execute(
        select(BacktestResult).where(BacktestResult.model_id == model_id).order_by(BacktestResult.tested_at.desc())
    )
    return list(result.scalars().all())
