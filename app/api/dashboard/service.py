from datetime import datetime
from typing import Annotated
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.dashboard.schemas import (
    DashboardResponse,
    AuthorDashboardStats,
    ReviewerDashboardStats,
    RecentActivity,
)
from app.models.main.users import TblUsers
from app.models.main.books import TblBooks
from app.models.main.reviews import TblReviews
from app.models.main.books_downloads import TblBookDownloads
from app.utils.schema_utils import CustomResponse, JWTPayloadSchema, UserType


class DashboardService:
    def __init__(self, db: Session, current_user: JWTPayloadSchema | None = None):
        self.db = db
        self.current_user = current_user

    async def get_dashboard_data(self):
        """Get dashboard data based on user type."""
        if not self.current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        user_type = self.current_user.user_type

        if user_type == "author":
            return await self._get_author_dashboard()
        elif user_type == "reviewer":
            return await self._get_reviewer_dashboard()
        elif user_type == "admin":
            # Not requested but good to have a placeholder
            return await self._get_author_dashboard()  # Fallback for now
        else:
            raise HTTPException(status_code=400, detail="Unknown user type")

    async def _get_author_dashboard(self):
        """Calculate stats for author."""
        user_id = self.current_user.user_id

        # 1. Stats
        total_books = (
            self.db.query(func.count(TblBooks.book_id))
            .filter(TblBooks.author_id == user_id)
            .scalar()
        )
        published_books = (
            self.db.query(func.count(TblBooks.book_id))
            .filter(TblBooks.author_id == user_id, TblBooks.status == 1)
            .scalar()
        )
        draft_books = (
            self.db.query(func.count(TblBooks.book_id))
            .filter(TblBooks.author_id == user_id, TblBooks.status == 0)
            .scalar()
        )

        # Total Reviews Received: Reviews on books written by this author
        total_reviews = (
            self.db.query(func.count(TblReviews.review_id))
            .join(TblBooks)
            .filter(TblBooks.author_id == user_id)
            .scalar()
        )

        # Total Downloads: Downloads of books written by this author
        total_downloads = (
            self.db.query(func.count(TblBookDownloads.download_id))
            .join(TblBooks)
            .filter(TblBooks.author_id == user_id)
            .scalar()
        )

        # Avg Rating
        avg_rating = (
            self.db.query(func.avg(TblReviews.rating))
            .join(TblBooks)
            .filter(TblBooks.author_id == user_id)
            .scalar()
        )
        avg_rating = round(float(avg_rating), 1) if avg_rating else 0.0

        stats = AuthorDashboardStats(
            total_books=total_books or 0,
            published_books=published_books or 0,
            draft_books=draft_books or 0,
            total_reviews_received=total_reviews or 0,
            total_downloads=total_downloads or 0,
            average_rating=avg_rating,
        )

        # 2. Recent Activity (Recent Books Created/Updated)
        recent_books = (
            self.db.query(TblBooks)
            .filter(TblBooks.author_id == user_id)
            .order_by(TblBooks.updated_at.desc())
            .limit(5)
            .all()
        )
        activity = [
            RecentActivity(
                id=b.book_id,
                type="book",
                title=b.title,
                date=b.updated_at,
                status=b.status,
            )
            for b in recent_books
        ]

        return CustomResponse(
            status="1",
            status_code=200,
            message="Dashboard data fetched successfully",
            data=DashboardResponse(
                user_type=UserType.AUTHOR, stats=stats, recent_activity=activity
            ),
        )

    async def _get_reviewer_dashboard(self):
        """Calculate stats for reviewer."""
        user_id = self.current_user.user_id

        # 1. Stats
        total_reviews = (
            self.db.query(func.count(TblReviews.review_id))
            .filter(TblReviews.reviewer_id == user_id)
            .scalar()
        )

        # Books Downloaded/Read
        books_downloaded = (
            self.db.query(func.count(TblBookDownloads.download_id))
            .filter(TblBookDownloads.user_id == user_id)
            .scalar()
        )

        stats = ReviewerDashboardStats(
            total_reviews_given=total_reviews or 0,
            books_downloaded=books_downloaded or 0,
        )

        # 2. Recent Activity (Recent Reviews Given)
        recent_reviews = (
            self.db.query(TblReviews, TblBooks.title)
            .join(TblBooks)
            .filter(TblReviews.reviewer_id == user_id)
            .order_by(TblReviews.created_at.desc())
            .limit(5)
            .all()
        )

        activity = []
        for r, book_title in recent_reviews:
            activity.append(
                RecentActivity(
                    id=r.review_id,
                    type="review",
                    title=f"Review for {book_title}",
                    date=r.created_at,
                    status=r.status,
                    description=r.comment[:50] + "..." if r.comment else "",
                )
            )

        return CustomResponse(
            status="1",
            status_code=200,
            message="Dashboard data fetched successfully",
            data=DashboardResponse(
                user_type=UserType.REVIEWER, stats=stats, recent_activity=activity
            ),
        )
