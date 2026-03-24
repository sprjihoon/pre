from datetime import date, datetime
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class UploadFile(Base):
    __tablename__ = "upload_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(500))
    original_filename: Mapped[str] = mapped_column(String(500))
    file_type: Mapped[str] = mapped_column(String(10))
    file_path: Mapped[str] = mapped_column(String(1000))
    date_range_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_range_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[str] = mapped_column(String(20), default="active")
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    records: Mapped[list["UploadRecord"]] = relationship(back_populates="upload_file", cascade="all, delete-orphan")


class UploadRecord(Base):
    __tablename__ = "upload_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    upload_file_id: Mapped[int] = mapped_column(ForeignKey("upload_files.id"))
    order_date: Mapped[date] = mapped_column(Date)
    supplier_code: Mapped[str] = mapped_column(String(50), index=True)
    supplier_name: Mapped[str] = mapped_column(String(200))
    sku_code: Mapped[str] = mapped_column(String(100), index=True)
    sku_name: Mapped[str] = mapped_column(String(500))
    option_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    combination_key: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)

    upload_file: Mapped["UploadFile"] = relationship(back_populates="records")
