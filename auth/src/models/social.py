from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)

from db.postgres import db
from models.mixins import TimeStampedMixin, UUIDMixin


class SocialAccount(UUIDMixin, TimeStampedMixin, db.Model):
    __tablename__ = 'social_account'
    __table_args__ = (
        db.UniqueConstraint('social_id', 'social_name'),
    )

    user_id = db.Column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    social_id = db.Column(Text, nullable=False)
    social_name = db.Column(String(40), nullable=False)

    def __repr__(self) -> str:
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
