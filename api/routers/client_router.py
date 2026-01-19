from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.client_schema import (
    ClientCreate,
    ClientRead,
    ClientUpdate,
)
from api.services import client_service
from api.routers.dependencies import require_roles

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)

AdminOrOpColis = require_roles("Admin", "OP-colis")


@router.post(
    "/",
    response_model=ClientRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AdminOrOpColis)],
)
def create_client_endpoint(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
):
    try:
        client = client_service.create_client(db, client_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return client


@router.get(
    "/",
    response_model=List[ClientRead],
    dependencies=[Depends(AdminOrOpColis)],
)
def list_clients_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return client_service.list_clients(db, skip, limit)


@router.get(
    "/{client_id}",
    response_model=ClientRead,
    dependencies=[Depends(AdminOrOpColis)],
)
def get_client_endpoint(
    client_id: int,
    db: Session = Depends(get_db),
):
    from api.repositories import client_repository as repo

    client = repo.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client


@router.put(
    "/{client_id}",
    response_model=ClientRead,
    dependencies=[Depends(AdminOrOpColis)],
)
def update_client_endpoint(
    client_id: int,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
):
    try:
        client = client_service.update_client(db, client_id, client_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return client


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AdminOrOpColis)],
)
def delete_client_endpoint(
    client_id: int,
    db: Session = Depends(get_db),
):
    try:
        client_service.delete_client(db, client_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
