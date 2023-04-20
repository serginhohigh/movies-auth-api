from enum import Enum, unique


@unique
class Permissions(Enum):
    USER = 'user'
    SUBSCRIBER = 'subscriber'
    ADMIN = 'admin'

    def __str__(self) -> str:
        return self.value
