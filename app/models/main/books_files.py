from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String
from app.models.base_class import Base
from app.utils.schema_utils import CustomModel
from pydantic import Field


class BookFilesBaseModel(CustomModel):
    file_id: int | None = Field(default=None)
    book_id: int | None = Field(default=None)
    file_type: str | None = Field(default=None)
    file_url: str | None = Field(default=None)
    file_size: int | None = Field(default=None)
    version: int | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    uploaded_at: datetime | None = Field(default=None)


class TblBookFiles(Base):
    __tablename__ = "book_files"

    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )

    file_type: Mapped[str] = mapped_column(
        "file_type", String(20), nullable=False
    )  # PDF, EPUB
    file_url: Mapped[str] = mapped_column("file_url", Text, nullable=False)
    file_size: Mapped[int] = mapped_column("file_size", Integer, nullable=True)

    version: Mapped[int] = mapped_column("file_version", Integer, default=1)
    is_active: Mapped[bool] = mapped_column("file_isActive", Boolean, default=True)

    uploaded_at: Mapped[datetime] = mapped_column(
        "file_uploadedAt", DateTime, default=datetime.utcnow
    )

    @classmethod
    def create(cls, data: BookFilesBaseModel, db: Session) -> "TblBookFiles":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data

    @classmethod
    def update(cls, data: BookFilesBaseModel, db: Session) -> None:
        """Update the record."""
        user = db.query(cls).filter(cls.file_id == data.file_id).first()
        if user:
            data_dict = data.model_dump(by_alias=False, exclude_none=True)
            for field, value in data_dict.items():
                setattr(user, field, value)
            db.flush()
            db.refresh(user)

    @classmethod
    def get_by_book_id(cls, book_id: int, db: Session) -> "TblBookFiles":
        """Get book files by book id."""
        return db.query(cls).filter(cls.book_id == book_id).first()
