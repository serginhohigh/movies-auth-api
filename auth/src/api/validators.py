from http import HTTPStatus
from uuid import UUID

from flask_smorest import abort
from sqlalchemy.exc import NoResultFound

from models.role import Role
from models.user import User


def valid_user_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()
    if not user:
        abort(HTTPStatus.NOT_FOUND, message='User with this email doesnt find')
    return user


def valid_user_id(user_id: UUID) -> User:
    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, message='User not found')
    return user


def valid_user_password(user: User, password: str) -> None:
    if not user.password_verify(password):
        abort(HTTPStatus.CONFLICT, message='Incorrect password')


def valid_role_id(role_id: UUID) -> Role:
    try:
        role = Role.query.filter_by(id=role_id).one()
    except NoResultFound:
        abort(HTTPStatus.NOT_FOUND, message='Role not found')
    return role
