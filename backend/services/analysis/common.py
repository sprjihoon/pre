from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.upload import UploadRecord, UploadFile


async def get_active_records(db: AsyncSession, supplier_code: str | None = None):
    q = (
        select(UploadRecord)
        .join(UploadFile)
        .where(UploadFile.is_active == True)
    )
    if supplier_code:
        q = q.where(UploadRecord.supplier_code == supplier_code)
    result = await db.execute(q)
    return result.scalars().all()
