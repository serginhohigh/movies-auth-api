import json
from abc import ABC, abstractmethod
from typing import Any as AnyType
from uuid import UUID

from redis import Redis


class CacheClient(ABC):
    @abstractmethod
    def set(self) -> Exception:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Exception:
        raise NotImplementedError


class RedisCacheClient(CacheClient):
    def __init__(self, connection: Redis) -> None:
        self.redis = connection

    def set(self, key: str | UUID, value: AnyType, ttl: int) -> None:
        if isinstance(key, UUID):
            key = str(key)

        value = json.dumps(value)
        self.redis.set(key, value, ttl)

    def get(self, key: str) -> AnyType:
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return value


def init_redis(
        host: str,
        port: int,
        password: str,
        db: int,
    ) -> Redis:
    return Redis(host=host, port=port, password=password, db=db, decode_responses=True)
