from ..models import Conditionnement
from sqlalchemy.orm import Session

class ConditionnementRepository:
    """
    Repository class for managing conditionnement operations in database.

    Receive a dictionary from service, save it to the database and return the conditionnement model to service.
    """

    def get_all_conditionnements(self, db: Session):
        return list(db.query(Conditionnement).all())
    
    def get_conditionnements_by_id(self, db: Session, id: int):
        return db.query(Conditionnement).get(id)
    
    def create_conditionnements(self, db: Session, data_conditionnement: dict):
        conditionnement = Conditionnement(**data_conditionnement)
        db.add(conditionnement)
        db.commit()
        db.refresh(conditionnement)
        return conditionnement

    def patch_conditionnement(self, db: Session, id: int, data_conditionnement: dict):
        conditionnement = db.query(Conditionnement).get(id)
        for key, value in data_conditionnement.items():
            setattr(conditionnement, key, value)
        db.commit()
        db.refresh(conditionnement)
        return conditionnement
    
    def delete_conditionnement(self, db: Session, id: int):
        conditionnement = db.query(Conditionnement).get(id)
        db.delete(conditionnement)
        db.commit()
        return conditionnement