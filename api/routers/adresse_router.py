from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.adresse_schema import (
    AdresseCreate,
    AdresseRead,
    AdresseUpdate,
)
from api.services import adresse_service
from api.routers.dependencies import get_current_utilisateur

router = APIRouter(
    prefix="/adresses",
    tags=["adresses"],
)


@router.post(
    "/",
    response_model=AdresseRead,
    status_code=status.HTTP_201_CREATED,
)
def create_adresse(
    adresse_in: AdresseCreate,
    db: Session = Depends(get_db),
    current_utilisateur = Depends(get_current_utilisateur),
):
    try:
        adresse = adresse_service.create_adresse(db, adresse_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return adresse


@router.get(
    "/",
    response_model=List[AdresseRead],
)
def list_adresses(
    db: Session = Depends(get_db),
    current_utilisateur = Depends(get_current_utilisateur),
    skip: int = 0,
    limit: int = 100,
):
    return adresse_service.list_adresses(db, skip, limit)


@router.get(
    "/{adresse_id}",
    response_model=AdresseRead,
)
def get_adresse(
    adresse_id: int,
    db: Session = Depends(get_db),
    current_utilisateur = Depends(get_current_utilisateur),
):
    from api.repositories import adresse_repository as repo

    adresse = repo.get_adresse(db, adresse_id)
    if not adresse:
        raise HTTPException(status_code=404, detail="Adresse non trouvée")
    return adresse


@router.put(
    "/{adresse_id}",
    response_model=AdresseRead,
)
def update_adresse(
    adresse_id: int,
    adresse_in: AdresseUpdate,
    db: Session = Depends(get_db),
    current_utilisateur = Depends(get_current_utilisateur),
):
    try:
        adresse = adresse_service.update_adresse(db, adresse_id, adresse_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return adresse


@router.delete(
    "/{adresse_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_adresse(
    adresse_id: int,
    db: Session = Depends(get_db),
    current_utilisateur = Depends(get_current_utilisateur),
):
    try:
        adresse_service.delete_adresse(db, adresse_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
