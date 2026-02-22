from app.utils.crypto_utils import decrypt
from pydantic import field_validator
from app.utils.schema_utils import UserType
from pydantic import Field
from app.utils.schema_utils import CustomModel


class UserRequest(CustomModel):
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)
    type: UserType = Field(default=UserType.AUTHOR)


class UserResponse(CustomModel):
    uuid: str | None = Field(default=None)
    username: str | None = Field(default=None)
    email: str | None = Field(default=None)
    type: UserType | None = Field(default=None)

    @field_validator("email")
    def validate_email(cls, v):
        if v:
            return decrypt(v)
        return None


class UserProfileResponse(UserResponse):
    joined_at: str | None = Field(default=None)
    profile_picture: str | None = Field(default=None)
    tagline: str | None = Field(default="Discovering new worlds, one page at a time.")
    level: int = Field(default=1)
    stats: dict | None = Field(default=None)
    achievements: list | None = Field(default=None)
    recent_history: list | None = Field(default=None)


class UserProfileUpdateRequest(CustomModel):
    profile_picture: str | None = Field(default=None)
    tagline: str | None = Field(default=None)
    preferences: list | None = Field(default=None)
