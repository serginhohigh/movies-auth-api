from collections.abc import Callable
from http import HTTPStatus
from uuid import UUID

import pytest
from requests import Response

from tests.functional.testdata.tests_cases import AdminTestCase


def test_admin_login(make_request: Callable[..., Response]) -> None:
    method = 'POST'
    subpath = '/auth/login'
    body = {
        'email': AdminTestCase.ADMIN_EMAIL,
        'password': AdminTestCase.ADMIN_PASSWORD,
    }

    resp = make_request(method, subpath, body)

    assert resp.status_code == HTTPStatus.OK


def test_admin_get_roles(make_request: Callable[..., Response]) -> None:
    method = 'GET'
    subpath = '/admin/roles'

    resp = make_request(method, subpath)

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()


@pytest.mark.parametrize(
    ('body', 'expected_status'),
    [
        (
            {
                'name': AdminTestCase.ROLE_CREATE_NAME,
                'description': AdminTestCase.ROLE_CREATE_DESC,
            },
            HTTPStatus.CREATED,
        ),
        (
            {
                'name': AdminTestCase.ROLE_NAME,
                'description': AdminTestCase.ROLE_DESC,
            },
            HTTPStatus.CONFLICT,
        ),
        (
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_admin_create_role(
        make_request: Callable[..., Response],
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'POST'
    subpath = '/admin/roles'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('role_id', 'body', 'expected_status'),
    [
        (
            AdminTestCase.ROLE_ID,
            {
                'name': AdminTestCase.ROLE_RENAME_NEW,
                'description': AdminTestCase.ROLE_REDESC_NEW,
            },
            HTTPStatus.OK,
        ),
        (
            AdminTestCase.ROLE_ID,
            {
                'name': AdminTestCase.ROLE_NAME_EXISTED,
                'description': '',
            },
            HTTPStatus.CONFLICT,
        ),
        (
            AdminTestCase.ROLE_ID_FAKE,
            {
                'name': 'HACKER',
                'description': 'HACKYOU',
            },
            HTTPStatus.NOT_FOUND,
        ),
        (
            AdminTestCase.ROLE_ID,
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_admin_change_role(
        make_request: Callable[..., Response],
        role_id: UUID,
        body: dict,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'PUT'
    subpath = f'/admin/roles/{role_id}'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('user_id', 'expected_status'),
    [
        (
            AdminTestCase.USER_ID,
            HTTPStatus.OK,
        ),
        (
            AdminTestCase.USER_ID_FAKE,
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
def test_admin_users_get_role(
        make_request: Callable[..., Response],
        user_id: UUID,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'GET'
    subpath = f'/admin/users/{user_id}/roles'

    resp = make_request(method, subpath)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('user_id', 'body', 'expected_status'),
    [
        (
            AdminTestCase.USER_ID,
            {
                'role_id': str(AdminTestCase.ROLE_ID),
            },
            HTTPStatus.OK,
        ),
        (
            AdminTestCase.USER_ID_FAKE,
            {
                'role_id': str(AdminTestCase.ROLE_ID),
            },
            HTTPStatus.NOT_FOUND,
        ),
        (
            AdminTestCase.USER_ID,
            {
                'role_id': str(AdminTestCase.ROLE_ID_FAKE),
            },
            HTTPStatus.NOT_FOUND,
        ),
        (
            AdminTestCase.USER_ID,
            {},
            HTTPStatus.UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_admin_users_assign_role(
        make_request: Callable[..., Response],
        user_id: UUID,
        body: UUID,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'PUT'
    subpath = f'/admin/users/{user_id}/roles'

    resp = make_request(method, subpath, body)

    assert resp.status_code == expected_status


@pytest.mark.parametrize(
    ('role_id', 'expected_status'),
    [
        (
            AdminTestCase.ROLE_ID_FOR_DELETE,
            HTTPStatus.OK,
        ),
        (
            AdminTestCase.ROLE_ID,
            HTTPStatus.CONFLICT,
        ),
        (
            AdminTestCase.ROLE_ID_FAKE,
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
def test_admin_delete_role(
        make_request: Callable[..., Response],
        role_id: UUID,
        expected_status: HTTPStatus,
    ) -> None:
    method = 'DELETE'
    subpath = f'/admin/roles/{role_id}'

    resp = make_request(method, subpath)

    assert resp.status_code == expected_status
