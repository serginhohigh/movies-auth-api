from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response, g, make_response, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from api.decorators import jwt_required, login_required
from api.schemas.user import UserLoginSchema, UserRegisterSchema
from api.validators import valid_user_email, valid_user_id, valid_user_password
from core.containers import Container
from db.postgres import db
from models.role import Role
from models.user import User
from services.auth import AuthService

auth_bp = Blueprint('auth', 'auth')


@auth_bp.route('/login')
class UsersLogin(MethodView):
    @auth_bp.arguments(UserLoginSchema, required=True)
    @auth_bp.alt_response(HTTPStatus.NOT_FOUND)
    @auth_bp.alt_response(HTTPStatus.CONFLICT)
    @auth_bp.response(HTTPStatus.OK)
    @inject
    def post(
            self,
            body: dict,
            auth_service: AuthService = Provide[Container.auth_service],
        ) -> Response:
        """Аутентификация пользователя

        Выполнить аутентификацию пользователя на сервисе AUTH
        """

        email = body['email']
        password = body['password']

        user = valid_user_email(email)
        valid_user_password(user, password)

        client_ip = request.headers.get('X-Forwarded-For') or request.remote_addr
        user_agent = request.headers.get('User-Agent')

        user.make_login(ip_address=client_ip, user_agent=user_agent)

        resp = make_response({'success': True}, HTTPStatus.OK)
        return auth_service.gen_tokens(resp, user.id, user.role.name)


@auth_bp.route('/register')
class UsersRegister(MethodView):
    @auth_bp.arguments(UserRegisterSchema, required=True)
    @auth_bp.alt_response(HTTPStatus.CONFLICT)
    @auth_bp.response(HTTPStatus.CREATED)
    def post(self, body: dict):
        """Регистрация пользователя

        Зарегистрировать пользователя в сервисе AUTH
        """

        user = User(**body, role=Role.default)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT, message='Username or email already used')

        return {'success': True}


@auth_bp.route('/logout')
class UsersLogout(MethodView):
    @auth_bp.alt_response(HTTPStatus.UNAUTHORIZED)
    @auth_bp.response(HTTPStatus.OK)
    @login_required(refresh=True)
    def post(
            self,
            auth_service: AuthService = Provide[Container.auth_service],
        ) -> Response:
        """Выйти из аккаунта

        Выполнить выход из аккаунта
        с последующим удалением и занесением в блэклист refresh токена
        """

        refresh_token_jti = g.refresh_token_jti
        refresh_token_exp = g.refresh_token_exp
        user_id = g.user_id
        client_ip = request.headers.get('X-Forwarded-For') or request.remote_addr
        user_agent = request.headers.get('User-Agent')

        auth_service.add_token_to_blacklist(
            jti=refresh_token_jti,
            user_id=user_id,
            token_exp=refresh_token_exp,
        )

        user = User.query.filter_by(id=user_id).first()
        user.make_logout(ip_address=client_ip, user_agent=user_agent)

        resp = make_response({'success': True}, HTTPStatus.OK)
        resp.delete_cookie(auth_service.access_token_cookie_name)
        resp.delete_cookie(auth_service.refresh_token_cookie_name)
        return resp


@auth_bp.route('/refresh')
class UsersLoginRefresh(MethodView):
    @auth_bp.alt_response(HTTPStatus.UNAUTHORIZED)
    @auth_bp.alt_response(HTTPStatus.NOT_FOUND)
    @auth_bp.response(HTTPStatus.OK)
    @jwt_required(access=False, refresh=True)
    def post(
            self,
            auth_service: AuthService = Provide[Container.auth_service],
        ) -> Response:
        """Обновить токен

        Обновить access токен.
        """

        user = valid_user_id(g.user_id)

        resp = make_response({'success': True}, HTTPStatus.OK)
        return auth_service.gen_tokens(resp, user.id, user.role.name)
