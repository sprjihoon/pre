import os
import uuid
from datetime import datetime

from fastapi import UploadFile as FastAPIUploadFile
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models.upload import UploadFile, UploadRecord
from services.parser_service import parse_file


async def save_upload_file(file: FastAPIUploadFile, db: AsyncSession) -> UploadFile:
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in (".xlsx", ".xls", ".csv"):
        raise ValueError("지원하지 않는 파일 형식입니다. xlsx, xls, csv만 가능합니다.")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    records_data = parse_file(file_path, ext)
    if not records_data:
        raise ValueError("파일에서 유효한 레코드를 찾을 수 없습니다.")

    dates = [r["order_date"] for r in records_data]
    date_start = min(dates)
    date_end = max(dates)

    existing = await db.execute(
        select(UploadFile).where(
            UploadFile.date_range_start == date_start,
            UploadFile.date_range_end == date_end,
            UploadFile.is_active == True,
        )
    )
    prev = existing.scalars().first()
    version = 1
    if prev:
        version = prev.version + 1
        await db.execute(
            update(UploadFile)
            .where(UploadFile.id == prev.id)
            .values(is_active=False, status="superseded")
        )

    upload_file = UploadFile(
        filename=unique_name,
        original_filename=file.filename or "unknown",
        file_type=ext.lstrip("."),
        file_path=file_path,
        date_range_start=date_start,
        date_range_end=date_end,
        uploaded_at=datetime.now(),
        status="active",
        record_count=len(records_data),
        version=version,
        is_active=True,
    )
    db.add(upload_file)
    await db.flush()

    for rd in records_data:
        rec = UploadRecord(
            upload_file_id=upload_file.id,
            order_date=rd["order_date"],
            supplier_code=rd["supplier_code"],
            supplier_name=rd["supplier_name"],
            sku_code=rd["sku_code"],
            sku_name=rd["sku_name"],
            option_name=rd.get("option_name"),
            quantity=rd["quantity"],
            combination_key=rd.get("combination_key"),
        )
        db.add(rec)

    await db.commit()
    await db.refresh(upload_file)
    return upload_file


async def get_upload_files(db: AsyncSession, active_only: bool = True) -> list[UploadFile]:
    q = select(UploadFile).order_by(UploadFile.uploaded_at.desc())
    if active_only:
        q = q.where(UploadFile.is_active == True)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_upload_file_detail(db: AsyncSession, file_id: int) -> UploadFile | None:
    result = await db.execute(
        select(UploadFile).where(UploadFile.id == file_id)
    )
    return result.scalars().first()


async def get_upload_records(
    db: AsyncSession, file_id: int, skip: int = 0, limit: int = 100
) -> list[UploadRecord]:
    result = await db.execute(
        select(UploadRecord)
        .where(UploadRecord.upload_file_id == file_id)
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())
