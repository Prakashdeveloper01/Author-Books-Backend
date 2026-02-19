from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String
from app.models.base_class import Base
from app.utils.schema_utils import CustomModel
from pydantic import Field


class ReviewsBaseModel(CustomModel):
    review_id: int | None = Field(default=None)
    book_id: int | None = Field(default=None)
    reviewer_id: int | None = Field(default=None)
    rating: int | None = Field(default=None)
    comment: str | None = Field(default=None)
    status: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)


class TblReviews(Base):
    __tablename__ = "reviews"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False
    )

    reviewer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.usr_id", ondelete="CASCADE"), nullable=False
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[int] = mapped_column(
        "review_status",
        Integer,
        default=0,  # 0=PENDING, 1=APPROVED, 2=REJECTED
    )

    created_at: Mapped[datetime] = mapped_column(
        "review_createdAt", DateTime, default=datetime.utcnow
    )


    @classmethod
    def create(cls, data: ReviewsBaseModel, db: Session) -> "TblReviews":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data

    @classmethod
    def update(cls, data: ReviewsBaseModel, db: Session) -> None:
        """Update the record."""
        user = db.query(cls).filter(cls.review_id == data.review_id).first()
        if user:
            data_dict = data.model_dump(by_alias=False, exclude_none=True)
            for field, value in data_dict.items():
                setattr(user, field, value)
            db.flush()
            db.refresh(user)