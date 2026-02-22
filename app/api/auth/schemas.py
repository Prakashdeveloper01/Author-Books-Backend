from app.utils.schema_utils import CustomModel
from pydantic import Field


class UserLoginResponse(CustomModel):
    """Login response schema."""

    uuid: str
    user_type: str | None = Field(default=None)
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expire_minutes: int


class SendOTPRequest(CustomModel):
    """Schema for sending OTP."""

    email: str = Field(..., description="Email address to send OTP to")


class VerifyOTPRequest(CustomModel):
    """Schema for verifying OTP."""

    email: str = Field(..., description="Email address")
    otp_code: str = Field(..., description="OTP code received")

class ForgotPasswordRequest(CustomModel):
    """Schema for forgot password."""

    email: str = Field(..., description="Email address")

class ResetPasswordRequest(CustomModel):
    """Schema for reset password."""

    email: str = Field(..., description="Email address")
    otp_code: str = Field(..., description="OTP code received")
    new_password: str = Field(..., description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
