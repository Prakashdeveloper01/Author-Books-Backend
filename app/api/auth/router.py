from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from app.database.main.mysql import get_db
from app.api.auth.service import AuthService
from app.api.auth.schemas import UserLoginResponse, SendOTPRequest, VerifyOTPRequest

auth_router = APIRouter()


@auth_router.post("/login", response_model=UserLoginResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await AuthService(db).login(form_data)


@auth_router.post("/send-otp")
async def send_otp_endpoint(
    request: SendOTPRequest,
    db: Annotated[Session, Depends(get_db)],
):
    return await AuthService(db).send_otp(request.email)


@auth_router.post("/verify-otp")
async def verify_otp_endpoint(
    request: VerifyOTPRequest,
    db: Annotated[Session, Depends(get_db)],
):
    return await AuthService(db).verify_otp(request.email, request.otp_code)
