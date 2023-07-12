# Сервис аутентификации и авторизации

Сервис аутентификации и авторизации для онлайн кинотеатра. Позволяет осуществлять следующие действия:

- Со стороны пользователя:

  - Вход с помощью email, password
  - Вход с помощью yandex, google
  - Зарегистрироваться
  - Выйти из аккаунта
  - Обновить access токен с помощью refresh токена
  - Посмотреть список подключений (устройства и дата) с пагинацией
  - Изменить никнейм
  - Изменить пароль

- CRUD для администратора:

  - Получить список созданных ролей
  - Создать/Удалить/Изменить роль
  - Получить текущую роль определенного пользователя
  - Назначить необходимую роль определенному пользователю

## Что используется в проекте

- [Nginx](https://nginx.org/)
- [Flask](https://flask.palletsprojects.com/en/latest/) +
  [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [flask-smorest](https://github.com/marshmallow-code/flask-smorest) для реализации API
  с возможностью автогенерации документации
  и валидации с помощью [marshmallow](https://github.com/marshmallow-code/marshmallow)
- [Authlib](https://authlib.org/) для аутентификации с помощью сторонних социальных провайдеров (Yandex, Google)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/) +
  [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) для взаимодействия с базой данных и выполнения миграций
- [OTLP](https://opentelemetry.io/) + [jaeger](https://www.jaegertracing.io/)
- [pytest](https://docs.pytest.org/en/latest/) для функционального тестирования

## Как запуститься

- Выполнить команду `make install`
- Заполнить `.env` файлы в каталогах `./`, `./auth`, `./tests/functional`
- Выполнить команду `make up`
- Выполнить первоначальную миграцию при необходимости можно с помощью команды `make migrate`
- Cоздать учетную запись с правами администратора можно с помощью следующей команды

```
docker exec -it auth flask create-superuser admin admin@mail.local
```

---

Для включения трассировки необходимо выполнить указанные ниже действия. Для просмотра в браузере используйте путь `/admin/jaeger`.

- изменить в `./auth/.env` переменную `DEBUG` и перезапустить сервис
- поднять jaeger с помощью команды `make dev-up c=jaeger`

Проверить rate-limiting можно с помощью указанной ниже команды. Текущая настройка позволяет отправлять 3 запроса в секунду.

```
for n in {1..22}; do echo $(curl -s -w " :: HTTP %{http_code}, %{size_download} bytes, %{time_total} s" -X GET http://127.0.0.1:8000/api/v1/service/ping); sleep 0.1; done
```

---

Контракты API по пути `/admin/api/v1/auth/swagger`.

Для проверки входа с помощью соц. провайдеров не забудьте заполнить необходимые поля в `./auth/.env`.

> Ручка для входа с помощью яндекса - `/api/v1/oauth/yandex/login`
>
> Ручка для входа с помощью гугла - `/api/v1/oauth/google/login`

## Как запустить тестирование

- Выполнить команду `make test`
  > При необходимости выполните `make install`
  >
  > Обратите внимание, что все `.env` файлы в каталогах `./`, `./ugc` и `./tests/functional` должны быть идентичными,
  > то есть иметь одинаковые значения у одинаковых переменных

## TODO

- [ ] Service-Repository pattern
- [ ] Убрать в сервисный слой логику в модели пользователя
- [ ] PDM or Poetry
- [ ] Gunicorn logging
- [ ] Postgres waiter (при тестах могут быть проблемы с миграциями,
      см. [тут](https://github.com/serginhohigh/movies-auth-api/blob/eba2d8a09032a4d2b99b9c98633c986eb1f309ef/Makefile#L50)
- [ ] Добавить статику для swagger,
      см. [тут](https://github.com/serginhohigh/movies-auth-api/blob/eba2d8a09032a4d2b99b9c98633c986eb1f309ef/auth/src/core/config.py#L49)
- [ ] Перевести README.md на английский язык
