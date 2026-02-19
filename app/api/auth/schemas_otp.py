from datetime import datetime
from pydantic import Field, EmailStr
from app.utils.schema_utils import CustomModel


class EmailSchema(CustomModel):
    email: list[EmailStr] = Field(...)
    body: dict = Field(default_factory=dict)


class VerifyOTPRequest(CustomModel):
    email: EmailStr = Field(...)
    otp_code: str = Field(..., max_length=6, min_length=6)
