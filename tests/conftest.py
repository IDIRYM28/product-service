import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
os.environ.setdefault("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
from app.main import app
from app.config.database import Base, get_db
os.environ.setdefault("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db_session(test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    import app.routers.product as ap
    import app.routers.rabbitmq as msg_mod
    monkeypatch.setattr(ap, "publish_client", lambda payload: None)
@pytest.fixture
def sample_product_data():
    return {
        "name": "Test Product",
        "description": "Test Description",
        "stock": 10,
        "prices": [{"amount": 19.99}]
    }