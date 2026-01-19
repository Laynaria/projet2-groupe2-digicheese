from decimal import Decimal

from fastapi import Response
from fastapi.testclient import TestClient
import pytest

OBJET_ENDPOINT = "/api/v1/objet"
AUTH_HEADERS = {"Authorization": "Bearer fake"}


@pytest.fixture
def objet_data(relcond_id):
    return {
        "libelle": "Mug",
        "taille": "S",
        "poids": "0.30",
        "bIndispo": 1,
        "points": 20,
        "relCond_id": relcond_id
    }


def test_get_all_objets(client: TestClient):
    response: Response = client.get(OBJET_ENDPOINT, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_objet(client: TestClient, objet_data):
    response: Response = client.post(OBJET_ENDPOINT, headers=AUTH_HEADERS, json=objet_data)
    print(response.status_code, response.json())
    assert response.status_code == 201

    data = response.json()
    assert data["idObjet"] is not None

    assert data["libelle"] == objet_data["libelle"]
    assert data["taille"] == objet_data["taille"]
    assert data["bIndispo"] == objet_data["bIndispo"]
    assert data["points"] == objet_data["points"]
    assert data["relCond_id"] == objet_data["relCond_id"]


def test_get_objet_by_id(client: TestClient, objet_data):

    create_response = client.post(OBJET_ENDPOINT, headers=AUTH_HEADERS, json=objet_data)
    id_objet = create_response.json()["idObjet"]

    response = client.get(f"{OBJET_ENDPOINT}/{id_objet}", headers=AUTH_HEADERS)
    assert response.status_code == 200

    data = response.json()

    assert data["idObjet"] == id_objet
    assert data["libelle"] == objet_data["libelle"]
    assert data["taille"] == objet_data["taille"]
    assert data["bIndispo"] == objet_data["bIndispo"]
    assert data["points"] == objet_data["points"]
    assert data["relCond_id"] == objet_data["relCond_id"]
    assert Decimal(str(data["poids"])) == Decimal(objet_data["poids"])


def test_patch_objet_by_id(client: TestClient, objet_data):

    create_response = client.post(
        OBJET_ENDPOINT,
        headers=AUTH_HEADERS,
        json=objet_data
    )
    id_objet = create_response.json()["idObjet"]

    patch_data = {
        "libelle": "Mug M",
        "taille": "M",
        "points": 30
    }

    response: Response = client.patch(
        f"{OBJET_ENDPOINT}/{id_objet}",
        headers=AUTH_HEADERS,
        json=patch_data
    )

    assert response.status_code == 200

    data = response.json()
    assert data["libelle"] == "Mug M"
    assert data["taille"] == "M"
    assert data["points"] == 30
    assert Decimal(data["poids"]) == Decimal("0.30")


def test_delete_objet_by_id(client: TestClient, objet_data):

    create_response = client.post(OBJET_ENDPOINT, headers=AUTH_HEADERS, json=objet_data)
    id_objet = create_response.json()["idObjet"]

    response = client.delete(f"{OBJET_ENDPOINT}/{id_objet}", headers=AUTH_HEADERS)
    assert response.status_code == 200

    get_response: Response = client.get(f"{OBJET_ENDPOINT}/{id_objet}", headers=AUTH_HEADERS)
    assert get_response.status_code == 404



