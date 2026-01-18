from typing import List
from sqlalchemy.orm import Session

from api.models.detail_commande_objet import DetailCommandeObjet
from api.models.detail_commande import DetailCommande
from api.models.objet import Objet
from api.repositories import detail_commande_objet_repository as repo
from api.schemas.detail_commande_objet_schema import (
    DetailCommandeObjetCreate,
    DetailCommandeObjetUpdate,
)


def _check_detail_commande_exists(db: Session, detail_id: int) -> None:
    if not db.query(DetailCommande).filter(DetailCommande.idDetailCommande == detail_id).first():
        raise ValueError(f"Détail commande introuvable (id={detail_id})")


def _check_objet_exists(db: Session, objet_id: int) -> None:
    if not db.query(Objet).filter(Objet.idObjet == objet_id).first():
        raise ValueError(f"Objet introuvable (id={objet_id})")


def create_detail_commande_objet(db: Session, dco_in: DetailCommandeObjetCreate) -> DetailCommandeObjet:
    _check_detail_commande_exists(db, dco_in.detailleCommande_id)
    _check_objet_exists(db, dco_in.objet_id)

    dco = DetailCommandeObjet(
        detailleCommande_id=dco_in.detailleCommande_id,
        objet_id=dco_in.objet_id,
    )
    return repo.create_detail_commande_objet(db, dco)


def update_detail_commande_objet(db: Session, dco_id: int, dco_in: DetailCommandeObjetUpdate) -> DetailCommandeObjet:
    dco = repo.get_detail_commande_objet(db, dco_id)
    if not dco:
        raise ValueError("DetailCommandeObjet introuvable")

    if dco_in.detailleCommande_id is not None:
        _check_detail_commande_exists(db, dco_in.detailleCommande_id)
        dco.detailleCommande_id = dco_in.detailleCommande_id

    if dco_in.objet_id is not None:
        _check_objet_exists(db, dco_in.objet_id)
        dco.objet_id = dco_in.objet_id

    return repo.update_detail_commande_objet(db, dco)


def delete_detail_commande_objet(db: Session, dco_id: int) -> None:
    dco = repo.get_detail_commande_objet(db, dco_id)
    if not dco:
        raise ValueError("DetailCommandeObjet introuvable")
    repo.delete_detail_commande_objet(db, dco)


def list_detail_commande_objets(db: Session, skip: int = 0, limit: int = 100) -> List[DetailCommandeObjet]:
    return repo.list_detail_commande_objets(db, skip, limit)
