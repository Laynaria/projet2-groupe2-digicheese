import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from api.main import app
from api.database import get_db
from api.models import Base
from api.routers.dependencies import get_current_utilisateur


def get_test_database_url():
    """
    Retourne l'URL de la base de données de test.
    Utilise MySQL/MariaDB si les variables d'environnement sont définies (CI),
    sinon utilise SQLite (développement local).
    """
    db_host = os.getenv("DB_HOST")

    if db_host:
        # Mode CI : utiliser MySQL/MariaDB
        db_user = os.getenv("DB_USER", "admin")
        db_password = os.getenv("DB_PASSWORD", "Admin123!")
        db_name = os.getenv("DB_NAME", "digicheese")
        db_port = os.getenv("DB_PORT", "3306")

        database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        print(f"📊 Using MySQL/MariaDB for tests: {db_host}:{db_port}/{db_name}")
        return database_url, {}
    else:
        # Mode local : utiliser SQLite
        database_url = "sqlite:///./test.db"
        print("📊 Using SQLite for tests: test.db")
        return database_url, {"check_same_thread": False}


# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL, connect_args = get_test_database_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture pour configurer la base de données avant chaque test."""
    # Supprimer les tables avant chaque test
    Base.metadata.drop_all(bind=engine)
    # Recréer les tables
    Base.metadata.create_all(bind=engine)
    yield
    # Nettoyage après le test
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Override pour injecter une session de test dans les dépendances."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def override_get_current_utilisateur():
    """Simule un utilisateur admin pour les tests."""

    class FakeRole:
        def __init__(self, libelleRole):
            self.libelleRole = libelleRole

    class FakeUser:
        idUtil = 1
        roles = [FakeRole("Admin")]

    return FakeUser()


@pytest.fixture(scope="module")
def client():
    """Client de test FastAPI avec overrides de dépendances."""
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_utilisateur] = override_get_current_utilisateur

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def relcond_id(client: TestClient):
    """Fixture pour créer une relation conditionnement de test."""
    relcond_data = {
        "quantiteObjet": 1
    }

    response = client.post(
        "/api/v1/rel-conds",
        headers={"Authorization": "Bearer fake"},
        json=relcond_data
    )

    assert response.status_code == 201, f"Failed to create relcond: {response.text}"
    return response.json()["idRelCond"]