from sqlalchemy import (
    TIMESTAMP,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import INET

from db.postgres import db
from models.mixins import UUIDMixin


class Device(UUIDMixin, db.Model):
    __tablename__ = 'devices'
    __table_args__ = (
        db.Index('devices_user_id_idx', 'user_id'),
    )

    user_id = db.Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_agent = db.Column(Text, nullable=False)
    ip_address = db.Column(INET, nullable=False)
    date_auth = db.Column(TIMESTAMP(timezone=True), nullable=True)
    date_logout = db.Column(TIMESTAMP(timezone=True), nullable=True)
