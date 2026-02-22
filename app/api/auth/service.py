from app.config import CONFIG_SETTINGS
from app.api.auth.schemas import UserLoginResponse, ResetPasswordRequest
from app.models import TblUsers
from sqlalchemy.orm import Session
from app.utils.schema_utils import JWTPayloadSchema
from app.dependencies.authentication import JWTService
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
from app.utils.crypto_utils import verify_password
from app.utils.crypto_utils import encrypt
from app.utils.email_templates import create_otp_email_template


class AuthService:
    """Authentication service class."""

    def __init__(self, db: Session) -> None:
        """Initialize Borrower service class."""
        self.db = db

    async def login(self, form_data: OAuth2PasswordRequestForm) -> UserLoginResponse:
        """Login user."""
        encrypted_email = encrypt(
            form_data.username
        )  # Assuming username field holds email
        user = self.db.query(TblUsers).filter(TblUsers.email == encrypted_email).first()

        if not user:
            # Also try matching clear username just in case (optional, but good for robustness if username is allowed)
            # Or assume username is email. The requirement for TblUsers has both 'username' and 'email'.
            # form_data uses 'username' field which can be email or username.
            # Let's try matching username too if email fails
            user = (
                self.db.query(TblUsers)
                .filter(TblUsers.username == form_data.username)
                .first()
            )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await self._generate_jwt_tokens(user)

    async def _generate_jwt_tokens(self, user: TblUsers) -> UserLoginResponse:
        """Create access and refresh tokens."""
        if user.type and user.usr_id and user.uuid:
            create_jwt = JWTPayloadSchema(
                user_id=user.usr_id, user_type=user.type, uuid=user.uuid
            )
            access_token = await JWTService().create_access_token(create_jwt)
            refresh_token = await JWTService().create_refresh_token(create_jwt)

            return UserLoginResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                uuid=user.uuid if user.uuid else "",
                user_type=user.type if user.type else None,
                token_type="bearer",
                expire_minutes=CONFIG_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES,
            )

    async def send_otp(self, email: str):
        """Send OTP to the given email."""
        import random
        from app.models import TblOTPCodes
        from app.utils.email_utils import send_email

        otp_code = str(random.randint(100000, 999999))

        # Save to DB
        TblOTPCodes.create(self.db, encrypt(email), otp_code)

        # Send Email
        # We run this synchronously here for simplicity as per requirement,
        # or we could use BackgroundTasks if passed to the service.
        # Given the previous context was generic SMTP setup, usually async is better but let's stick to direct call or threadpool.
        # send_email is blocking (smtplib).
        # We should run it in a threadpool to avoid blocking event loop.
        from fastapi.concurrency import run_in_threadpool

        html_content = create_otp_email_template(otp_code)

        await run_in_threadpool(
            send_email,
            email,
            "Your OTP Code",
            html_content,
        )

        return {"message": "OTP sent successfully"}

    async def verify_otp(self, email: str, otp_code: str):
        """Verify the OTP."""
        from app.models import TblOTPCodes
        from datetime import datetime

        otp_record = TblOTPCodes.get_latest_by_email(self.db, encrypt(email))

        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP not found")

        if otp_record.otp_code != otp_code:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        if otp_record.verify:
            raise HTTPException(status_code=400, detail="OTP already verified")

        # Check expiration (e.g. 5 minutes)
        if (datetime.utcnow() - otp_record.created_at).total_seconds() > 300:
            raise HTTPException(status_code=400, detail="OTP expired")

        otp_record.verify = True
        self.db.commit()

        return {"message": "OTP verified successfully"}

    async def logout(self, current_user: JWTPayloadSchema):
        """Logout user by revoking tokens."""
        await JWTService().revoke_token(current_user.uuid)
        return {"message": "Logged out successfully"}

    async def forgot_password(self, email: str):
        """Initiate forgot password process by sending an OTP."""
        encrypted_email = encrypt(email)
        user = self.db.query(TblUsers).filter(TblUsers.email == encrypted_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.send_otp(email)

    async def reset_password(self, request: ResetPasswordRequest):
        """Reset password using OTP."""
        from app.models import TblOTPCodes
        from datetime import datetime
        from app.utils.crypto_utils import hash_password

        if request.new_password != request.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        encrypted_email = encrypt(request.email)
        otp_record = TblOTPCodes.get_latest_by_email(self.db, encrypted_email)

        if not otp_record:
            raise HTTPException(status_code=400, detail="OTP not found")

        if otp_record.otp_code != request.otp_code:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        if otp_record.verify:
            raise HTTPException(status_code=400, detail="OTP already verified")

        if (datetime.utcnow() - otp_record.created_at).total_seconds() > 300:
            raise HTTPException(status_code=400, detail="OTP expired")

        # Mark OTP as verified
        otp_record.verify = True

        # update password
        user = self.db.query(TblUsers).filter(TblUsers.email == encrypted_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = hash_password(request.new_password)
        self.db.commit()

        return {"message": "Password reset successfully"}
