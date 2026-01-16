"""
References all commande-related endpoints in the FastAPI application.

Receives requests from the commande router, transform in commande schema and process them using our CommandeService.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import CommandePost, CommandePatch, CommandeInDB
from ..database import get_db
from ..services import CommandeService

# Create a router for commande-related endpoints
router = APIRouter(prefix="/commande", tags=["commande"])

# Initialize the commande service to have acces to commande operations
service = CommandeService()

@router.get("/", status_code=200, response_model=list[CommandeInDB])
def get_commandes(db: Session=Depends(get_db)):
    return service.get_all_commandes(db)

@router.get("/{commande_id}", status_code=200, response_model=CommandeInDB)
def get_commande(commande_id: int, db: Session=Depends(get_db)):
    commande = service.get_commande_by_id(db, commande_id)
    if commande is None:
        raise HTTPException(status_code=404, detail="Commande non trouvé")
    return commande

@router.post("/", status_code=201, response_model=CommandeInDB)
def create_commande(data_commande: CommandePost, db: Session=Depends(get_db)):
    return service.create_commande(db, data_commande)

@router.patch("/{commande_id}", status_code=200, response_model=CommandeInDB)
def patch_commande(commande_id: int, data_commande: CommandePatch, db: Session=Depends(get_db)):
    commande = service.get_commande_by_id(db, commande_id)
    if commande is None:
        raise HTTPException(status_code=404, detail="Commande non trouvé")
    return service.patch_commande(db, commande_id, data_commande)

@router.delete("/{commande_id}", status_code=200, response_model=CommandeInDB)
def delete_commande(commande_id: int, db: Session=Depends(get_db)):
    commande = service.get_commande_by_id(db, commande_id)
    if commande is None:
        raise HTTPException(status_code=404, detail="Commande non trouvé")
    return service.delete_commande(db, commande_id)