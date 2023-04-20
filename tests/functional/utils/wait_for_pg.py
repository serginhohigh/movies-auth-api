import psycopg

from tests.functional.settings import pg_settings
from tests.functional.utils.backoff import backoff


@backoff()
def main() -> None:
    with psycopg.connect(**pg_settings) as _:
        pass


if __name__ == '__main__':
    main()
