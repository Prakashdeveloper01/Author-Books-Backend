from app.api.utils.service import UtilsService
from sqlalchemy.orm import Session
from app.database.main.mysql import get_db
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status, APIRouter
from app.utils.schema_utils import CustomResponse
from app.database.main.mysql import _engine
from app.models.base_class import Base

utils_product_router = APIRouter()

@utils_product_router.get("/create-engine", tags=["Utils:Database"])
def create_engine() -> CustomResponse:
    """Create engine."""
    Base.metadata.create_all(bind=_engine)
    return CustomResponse(status="1",status_code=status.HTTP_200_OK,
                          message="Engine created successfully")

@utils_product_router.post("/token", tags=["Utils:JWTToken"])
async def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await UtilsService(db).token_login(form_data)