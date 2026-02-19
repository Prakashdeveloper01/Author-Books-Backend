from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.database.main.mysql import get_db
from app.api.books.service import BookService
from app.api.books.schemas import (
    BookCreateRequest,
    BookResponse,
    BookDetailsResponse,
    BookFileResponse,
    BookFilter,
    BookUpdateRequest,
)
from app.utils.schema_utils import JWTPayloadSchema, CustomResponse
from app.dependencies.authentication import get_current_user

book_router = APIRouter()


@book_router.post("", response_model=CustomResponse[BookResponse])
async def create_book(
    request: BookCreateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await BookService(db, current_user).create_book(request)


@book_router.get("", response_model=CustomResponse[list[BookResponse]])
async def list_books(
    db: Annotated[Session, Depends(get_db)],
    author_id: int | None = Query(default=None),
    status: int | None = Query(default=None),
):
    filter_params = BookFilter(author_id=author_id, status=status)
    return await BookService(db).list_books(filter_params)


@book_router.get("/{uuid}", response_model=CustomResponse[BookResponse])
async def get_book(
    uuid: str,
    db: Annotated[Session, Depends(get_db)],
):
    return await BookService(db).get_book(uuid)


@book_router.put("/{uuid}", response_model=CustomResponse[BookResponse])
async def update_book(
    uuid: str,
    request: BookUpdateRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await BookService(db, current_user).update_book(uuid, request)


@book_router.delete("/{uuid}", response_model=CustomResponse[None])
async def delete_book(
    uuid: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await BookService(db, current_user).delete_book(uuid)


@book_router.post("/{uuid}/files", response_model=CustomResponse[BookFileResponse])
async def upload_book_file(
    uuid: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
    file: UploadFile = File(...),
    file_type: str = Form(..., description="PDF or EPUB"),
):
    return await BookService(db, current_user).upload_book_file(uuid, file, file_type)


@book_router.get("/{uuid}/download/{file_id}")
async def download_book(
    uuid: str,
    file_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await BookService(db, current_user).download_book(uuid, file_id)
