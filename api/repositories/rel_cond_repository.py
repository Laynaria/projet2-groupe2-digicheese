from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.rel_cond import RelCond


def get_rel_cond(db: Session, rel_cond_id: int) -> Optional[RelCond]:
    return db.query(RelCond).filter(RelCond.idRelCond == rel_cond_id).first()


def list_rel_conds(db: Session, skip: int = 0, limit: int = 100) -> List[RelCond]:
    return (
        db.query(RelCond)
        .order_by(RelCond.idRelCond)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_rel_cond(db: Session, rel_cond: RelCond) -> RelCond:
    db.add(rel_cond)
    db.commit()
    db.refresh(rel_cond)
    return rel_cond


def update_rel_cond(db: Session, rel_cond: RelCond) -> RelCond:
    db.commit()
    db.refresh(rel_cond)
    return rel_cond


def delete_rel_cond(db: Session, rel_cond: RelCond) -> None:
    db.delete(rel_cond)
    db.commit()
