from flask import Flask, request
from flask_smorest import Api

from api.v1.admin import admin_bp
from api.v1.auth import auth_bp
from api.v1.user import user_bp
from cli import cli_bp
from core.config import settings
from core.containers import Container
from db.postgres import db, init_migrations, init_sqlalchemy_opentelemetry
from tracing import init_jaeger_tracing


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

    if settings.DEBUG:
        init_jaeger_tracing(app)
        init_sqlalchemy_opentelemetry(app)

    return app


app = create_app()


@app.before_request
def before_request() -> None:
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')
