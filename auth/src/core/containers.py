from dependency_injector import containers, providers

from db.redis import RedisCacheClient, init_redis
from services.auth import AuthService
from services.tokens import TokenJWT


class Container(containers.DeclarativeContainer):
    """Основной класс-контейнер для инициализации зависимостей."""

    config = providers.Configuration()

    redis_conn = providers.Singleton(
        init_redis,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        db=config.REDIS_DB,
    )

    redis_client = providers.Singleton(
        RedisCacheClient,
        connection=redis_conn,
    )

    token_service = providers.Singleton(
        TokenJWT,
        jwt_secret_key=config.JWT_SECRET_KEY,
        jwt_access_lifetime=config.JWT_ACCESS_LIFETIME,
        jwt_refresh_lifetime=config.JWT_REFRESH_LIFETIME,
    )

    auth_service = providers.Singleton(
        AuthService,
        cache_client=redis_conn,
        token_service=token_service,
        access_token_cookie_name=config.JWT_ACCESS_COOKIE_NAME,
        refresh_token_cookie_name=config.JWT_REFRESH_COOKIE_NAME,
    )
