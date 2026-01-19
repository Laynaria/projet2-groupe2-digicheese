# api/routers/commune_router.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.commune_schema import (
    CommuneCreate,
    CommuneRead,
    CommuneUpdate,
)
from api.services import commune_service
from api.routers.dependencies import require_roles

router = APIRouter(
    prefix="/communes",
    tags=["communes"],
)

# Seul l'Admin peut créer / modifier / supprimer
AdminOnly = require_roles("Admin")
# Admin ou OP-colis peuvent lister / consulter
AdminOrOpColis = require_roles("Admin", "OP-colis")


@router.post(
    "/",
    response_model=CommuneRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminOnly)],
)
def create_commune(
    commune_in: CommuneCreate,
    db: Session = Depends(get_db),
):
    try:
        commune = commune_service.create_commune(db, commune_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return commune


@router.get(
    "/",
    response_model=List[CommuneRead],
    dependencies=[Depends(AdminOrOpColis)],
)
def list_communes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return commune_service.list_communes(db, skip, limit)


@router.get(
    "/{commune_id}",
    response_model=CommuneRead,
    dependencies=[Depends(AdminOrOpColis)],
)
def get_commune(
    commune_id: int,
    db: Session = Depends(get_db),
):
    from api.repositories import commune_repository as repo

    commune = repo.get_commune(db, commune_id)
    if not commune:
        raise HTTPException(status_code=404, detail="Commune non trouvée")
    return commune


@router.put(
    "/{commune_id}",
    response_model=CommuneRead,
    dependencies=[Depends(AdminOnly)],
)
def update_commune(
    commune_id: int,
    commune_in: CommuneUpdate,
    db: Session = Depends(get_db),
):
    try:
        commune = commune_service.update_commune(db, commune_id, commune_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return commune


@router.delete(
    "/{commune_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminOnly)],
)
def delete_commune(
    commune_id: int,
    db: Session = Depends(get_db),
):
    try:
        commune_service.delete_commune(db, commune_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
