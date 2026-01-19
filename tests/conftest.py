import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from api.main import app
from api.database import get_db
from api.models import Base
from api.routers.dependencies import get_current_utilisateur

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture pour configurer la base de données avant chaque test."""
    Base.metadata.drop_all(bind=engine)  # Supprimer les tables avant chaque test
    Base.metadata.create_all(bind=engine)  # Recréer les tables
    yield
    Base.metadata.drop_all(bind=engine)  # Nettoyage après le test


def override_get_db():
    """Override pour injecter une session de test dans les dépendances."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_utilisateur():
    class FakeRole:
        def __init__(self, libelleRole):
            self.libelleRole = libelleRole

    class FakeUser:
        idUtil = 1
        roles = [FakeRole("Admin")]

    return FakeUser()



@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_utilisateur] = override_get_current_utilisateur

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
