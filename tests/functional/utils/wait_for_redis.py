from redis import Redis

from tests.functional.settings import settings
from tests.functional.utils.backoff import backoff


@backoff()
def main() -> None:
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    )
    redis_client.ping()


if __name__ == '__main__':
    main()
