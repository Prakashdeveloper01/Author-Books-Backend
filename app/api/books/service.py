from datetime import datetime
import os
import shutil
import uuid
from typing import Annotated
from fastapi import UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.books.schemas import (
    BookCreateRequest,
    BookResponse,
    BookDetailsResponse,
    BookFileResponse,
    BookFilter,
    BookUpdateRequest,
)
from app.models.main.books import TblBooks, BooksBaseModel
from app.models.main.books_details import TblBookDetails, BookDetailsBaseModel
from app.models.main.books_files import TblBookFiles, BookFilesBaseModel
from app.models.main.books_downloads import TblBookDownloads, BookDownloadsBaseModel
from app.utils.schema_utils import CustomResponse, JWTPayloadSchema
from app.config import CONFIG_SETTINGS


class BookService:
    def __init__(self, db: Session, current_user: JWTPayloadSchema | None = None):
        self.db = db
        self.current_user = current_user

    async def create_book(self, request: BookCreateRequest):
        """Create a new book."""
        if not self.current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        # 1. Create Book Entry
        new_uuid = str(uuid.uuid4())
        book_data = BooksBaseModel(
            uuid=new_uuid,
            title=request.title,
            author_id=self.current_user.user_id,
            status=0,  # Draft
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        new_book = TblBooks.create(book_data, self.db)
        self.db.commit()  # Commit to get book_id

        # 2. Create Book Details
        details_data = BookDetailsBaseModel(
            book_id=new_book.book_id,
            description=request.description,
            language=request.language,
            isbn=request.isbn,
            page_count=request.page_count,
            created_at=datetime.now(),
            created_by=self.current_user.user_id,
            updated_at=datetime.now(),
            updated_by=self.current_user.user_id,
        )
        TblBookDetails.create(details_data, self.db)
        self.db.commit()

        return CustomResponse(
            status="1",
            status_code=201,
            message="Book created successfully",
            data=BookResponse(
                uuid=new_book.uuid,
                title=new_book.title,
                author_id=new_book.author_id,
                status=new_book.status,
                created_at=new_book.created_at,
                updated_at=new_book.updated_at,
                book_details=BookDetailsResponse(
                    description=request.description,
                    language=request.language,
                    isbn=request.isbn,
                    page_count=request.page_count,
                ),
            ),
        )

    async def get_book(self, book_uuid: str):
        """Get book details."""
        book = self.db.query(TblBooks).filter(TblBooks.uuid == book_uuid).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        details = TblBookDetails.get_by_book_id(book.book_id, self.db)
        files = TblBookFiles.get_by_book_id(
            book.book_id, self.db
        )  # Note: get_by_book_id returns single or list? Model says .first(). Fix if needed.
        # TblBookFiles.get_by_book_id implementation in user code returns .first().
        # But a book can have multiple files (PDF, EPUB).
        # I should probably change TblBookFiles to return a list or just get one.
        # For now, I'll follow the existing code but awareness is key.
        # Actually TblBookFiles.get_by_book_id in user provided code does `.first()`.
        # I will fetch all files manually here to be safe if multiple exist.
        all_files = (
            self.db.query(TblBookFiles)
            .filter(TblBookFiles.book_id == book.book_id)
            .all()
        )

        return CustomResponse(
            status="1",
            status_code=200,
            message="Book details fetched successfully",
            data=BookResponse(
                uuid=book.uuid,
                title=book.title,
                author_id=book.author_id,
                status=book.status,
                published_at=book.published_at,
                created_at=book.created_at,
                updated_at=book.updated_at,
                book_details=BookDetailsResponse(
                    description=details.description if details else None,
                    language=details.language if details else None,
                    isbn=details.isbn if details else None,
                    page_count=details.page_count if details else None,
                ),
                book_files=[
                    BookFileResponse(
                        file_id=f.file_id,
                        file_type=f.file_type,
                        file_url=f.file_url,  # Pass full URL or relative?
                        file_size=f.file_size,
                        version=f.version,
                        uploaded_at=f.uploaded_at,
                    )
                    for f in all_files
                ]
                if all_files
                else [],
            ),
        )

    async def list_books(self, filter_params: BookFilter):
        """List books with filters."""
        query = self.db.query(TblBooks)

        if filter_params.author_id:
            query = query.filter(TblBooks.author_id == filter_params.author_id)
        if filter_params.status is not None:
            query = query.filter(TblBooks.status == filter_params.status)

        books = query.all()

        # We might want to optimize this to avoid N+1 queries for details/files
        # But for now, simple loop is fine or just return basic info.

        response_data = []
        for book in books:
            # Basic info only for list? Or full?
            # Let's give basic info + details.
            details = TblBookDetails.get_by_book_id(book.book_id, self.db)

            # Fetch book files
            all_files = (
                self.db.query(TblBookFiles)
                .filter(TblBookFiles.book_id == book.book_id)
                .all()
            )

            response_data.append(
                BookResponse(
                    book_id=book.book_id,
                    uuid=book.uuid,
                    title=book.title,
                    author_id=book.author_id,
                    status=book.status,
                    published_at=book.published_at,
                    created_at=book.created_at,
                    updated_at=book.updated_at,
                    book_details=BookDetailsResponse(
                        description=details.description if details else None,
                        language=details.language if details else None,
                        isbn=details.isbn if details else None,
                        page_count=details.page_count if details else None,
                    ),
                    book_files=[
                        BookFileResponse(
                            file_id=f.file_id,
                            file_type=f.file_type,
                            file_url=f.file_url,
                            file_size=f.file_size,
                            version=f.version,
                            uploaded_at=f.uploaded_at,
                        )
                        for f in all_files
                    ]
                    if all_files
                    else [],
                )
            )

        return CustomResponse(
            status="1",
            status_code=200,
            message="Books list fetched successfully",
            data=response_data,
        )

    async def upload_book_file(self, book_uuid: str, file: UploadFile, file_type: str):
        """Upload a file for a book."""
        book = self.db.query(TblBooks).filter(TblBooks.uuid == book_uuid).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # Verify ownership?
        if self.current_user and book.author_id != self.current_user.user_id:
            # Unless admin?
            # For now strict ownership.
            raise HTTPException(
                status_code=403, detail="Not authorized to upload files for this book"
            )

        # Save file
        upload_dir = f"files/books/{book_uuid}"
        os.makedirs(upload_dir, exist_ok=True)

        file_path = f"{upload_dir}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create DB entry
        file_data = BookFilesBaseModel(
            book_id=book.book_id,
            file_type=file_type,  # PDF, EPUB
            file_url=file_path,  # Store relative path
            file_size=0,  # Calculate size if needed
            version=1,  # Logic for versioning?
            uploaded_at=datetime.now(),
        )

        new_file = TblBookFiles.create(file_data, self.db)
        self.db.commit()

        return CustomResponse(
            status="1",
            status_code=200,
            message="File uploaded successfully",
            data=BookFileResponse(
                file_id=new_file.file_id,
                file_type=new_file.file_type,
                file_url=new_file.file_url,
                uploaded_at=new_file.uploaded_at,
            ),
        )

    async def update_book(self, book_uuid: str, request: BookUpdateRequest):
        """Update a book."""
        book = self.db.query(TblBooks).filter(TblBooks.uuid == book_uuid).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if self.current_user and book.author_id != self.current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this book"
            )

        # Update Book
        if request.title:
            book.title = request.title
        if request.status is not None:
            book.status = request.status
        book.updated_at = datetime.now()

        # Update Details
        details = (
            self.db.query(TblBookDetails)
            .filter(TblBookDetails.book_id == book.book_id)
            .first()
        )
        if details:
            if request.description:
                details.description = request.description
            if request.language:
                details.language = request.language
            if request.isbn:
                details.isbn = request.isbn
            if request.page_count:
                details.page_count = request.page_count
            details.updated_at = datetime.now()
            details.updated_by = self.current_user.user_id

        self.db.commit()
        self.db.refresh(book)

        return CustomResponse(
            status="1",
            status_code=200,
            message="Book updated successfully",
            data=BookResponse(
                uuid=book.uuid,
                title=book.title,
                author_id=book.author_id,
                status=book.status,
                published_at=book.published_at,
                created_at=book.created_at,
                updated_at=book.updated_at,
            ),
        )

    async def delete_book(self, book_uuid: str):
        """Delete a book."""
        book = self.db.query(TblBooks).filter(TblBooks.uuid == book_uuid).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        if self.current_user and book.author_id != self.current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this book"
            )

        self.db.delete(
            book
        )  # Cascade should handle details/files if configured in DB, but SQLAlchemy relationship cascade might be needed if not.
        # User defined `ondelete="CASCADE"` in ForeignKeys in `books_details.py`, `books_files.py` etc.
        # So DB level cascade should work if DB supports it (MySQL/Postgres do).
        self.db.commit()

        return CustomResponse(
            status="1", status_code=200, message="Book deleted successfully", data=None
        )

    async def download_book(self, book_uuid: str, file_id: int):
        """Download a book file."""
        if not self.current_user:
            raise HTTPException(status_code=401, detail="Unauthorized")

        book = self.db.query(TblBooks).filter(TblBooks.uuid == book_uuid).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        file_record = (
            self.db.query(TblBookFiles)
            .filter(
                TblBookFiles.file_id == file_id, TblBookFiles.book_id == book.book_id
            )
            .first()
        )
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")

        # Check permissions? (e.g. if book is published, or user has paid?)
        # For now assuming free download if logged in.

        # Record download
        download_data = BookDownloadsBaseModel(
            book_id=book.book_id,
            user_id=self.current_user.user_id,
            downloaded_at=datetime.now(),
        )
        TblBookDownloads.create(download_data, self.db)
        self.db.commit()

        # Return FileResponse
        # Check if file exists
        if not os.path.exists(file_record.file_url):
            raise HTTPException(
                status_code=404, detail="File content not found on server"
            )

        return FileResponse(
            file_record.file_url, filename=os.path.basename(file_record.file_url)
        )
