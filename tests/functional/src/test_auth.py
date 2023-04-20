from collections.abc import Callable
from http import HTTPStatus

import pytest
from requests import Response

from tests.functional.testdata.tests_cases import UserTestCase


class TokenStorage:
    access_token = None
    refresh_token = None


@pytest.mark.parametrize(
    ('body', 'expected_status'),
    [
        (
            {
                'email': UserTestCase.EMAIL,
                'username': UserTestCase.USERNAME,
                'password': UserTestCase.PASSWORD,
            },
            HTTPStatus.CREATED,
        ),
        (
            {
                'email': UserTestCase.EMAIL,
                'username': UserTestCase.USERNAME,
                'password': UserTestCase.PASSWORD,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_auth_register(
        make_request: Callable[..., Response],
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'POST'
    subpath = '/auth/register'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('body', 'expected_status'),
    [
        (
            {
                'email': UserTestCase.EMAIL,
                'password': UserTestCase.PASSWORD,
            },
            HTTPStatus.OK,
        ),
        (
            {
                'email': UserTestCase.EMAIL,
                'password': UserTestCase.PASSWORD_FAKE,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {
                'email': UserTestCase.EMAIL_FAKE,
                'password': UserTestCase.PASSWORD,
            },
            HTTPStatus.NOT_FOUND,
        ),
        (
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_auth_login(
        make_request: Callable[..., Response],
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'POST'
    subpath = '/auth/login'

    resp = make_request(method, subpath, body)
    if expected_status is HTTPStatus.OK:
        TokenStorage.access_token = resp.cookies.get('access_token')
        TokenStorage.refresh_token = resp.cookies.get('refresh_token')

    assert resp.status_code == expected_status


@pytest.mark.order(-1)
def test_auth_refresh(make_request: Callable[..., Response]) -> None:
    method = 'POST'
    subpath = '/auth/refresh'

    resp = make_request(
        method,
        subpath,
        cookies={'refresh_token': TokenStorage.refresh_token},
        cookies_override=True,
    )

    assert resp.status_code == HTTPStatus.OK
    assert 'access_token' in resp.cookies


@pytest.mark.order(after='test_auth_refresh')
def test_auth_logout(make_request: Callable[..., Response]) -> None:
    method = 'POST'
    subpath = '/auth/logout'

    resp = make_request(method, subpath)

    assert resp.status_code == HTTPStatus.OK
    assert not resp.cookies


@pytest.mark.order(after='test_auth_refresh')
def test_auth_refresh_blacklisted(make_request: Callable[..., Response]) -> None:
    method = 'POST'
    subpath = '/auth/refresh'

    resp = make_request(
        method,
        subpath,
        cookies={'refresh_token': TokenStorage.refresh_token},
        cookies_override=True,
    )

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
