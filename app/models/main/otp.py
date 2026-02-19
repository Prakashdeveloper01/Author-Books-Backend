from app.utils.schema_utils import CustomModel
from pydantic import Field
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import Integer, String, DateTime, Boolean
from datetime import datetime
from app.models.base_class import Base


class UserOTPBaseModel(CustomModel):
    user_id: int = Field(...)
    otp_code: str = Field(...)
    is_verified: bool = Field(default=False)
    expires_at: datetime = Field(...)
    created_at: datetime = Field(default_factory=datetime.now)


class TblUserOTP(Base):
    __tablename__ = "user_otps"

    otp_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    otp_code: Mapped[str] = mapped_column(String(6), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    @classmethod
    def create(cls, data: UserOTPBaseModel, db: Session) -> "TblUserOTP":
        data_dict = data.model_dump()
        new_otp = cls(**data_dict)
        db.add(new_otp)
        db.flush()
        return new_otp
