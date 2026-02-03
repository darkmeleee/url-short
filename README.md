# url-short

Простой "укорачиватель" ссылок с PostgreSQL и JWT-авторизацией.

## Зависимости

- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- passlib[bcrypt]
- python-jose
- pydantic

## Переменные окружения

- `DATABASE_URL` (пример: `postgresql+psycopg2://postgres:postgres@localhost:5432/url_short`)
- `JWT_SECRET_KEY` (обязательно заменить на свой секрет)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (по умолчанию 60)

## Архитектура

- `app/main.py` — FastAPI приложение и подключение роутов
- `app/api/routes/*` — роуты (auth, links, admin)
- `app/core/*` — конфиг и безопасность (JWT)
- `app/db/*` — сессия БД
- `app/models.py` — модели SQLAlchemy
- `app/schemas.py` — Pydantic схемы
- `app/scripts/create_admin.py` — CLI для создания admin

## Миграции (Alembic)

1. Инициализация (уже в репозитории): `alembic/`
2. Создать миграцию:

```bash
alembic revision --autogenerate -m "init"
```

3. Применить миграции:

```bash
alembic upgrade head
```

## Запуск

1. Поднимите PostgreSQL и создайте базу `url_short`
2. Установите зависимости

3) Выполните миграции Alembic (см. выше)
4) Запустите приложение:

```bash
uvicorn app.main:app --reload
```

## Администратор

Создать admin пользователя:

```bash
python -m app.scripts.create_admin --email admin@mail.com --password admin123
```

## Эндпоинты

- `POST /auth/register` — регистрация
- `POST /auth/login` — получение JWT
- `POST /shorten` — создание ссылки (нужен Bearer токен)
- `GET /link?key=...` — редирект по короткой ссылке
- `GET /admin/users` — список пользователей (роль admin)
