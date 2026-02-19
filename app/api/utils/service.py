

from app.utils.schema_utils import CheckFieldModel
from app.utils.crypto_utils import verify_password
from app.utils.crypto_utils import encrypt
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.dependencies.authentication import JWTService
from app.utils.schema_utils import JWTPayloadSchema
from fastapi import HTTPException, status
from app.models import TblUsers
from sqlalchemy.orm import Session

class UtilsService:
    """Utils service class."""

    def __init__(self,db: Session) -> None:
        self.db = db

    async def token_login(self, form_data: OAuth2PasswordRequestForm) -> dict:
        """Token login."""
        filters = CheckFieldModel(email=encrypt(form_data.username))
        user = TblUsers.get_by_filter(filters, self.db)
        if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect username or password")
        create_jwt = JWTPayloadSchema(user_id=user.usr_id, user_type=user.type,
                                    uuid=user.uuid)
        access_token_expires = await JWTService().create_access_token(create_jwt)
        return {"access_token":access_token_expires, "token_type":"bearer"}