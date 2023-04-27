import uuid

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import INET

from db.postgres import db


class Device(db.Model):
    __tablename__ = 'devices'
    __table_args__ = (
        db.UniqueConstraint('id', 'logged_in_at'),
        {
            'postgresql_partition_by': 'RANGE (logged_in_at)',
        },
    )

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    user_id = db.Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(Text, nullable=False)
    ip_address = db.Column(INET, nullable=False)
    logged_in_at = db.Column(TIMESTAMP(timezone=True), primary_key=True, nullable=True)
