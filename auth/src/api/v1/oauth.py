from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import make_response, url_for
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from api.utils.oauth import oauth
from api.utils.social_providers import SocialProviderType
from core.containers import Container
from models.user import User
from services.auth import AuthService

oauth_bp = Blueprint('oauth', 'oauth')


@oauth_bp.route('/<social:provider>/login')
class OauthSocialProviderLogin(MethodView):
    @oauth_bp.alt_response(HTTPStatus.NOT_FOUND)
    @oauth_bp.response(HTTPStatus.OK)
    def get(self, provider: str):
        """Аутентификация с помощью стороннего социального провайдера

        Аутентификация с помощью Yandex или Google.
        """

        oauth_client = oauth.create_client(provider)
        return oauth_client.authorize_redirect(
            url_for(
                'oauth.OauthSocialProviderCallback',
                provider=provider,
                _external=True,
            ),
        )


@oauth_bp.route('/<social:provider>/callback')
class OauthSocialProviderCallback(MethodView):
    @oauth_bp.alt_response(HTTPStatus.BAD_REQUEST)
    @oauth_bp.alt_response(HTTPStatus.NOT_FOUND)
    @oauth_bp.response(HTTPStatus.OK)
    @inject
    def get(
            self,
            provider: str,
            auth_service: AuthService = Provide[Container.auth_service],
        ):
        """Коллбэк для аутентификации с помощью стороннего социального провайдера"""

        oauth_client = oauth.create_client(provider)
        oauth_client.authorize_access_token()

        social_provider = SocialProviderType[provider]

        try:
            social_id, email, username = social_provider.value.get_user_info(
                oauth_client.userinfo())
        except KeyError:
            abort(HTTPStatus.NOT_FOUND, message='Wrong answer from social provider')

        user = User.login_via_social(
            social_id,
            social_provider.name,
            email,
            username,
            auth_service.gen_random_password(),
        )

        resp = make_response({'success': True}, HTTPStatus.OK)
        return auth_service.gen_tokens(resp, user.id, user.role.name)
