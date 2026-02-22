from app.utils.schema_utils import CheckFieldModel
from pydantic import Field
from sqlalchemy import text
from sqlalchemy import TIMESTAMP
from sqlalchemy import DateTime
from datetime import datetime
from app.utils.schema_utils import CustomModel
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String
from app.models.base_class import Base


class UsersBaseModel(CustomModel):
    usr_id: int | None = Field(default=None)
    uuid: str | None = Field(default=None)
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)
    type: str | None = Field(default=None)
    profile_picture: str | None = Field(default=None)
    tagline: str | None = Field(default=None)
    preferences: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    created_by: int | None = Field(default=None)
    updated_by: int | None = Field(default=None)


class TblUsers(Base):
    __tablename__ = "users"

    usr_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[str] = mapped_column(
        "usr_uuid", String(36), nullable=False, unique=True
    )
    username: Mapped[str] = mapped_column("usr_username", String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        "usr_email", String(255), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column("usr_password", String(255), nullable=False)
    type: Mapped[str] = mapped_column("usr_type", String(255), nullable=False)
    profile_picture: Mapped[str] = mapped_column(
        "usr_profile_picture", String(255), nullable=True
    )
    tagline: Mapped[str] = mapped_column("usr_tagline", String(255), nullable=True)
    preferences: Mapped[str] = mapped_column(
        "usr_preferences", String(1000), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        "usr_createdAt", DateTime, nullable=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "usr_updatedAt",
        TIMESTAMP,
        nullable=True,
        server_default=text("NULL ON UPDATE current_timestamp()"),
    )
    created_by: Mapped[int] = mapped_column("usr_createdBy", Integer, nullable=True)
    updated_by: Mapped[int] = mapped_column("usr_updatedBy", Integer, nullable=True)

    @classmethod
    def create(cls, data: UsersBaseModel, db: Session) -> "TblUsers":
        """Create new record."""
        data_dict = data.model_dump()
        new_data = cls(**data_dict)
        db.add(new_data)
        db.flush()
        return new_data

    @classmethod
    def update(cls, data: UsersBaseModel, db: Session) -> None:
        """Update the record."""
        user = db.query(cls).filter(cls.uuid == data.uuid).first()
        if user:
            data_dict = data.model_dump(by_alias=False, exclude_none=True)
            for field, value in data_dict.items():
                setattr(user, field, value)
            db.flush()
            db.refresh(user)

    @classmethod
    def get_by_uuid(cls, uuid: str, db: Session) -> "TblUsers":
        """Get user by uuid."""
        return db.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    def get_by_filter(cls, filters: CheckFieldModel, db: Session) -> "TblUsers | None":
        """Get record by filter."""
        filter_data = filters.model_dump(by_alias=True, exclude_none=True)
        return db.query(cls).filter_by(**filter_data).first()
