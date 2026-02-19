from datetime import datetime
from pydantic import Field
from app.utils.schema_utils import CustomModel


class BookCreateRequest(CustomModel):
    title: str = Field(..., description="Title of the book")
    description: str | None = Field(default=None)
    language: str | None = Field(default=None)
    isbn: str | None = Field(default=None)
    page_count: int | None = Field(default=None)


class BookUpdateRequest(CustomModel):
    book_uuid: str = Field(..., description="UUID of the book")
    title: str | None = Field(default=None)
    status: int | None = Field(default=None)
    description: str | None = Field(default=None)
    language: str | None = Field(default=None)
    isbn: str | None = Field(default=None)
    page_count: int | None = Field(default=None)


class BookFileResponse(CustomModel):
    file_id: int | None = Field(default=None)
    file_type: str | None = Field(default=None)
    file_url: str | None = Field(default=None)
    file_size: int | None = Field(default=None)
    version: int | None = Field(default=None)
    uploaded_at: datetime | None = Field(default=None)


class BookDetailsResponse(CustomModel):
    description: str | None = Field(default=None)
    language: str | None = Field(default=None)
    isbn: str | None = Field(default=None)
    page_count: int | None = Field(default=None)


class BookResponse(CustomModel):
    book_id : int | None = Field(default=None)
    uuid: str | None = Field(default=None)
    title: str | None = Field(default=None)
    author_id: int | None = Field(default=None)
    status: int | None = Field(default=None)
    published_at: datetime | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    book_details: BookDetailsResponse | None = Field(default=None)
    book_files: list[BookFileResponse] | None = Field(default=None)


class BookFilter(CustomModel):
    book_uuid: str | None = Field(default=None)
    author_id: int | None = Field(default=None)
    status: int | None = Field(default=None)
