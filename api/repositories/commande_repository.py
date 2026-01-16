from ..models import Commande
from sqlalchemy.orm import Session

class CommandeRepository:
    """
    Repository class for managing commande operations in database.

    Receive a dictionary from service, save it to the database and return the commande model to service.
    """

    def get_all_commandes(self, db: Session):
        return list(db.query(Commande).all())
    
    def get_commande_by_id(self, db: Session, id: int):
        return db.query(Commande).get(id)
    
    def create_commande(self, db: Session, data_commande: dict):
        commande = Commande(**data_commande)
        db.add(commande)
        db.commit()
        db.refresh(commande)
        return commande

    def patch_commande(self, db: Session, id: int, data_commande: dict):
        commande = db.query(Commande).get(id)
        for key, value in data_commande.items():
            setattr(commande, key, value)
        db.commit()
        db.refresh(commande)
        return commande
    
    def delete_commande(self, db: Session, id: int):
        commande = db.query(Commande).get(id)
        db.delete(commande)
        db.commit()
        return commande