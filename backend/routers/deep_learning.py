from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.deep_learning import (
    DLModelOut, TrainRequest, PredictRequest, PredictResult,
    BacktestRequest, BacktestResultOut,
)
from engines.deep_learning.train_service import train_model
from engines.deep_learning.predict_service import predict
from engines.deep_learning.backtest_service import run_backtest
from engines.deep_learning.model_registry import get_models, get_model, activate_model, get_backtest_results
from engines.deep_learning.evaluation_service import compare_models

router = APIRouter(prefix="/api/dl", tags=["딥러닝"])


@router.post("/train", response_model=DLModelOut)
async def train(body: TrainRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await train_model(
            db, body.model_type, body.supplier_code,
            body.epochs, body.batch_size, body.learning_rate, body.lookback_days,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/predict", response_model=list[PredictResult])
async def do_predict(body: PredictRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await predict(db, body.model_id, body.target_date, body.supplier_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/backtest", response_model=BacktestResultOut)
async def do_backtest(body: BacktestRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await run_backtest(db, body.model_id, body.test_start, body.test_end, body.supplier_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/models", response_model=list[DLModelOut])
async def list_models(status: str = Query(default=None), db: AsyncSession = Depends(get_db)):
    return await get_models(db, status)


@router.post("/models/{model_id}/activate", response_model=DLModelOut)
async def activate(model_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await activate_model(db, model_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/models/{model_id}/backtests", response_model=list[BacktestResultOut])
async def list_backtests(model_id: int, db: AsyncSession = Depends(get_db)):
    return await get_backtest_results(db, model_id)


@router.post("/compare")
async def compare(model_ids: list[int], db: AsyncSession = Depends(get_db)):
    return await compare_models(db, model_ids)
