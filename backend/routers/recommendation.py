from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.recommendation import (
    RecommendationOut, ApprovalRequest, ApprovalOut,
    ExecutionRequest, ExecutionUpdateRequest, ExecutionOut,
)
from services.recommendation import (
    get_recommendations, approve_recommendation,
    create_execution, update_execution,
)

router = APIRouter(prefix="/api/recommendation", tags=["추천/승인"])


@router.get("", response_model=list[RecommendationOut])
async def list_recommendations(
    target_date: date = Query(default=None),
    supplier_code: str = Query(default=None),
    status: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    return await get_recommendations(db, target_date, supplier_code, status)


@router.post("/{rec_id}/approve", response_model=ApprovalOut)
async def approve(rec_id: int, body: ApprovalRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await approve_recommendation(db, rec_id, body.action, body.approved_qty, body.memo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{rec_id}/execute", response_model=ExecutionOut)
async def execute(rec_id: int, body: ExecutionRequest, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    from models.approval import Approval
    result = await db.execute(select(Approval).where(Approval.recommendation_id == rec_id))
    approval = result.scalars().first()
    if not approval:
        raise HTTPException(status_code=404, detail="승인 정보를 찾을 수 없습니다.")
    try:
        return await create_execution(db, approval.id, body.actual_packed_qty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/execution/{exec_id}", response_model=ExecutionOut)
async def update_exec(exec_id: int, body: ExecutionUpdateRequest, db: AsyncSession = Depends(get_db)):
    try:
        return await update_execution(db, exec_id, body.used_qty, body.remaining_qty, body.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
