"""
References all detail_commande-related endpoints in the FastAPI application.

Receives requests from the detail_commande router, transform in detail_commande schema and process them using our DetailCommandeService.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import DetailCommandePost, DetailCommandePatch, DetailCommandeInDB
from ..database import get_db
from ..services import DetailCommandeService

# Create a router for commande-related endpoints
router = APIRouter(prefix="/detail-commande", tags=["detail_commande"])

# Initialize the commande service to have acces to commande operations
service = DetailCommandeService()

@router.get("/", status_code=200, response_model=list[DetailCommandeInDB])
def get_detail_commandes(db: Session=Depends(get_db)):
    return service.get_all_detail_commandes(db)

@router.get("/{detail_commande_id}", status_code=200, response_model=DetailCommandeInDB)
def get_detail_commande(detail_commande_id: int, db: Session=Depends(get_db)):
    detail_commande = service.get_detail_commande_by_id(db, detail_commande_id)
    if detail_commande is None:
        raise HTTPException(status_code=404, detail="Détail de commande non trouvé")
    return detail_commande

@router.post("/", status_code=201, response_model=DetailCommandeInDB)
def create_detail_commande(data_detail_commande: DetailCommandePost, db: Session=Depends(get_db)):
    return service.create_detail_commande(db, data_detail_commande)

@router.patch("/{detail_commande_id}", status_code=200, response_model=DetailCommandeInDB)
def patch_detail_commande(detail_commande_id: int, data_detail_commande: DetailCommandePatch, db: Session=Depends(get_db)):
    detail_commande = service.get_detail_commande_by_id(db, detail_commande_id)
    if detail_commande is None:
        raise HTTPException(status_code=404, detail="Détail de commande non trouvé")
    return service.patch_detail_commande(db, detail_commande_id, data_detail_commande)

@router.delete("/{detail_commande_id}", status_code=200, response_model=DetailCommandeInDB)
def delete_detail_commande(detail_commande_id: int, db: Session=Depends(get_db)):
    detail_commande = service.get_detail_commande_by_id(db, detail_commande_id)
    if detail_commande is None:
        raise HTTPException(status_code=404, detail="Commande non trouvé")
    return service.delete_detail_commande(db, detail_commande_id)