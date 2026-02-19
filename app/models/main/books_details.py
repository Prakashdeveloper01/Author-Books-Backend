from sqlalchemy import text
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String
from app.models.base_class import Base
from app.utils.schema_utils import CustomModel
from pydantic import Field

class BookDetailsBaseModel(CustomModel):
    book_id: int | None = Field(default=None)
    description: str | None = Field(default=None)
    language: str | None = Field(default=None)
    isbn: str | None = Field(default=None)
    page_count: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    created_by: int | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    updated_by: int | None = Field(default=None)

class TblBookDetails(Base):
    __tablename__ = "book_details"

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True
    )

    description: Mapped[str] = mapped_column("book_description", Text, nullable=True)
    language: Mapped[str] = mapped_column("book_language", String(50), nullable=True)
    isbn: Mapped[str] = mapped_column("book_isbn", String(20), nullable=True)
    page_count: Mapped[int] = mapped_column("book_pageCount", Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column("book_createdAt", DateTime, nullable=False, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column("book_createdBy", Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column("book_updatedAt", TIMESTAMP, nullable=True, server_default=text("NULL ON UPDATE current_timestamp()"))
    updated_by: Mapped[int] = mapped_column("book_updatedBy", Integer, nullable=True)

    @classmethod
    def create(cls, data: BookDetailsBaseModel,db: Session) -> "TblBookDetails":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data

    @classmethod
    def update(cls,data:BookDetailsBaseModel,db:Session)->None:
        """Update the record."""
        user = db.query(cls).filter(cls.book_id==data.book_id).first()
        if user:

            data_dict = data.model_dump(by_alias=False, exclude_none=True)
            for field, value in data_dict.items():
                setattr(user, field, value)
            db.flush()
            db.refresh(user)

    @classmethod
    def get_by_book_id(cls,book_id:int,db:Session)->"TblBookDetails":
        """Get book details by book id."""
        return db.query(cls).filter(cls.book_id==book_id).first()

