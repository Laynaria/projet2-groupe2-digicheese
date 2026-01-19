from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.detail_commande_objet import DetailCommandeObjet


def get_detail_commande_objet(db: Session, dco_id: int) -> Optional[DetailCommandeObjet]:
    return (
        db.query(DetailCommandeObjet)
        .filter(DetailCommandeObjet.idDetailCommandeObjet == dco_id)
        .first()
    )


def list_detail_commande_objets(db: Session, skip: int = 0, limit: int = 100) -> List[DetailCommandeObjet]:
    return (
        db.query(DetailCommandeObjet)
        .order_by(DetailCommandeObjet.idDetailCommandeObjet)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_detail_commande_objet(db: Session, dco: DetailCommandeObjet) -> DetailCommandeObjet:
    db.add(dco)
    db.commit()
    db.refresh(dco)
    return dco


def update_detail_commande_objet(db: Session, dco: DetailCommandeObjet) -> DetailCommandeObjet:
    db.commit()
    db.refresh(dco)
    return dco


def delete_detail_commande_objet(db: Session, dco: DetailCommandeObjet) -> None:
    db.delete(dco)
    db.commit()
