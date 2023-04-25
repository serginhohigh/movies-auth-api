from authlib.integrations.flask_client import OAuth
from flask import Flask

oauth = OAuth()


def init_oauth(app: Flask) -> None:
    """Отложенная ининциализации authlib.

    Вся необходимая информация для регистрации провайдеров берется
    из переменных окружения.
    Более поробно читайте в https://docs.authlib.org/en/latest/client/flask.html#flask-client
    """

    oauth.init_app(app)

    oauth.register(
        name='yandex',
        userinfo_endpoint='https://login.yandex.ru/info',
    )

    oauth.register(
        name='google',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={
            'scope': 'profile email',
        },
    )
