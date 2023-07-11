from http import HTTPStatus

import jwt
from dependency_injector.wiring import Provide, inject
from flask import g, request
from flask_smorest import abort
from jwt.exceptions import InvalidTokenError

from core.containers import Container
from core.permissions import Permissions
from services.auth import AuthService
from services.tokens import JWT, JWTClaims, TokenType


@inject
def get_access_token(
        name: str = Provide[Container.config.JWT_ACCESS_COOKIE_NAME],
    ) -> JWT | None:
    try:
        return request.cookies.get(name) or request.headers.get(
            'Authorization').split(' ')[1]
    except AttributeError:
        return None


@inject
def get_refresh_token(
        name: str = Provide[Container.config.JWT_REFRESH_COOKIE_NAME],
    ) -> JWT | None:
    return request.cookies.get(name)


@inject
def jwt_decoder(
        token: JWT,
        jwt_secret_key: str = Provide[Container.config.JWT_SECRET_KEY],
        jwt_algorithms: str = Provide[Container.config.JWT_ALGORITHMS],
    ) -> JWTClaims:
    return jwt.decode(
        token,
        jwt_secret_key,
        algorithms=jwt_algorithms.split(','),
    )


def validate_jwt_token(token: JWT) -> JWTClaims:
    try:
        token_decoded = jwt_decoder(token)
    except InvalidTokenError:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')
    return token_decoded


def check_token_type(*, token_claims: JWTClaims, refresh: bool = False) -> None:
    try:
        token_type = TokenType(token_claims.get('type'))
    except ValueError:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')

    if refresh and token_type != TokenType.REFRESH:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')

    if not refresh and token_type != TokenType.ACCESS:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')


def check_permissions(permission: str, permissions: list[Permissions]) -> None:
    try:
        permission = Permissions(permission)
    except ValueError:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')

    if permission not in permissions:
        abort(HTTPStatus.UNAUTHORIZED, message='Low permissions')


@inject
def check_token_blacklisted(
        jti: str,
        auth_service: AuthService = Provide[Container.auth_service],
    ) -> None:
    if auth_service.get_token_from_blacklist(jti):
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')


def validate_refresh_token(token_claims: JWTClaims) -> None:
    try:
        jti = token_claims['jti']
    except KeyError:
        abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')
    check_token_blacklisted(jti)


def verify_jwt_in_request(
        *,
        permissions: list[Permissions] | None = None,
        access: bool = True,
        refresh: bool = False,
    ) -> None:

    if access:
        access_token = get_access_token()
        access_token_decoded = validate_jwt_token(access_token)
        check_token_type(token_claims=access_token_decoded)

        g.access_token = access_token
        try:
            g.user_role = access_token_decoded['role']
            g.access_token_exp = access_token_decoded['exp']
            g.user_id = access_token_decoded['sub']
        except KeyError:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')

        if permissions:
            check_permissions(g.user_role, permissions)

    if refresh:
        refresh_token = get_refresh_token()
        refresh_token_decoded = validate_jwt_token(refresh_token)
        check_token_type(token_claims=refresh_token_decoded, refresh=True)
        validate_refresh_token(refresh_token_decoded)

        g.refresh_token = refresh_token
        g.refresh_token_jti = refresh_token_decoded['jti']
        try:
            g.refresh_token_exp = refresh_token_decoded['exp']
            if not hasattr(g, 'user_id'):
                g.user_id = refresh_token_decoded['sub']
        except KeyError:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid token')
