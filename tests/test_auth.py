import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from api.database import get_db
from api.models import Base
from api.models.utilisateur import Utilisateur
from api.models.role import Role
from api.models.utilisateur_role import UtilisateurRole
from api.routers.dependencies import get_current_utilisateur
from api.services.security_service import get_password_hash, create_access_token

# --- Bypass AdminOnly ---
_ADMIN_ONLY_DEPS = []
try:
    from api.routers.utilisateur_router import AdminOnly as UtilisateursAdminOnly

    _ADMIN_ONLY_DEPS.append(UtilisateursAdminOnly)
except Exception:
    pass

try:
    from api.routers.role_router import AdminOnly as RolesAdminOnly

    _ADMIN_ONLY_DEPS.append(RolesAdminOnly)
except Exception:
    pass

# ---- DB de test ISOLÉE (nom différent) ----
SQLALCHEMY_DATABASE_URL_AUTH = "sqlite:///./test_auth.db"
engine_auth = create_engine(
    SQLALCHEMY_DATABASE_URL_AUTH, connect_args={"check_same_thread": False}
)
TestingSessionLocalAuth = sessionmaker(autocommit=False, autoflush=False, bind=engine_auth)


# ---- Classe pour isoler l'app ----
class IsolatedApp:
    """Context manager pour isoler les overrides de l'app."""

    def __init__(self):
        self.saved_overrides = None

    def __enter__(self):
        # Sauvegarder les overrides actuels
        self.saved_overrides = app.dependency_overrides.copy()
        return self

    def __exit__(self, *args):
        # Restaurer les overrides
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.saved_overrides)


@pytest.fixture(scope="function", autouse=True)
def setup_auth_database():
    """Setup/teardown de la base de données pour chaque test."""
    Base.metadata.drop_all(bind=engine_auth)
    Base.metadata.create_all(bind=engine_auth)
    yield
    Base.metadata.drop_all(bind=engine_auth)


def override_get_db_auth():
    """Override get_db pour les tests d'auth."""
    db = TestingSessionLocalAuth()
    try:
        yield db
    finally:
        db.close()


def override_get_current_utilisateur_admin():
    class FakeRole:
        def __init__(self, libelleRole):
            self.libelleRole = libelleRole

    class FakeUser:
        idUtil = 1
        roles = [FakeRole("Admin")]

    return FakeUser()


def override_get_current_utilisateur_user():
    class FakeRole:
        def __init__(self, libelleRole):
            self.libelleRole = libelleRole

    class FakeUser:
        idUtil = 2
        roles = [FakeRole("User")]

    return FakeUser()


def override_admin_only():
    """Bypass du require_roles('Admin')."""
    return True


@pytest.fixture(scope="function")
def client_admin():
    """Client avec droits admin."""
    with IsolatedApp():
        app.dependency_overrides[get_db] = override_get_db_auth
        app.dependency_overrides[get_current_utilisateur] = override_get_current_utilisateur_admin

        for dep in _ADMIN_ONLY_DEPS:
            app.dependency_overrides[dep] = override_admin_only

        with TestClient(app) as c:
            yield c


@pytest.fixture(scope="function")
def client_user():
    """Client avec droits user."""
    with IsolatedApp():
        app.dependency_overrides[get_db] = override_get_db_auth
        app.dependency_overrides[get_current_utilisateur] = override_get_current_utilisateur_user

        with TestClient(app) as c:
            yield c


# ---- JWT headers ----
def make_auth_headers(*roles: str, user_id: int = 1) -> dict:
    token = create_access_token(user_id=user_id, roles=list(roles))
    return {"Authorization": f"Bearer {token}"}


ADMIN_AUTH_HEADERS = make_auth_headers("Admin", user_id=1)
USER_AUTH_HEADERS = make_auth_headers("User", user_id=2)


# ---- Helpers DB ----
def seed_role(db, libelle: str) -> Role:
    role = Role(libelleRole=libelle)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def seed_user(db, *, email: str, password_plain: str, nom="Doe", prenom="John") -> Utilisateur:
    user = Utilisateur(
        nomUtil=nom,
        prenomUtil=prenom,
        emailUtil=email,
        motDePasse=get_password_hash(password_plain),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def attach_role(db, user_id: int, role_id: int):
    db.add(UtilisateurRole(idUtil=user_id, idRole=role_id))
    db.commit()


# ===================== TESTS AUTH =====================
AUTH_LOGIN_ENDPOINT = "/api/v1/auth/login"


def test_login_ok_returns_token(client_admin: TestClient):
    db = TestingSessionLocalAuth()
    try:
        admin_role = seed_role(db, "Admin")
        u = seed_user(db, email="admin@test.com", password_plain="Password123!")
        attach_role(db, u.idUtil, admin_role.idRole)
    finally:
        db.close()

    payload = {"email": "admin@test.com", "motDePasse": "Password123!"}
    r = client_admin.post(AUTH_LOGIN_ENDPOINT, json=payload)
    assert r.status_code == 200, r.text

    data = r.json()
    assert "access_token" in data
    assert data.get("token_type", "").lower() == "bearer"


def test_login_bad_password_returns_401(client_admin: TestClient):
    db = TestingSessionLocalAuth()
    try:
        seed_role(db, "Admin")
        seed_user(db, email="user@test.com", password_plain="GoodPwd123!")
    finally:
        db.close()

    payload = {"email": "user@test.com", "motDePasse": "WrongPwd"}
    r = client_admin.post(AUTH_LOGIN_ENDPOINT, json=payload)
    assert r.status_code == 401


def test_login_unknown_user_returns_401(client_admin: TestClient):
    payload = {"email": "unknown@test.com", "motDePasse": "DoesNotMatter"}
    r = client_admin.post(AUTH_LOGIN_ENDPOINT, json=payload)
    assert r.status_code == 401


# ===================== TESTS UTILISATEURS =====================
USERS_ENDPOINT = "/api/v1/utilisateurs"


def test_admin_can_create_user(client_admin: TestClient):
    db = TestingSessionLocalAuth()
    try:
        admin_role = seed_role(db, "Admin")
        user_role = seed_role(db, "User")
        admin_role_id = admin_role.idRole
        user_role_id = user_role.idRole
    finally:
        db.close()

    payload = {
        "nomUtil": "Doe",
        "prenomUtil": "Jane",
        "emailUtil": "jane.doe@test.com",
        "motDePasse": "Secret123!",
        "roles_ids": [admin_role_id, user_role_id],
    }

    r = client_admin.post(USERS_ENDPOINT + "/", headers=ADMIN_AUTH_HEADERS, json=payload)
    assert r.status_code == 201, r.text

    data = r.json()
    assert data["emailUtil"] == "jane.doe@test.com"
    assert {rr["libelleRole"] for rr in data["roles"]} == {"Admin", "User"}


def test_non_admin_cannot_create_user(client_user: TestClient):
    db = TestingSessionLocalAuth()
    try:
        role = seed_role(db, "User")
        role_id = role.idRole
    finally:
        db.close()

    payload = {
        "nomUtil": "X",
        "prenomUtil": "Y",
        "emailUtil": "x.y@test.com",
        "motDePasse": "Secret123!",
        "roles_ids": [role_id],
    }

    r = client_user.post(USERS_ENDPOINT + "/", headers=USER_AUTH_HEADERS, json=payload)
    assert r.status_code in (401, 403), r.text


def test_admin_list_users(client_admin: TestClient):
    db = TestingSessionLocalAuth()
    try:
        role = seed_role(db, "User")
        u = seed_user(db, email="someone@test.com", password_plain="Pwd123!")
        attach_role(db, u.idUtil, role.idRole)
    finally:
        db.close()

    r = client_admin.get(USERS_ENDPOINT + "/", headers=ADMIN_AUTH_HEADERS)
    assert r.status_code == 200, r.text
    assert any(u["emailUtil"] == "someone@test.com" for u in r.json())


def test_admin_get_user_by_id(client_admin: TestClient):
    db = TestingSessionLocalAuth()
    try:
        seed_role(db, "User")
        u = seed_user(db, email="getbyid@test.com", password_plain="Pwd123!")
        user_id = u.idUtil
    finally:
        db.close()

    r = client_admin.get(f"{USERS_ENDPOINT}/{user_id}", headers=ADMIN_AUTH_HEADERS)
    assert r.status_code == 200, r.text
    assert r.json()["emailUtil"] == "getbyid@test.com"