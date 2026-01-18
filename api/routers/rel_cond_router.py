from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.rel_cond_schema import RelCondCreate, RelCondUpdate, RelCondRead
from api.services import rel_cond_service

router = APIRouter(
    prefix="/rel-conds",
    tags=["rel-conds"],
)


@router.post("/", response_model=RelCondRead, status_code=status.HTTP_201_CREATED)
def create_rel_cond(
    rel_cond_in: RelCondCreate,
    db: Session = Depends(get_db),
):
    return rel_cond_service.create_rel_cond(db, rel_cond_in)


@router.get("/", response_model=List[RelCondRead])
def list_rel_conds(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return rel_cond_service.list_rel_conds(db, skip, limit)


@router.get("/{rel_cond_id}", response_model=RelCondRead)
def get_rel_cond(
    rel_cond_id: int,
    db: Session = Depends(get_db),
):
    from api.repositories import rel_cond_repository as repo
    rel_cond = repo.get_rel_cond(db, rel_cond_id)
    if not rel_cond:
        raise HTTPException(status_code=404, detail="RelCond non trouvé")
    return rel_cond


@router.put("/{rel_cond_id}", response_model=RelCondRead)
def update_rel_cond(
    rel_cond_id: int,
    rel_cond_in: RelCondUpdate,
    db: Session = Depends(get_db),
):
    try:
        return rel_cond_service.update_rel_cond(db, rel_cond_id, rel_cond_in)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{rel_cond_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rel_cond(
    rel_cond_id: int,
    db: Session = Depends(get_db),
):
    try:
        rel_cond_service.delete_rel_cond(db, rel_cond_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
