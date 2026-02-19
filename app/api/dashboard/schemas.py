from datetime import datetime
from pydantic import Field
from app.utils.schema_utils import CustomModel, UserType


class AuthorDashboardStats(CustomModel):
    total_books: int = Field(default=0)
    published_books: int = Field(default=0)
    draft_books: int = Field(default=0)
    total_reviews_received: int = Field(default=0)
    total_downloads: int = Field(default=0)
    average_rating: float = Field(default=0.0)


class ReviewerDashboardStats(CustomModel):
    total_reviews_given: int = Field(default=0)
    books_downloaded: int = Field(default=0)


class RecentActivity(CustomModel):
    id: int
    type: str  # "book", "review", "download"
    title: str
    description: str | None = None
    date: datetime
    status: int | None = None


class DashboardResponse(CustomModel):
    user_type: UserType
    stats: AuthorDashboardStats | ReviewerDashboardStats
    recent_activity: list[RecentActivity] = Field(default_factory=list)
