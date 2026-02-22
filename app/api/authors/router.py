from app.api.authors.service import AuthorService
from app.dependencies.authentication import get_current_user
from app.utils.schema_utils import JWTPayloadSchema, CustomResponse
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.main.mysql import get_db
from app.api.authors.service import UserService
from app.api.authors.schemas import (
    UserRequest,
    UserProfileResponse,
    UserProfileUpdateRequest,
)
from fastapi import APIRouter, Depends

author_router = APIRouter()


@author_router.post("/users")
async def create_user(
    user: UserRequest,
    db: Annotated[Session, Depends(get_db)],
):
    return await UserService(db).create_user(user)


@author_router.get("/profile", response_model=CustomResponse[UserProfileResponse])
async def get_profile(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await AuthorService(db, current_user).get_profile()


@author_router.put("/profile", response_model=CustomResponse[UserProfileResponse])
async def update_profile(
    request: UserProfileUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await AuthorService(db, current_user).update_profile(request)
