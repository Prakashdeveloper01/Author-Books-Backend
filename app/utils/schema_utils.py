from datetime import datetime
import enum
from pydantic import BaseModel, Field, ConfigDict
from typing import TypeVar, Generic
from pydantic.alias_generators import to_camel


class CustomModel(BaseModel):
    """Base model for all models in the application."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
        coerce_numbers_to_str=True,
        arbitrary_types_allowed=True,
    )


DataT = TypeVar("DataT")

class CustomResponse(CustomModel, Generic[DataT]):
    """Custom response model for the API."""

    status: str = Field(..., examples=["1", "-1"])
    status_code: int = Field(...,examples=["200","201"])
    message: str = Field(..., examples=["Message", "User already exists"])
    data: DataT | None = None

class JWTPayloadSchema(BaseModel):
    """JWT Payload Schema."""

    user_id: int
    uuid: str
    user_type: str
    exp: datetime | None =Field(default=None)

class UserType(str, enum.Enum):
    ADMIN = "admin"
    AUTHOR = "author"
    REVIEWER = "reviewer"

class CheckFieldModel(CustomModel):
    """User filter model."""

    usr_id: int | None = Field(default=None,alias="usr_id")
    email: str | None = Field(default=None)