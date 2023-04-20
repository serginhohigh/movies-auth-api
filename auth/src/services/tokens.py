from datetime import UTC, datetime, timedelta
from enum import Enum, unique
from typing import Any as AnyType
from typing import TypeAlias
from uuid import UUID, uuid4

import jwt

JWT: TypeAlias = str
JWTClaims: TypeAlias = dict[str, AnyType]


@unique
class TokenType(Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'

    def __str__(self) -> str:
        return self.value


class TokenJWT:
    def __init__(
            self,
            jwt_secret_key: str,
            jwt_access_lifetime: int,
            jwt_refresh_lifetime: int,
        ) -> None:
        self.jwt_secret_key = jwt_secret_key
        self.jwt_access_lifetime = timedelta(hours=jwt_access_lifetime)
        self.jwt_refresh_lifetime = timedelta(days=jwt_refresh_lifetime)

    def create_access_token(self, user_id: UUID, user_role: str) -> JWT:
        claims = {
            'sub': str(user_id),
            'role': user_role,
            'exp': datetime.now(tz=UTC) + self.jwt_access_lifetime,
            'iat': datetime.now(tz=UTC),
            'type': 'access',
        }
        return jwt.encode(claims, self.jwt_secret_key)

    def create_refresh_token(self, user_id: UUID) -> JWT:
        claims = {
            'jti': str(uuid4()),
            'sub': str(user_id),
            'exp': datetime.now(tz=UTC) + self.jwt_refresh_lifetime,
            'iat': datetime.now(tz=UTC),
            'type': 'refresh',
        }
        return jwt.encode(claims, self.jwt_secret_key)
