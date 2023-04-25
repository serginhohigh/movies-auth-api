import json
from typing import Any as AnyType
from uuid import UUID

from flask import Flask
from opentelemetry.instrumentation.redis import RedisInstrumentor
from redis import Redis

from db.abstract.cache import CacheClient


class RedisCacheClient(CacheClient):
    def __init__(self, connection: Redis) -> None:
        self.redis = connection

    def set(self, key: str | UUID, value: AnyType, ttl: int = -1) -> None:
        if isinstance(key, UUID):
            key = str(key)

        value = json.dumps(value)
        self.redis.set(key, value, ttl)

    def get(self, key: str) -> AnyType:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return value


def init_redis_opentelemetry(app: Flask) -> None:
    with app.app_context():
        RedisInstrumentor().instrument()


def init_redis(
        host: str,
        port: int,
        password: str,
        db: int,
    ) -> Redis:
    return Redis(host=host, port=port, password=password, db=db, decode_responses=True)
