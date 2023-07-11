from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from functools import wraps
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask_smorest import abort

from core.containers import Container
from db.redis import RedisCacheClient


class Limiter:
    def per_second(self, max_req_count: int, subkey: Callable) -> Callable:
        """Декоратор для проверки посекундного ограничения трафика.

        Подробнее читайте в self.__check_limit_per_second.

        Args:
            max_req_count (int): Максимальное количество запросов в секунду
            subkey (Callable): Объект, при вызове которого возвращается строка
                с частью ключа для поиска в редисе
        """

        def func_wrapper(fn: Callable) -> Callable:
            @wraps(fn)
            def inner(
                    *args: Sequence,
                    **kwargs: Mapping,
                ) -> Callable:
                self.__check_limit_per_second(subkey(), max_req_count)
                return fn(*args, **kwargs)
            return inner
        return func_wrapper

    @inject
    def __check_limit_per_second(
        self,
        redis_subkey: str,
        max_req_count: int,
        redis_client: RedisCacheClient = Provide[Container.redis_client],
        ) -> None:
        """Проверка посекундного ограничения трафика.

        При выполнении каждого запроса создается ключ следующего вида:
        limit_127.0.0.1_24, где второй и третий элементы при разделении по _
        - это адрес (или любой другой ключ-строка) и текущая минута в часе.
        Значение же хранится в виде списка, где первым элементом является
        текущая секунда в минуте, а вторым количество запросов выполненных
        за эту секунду.

        Args:
            redis_subkey (str): Ключ для поиска в редисе
            max_req_count (int): Максимальное количество запросов в секунду
            redis_client (RedisCacheClient): Клиент для взаимодействия с редисом
        """

        current_datetime = datetime.now(tz=UTC)

        search_key = f'limit_{redis_subkey}_{current_datetime.minute}'

        current_state = redis_client.get(search_key)
        if not current_state:
            redis_client.set(search_key, [current_datetime.second, 1], 59)
            return

        current_second_in_minute, req_count_per_second = current_state

        if current_second_in_minute == current_datetime.second:
            if req_count_per_second >= max_req_count:
                abort(HTTPStatus.TOO_MANY_REQUESTS, message='Too many requests')

            redis_client.set(
                search_key,
                [current_datetime.second, req_count_per_second + 1],
                60 - current_datetime.second,
            )
            return

        redis_client.set(
            search_key, [current_datetime.second, 1], 60 - current_datetime.second)
