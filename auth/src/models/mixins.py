import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db


class UUIDMixin:
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TimeStampedMixin:
    created = db.Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    modified = db.Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
