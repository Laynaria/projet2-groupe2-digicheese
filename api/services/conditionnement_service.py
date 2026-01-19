from sqlalchemy.orm import Session
from ..repositories import ConditionnementRepository
from ..schemas import ConditionnementPatch, ConditionnementPost

class ConditionnementService:
    """Service class for managing conditionnement operations.
    
    Receive a schema from router and return a dictionary to conditionnement repository"""

    def __init__(self):
        self.repository = ConditionnementRepository()

    def __traitement(self, conditionnement: dict):
        return conditionnement
    
    def get_all_conditionnements(self, db: Session):
        return self.repository.get_all_conditionnements(db)
    
    def get_conditionnement_by_id(self, db: Session, conditionnement_id: int):
        return self.repository.get_conditionnement_by_id(db, conditionnement_id)
    
    def create_conditionnement(self, db: Session, new_conditionnement: ConditionnementPost):
        new_conditionnement = new_conditionnement.model_dump()
        new_conditionnement = self.__traitement(new_conditionnement)
        return self.repository.create_conditionnement(db, new_conditionnement)
    
    def patch_conditionnement(self, db: Session, conditionnement_id: int, conditionnement: ConditionnementPatch):
        conditionnement = conditionnement.model_dump(exclude_unset=True)
        conditionnement = self.__traitement(conditionnement)
        return self.repository.patch_conditionnement(db, conditionnement_id, conditionnement)
    
    def delete_conditionnement(self, db: Session, conditionnement_id: int):
        return self.repository.delete_conditionnement(db, conditionnement_id)