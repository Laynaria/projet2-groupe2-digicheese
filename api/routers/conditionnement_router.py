"""
References all conditionnement-related endpoints in the FastAPI application.

Receives requests from the conditionnement router, transform in conditionnement schema and process them using our ConditionnementService.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ConditionnementPost, ConditionnementPatch, ConditionnementInDB
from ..database import get_db
from ..services import ConditionnementService
from .dependencies import require_roles

# Create a router for conditionnement-related endpoints
router = APIRouter(prefix="/conditionnement", tags=["conditionnement"])

# create a requirement condition of being an Admin, can be used on routes
AdminOnly = require_roles("Admin")

# Initialize the conditionnement service to have acces to conditionnement operations
service = ConditionnementService()

@router.get("/", status_code=200, response_model=list[ConditionnementInDB])
def get_conditionnements(db: Session=Depends(get_db)):
    return service.get_all_conditionnements(db)

@router.get("/{conditionnement_id}", status_code=200, response_model=ConditionnementInDB)
def get_conditionnement(conditionnement_id: int, db: Session=Depends(get_db)):
    conditionnement = service.get_conditionnement_by_id(db, conditionnement_id)
    if conditionnement is None:
        raise HTTPException(status_code=404, detail="Conditionnement non trouvé")
    return conditionnement

@router.post("/", status_code=201, response_model=ConditionnementInDB,
    dependencies=[Depends(AdminOnly)],)
def create_conditionnement(data_conditionnement: ConditionnementPost, db: Session=Depends(get_db)):
    return service.create_conditionnement(db, data_conditionnement)

@router.patch("/{conditionnement_id}", status_code=200, response_model=ConditionnementInDB,
    dependencies=[Depends(AdminOnly)],)
def patch_conditionnement(conditionnement_id: int, data_conditionnement: ConditionnementPatch, db: Session=Depends(get_db)):
    conditionnement = service.get_conditionnement_by_id(db, conditionnement_id)
    if conditionnement is None:
        raise HTTPException(status_code=404, detail="Conditionnement non trouvé")
    return service.patch_conditionnement(db, conditionnement_id, data_conditionnement)

@router.delete("/{conditionnement_id}", status_code=200, response_model=ConditionnementInDB,
    dependencies=[Depends(AdminOnly)],)
def delete_conditionnement(conditionnement_id: int, db: Session=Depends(get_db)):
    conditionnement = service.get_conditionnement_by_id(db, conditionnement_id)
    if conditionnement is None:
        raise HTTPException(status_code=404, detail="Conditionnement non trouvé")
    return service.delete_conditionnement(db, conditionnement_id)