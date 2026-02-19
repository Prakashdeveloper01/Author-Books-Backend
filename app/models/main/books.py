from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String
from app.models.base_class import Base
from app.utils.schema_utils import CustomModel
from pydantic import Field

class BooksBaseModel(CustomModel):
    book_id: int | None = Field(default=None)
    uuid: str | None = Field(default=None)
    title: str | None = Field(default=None)
    author_id: int | None = Field(default=None)
    status: int | None = Field(default=None)
    published_at: datetime | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class TblBooks(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(
        "book_uuid", String(36), nullable=False, unique=True
    )
    title: Mapped[str] = mapped_column("book_title", String(255), nullable=False)

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.usr_id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[int] = mapped_column(
        "book_status",
        Integer,
        nullable=False,
        default=0,  # 0=DRAFT, 1=PUBLISHED, 2=REJECTED
    )

    published_at: Mapped[datetime] = mapped_column(
        "book_publishedAt", DateTime, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        "book_createdAt", DateTime, nullable=False, default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        "book_updatedAt",
        TIMESTAMP,
        nullable=True,
        server_default=text("NULL ON UPDATE current_timestamp()"),
    )

    @classmethod
    def create(cls, data: BooksBaseModel,db: Session) -> "TblBooks":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data


    @classmethod
    def update(cls,data:BooksBaseModel,db:Session)->None:
        """Update the record."""
        user = db.query(cls).filter(cls.uuid==data.uuid).first()
        if user:

            data_dict = data.model_dump(by_alias=False, exclude_none=True)
            for field, value in data_dict.items():
                setattr(user, field, value)
            db.flush()
            db.refresh(user)