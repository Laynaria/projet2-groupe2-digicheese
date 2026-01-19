from typing import List
from sqlalchemy.orm import Session

from api.models.client import Client
from api.repositories import client_repository as repo
from api.schemas.client_schema import ClientCreate, ClientUpdate


def create_client(db: Session, client_in: ClientCreate) -> Client:
    if repo.get_client_by_email(db, client_in.emailClient):
        raise ValueError("Un client avec cet email existe déjà")

    db_client = Client(
        nomClient=client_in.nomClient,
        prenomClient=client_in.prenomClient,
        genre=client_in.genre,
        emailClient=client_in.emailClient,
        telephone=client_in.telephone,
    )
    return repo.create_client(db, db_client)


def update_client(
    db: Session, client_id: int, client_in: ClientUpdate
) -> Client:
    db_client = repo.get_client(db, client_id)
    if not db_client:
        raise ValueError("Client introuvable")

    if client_in.emailClient is not None:
        existing = repo.get_client_by_email(db, client_in.emailClient)
        if existing and existing.idClient != db_client.idClient:
            raise ValueError("Un client avec cet email existe déjà")
        db_client.emailClient = client_in.emailClient

    if client_in.nomClient is not None:
        db_client.nomClient = client_in.nomClient
    if client_in.prenomClient is not None:
        db_client.prenomClient = client_in.prenomClient
    if client_in.genre is not None:
        db_client.genre = client_in.genre
    if client_in.telephone is not None:
        db_client.telephone = client_in.telephone

    return repo.update_client(db, db_client)


def delete_client(db: Session, client_id: int) -> None:
    db_client = repo.get_client(db, client_id)
    if not db_client:
        raise ValueError("Client introuvable")
    repo.delete_client(db, db_client)


def list_clients(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Client]:
    return repo.list_clients(db, skip, limit)