from sqlalchemy.orm import Session
from ..repositories import DetailCommandeRepository
from ..schemas import DetailCommandePost, DetailCommandePatch

class DetailCommandeService:
    """Service class for managing detail_commande operations.
    
    Receive a schema from router and return a dictionary to detail_commande repository"""

    def __init__(self):
        self.repository = DetailCommandeRepository()

    def __traitement(self, detail_commande: dict):
        return detail_commande
    
    def get_all_detail_commandes(self, db: Session):
        return self.repository.get_all_detail_commandes(db)
    
    def get_detail_commande_by_id(self, db: Session, detail_commande_id: int):
        return self.repository.get_detail_commande_by_id(db, detail_commande_id)
    
    def create_detail_commande(self, db: Session, new_detail_commande: DetailCommandePost):
        new_detail_commande = new_detail_commande.model_dump()
        new_detail_commande = self.__traitement(new_detail_commande)
        return self.repository.create_detail_commande(db, new_detail_commande)
    
    def patch_detail_commande(self, db: Session, detail_commande_id: int, detail_commande: DetailCommandePatch):
        detail_commande = detail_commande.model_dump(exclude_unset=True)
        detail_commande = self.__traitement(detail_commande)
        return self.repository.patch_detail_commande(db, detail_commande_id, detail_commande)
    
    def delete_detail_commande(self, db: Session, detail_commande_id: int):
        return self.repository.delete_detail_commande(db, detail_commande_id)