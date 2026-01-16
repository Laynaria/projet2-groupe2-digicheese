from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.adresse import Adresse


def get_adresse(db: Session, adresse_id: int) -> Optional[Adresse]:
    return db.query(Adresse).filter(Adresse.idAdresse == adresse_id).first()


def list_adresses(db: Session, skip: int = 0, limit: int = 100) -> List[Adresse]:
    return (
        db.query(Adresse)
        .order_by(Adresse.idAdresse)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_adresse(db: Session, adresse: Adresse) -> Adresse:
    db.add(adresse)
    db.commit()
    db.refresh(adresse)
    return adresse


def update_adresse(db: Session, adresse: Adresse) -> Adresse:
    db.commit()
    db.refresh(adresse)
    return adresse


def delete_adresse(db: Session, adresse: Adresse) -> None:
    db.delete(adresse)
    db.commit()
