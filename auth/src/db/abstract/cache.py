from abc import ABC, abstractmethod
from typing import Any as AnyType
from uuid import UUID


class CacheClient(ABC):
    @abstractmethod
    def set(self, key: str | UUID, value: AnyType, ttl: int = -1) -> Exception:
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> Exception:
        raise NotImplementedError
