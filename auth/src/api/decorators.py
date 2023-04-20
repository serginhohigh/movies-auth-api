from collections.abc import Callable, Sequence
from functools import wraps

from api.utils import verify_jwt_in_request
from core.permissions import Permissions


def admin_required(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Sequence, **kwargs: dict) -> Callable:
        verify_jwt_in_request(permissions=[Permissions.ADMIN])
        return fn(*args, **kwargs)
    return wrapper


def subscriber_required(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Sequence, **kwargs: dict) -> Callable:
        verify_jwt_in_request(permissions=[Permissions.SUBSCRIBER, Permissions.ADMIN])
        return fn(*args, **kwargs)
    return wrapper


def login_required(*, refresh: bool = False) -> Callable:
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args: Sequence, **kwargs: dict) -> Callable | None:
            verify_jwt_in_request(refresh=refresh)
            return fn(*args, **kwargs)
        return inner
    return wrapper


def jwt_required(*, access: bool = True, refresh: bool = False) -> Callable:
    def wrapper(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args: Sequence, **kwargs: dict) -> Callable | None:
            verify_jwt_in_request(access=access, refresh=refresh)
            return fn(*args, **kwargs)
        return inner
    return wrapper
