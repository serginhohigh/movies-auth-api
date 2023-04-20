"""Initial migration

Revision ID: dbc9d353c0e6
Revises:
Create Date: 2023-04-18 19:00:34.880620

"""
import uuid
from datetime import datetime, UTC

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dbc9d353c0e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE SCHEMA IF NOT EXISTS auth')
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('modified', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='auth'
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', postgresql.BYTEA(length=40), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('modified', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['auth.roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username'),
    schema='auth'
    )
    op.create_table('devices',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip_address', postgresql.INET(), nullable=False),
    sa.Column('date_auth', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_logout', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    schema='auth'
    )
    with op.batch_alter_table('devices', schema='auth') as batch_op:
        batch_op.create_index('devices_user_id_idx', ['user_id'], unique=False)

    op.create_table('users_info',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('city', sa.String(length=90), nullable=True),
    sa.Column('country', sa.String(length=64), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('modified', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['auth.users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id'),
    schema='auth'
    )
    # ### end Alembic commands ###

    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind(), only=('roles',))
    roles_table = sa.Table('roles', meta)
    roles_created = datetime.now(tz=UTC)
    op.bulk_insert(
        roles_table,
        [
            {
                'id': uuid.uuid4(),
                'name': 'admin',
                'description': '',
                'created': roles_created,
                'modified': roles_created,
            },
            {
                'id': uuid.uuid4(),
                'name': 'user',
                'description': '',
                'created': roles_created,
                'modified': roles_created,
            },
            {
                'id': uuid.uuid4(),
                'name': 'subscriber',
                'description': '',
                'created': roles_created,
                'modified': roles_created,
            },
        ]
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_info', schema='auth')
    with op.batch_alter_table('devices', schema='auth') as batch_op:
        batch_op.drop_index('devices_user_id_idx')

    op.drop_table('devices', schema='auth')
    op.drop_table('users', schema='auth')
    op.drop_table('roles', schema='auth')
    # ### end Alembic commands ###