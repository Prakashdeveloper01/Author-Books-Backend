from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.main.mysql import get_db
from app.api.dashboard.service import DashboardService
from app.api.dashboard.schemas import DashboardResponse
from app.utils.schema_utils import JWTPayloadSchema, CustomResponse
from app.dependencies.authentication import get_current_user

dashboard_router = APIRouter()


@dashboard_router.get("", response_model=CustomResponse[DashboardResponse])
async def get_dashboard(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[JWTPayloadSchema, Depends(get_current_user)],
):
    return await DashboardService(
        db, current_user
    ).get_dashboard_data()
