from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_SCHEMA: str = Field(default='auth')
    PG_USER: str
    PG_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    REDIS_PASSWORD: str

    SECRET_KEY: str

    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    YANDEX_AUTHORIZE_URL: str
    YANDEX_ACCESS_TOKEN_URL: str

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_AUTHORIZE_URL: str
    GOOGLE_ACCESS_TOKEN_URL: str
    GOOGLE_SERVER_METADATA_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHMS: str
    JWT_ACCESS_LIFETIME: int
    JWT_REFRESH_LIFETIME: int
    JWT_ACCESS_COOKIE_NAME: str = Field(default='access_token')
    JWT_REFRESH_COOKIE_NAME: str = Field(default='refresh_token')

    SQLALCHEMY_DATABASE_URI: str | None = Field(default=None)
    SQLALCHEMY_ECHO: bool = Field(default=False)

    API_TITLE: str
    API_VERSION: str
    API_DESCRIPTION: str
    API_SPEC_OPTIONS: dict | None = None
    OPENAPI_VERSION: str
    OPENAPI_JSON_PATH: str
    OPENAPI_URL_PREFIX: str
    OPENAPI_SWAGGER_UI_PATH: str
    OPENAPI_SWAGGER_UI_URL: str = Field(default='https://cdn.jsdelivr.net/npm/swagger-ui-dist@4.18.1/')

    DEBUG: bool = False

    def __init__(self, **data: dict) -> None:
        super().__init__(**data)

        self.SQLALCHEMY_DATABASE_URI = (
            f'postgresql://{self.PG_USER}:{self.PG_PASSWORD}'
            f'@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'
            f'?options=-c search_path=public,{self.PG_SCHEMA}'
        )

        self.API_SPEC_OPTIONS = {
            'info': {
                'description': self.API_DESCRIPTION,
            },
        }


settings = Settings()
