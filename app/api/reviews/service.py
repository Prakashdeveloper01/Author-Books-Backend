from datetime import datetime
from typing import Annotated
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.reviews.schemas import (
    ReviewCreateRequest,
    ReviewResponse,
    ReviewFilter,
    ReviewUpdateRequest,
)
from app.models.main.reviews import TblReviews, ReviewsBaseModel
from app.utils.schema_utils import CustomResponse, JWTPayloadSchema
from app.config import CONFIG_SETTINGS


class ReviewService:
    def __init__(self, db: Session, current_user: JWTPayloadSchema | None = None):
        self.db = db
        self.current_user = current_user

    async def create_review(self, request: ReviewCreateRequest):
        """Create a new review."""
        if not self.current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        # Check if already reviewed?
        existing = (
            self.db.query(TblReviews)
            .filter(
                TblReviews.book_id == request.book_id,
                TblReviews.reviewer_id == self.current_user.user_id,
            )
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=400, detail="You have already reviewed this book"
            )

        review_data = ReviewsBaseModel(
            book_id=request.book_id,
            reviewer_id=self.current_user.user_id,
            rating=request.rating,
            comment=request.comment,
            status=0,  # Pending
            created_at=datetime.now(),
        )

        new_review = TblReviews.create(review_data, self.db)
        self.db.commit()

        return CustomResponse(
            status="1",
            status_code=201,
            message="Review submitted successfully",
            data=ReviewResponse(
                review_id=new_review.review_id,
                book_id=new_review.book_id,
                reviewer_id=new_review.reviewer_id,
                rating=new_review.rating,
                comment=new_review.comment,
                status=new_review.status,
                created_at=new_review.created_at,
            ),
        )

    async def list_reviews(self, filter_params: ReviewFilter):
        """List reviews with filters."""
        query = self.db.query(TblReviews)

        if filter_params.book_id:
            query = query.filter(TblReviews.book_id == filter_params.book_id)
        if filter_params.reviewer_id:
            query = query.filter(TblReviews.reviewer_id == filter_params.reviewer_id)
        if filter_params.status is not None:
            query = query.filter(TblReviews.status == filter_params.status)

        # Order by created_at desc?
        query = query.order_by(TblReviews.created_at.desc())

        reviews = query.all()

        return CustomResponse(
            status="1",
            status_code=200,
            message="Reviews fetched successfully",
            data=[
                ReviewResponse(
                    review_id=r.review_id,
                    book_id=r.book_id,
                    reviewer_id=r.reviewer_id,
                    rating=r.rating,
                    comment=r.comment,
                    status=r.status,
                    created_at=r.created_at,
                )
                for r in reviews
            ],
        )

    async def update_review(self, review_id: int, request: ReviewUpdateRequest):
        """Update a review."""
        review = (
            self.db.query(TblReviews).filter(TblReviews.review_id == review_id).first()
        )
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        # Check permissions
        # If updating status, requires admin/moderator?
        # If updating content, requires owner?

        is_owner = self.current_user and review.reviewer_id == self.current_user.user_id
        # Assuming admin check if needed later. But for now owners update their reviews.

        if request.status is not None:
            # Only allow status change if admin? Or maybe implemented later.
            # For now, let's allow it if present (maybe for approval flow).
            # But if owner changes content, should it go back to pending?
            review.status = request.status

        if is_owner:
            if request.rating:
                review.rating = request.rating
            if request.comment:
                review.comment = request.comment

            # Allow status reset to pending if edited?
            # review.status = 0
        elif not (
            self.current_user and self.current_user.user_type in ["admin", "author"]
        ):  # Example roles
            # If not owner and not admin, forbid
            raise HTTPException(status_code=403, detail="Not authorized")

        self.db.commit()
        self.db.refresh(review)

        return CustomResponse(
            status="1",
            status_code=200,
            message="Review updated successfully",
            data=ReviewResponse(
                review_id=review.review_id,
                book_id=review.book_id,
                reviewer_id=review.reviewer_id,
                rating=review.rating,
                comment=review.comment,
                status=review.status,
                created_at=review.created_at,
            ),
        )

    async def delete_review(self, review_id: int):
        """Delete a review."""
        review = (
            self.db.query(TblReviews).filter(TblReviews.review_id == review_id).first()
        )
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        # Check owner or admin
        if self.current_user and review.reviewer_id != self.current_user.user_id:
            # Allow admin override here ideally
            raise HTTPException(status_code=403, detail="Not authorized")

        self.db.delete(review)
        self.db.commit()

        return CustomResponse(
            status="1",
            status_code=200,
            message="Review deleted successfully",
            data=None,
        )
