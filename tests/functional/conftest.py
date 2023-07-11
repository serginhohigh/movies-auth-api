from collections.abc import Callable, Generator

import psycopg
import pytest
import requests

from tests.functional.settings import pg_settings, settings
from tests.functional.testdata.tests_cases import AdminTestCase
from tests.functional.utils.admin import create_role, create_user


@pytest.fixture(scope='session')
def api_client() -> Generator[requests.Session, None, None]:
    with requests.Session() as s:
        yield s


@pytest.fixture(scope='session', autouse=True)
def _prepare_test_env() -> None:
    with psycopg.connect(**pg_settings) as conn, conn.cursor() as cur:
        create_role(
            cur,
            AdminTestCase.ROLE_ID_FOR_DELETE,
            AdminTestCase.ROLE_NAME_FOR_DELETE,
            AdminTestCase.ROLE_DESC_FOR_DELETE,
        )
        create_role(
            cur,
            AdminTestCase.ROLE_ID,
            AdminTestCase.ROLE_NAME,
            AdminTestCase.ROLE_DESC,
        )
        create_user(
            cur,
            AdminTestCase.ADMIN_USER_ID,
            AdminTestCase.ADMIN_USERNAME,
            AdminTestCase.ADMIN_EMAIL,
            AdminTestCase.ADMIN_PASSWORD,
            'admin',
        )
        create_user(
            cur,
            AdminTestCase.USER_ID,
            AdminTestCase.USERNAME,
            AdminTestCase.EMAIL,
            AdminTestCase.PASSWORD,
            AdminTestCase.ROLE_NAME,
        )


@pytest.fixture
def make_request(api_client: requests.Session) -> Callable[..., requests.Response]:
    def inner(
            method: str,
            subpath: str,
            body: dict | None = None,
            *,
            cookies: dict | None = None,
            cookies_override: bool = False,
        ) -> requests.Response:

        if cookies:
            if cookies_override:
                api_client.cookies.clear()

            for k, v in cookies.items():
                api_client.cookies.set(k, v)

        url = f'{settings.AUTH_URL}{subpath}'
        return api_client.request(
            method,
            url,
            json=body,
            headers={'X-Request-Id': '6117bcb5-f903-45dc-9bc5-7d0c67643ea7'},
        )
    return inner
