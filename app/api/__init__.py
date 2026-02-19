from app.api.auth.router import auth_router
from app.api.authors.router import author_router
from app.api.utils.router import utils_product_router
from app.api.books.router import book_router
from app.api.reviews.router import review_router
from app.api.dashboard.router import dashboard_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(prefix="/utils", router=utils_product_router)
api_router.include_router(prefix="/users", router=author_router, tags=["users"])
api_router.include_router(prefix="/auth", router=auth_router, tags=["auth"])
api_router.include_router(prefix="/books", router=book_router, tags=["books"])
api_router.include_router(prefix="/reviews", router=review_router, tags=["reviews"])
api_router.include_router(
    prefix="/dashboard", router=dashboard_router, tags=["dashboard"]
)
