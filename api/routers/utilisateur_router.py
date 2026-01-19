from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.utilisateur_schema import (
    UtilisateurCreate,
    UtilisateurRead,
    UtilisateurUpdate,
)
from api.services import utilisateur_service
from api.routers.dependencies import require_roles

router = APIRouter(
    prefix="/utilisateurs",
    tags=["utilisateurs"],
)

AdminOnly = require_roles("Admin")


@router.post(
    "/",
    response_model=UtilisateurRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminOnly)],
)
def create_utilisateur(
    utilisateur_in: UtilisateurCreate,
    db: Session = Depends(get_db),
) -> UtilisateurRead:
    try:
        utilisateur = utilisateur_service.create_utilisateur(db, utilisateur_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return utilisateur


@router.get(
    "/",
    response_model=List[UtilisateurRead],
    dependencies=[Depends(AdminOnly)],
)
def list_utilisateurs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[UtilisateurRead]:
    return utilisateur_service.list_utilisateurs(db, skip, limit)


@router.get(
    "/{utilisateur_id}",
    response_model=UtilisateurRead,
    dependencies=[Depends(AdminOnly)],
)
def get_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db),
) -> UtilisateurRead:
    from api.repositories import utilisateur_repository as repo

    utilisateur = repo.get_utilisateur(db, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur


@router.put(
    "/{utilisateur_id}",
    response_model=UtilisateurRead,
    dependencies=[Depends(AdminOnly)],
)
def update_utilisateur(
    utilisateur_id: int,
    utilisateur_in: UtilisateurUpdate,
    db: Session = Depends(get_db),
) -> UtilisateurRead:
    try:
        utilisateur = utilisateur_service.update_utilisateur(
            db, utilisateur_id, utilisateur_in
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return utilisateur


@router.delete(
    "/{utilisateur_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminOnly)],
)
def delete_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db),
) -> None:
    from api.services import utilisateur_service as service

    try:
        service.delete_utilisateur(db, utilisateur_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
