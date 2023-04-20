from flask import Flask
from flask_smorest import Api

from api.v1.admin import admin_bp
from api.v1.auth import auth_bp
from api.v1.user import user_bp
from cli import cli_bp
from core.config import settings
from core.containers import Container
from db.postgres import db, init_migrations


def create_app() -> Flask:
    container = Container()
    container.config.from_pydantic(settings)
    container.wire(packages=['api', 'api.v1', 'services'])

    app = Flask(__name__)
    app.container = container
    app.config.from_object(settings)

    db.init_app(app)
    init_migrations(app, db)

    api = Api(app)
    api.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    api.register_blueprint(user_bp, url_prefix='/api/v1/users')
    api.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    app.register_blueprint(cli_bp, cli_group=None)
    return app


app = create_app()