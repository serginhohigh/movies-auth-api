from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError

from api.utils.social_providers import SocialProviderType


class SocialConverter(BaseConverter):
    def to_python(self, value: str) -> str | Exception:
        if value not in SocialProviderType.to_list():
            raise ValidationError
        return value


def init_converters(app: Flask) -> None:
    app.url_map.converters['social'] = SocialConverter
