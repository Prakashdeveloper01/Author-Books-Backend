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

    IMAGE: str = ""
    TAG: str = ""
    PORT: int = 0
    APPLICATION_FILES: str = ""

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
    APP_JWT_PRIVATE_KEY: str = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAxVqr1rBt2vsy6c2+arHwf00pdAt1wzJrea/EwLYcWYqDUJ4f\naa+ZN3XlBZdAxeS0J5j6PqQxK/T8llKMhojoS6SQks5EyuLdUV25w/tKenfhBzDP\nMiDdrfWmtJb5/HpiHqR+MXq4KI8Gk+eVaJFKOJaXQ8G8KTps1P7X3un3v3jvoB53\nIO+M/C/AmySdll2zh7kQtFczck4+lYcEEQl64VJ7OJDmPeSRP8GB1eqpyoNlQriw\nbPUKpO8Ki/GFOARuDPc2tptKYkePH1LdACy+/JPnTTrQRdALaepoC5WIerbWmQ0X\nPdyKmYCiJV7AOv05bvnd8iy4DlCwTw6uoammDwIDAQABAoIBAQCQFvBJckzyyd7V\nV3NEYSBPQZ4XbNqRJrnTgaJsdUnjkj7n2FrlBeEe3gPVfiY7lgx2sLlcjPKdvmPA\nuQqCm2jG+aLYnKMbYmHmK0EbNtic6/OvFVLhrZ9MiIMrbOOeFBiZeM3uAER+0FYk\nHLw4OYPwJvrP7J4dl9un81zXEwngj/kdsTAjeWaCeRwh6skI+ryz+82YS/lstvbH\n+ww7oPYOrzC64Ygk6L4r8s8Jhf5Y+jspSj0TQ+I59vX2+XNyWLszca8qy0bZW3i/\naLCoZQuyYBwSxVUejMnTMNjlB5HMc4FEy/ayUy9MRNjNwSgcAqra9LIgByYA7+uv\n7SZjbsvBAoGBAPV4y71UHJui9BF0sNGPSF1hGnL/sgesE8N/NvsONxeX5RKt+iBA\nZArLT95iTQZ7vRZzoguuXs+6JaFuDfjhX1mENXKvnSvHSz0e7R2lfj0mzTZuZKl3\nLoQB3cUufSGyUBYUFX3pAotY8Q8KjfhaM7bKXnpLSR6RzikaEnvhd5gvAoGBAM3R\njvK46GWik0H9nBAE0OualOnAmYqN3MUg3TQXn0pEGOfZH2PDpABwtEkaBDOFg7E0\n1JPnoi4GKD4eKjNBA1+5dyTLDWmH9BCACLJy/TJnfoaGSKaqfxfghVBkO42Q6GjO\npJ7gxmgjxVUrBBxo5uDKtpgrrF6g9gC0ZRNpZ3ghAoGAD1OnhP7HeoBGNQDQOYV0\nwz/Y4u1MNGZuJXq/+BT/I538U5pBT9o1ZOck6YHBxXHccJZvu8L7cITy7I1umeeY\niIJUxABrE9yxufNAYuV+aFsP3SIvbtVeNifXrQQmFACKN5axcNcnrYO0KXhDPQqE\nyBkCpSgmPJ5l/PL/zHRbf0kCgYAufR4PvypnApDGgBVHHP9fqDvojKNhw2dRc3nj\ncU5+hOEnRUiszRz3KH3gYSr/xDGZzjgR7GkagjOGzGN1zkKH1amOuvqdkqLTM0hD\nnmuIfg37LsusMaihaQpTvUAiWs/UFJDkfhrynNnOwfecvykfL0qNFphJi4vlXtnR\nx6YiYQKBgQDr5+sLjms/h1ebjzg4BTckQDxKsuFl+ZMR2pgCrrInY3+g3xuHcw8z\n1LgDAviMXmxtA4RVZeyzJdOczSQev4IxkFtccYykov/+qDBxGYCKUVA6iYhGQEuX\nuj5fV3Oub5b+kUf2K2sL74AIJmzAksN9ktMG/Un1olS+WyjDKJtPfQ==\n-----END RSA PRIVATE KEY-----"
    APP_JWT_PUBLIC_KEY: str = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxVqr1rBt2vsy6c2+arHw\nf00pdAt1wzJrea/EwLYcWYqDUJ4faa+ZN3XlBZdAxeS0J5j6PqQxK/T8llKMhojo\nS6SQks5EyuLdUV25w/tKenfhBzDPMiDdrfWmtJb5/HpiHqR+MXq4KI8Gk+eVaJFK\nOJaXQ8G8KTps1P7X3un3v3jvoB53IO+M/C/AmySdll2zh7kQtFczck4+lYcEEQl6\n4VJ7OJDmPeSRP8GB1eqpyoNlQriwbPUKpO8Ki/GFOARuDPc2tptKYkePH1LdACy+\n/JPnTTrQRdALaepoC5WIerbWmQ0XPdyKmYCiJV7AOv05bvnd8iy4DlCwTw6uoamm\nDwIDAQAB\n-----END PUBLIC KEY-----"

    REDIS_HOST: str = ""
    REDIS_PORT: int = 0
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_PASS: str = ""
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
    IS_SWAGGER_ENABLED: bool = True
    FASTAPI_DEBUG: bool = False
    SWAGGER_UI_USERNAME: str = ""
    SWAGGER_UI_PASSWORD: str = ""


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
