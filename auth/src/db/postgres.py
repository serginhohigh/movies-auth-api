from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import MetaData

from core.config import settings

db = SQLAlchemy(metadata=MetaData(schema=settings.PG_SCHEMA))
migrate = Migrate()


def init_migrations(app: Flask, db: SQLAlchemy) -> None:
    """Используется для корректной инициализации flask-migrate.
    Без предварительного импорта моделей работать миграции не будут!
    """

    from models import device, role, social, user

    migrate.init_app(app, db, compare_type=True)


def init_sqlalchemy_opentelemetry(app: Flask) -> None:
    with app.app_context():
        SQLAlchemyInstrumentor().instrument(engine=db.get_engine())
