import string
from datetime import UTC, datetime
from secrets import choice as secrets_choice
from typing import Any as AnyType
from typing import TypeAlias
from uuid import UUID

from flask import Response

from db.redis import CacheClient
from services.tokens import TokenJWT

TimeStampType: TypeAlias = float


class AuthService:
    def __init__(
            self,
            cache_client: CacheClient,
            token_service: TokenJWT,
            access_token_cookie_name: str,
            refresh_token_cookie_name: str,
        ) -> None:
        self.cache_client = cache_client
        self.token_service = token_service

        self.access_token_cookie_name = access_token_cookie_name
        self.refresh_token_cookie_name = refresh_token_cookie_name

    def add_token_to_blacklist(
            self,
            *,
            jti: str,
            user_id: UUID,
            token_exp: TimeStampType,
        ) -> None:
        ttl = (
            datetime.fromtimestamp(token_exp, tz=UTC) - datetime.now(tz=UTC)
        ).total_seconds()
        self.cache_client.set(jti, user_id, round(ttl) + 1)

    def gen_random_password(self) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets_choice(alphabet) for _ in range(16))

    def get_token_from_blacklist(self, jti: str) -> AnyType | None:
        return self.cache_client.get(jti)

    def gen_tokens(
            self,
            resp: Response,
            user_id: UUID,
            user_role: str,
        ) -> Response:
        resp.set_cookie(
            self.access_token_cookie_name,
            self.token_service.create_access_token(user_id, user_role),
            max_age=self.token_service.jwt_access_lifetime,
            httponly=True,
        )
        resp.set_cookie(
            self.refresh_token_cookie_name,
            self.token_service.create_refresh_token(user_id),
            max_age=self.token_service.jwt_refresh_lifetime,
            httponly=True,
        )

        return resp
