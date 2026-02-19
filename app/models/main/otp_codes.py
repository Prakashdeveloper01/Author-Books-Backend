from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session
from app.models.base_class import Base


class TblOTPCodes(Base):
    __tablename__ = "otp_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    otp_code: Mapped[str] = mapped_column(String(6), nullable=False)
    verify: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    @classmethod
    def create(cls, session: Session, email: str, otp_code: str) -> "TblOTPCodes":
        instance = cls(email=email, otp_code=otp_code)
        session.add(instance)
        try:
            session.flush()
            session.commit()
            session.refresh(instance)
        except Exception:
            session.rollback()
            raise
        return instance

    @classmethod
    def get_latest_by_email(cls, session: Session, email: str) -> "TblOTPCodes | None":
        return (
            session.query(cls)
            .filter(cls.email == email)
            .order_by(cls.created_at.desc())
            .first()
        )
