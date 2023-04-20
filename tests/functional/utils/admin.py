from datetime import UTC, datetime
from uuid import UUID

import bcrypt
import psycopg

create_user_sql = """
INSERT INTO users (id, username, email, password_hash, role_id, modified, created)
VALUES (%s, %s, %s, %s, (select id from roles where name = %s), %s, %s)
"""

create_role_sql = """
INSERT INTO roles (id, name, description, modified, created) VALUES (%s, %s, %s, %s, %s)
"""

def create_role(
        cursor: psycopg.Cursor,
        role_id: UUID,
        role_name: str,
        role_desc: str,
    ) -> None:
    ts = datetime.now(tz=UTC)
    cursor.execute(
        create_role_sql,
        (role_id, role_name, role_desc, ts, ts),
    )


def create_user(
        cursor: psycopg.Cursor,
        user_id: UUID,
        username: str,
        email: str,
        password: str,
        role_name: str,
    ) -> None:
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    ts = datetime.now(tz=UTC)
    cursor.execute(
        create_user_sql,
        (user_id, username, email, password_hash, role_name, ts, ts),
    )
