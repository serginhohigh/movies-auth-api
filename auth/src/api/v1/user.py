from http import HTTPStatus

from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint, Page, abort
from sqlalchemy.exc import IntegrityError

from api.schemas.device import DeviceSchema
from api.schemas.user import UserChangePasswordSchema, UserChangeUsernameSchema
from api.utils import verify_jwt_in_request
from api.validators import valid_user_id, valid_user_password
from db.postgres import db
from models.device import Device
from models.user import User

user_bp = Blueprint('users', 'users')


@user_bp.before_request
def verify_login() -> None:
    verify_jwt_in_request()


class CursorPage(Page):
    @property
    def item_count(self):
        return self.collection.count()


@user_bp.route('/history/login')
class UsersByJWTHistoryLogin(MethodView):
    @user_bp.alt_response(HTTPStatus.NOT_FOUND)
    @user_bp.response(HTTPStatus.OK, DeviceSchema(many=True))
    @user_bp.paginate(CursorPage)
    def get(self):
        """История подключений пользователя"""

        valid_user_id(g.user_id)
        return Device.query.filter_by(user_id=g.user_id)


@user_bp.route('/username')
class UsersByJWTChangeUsername(MethodView):
    @user_bp.arguments(UserChangeUsernameSchema, required=True)
    @user_bp.alt_response(HTTPStatus.CONFLICT)
    @user_bp.response(HTTPStatus.OK)
    def put(self, body: dict):
        """Изменить никнейм (username)"""

        user_password = body['password']
        user_username_new = body['username_new']

        user: User = valid_user_id(g.user_id)

        valid_user_password(user, user_password)

        user.username = user_username_new
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT, message='This username already used')

        return {'success': True}


@user_bp.route('/password')
class UsersByJWTChangePassword(MethodView):
    @user_bp.arguments(UserChangePasswordSchema, required=True)
    @user_bp.alt_response(HTTPStatus.CONFLICT)
    @user_bp.response(HTTPStatus.OK)
    def put(self, body: dict):
        """Изменить пароль"""

        password_new = body['password_new']
        password_old = body['password_old']

        user: User = valid_user_id(g.user_id)

        valid_user_password(user, password_old)

        user.password = password_new
        db.session.add(user)
        db.session.commit()

        return {'success': True}
