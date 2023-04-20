from uuid import UUID, uuid4


class AdminTestCase:
    ADMIN_USER_ID: UUID = uuid4()
    ADMIN_USERNAME = 'admintestuser'
    ADMIN_EMAIL = 'admintestuser@mail.local'
    ADMIN_PASSWORD = 'admintestpassword'

    USER_ID: UUID = uuid4()
    USERNAME = 'testuser'
    EMAIL = 'testuser@mail.local'
    PASSWORD = 'testpassword'

    USER_ID_FAKE: UUID = uuid4()

    ROLE_ID: UUID = uuid4()
    ROLE_NAME = 'moderator'
    ROLE_DESC = 'The moderator of resource'
    ROLE_RENAME_NEW = 'ChiefModerator'
    ROLE_REDESC_NEW = 'The ChiefModerator of resource'

    ROLE_CREATE_NAME = 'anon'
    ROLE_CREATE_DESC = 'The anon'

    ROLE_NAME_EXISTED = 'subscriber'

    ROLE_ID_FAKE: UUID = uuid4()

    ROLE_ID_FOR_DELETE: UUID = uuid4()
    ROLE_NAME_FOR_DELETE = 'deleteme'
    ROLE_DESC_FOR_DELETE = 'deletemenow!'


class UserTestCase:
    USERNAME = 'test'
    EMAIL = 'test@mail.local'
    PASSWORD = '123321'

    USERNAME_NEW = 'testNew'
    USERNAME_EXISTED = AdminTestCase.USERNAME
    EMAIL_FAKE = 'abcd@mail.local'
    PASSWORD_FAKE = '123'
    PASSWORD_NEW = '123456'
