from app.api.authors.schemas import UserResponse
from app.utils.crypto_utils import encrypt
from app.utils.crypto_utils import hash_password
from app.api.auth.service import AuthService
from app.utils.schema_utils import CustomResponse
from app.models.main.users import TblUsers
from datetime import datetime
import uuid
from app.models.main.users import UsersBaseModel
from app.api.authors.schemas import UserRequest
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.schema_utils import JWTPayloadSchema
from app.api.authors.schemas import UserProfileResponse
from app.models.main.books import TblBooks
from app.models.main.reviews import TblReviews
from app.models.main.books_downloads import TblBookDownloads


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user: UserRequest):
        """Create a new user."""
        user_data = UsersBaseModel.model_validate(user)
        user_data.uuid = str(uuid.uuid4())
        user_data.created_at = datetime.now()
        user_data.updated_at = datetime.now()
        user_data.password = hash_password(user.password)
        user_data.email = encrypt(user.email)
        user_data.created_by = 1
        data = TblUsers.create(user_data, self.db)
        self.db.commit()
        tokens = await AuthService(self.db)._generate_jwt_tokens(data)
        return CustomResponse(
            status="1",
            status_code=200,
            message="User created successfully",
            data=tokens,
        )


class AuthorService:
    def __init__(self, db: Session, current_user: JWTPayloadSchema):
        self.db = db
        self.current_user = current_user

    async def get_profile(self):
        """Get user profile."""
        data = TblUsers.get_by_uuid(self.current_user.uuid, self.db)
        if not data:
            # Should not happen if JWT is valid but good to handle
            return CustomResponse(
                status="-1", status_code=404, message="User not found", data=None
            )

        profile_data = UserProfileResponse.model_validate(data)
        profile_data.joined_at = data.created_at.strftime("%Y-%m-%d")  # Format date

        # Calculate Stats
        stats = {}
        if data.type == "author":
            total_books = (
                self.db.query(func.count(TblBooks.book_id))
                .filter(TblBooks.author_id == data.usr_id)
                .scalar()
            )
            total_downloads = (
                self.db.query(func.count(TblBookDownloads.download_id))
                .join(TblBooks)
                .filter(TblBooks.author_id == data.usr_id)
                .scalar()
            )
            stats = {
                "total_books": total_books or 0,
                "total_downloads": total_downloads or 0,
            }
        elif data.type == "reviewer":
            total_reviews = (
                self.db.query(func.count(TblReviews.review_id))
                .filter(TblReviews.reviewer_id == data.usr_id)
                .scalar()
            )
            stats = {"total_reviews": total_reviews or 0}

        profile_data.stats = stats

        return CustomResponse(
            status="1", status_code=200, message="User profile", data=profile_data
        )
