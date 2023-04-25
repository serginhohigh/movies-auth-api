from abc import ABC, abstractmethod
from enum import Enum


class SocialProvider(ABC):
    @abstractmethod
    def get_user_info(self, user_info: dict) -> tuple:
        raise NotImplementedError


class YandexSocialProvider(SocialProvider):
    def get_user_info(self, user_info: dict) -> tuple:
        return user_info['id'], user_info['default_email'], user_info['login']


class GoogleSocialProvider(SocialProvider):
    def get_user_info(self, user_info: dict) -> tuple:
       return user_info['sub'], user_info['email'], user_info['name']


class SocialProviderType(Enum):
    yandex = YandexSocialProvider()
    google = GoogleSocialProvider()

    @staticmethod
    def to_list() -> list:
        return [provider.name for provider in list(SocialProviderType)]
