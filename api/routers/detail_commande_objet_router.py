from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.detail_commande_objet_schema import (
    DetailCommandeObjetCreate,
    DetailCommandeObjetUpdate,
    DetailCommandeObjetRead,
)
from api.services import detail_commande_objet_service
from api.routers.dependencies import get_current_utilisateur

router = APIRouter(
    prefix="/detail-commande-objets",
    tags=["detail-commande-objets"],
)


@router.post("/", response_model=DetailCommandeObjetRead, status_code=status.HTTP_201_CREATED)
def create_dco(
    dco_in: DetailCommandeObjetCreate,
    db: Session = Depends(get_db),
    current_utilisateur=Depends(get_current_utilisateur),
):
    try:
        return detail_commande_objet_service.create_detail_commande_objet(db, dco_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[DetailCommandeObjetRead])
def list_dcos(
    db: Session = Depends(get_db),
    current_utilisateur=Depends(get_current_utilisateur),
    skip: int = 0,
    limit: int = 100,
):
    return detail_commande_objet_service.list_detail_commande_objets(db, skip, limit)


@router.get("/{dco_id}", response_model=DetailCommandeObjetRead)
def get_dco(
    dco_id: int,
    db: Session = Depends(get_db),
    current_utilisateur=Depends(get_current_utilisateur),
):
    from api.repositories import detail_commande_objet_repository as repo

    dco = repo.get_detail_commande_objet(db, dco_id)
    if not dco:
        raise HTTPException(status_code=404, detail="DetailCommandeObjet non trouvé")
    return dco


@router.put("/{dco_id}", response_model=DetailCommandeObjetRead)
def update_dco(
    dco_id: int,
    dco_in: DetailCommandeObjetUpdate,
    db: Session = Depends(get_db),
    current_utilisateur=Depends(get_current_utilisateur),
):
    try:
        return detail_commande_objet_service.update_detail_commande_objet(db, dco_id, dco_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{dco_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dco(
    dco_id: int,
    db: Session = Depends(get_db),
    current_utilisateur=Depends(get_current_utilisateur),
):
    try:
        detail_commande_objet_service.delete_detail_commande_objet(db, dco_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
