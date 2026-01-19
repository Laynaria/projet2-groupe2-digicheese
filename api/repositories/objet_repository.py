from ..models import Objet
from sqlalchemy.orm import Session


class ObjetRepository:
    
    def get_all_objets(self, db: Session):
        return list(db.query(Objet).all())
    
    def get_objet_by_id(self, db: Session, id: int):
        return db.query(Objet).get(id)
    
    def create_objet(self, db: Session, data_objet: dict):
        objet = Objet(**data_objet)
        db.add(objet)
        db.commit()
        db.refresh(objet)
        return objet
    
    def patch_objet(self, db: Session, id: int, data_objet: dict):
        objet = db.query(Objet).get(id)
        for key, value in data_objet.items():
            setattr(objet, key, value)
        db.commit()
        db.refresh(objet)
        return objet
    
    def delete_objet(self, db: Session, id: int):
        objet = db.query(Objet).get(id)
        db.delete(objet)
        db.commit()
        return objet