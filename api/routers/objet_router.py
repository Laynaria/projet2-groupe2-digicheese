

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import ObjetPost, ObjetPatch, ObjetInDB
from ..database import get_db
from ..services import ObjetService

router = APIRouter(prefix="/objet", tags=["objet"])

service = ObjetService()


@router.get("/", status_code=200, response_model=list[ObjetInDB])
def get_objets(db: Session = Depends(get_db)):
    return service.get_all_objets(db)


@router.get("/{objet_id}", status_code=200, response_model=ObjetInDB)
def get_objet(objet_id: int, db: Session = Depends(get_db)):
    objet = service.get_objet_by_id(db, objet_id)
    if objet is None:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    return objet


@router.post("/", status_code=201, response_model=ObjetInDB)
def create_objet(data_objet: ObjetPost, db: Session = Depends(get_db)):
    return service.create_objet(db, data_objet)


@router.patch("/{objet_id}", status_code=200, response_model=ObjetInDB)
def patch_objet(objet_id: int, data_objet: ObjetPatch, db: Session = Depends(get_db)):
    objet = service.get_objet_by_id(db, objet_id)
    if objet is None:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    return service.patch_objet(db, objet_id, data_objet)


@router.delete("/{objet_id}", status_code=200, response_model=ObjetInDB)
def delete_objet(objet_id: int, db: Session = Depends(get_db)):
    objet = service.get_objet_by_id(db, objet_id)
    if objet is None:
        raise HTTPException(status_code=404, detail="Objet non trouvé")
    return service.delete_objet(db, objet_id)