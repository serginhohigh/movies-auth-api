import click
from flask import Blueprint

from db.postgres import db
from models.role import Role
from models.user import User

cli_bp = Blueprint('cli_bp', __name__)


@cli_bp.cli.command('create-superuser')
@click.argument('username')
@click.argument('email')
@click.option(
    '--password',
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
)
def create_superuser(username: str, email: str, password: str) -> None:
    user = User(
        username=username,
        email=email,
        password=password,
    )
    role = db.session.scalar(db.select(Role).filter_by(name='admin'))
    user.role = role

    db.session.add(user)
    db.session.commit()
