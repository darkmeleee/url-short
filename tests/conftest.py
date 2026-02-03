import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core import security
from app.db.session import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def test_engine(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("data") / "test.db"
    engine = create_engine(
        f"sqlite+pysqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        try:
            Base.metadata.drop_all(bind=engine)
        finally:
            engine.dispose()
            try:
                db_path.unlink(missing_ok=True)
            except TypeError:
                if db_path.exists():
                    db_path.unlink()


@pytest.fixture()
def db_session(test_engine):
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    old_secret = settings.jwt_secret_key
    settings.jwt_secret_key = "test-secret"

    old_pwd_context = security.pwd_context
    security.pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    with TestClient(app) as c:
        yield c

    security.pwd_context = old_pwd_context
    settings.jwt_secret_key = old_secret

    app.dependency_overrides.clear()


@pytest.fixture()
def user_credentials():
    return {"email": "user@example.com", "password": "password12333"}


@pytest.fixture()
def admin_credentials():
    return {"email": "admin@example.com", "password": "admin12333"}


@pytest.fixture()
def login(client: TestClient):
    def _login(email: str, password: str) -> str:
        resp = client.post(
            "/auth/login",
            data={"username": email, "password": password},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 200, resp.text
        return resp.json()["access_token"]

    return _login
