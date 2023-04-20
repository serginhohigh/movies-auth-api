from collections.abc import Callable
from http import HTTPStatus

import pytest
from requests import Response

from tests.functional.testdata.tests_cases import UserTestCase


def test_user_history_login(make_request: Callable[..., Response]) -> None:
    method = 'GET'
    subpath = '/users/history/login'

    resp: Response = make_request(method, subpath)

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()


@pytest.mark.parametrize(
    ('body', 'expected_status'),
    [
        (
            {
                'password': UserTestCase.PASSWORD,
                'username_new': UserTestCase.USERNAME_NEW,
            },
            HTTPStatus.OK,
        ),
        (
            {
                'password': UserTestCase.PASSWORD_FAKE,
                'username_new': UserTestCase.USERNAME_NEW,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {
                'password': UserTestCase.PASSWORD,
                'username_new': UserTestCase.USERNAME_EXISTED,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_user_change_username(
        make_request: Callable[..., Response],
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'PUT'
    subpath = '/users/username'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('body', 'expected_status'),
    [
        (
            {
                'password_old': UserTestCase.PASSWORD,
                'password_new': UserTestCase.PASSWORD_NEW,
            },
            HTTPStatus.OK,
        ),
        (
            {
                'password_old': UserTestCase.PASSWORD,
                'password_new': UserTestCase.PASSWORD_NEW,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_user_change_password(
        make_request: Callable[..., Response],
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'PUT'
    subpath = '/users/password'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


def test_user_wrong_permissions(make_request: Callable[..., Response]) -> None:
    method = 'GET'
    subpath = '/admin/roles'

    resp = make_request(method, subpath)

    assert resp.status_code == HTTPStatus.UNAUTHORIZED
