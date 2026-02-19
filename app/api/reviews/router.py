from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.main.mysql import get_db
from app.api.reviews.service import ReviewService
from app.api.reviews.schemas import (
    ReviewCreateRequest,
    ReviewResponse,
    ReviewFilter,
    ReviewUpdateRequest,
)
from app.utils.schema_utils import JWTPayloadSchema, CustomResponse
from app.dependencies.authentication import get_current_user

review_router = APIRouter()


@review_router.post("", response_model=CustomResponse[ReviewResponse])
async def create_review(
    request: ReviewCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await ReviewService(db, current_user).create_review(request)


@review_router.get("", response_model=CustomResponse[list[ReviewResponse]])
async def list_reviews(
    db: Annotated[Session, Depends(get_db)],
    book_id: int | None = Query(default=None),
    reviewer_id: int | None = Query(default=None),
    status: int | None = Query(default=None),
):
    filter_params = ReviewFilter(
        book_id=book_id, reviewer_id=reviewer_id, status=status
    )
    return await ReviewService(db).list_reviews(filter_params)


@review_router.put("/{review_id}", response_model=CustomResponse[ReviewResponse])
async def update_review(
    review_id: int,
    request: ReviewUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await ReviewService(db, current_user).update_review(review_id, request)


@review_router.delete("/{review_id}", response_model=CustomResponse[None])
async def delete_review(
    review_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await ReviewService(db, current_user).delete_review(review_id)
