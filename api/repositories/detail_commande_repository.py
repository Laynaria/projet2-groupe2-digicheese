from ..models import DetailCommande
from sqlalchemy.orm import Session

class DetailCommandeRepository:
    """
    Repository class for managing detail_commande operations in database.

    Receive a dictionary from service, save it to the database and return the detail_commande model to service.
    """

    def get_all_detail_commandes(self, db: Session):
        return list(db.query(DetailCommande).all())
    
    def get_detail_commande_by_id(self, db: Session, id: int):
        return db.query(DetailCommande).get(id)
    
    def create_detail_commande(self, db: Session, data_detail_commande: dict):
        detail_commande = DetailCommande(**data_detail_commande)
        db.add(detail_commande)
        db.commit()
        db.refresh(detail_commande)
        return detail_commande

    def patch_detail_commande(self, db: Session, id: int, data_detail_commande: dict):
        detail_commande = db.query(DetailCommande).get(id)
        for key, value in data_detail_commande.items():
            setattr(detail_commande, key, value)
        db.commit()
        db.refresh(detail_commande)
        return detail_commande
    
    def delete_detail_commande(self, db: Session, id: int):
        detail_commande = db.query(DetailCommande).get(id)
        db.delete(detail_commande)
        db.commit()
        return detail_commande