from http import HTTPStatus
from uuid import UUID

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from api.schemas.role import RoleSchema, RoleSchemaCreate, RoleSchemaModify
from api.schemas.user import UserAssignRoleSchema
from api.utils.jwt_verifier import verify_jwt_in_request
from api.validators import valid_role_id, valid_user_id
from core.permissions import Permissions
from db.postgres import db
from models.role import Role
from models.user import User

admin_bp = Blueprint('admin', 'admin')


@admin_bp.before_request
def verify_admin_access() -> None:
    verify_jwt_in_request(permissions=[Permissions.ADMIN])


@admin_bp.route('/roles')
class Roles(MethodView):
    @admin_bp.response(HTTPStatus.OK, RoleSchema(many=True))
    def get(self):
        """Список ролей

        Получить весь список ролей.
        """

        return Role.query.all()

    @admin_bp.arguments(RoleSchemaCreate, required=True)
    @admin_bp.response(HTTPStatus.CREATED, RoleSchema)
    @admin_bp.alt_response(HTTPStatus.CONFLICT)
    def post(self, body: dict):
        """Создать роль

        Создать роль с указанием названия и описания.
        """

        role = Role(**body)

        try:
            db.session.add(role)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT, 'Role already exist')

        return role


@admin_bp.route('/roles/<uuid:role_id>')
class RolesById(MethodView):
    @admin_bp.arguments(RoleSchemaModify, required=True)
    @admin_bp.response(HTTPStatus.OK, RoleSchema)
    @admin_bp.alt_response(HTTPStatus.NOT_FOUND)
    @admin_bp.alt_response(HTTPStatus.CONFLICT)
    def put(self, body: dict, role_id: UUID):
        """Изменить роль

        Изменить имя или описание роли.
        """

        role_name = body.get('name')
        role_description = body.get('description')

        role: Role = valid_role_id(role_id)

        if role_name:
            role.name = role_name

        if role_description:
            role.description = role_description

        try:
            db.session.add(role)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT, message='Another role have same name')

        return role

    @admin_bp.response(HTTPStatus.OK, RoleSchema)
    @admin_bp.alt_response(HTTPStatus.NOT_FOUND)
    @admin_bp.alt_response(HTTPStatus.CONFLICT)
    def delete(self, role_id: UUID):
        """Удалить роль"""

        role: Role = valid_role_id(role_id)
        try:
            db.session.delete(role)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.CONFLICT, message='Role have assignies')

        return role


@admin_bp.route('/users/<uuid:user_id>/roles')
class UsersByIdManageRoles(MethodView):
    @admin_bp.response(HTTPStatus.OK, RoleSchema)
    @admin_bp.alt_response(HTTPStatus.NOT_FOUND)
    def get(self, user_id: UUID):
        """Текущая роль пользователя"""

        user: User = valid_user_id(user_id)
        return user.role

    @admin_bp.arguments(UserAssignRoleSchema, required=True)
    @admin_bp.response(HTTPStatus.OK)
    @admin_bp.alt_response(HTTPStatus.NOT_FOUND)
    def put(self, body: dict, user_id: UUID):
        """Назначить пользователю роль"""

        role: Role = valid_role_id(body['role_id'])
        user: User = valid_user_id(user_id)

        user.role = role
        db.session.add(user)
        db.session.commit()

        return {'success': True}
