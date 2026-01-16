from typing import List
from sqlalchemy.orm import Session

from api.models.adresse import Adresse
from api.models.commune import Commune
from api.models.client import Client
from api.repositories import adresse_repository as repo
from api.schemas.adresse_schema import AdresseCreate, AdresseUpdate


def _check_commune_exists(db: Session, id_commune: int) -> None:
    if not db.query(Commune).filter(Commune.idCommune == id_commune).first():
        raise ValueError(f"Commune introuvable (idCommune={id_commune})")


def _check_client_exists(db: Session, id_client: int) -> None:
    if not db.query(Client).filter(Client.idClient == id_client).first():
        raise ValueError(f"Client introuvable (idClient={id_client})")


def create_adresse(db: Session, adresse_in: AdresseCreate) -> Adresse:
    _check_commune_exists(db, adresse_in.idCommune)
    _check_client_exists(db, adresse_in.idClient)

    db_adresse = Adresse(
        compAdresse1=adresse_in.compAdresse1,
        compAdresse2=adresse_in.compAdresse2,
        compAdresse3=adresse_in.compAdresse3,
        numeroVoie=adresse_in.numeroVoie,
        nomVoie=adresse_in.nomVoie,
        idCommune=adresse_in.idCommune,
        idClient=adresse_in.idClient,
    )
    return repo.create_adresse(db, db_adresse)


def update_adresse(
    db: Session, adresse_id: int, adresse_in: AdresseUpdate
) -> Adresse:
    db_adresse = repo.get_adresse(db, adresse_id)
    if not db_adresse:
        raise ValueError("Adresse introuvable")

    if adresse_in.compAdresse1 is not None:
        db_adresse.compAdresse1 = adresse_in.compAdresse1
    if adresse_in.compAdresse2 is not None:
        db_adresse.compAdresse2 = adresse_in.compAdresse2
    if adresse_in.compAdresse3 is not None:
        db_adresse.compAdresse3 = adresse_in.compAdresse3
    if adresse_in.numeroVoie is not None:
        db_adresse.numeroVoie = adresse_in.numeroVoie
    if adresse_in.nomVoie is not None:
        db_adresse.nomVoie = adresse_in.nomVoie
    if adresse_in.idCommune is not None:
        _check_commune_exists(db, adresse_in.idCommune)
        db_adresse.idCommune = adresse_in.idCommune
    if adresse_in.idClient is not None:
        _check_client_exists(db, adresse_in.idClient)
        db_adresse.idClient = adresse_in.idClient

    return repo.update_adresse(db, db_adresse)


def delete_adresse(db: Session, adresse_id: int) -> None:
    db_adresse = repo.get_adresse(db, adresse_id)
    if not db_adresse:
        raise ValueError("Adresse introuvable")
    repo.delete_adresse(db, db_adresse)


def list_adresses(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Adresse]:
    return repo.list_adresses(db, skip, limit)
