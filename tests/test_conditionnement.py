from fastapi import Response
from fastapi.testclient import TestClient
import pytest

# Constantes pour l'endpoint
CLIENT_ENDPOINT = "/api/v1/conditionnement"

AUTH_HEADERS = {"Authorization": "Bearer fake"}

@pytest.fixture
def conditionnement_data():
    """Données de test pour créer un conditionnement."""
    return {
        "libelle": "Ceci est une boîte de type boîte!",
        "poidsConditionnement": 50.5,
        "ordreImpression": 7,
    }

def test_get_all_conditionnements(client: TestClient):
    """Tester l'obtention de tous les conditionnements (doit renvoyer une liste vide au début)."""
    response: Response = client.get(CLIENT_ENDPOINT, headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0

def test_create_conditionnement(client: TestClient, conditionnement_data):
    """Tester la création d'un conditionnement."""
    response: Response = client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=conditionnement_data)
    print(response.status_code, response.json())
    assert response.status_code == 201

    data = response.json()
    del data["idConditionnement"]
    assert data == conditionnement_data

def test_get_conditionnement_by_id(client: TestClient, conditionnement_data):
    """Tester la récupération d'un conditionnement par son ID."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=conditionnement_data)

    # Récupérer le client par ID
    response: Response = client.get(f"{CLIENT_ENDPOINT}/1")
    assert response.status_code == 200

    data = response.json()
    del data["idConditionnement"]
    assert data == conditionnement_data

def test_patch_conditionnement(client: TestClient, conditionnement_data):
    """Tester la mise à jour complète des informations d'un client avec PUT."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=conditionnement_data)

    # Modifier les données pour la mise à jour
    updated_data = conditionnement_data.copy()
    updated_data["libelle"] = "Ceci est une meilleure boîte finalement"
    updated_data["poidsConditionnement"] = 60.7

    # Mettre à jour le client avec PUT
    response: Response = client.patch(f"{CLIENT_ENDPOINT}/1", headers=AUTH_HEADERS, json=updated_data)
    assert response.status_code == 200

    data = response.json()
    assert data["libelle"] == updated_data["libelle"]
    assert data["poidsConditionnement"] == updated_data["poidsConditionnement"]
    assert data["ordreImpression"] == 7

def test_delete_conditionnement(client: TestClient, conditionnement_data):
    """Tester la suppression d'un conditionnement par son ID."""

    # Créer un client
    client.post(CLIENT_ENDPOINT, headers=AUTH_HEADERS, json=conditionnement_data)

    # Supprimer le client
    response = client.delete(f"{CLIENT_ENDPOINT}/1", headers=AUTH_HEADERS)
    assert response.status_code == 200  # OK

    # Vérifier que le client n'existe plus
    response: Response = client.get(f"{CLIENT_ENDPOINT}/1")
    assert response.status_code == 404 # Not Found