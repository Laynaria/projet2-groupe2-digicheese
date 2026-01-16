from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.commune import Commune

def get_commune(db: Session, commune_id: int) -> Optional[Commune]:
    return db.query(Commune).filter(Commune.idCommune == commune_id).first()


def get_commune_by_cp_and_nom(
    db: Session,
    cp: str,
    nom_commune: str,
) -> Optional[Commune]:
    return (
        db.query(Commune)
        .filter(Commune.cp == cp, Commune.nom_commune == nom_commune)
        .first()
    )


def list_communes(db: Session, skip: int = 0, limit: int = 100) -> List[Commune]:
    return (
        db.query(Commune)
        .order_by(Commune.cp, Commune.nom_commune)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_commune(db: Session, commune: Commune) -> Commune:
    db.add(commune)
    db.commit()
    db.refresh(commune)
    return commune


def update_commune(db: Session, commune: Commune) -> Commune:
    db.commit()
    db.refresh(commune)
    return commune


def delete_commune(db: Session, commune: Commune) -> None:
    db.delete(commune)
    db.commit()
