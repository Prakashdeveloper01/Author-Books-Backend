from datetime import datetime
from pydantic import Field
from app.utils.schema_utils import CustomModel


class ReviewCreateRequest(CustomModel):
    book_id: int = Field(..., description="ID of the book being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str | None = Field(default=None)


class ReviewUpdateRequest(CustomModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = Field(default=None)
    status: int | None = Field(
        default=None, description="0=PENDING, 1=APPROVED, 2=REJECTED"
    )


class ReviewResponse(CustomModel):
    review_id: int | None = Field(default=None)
    book_id: int | None = Field(default=None)
    reviewer_id: int | None = Field(default=None)
    rating: int | None = Field(default=None)
    comment: str | None = Field(default=None)
    status: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)


class ReviewFilter(CustomModel):
    book_id: int | None = Field(default=None)
    reviewer_id: int | None = Field(default=None)
    status: int | None = Field(default=None)
