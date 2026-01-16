from sqlalchemy.orm import Session
from ..repositories import ObjetRepository
from ..schemas import ObjetPost, ObjetPatch

class ObjetService:

    def __init__(self):
        self.repository = ObjetRepository()
    
    def __process(self, objet: dict):
        return objet

    
    def get_all_objets(self, db: Session):
        return self.repository.get_all_objets(db)
    
    
    def get_objet_by_id(self, db: Session, objet_id: int):
        return self.repository.get_objet_by_id(db, objet_id)
    
    
    def create_objet(self, db: Session, new_objet: ObjetPost):
        new_objet = new_objet.model_dump()
        new_objet = self.__process(new_objet)
        return self.repository.create_objet(db, new_objet)
    
    
    def patch_objet(self, db: Session, objet_id: int, objet: ObjetPatch):
        objet = objet.model_dump(exclude_unset=True)
        objet = self.__process(objet)
        return self.repository.patch_objet(db, objet_id, objet)
    
    
    def delete_objet(self, db: Session, objet_id: int):
        return self.repository.delete_objet(db, objet_id)