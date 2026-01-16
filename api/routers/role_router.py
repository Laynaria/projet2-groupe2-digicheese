from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.role_schema import RoleCreate, RoleUpdate, RoleRead
from api.services import role_service
from api.routers.dependencies import require_roles

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)

AdminOnly = require_roles("Admin")


@router.post(
    "/",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminOnly)],
)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
):
    try:
        role = role_service.create_role(db, role_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return role


@router.get(
    "/",
    response_model=List[RoleRead],
    dependencies=[Depends(AdminOnly)],
)
def list_roles(
    db: Session = Depends(get_db),
):
    return role_service.list_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(AdminOnly)],
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    from api.repositories import role_repository as repo

    role = repo.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rôle non trouvé")
    return role


@router.put(
    "/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(AdminOnly)],
)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
):
    try:
        role = role_service.update_role(db, role_id, role_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return role


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminOnly)],
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    try:
        role_service.delete_role(db, role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
