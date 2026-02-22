from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Configuration settings for the application."""

    model_config = SettingsConfigDict(
        env_file="./.env", env_file_encoding="utf-8", case_sensitive=True, extra="allow"
    )

    API_VERSION: str = ""
    PROJECT_TITLE: str = ""
    PROJECT_NAME: str = ""
    DESCRIPTION: str = ""

    APP_ENV: str = ""

    IS_DEBUG: bool = True

    SQL_HOST: str = ""
    SQL_ADMIN_USER: str = ""
    SQL_ADMIN_PASS: str = ""
    SQL_DB: str = ""
    SQL_PORT: int = 0
    SQL_SSL_CA: str | None = None

    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = ""
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 0
    APP_JWT_PRIVATE_KEY: str = ""
    APP_JWT_PUBLIC_KEY: str = ""

    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_DB_HOST: str = ""
    SSL_CA_CERTS: str | None = None

    MAIN_ENCRYPTION_KEY: str = ""
    MAIN_ENCRYPTION_IV: str = ""

    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    EMAILS_FROM_EMAIL: str = ""
    EMAILS_FROM_NAME: str = ""

    ROOT_PATH: str = ""


def get_settings(env: str = "local") -> Settings:
    """
    Return the settings object based on the environment.

    Parameters
    ----------
        env (str): The environment to retrieve the settings for. Defaults to "dev".

    Returns
    -------
        Settings: The settings object based on the environment.

    Raises
    ------
        ValueError: If the environment is invalid.
    """
    return Settings()


settings = get_settings()
CONFIG_SETTINGS = Settings()
