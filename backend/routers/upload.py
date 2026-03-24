from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.upload import UploadFileOut, UploadFileDetail, UploadRecordOut
from services.upload_service import save_upload_file, get_upload_files, get_upload_file_detail, get_upload_records

router = APIRouter(prefix="/api/upload", tags=["업로드"])


@router.post("", response_model=UploadFileOut)
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db)):
    try:
        result = await save_upload_file(file, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[UploadFileOut])
async def list_uploads(active_only: bool = True, db: AsyncSession = Depends(get_db)):
    return await get_upload_files(db, active_only)


@router.get("/{file_id}", response_model=UploadFileOut)
async def get_upload(file_id: int, db: AsyncSession = Depends(get_db)):
    result = await get_upload_file_detail(db, file_id)
    if not result:
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    return result


@router.get("/{file_id}/records", response_model=list[UploadRecordOut])
async def get_records(file_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await get_upload_records(db, file_id, skip, limit)
