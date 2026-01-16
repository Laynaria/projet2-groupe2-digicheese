from typing import List
from sqlalchemy.orm import Session

from api.models.commune import Commune
from api.repositories import commune_repository as repo
from api.schemas.commune_schema import CommuneCreate, CommuneUpdate


def create_commune(db: Session, commune_in: CommuneCreate) -> Commune:
    existing = repo.get_commune_by_cp_and_nom(
        db, commune_in.cp, commune_in.nom_commune
    )
    if existing:
        raise ValueError("Une commune avec ce code postal et ce nom existe déjà")

    db_commune = Commune(
        cp=commune_in.cp,
        nom_commune=commune_in.nom_commune,
        departement=commune_in.departement,
    )
    return repo.create_commune(db, db_commune)


def update_commune(
    db: Session, commune_id: int, commune_in: CommuneUpdate
) -> Commune:
    db_commune = repo.get_commune(db, commune_id)
    if not db_commune:
        raise ValueError("Commune introuvable")

    if commune_in.cp is not None:
        db_commune.cp = commune_in.cp
    if commune_in.nom_commune is not None:
        db_commune.nom_commune = commune_in.nom_commune
    if commune_in.departement is not None:
        db_commune.departement = commune_in.departement

    return repo.update_commune(db, db_commune)


def delete_commune(db: Session, commune_id: int) -> None:
    db_commune = repo.get_commune(db, commune_id)
    if not db_commune:
        raise ValueError("Commune introuvable")

    repo.delete_commune(db, db_commune)


def list_communes(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Commune]:
    return repo.list_communes(db, skip, limit)
