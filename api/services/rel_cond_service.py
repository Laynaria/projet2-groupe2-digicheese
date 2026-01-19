from typing import List
from sqlalchemy.orm import Session

from api.models.rel_cond import RelCond
from api.repositories import rel_cond_repository as repo
from api.schemas.rel_cond_schema import RelCondCreate, RelCondUpdate


def create_rel_cond(db: Session, rel_cond_in: RelCondCreate) -> RelCond:
    db_rel_cond = RelCond(quantiteObjet=rel_cond_in.quantiteObjet)
    return repo.create_rel_cond(db, db_rel_cond)


def update_rel_cond(db: Session, rel_cond_id: int, rel_cond_in: RelCondUpdate) -> RelCond:
    db_rel_cond = repo.get_rel_cond(db, rel_cond_id)
    if not db_rel_cond:
        raise ValueError("RelCond introuvable")

    if rel_cond_in.quantiteObjet is not None:
        db_rel_cond.quantiteObjet = rel_cond_in.quantiteObjet

    return repo.update_rel_cond(db, db_rel_cond)


def delete_rel_cond(db: Session, rel_cond_id: int) -> None:
    db_rel_cond = repo.get_rel_cond(db, rel_cond_id)
    if not db_rel_cond:
        raise ValueError("RelCond introuvable")
    repo.delete_rel_cond(db, db_rel_cond)


def list_rel_conds(db: Session, skip: int = 0, limit: int = 100) -> List[RelCond]:
    return repo.list_rel_conds(db, skip, limit)
