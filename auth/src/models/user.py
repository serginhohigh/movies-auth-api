from datetime import UTC, datetime

import bcrypt
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import BYTEA

from db.postgres import db
from models.device import Device
from models.mixins import TimeStampedMixin, UUIDMixin


class User(UUIDMixin, TimeStampedMixin, db.Model):
    __tablename__ = 'users'

    username = db.Column(String(80), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password_hash = db.Column(BYTEA(40), nullable=False)
    role_id = db.Column(ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', uselist=False, back_populates='users')
    devices = db.relationship('Device', cascade='all, delete', passive_deletes=True)
    info = db.relationship('UserInfo', cascade='all, delete', passive_deletes=True)
    socials = db.relationship(
        'SocialAccount', cascade='all, delete', passive_deletes=True)

    @property
    def password(self) -> Exception:
        raise AttributeError

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def password_verify(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def make_login(self, *, ip_address: str, user_agent: str) -> None:
        device = Device.query.filter_by(
            user_id=self.id, ip_address=ip_address, user_agent=user_agent,
        ).first()

        if device:
            device.date_auth = datetime.now(tz=UTC)
            db.session.add(device)
        else:
            device = Device(
                ip_address=ip_address,
                user_agent=user_agent,
                date_auth=datetime.now(tz=UTC),
            )
            self.devices.append(device)
            db.session.add(self)
        db.session.commit()


    def make_logout(self, *, ip_address: str, user_agent: str) -> None:
        device = Device.query.filter_by(
            user_id=self.id, ip_address=ip_address, user_agent=user_agent,
        ).first()

        if device:
            device.date_logout = datetime.now(tz=UTC)
            db.session.add(device)
            db.session.commit()

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class UserInfo(UUIDMixin, TimeStampedMixin, db.Model):
    __tablename__ = 'users_info'

    user_id = db.Column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    first_name = db.Column(String(64))
    last_name = db.Column(String(64))
    age = db.Column(Integer)
    city = db.Column(String(90))
    country = db.Column(String(64))
