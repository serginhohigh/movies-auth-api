from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    AUTH_HOST: str
    AUTH_PORT: str
    AUTH_URL: str | None = Field(default=None)
    AUTH_API_PREFIX: str = Field(default='api/v1')

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SCHEMA: str

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

        self.AUTH_URL = (
            f'http://{self.AUTH_HOST}:{self.AUTH_PORT}'
            f'/{self.AUTH_API_PREFIX}'
        )


settings = TestSettings()

pg_settings = {
    'dbname': settings.POSTGRES_DB,
    'user': settings.POSTGRES_USER,
    'password': settings.POSTGRES_PASSWORD,
    'host': settings.POSTGRES_HOST,
    'port': settings.POSTGRES_PORT,
    'options': f'-c search_path=public,{settings.POSTGRES_SCHEMA}',
}
