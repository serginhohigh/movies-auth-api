from typing import Self

from sqlalchemy import (
    String,
    Text,
)

from db.postgres import db
from models.mixins import TimeStampedMixin, UUIDMixin


class Role(UUIDMixin, TimeStampedMixin, db.Model):
    __tablename__ = 'roles'

    name = db.Column(String(80), unique=True, nullable=False)
    description = db.Column(Text, nullable=False)

    users = db.relationship('User', back_populates='role', viewonly=True)

    @classmethod
    @property
    def default(cls) -> Self:
        return cls.query.filter_by(name='user').first()

    def __repr__(self) -> str:
        return f'<Role {self.name}>'
