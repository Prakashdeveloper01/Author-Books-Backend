from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer
from app.models.base_class import Base
from app.utils.schema_utils import CustomModel
from pydantic import Field


class BookDownloadsBaseModel(CustomModel):
    download_id: int | None = Field(default=None)
    book_id: int | None = Field(default=None)
    user_id: int | None = Field(default=None)
    downloaded_at: datetime | None = Field(default=None)


class TblBookDownloads(Base):
    __tablename__ = "book_downloads"

    download_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.usr_id", ondelete="CASCADE"), nullable=False
    )

    downloaded_at: Mapped[datetime] = mapped_column(
        "downloaded_at", DateTime, default=datetime.utcnow
    )


    @classmethod
    def create(cls, data: BookDownloadsBaseModel, db: Session) -> "TblBookDownloads":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data

    @classmethod
    def get_by_book_id(cls, book_id: int, db: Session) -> "TblBookDownloads":
        """Get book downloads by book id."""
        return db.query(cls).filter(cls.book_id == book_id).first()

    @classmethod
    def get_by_user_id(cls, user_id: int, db: Session) -> "TblBookDownloads":
        """Get book downloads by user id."""
        return db.query(cls).filter(cls.user_id == user_id).first()