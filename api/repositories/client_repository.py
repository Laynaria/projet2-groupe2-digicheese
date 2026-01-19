from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.client import Client

def get_client(db: Session, client_id: int) -> Optional[Client]:
    return db.query(Client).filter(Client.idClient == client_id).first()


def get_client_by_email(db: Session, email: str) -> Optional[Client]:
    return db.query(Client).filter(Client.emailClient == email).first()


def list_clients(db: Session, skip: int = 0, limit: int = 100) -> List[Client]:
    return (
        db.query(Client)
        .order_by(Client.nomClient, Client.prenomClient)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_client(db: Session, client: Client) -> Client:
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def update_client(db: Session, client: Client) -> Client:
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client: Client) -> None:
    # Le cascade="all, delete-orphan" sur Client.adresses
    # supprime automatiquement les adresses liées.
    db.delete(client)
    db.commit()
