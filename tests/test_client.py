from fastapi import Response
from fastapi.testclient import TestClient
import pytest


# Constantes pour l'endpoint
CLIENT_ENDPOINT = "/api/v1/clients"

AUTH_HEADERS = {"Authorization": "Bearer fake"}



@pytest.fixture
def client_data():
    """Données de test pour créer un client."""
    return {
        "nomClient": "Doe",
        "prenomClient": "John",
        "genre": "M",
        "emailClient": "John.Doe@gmail.com",
        "telephone": "01.23.45.67.89",
    }


def test_get_all_clients(client: TestClient):
    """Tester l'obtention de tous les clients (doit renvoyer une liste vide au début)."""
    response: Response = client.get(CLIENT_ENDPOINT, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_client(client: TestClient, client_data):
    """Tester la création d'un client."""
    response: Response = client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)
    print(response.status_code, response.json())
    assert response.status_code == 201

    data = response.json()
    del data["idClient"]
    assert data == client_data


def test_get_client_by_id(client: TestClient, client_data):
    """Tester la récupération d'un client par son ID."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)

    # Récupérer le client par ID
    response: Response = client.get(f"{CLIENT_ENDPOINT}/1")
    assert response.status_code == 200

    data = response.json()
    del data["idClient"]
    assert data == client_data


from fastapi import Response
from fastapi.testclient import TestClient
import pytest

# Constantes pour l'endpoint
CLIENT_ENDPOINT = "/api/v1/clients"

AUTH_HEADERS = {"Authorization": "Bearer fake"}


@pytest.fixture
def client_data():
    """Données de test pour créer un client."""
    return {
        "nomClient": "Doe",
        "prenomClient": "John",
        "genre": "M",
        "emailClient": "John.Doe@gmail.com",
        "telephone": "01.23.45.67.89",
    }


def test_get_all_clients(client: TestClient):
    """Tester l'obtention de tous les clients (doit renvoyer une liste vide au début)."""
    response: Response = client.get(CLIENT_ENDPOINT, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_create_client(client: TestClient, client_data):
    """Tester la création d'un client."""
    response: Response = client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)
    print(response.status_code, response.json())
    assert response.status_code == 201

    data = response.json()
    client_id = data.pop("idClient", None)
    assert client_id is not None
    assert data == client_data


def test_get_client_by_id(client: TestClient, client_data):
    """Tester la récupération d'un client par son ID."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)

    # Récupérer le client par ID
    response: Response = client.get(f"{CLIENT_ENDPOINT}/1")
    assert response.status_code == 200

    data = response.json()
    client_id = data.pop("idClient", None)
    assert client_id is not None
    assert data == client_data


def test_put_client_by_id(client: TestClient, client_data):
    """Tester la mise à jour complète des informations d'un client avec PUT."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)

    # Modifier les données pour la mise à jour
    updated_data = client_data.copy()
    updated_data["emailClient"] = "john.doe.updated@gmail.com"
    updated_data["telephone"] = "09.87.65.43.21"

    # Mettre à jour le client avec PUT
    response: Response = client.put(f"{CLIENT_ENDPOINT}/1", headers=AUTH_HEADERS, json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["emailClient"] == "john.doe.updated@gmail.com"
    assert data["telephone"] == "09.87.65.43.21"
    assert data["nomClient"] == "Doe"
    assert data["prenomClient"] == "John"


def test_delete_client_by_id(client: TestClient, client_data):
    """Tester la suppression d'un client par son ID."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=client_data)

    # Supprimer le client
    response = client.delete(f"{CLIENT_ENDPOINT}/1", headers=AUTH_HEADERS)
    assert response.status_code == 204  # OK

    # Vérifier que le client n'existe plus
    response: Response = client.get(f"{CLIENT_ENDPOINT}/1")
    assert response.status_code == 404 # Not Found