from sqlalchemy.orm import Session
from ..repositories import CommandeRepository
from ..schemas import CommandePost, CommandePatch

class CommandeService:
    """Service class for managing commande operations.
    
    Receive a schema from router and return a dictionary to commande repository"""

    def __init__(self):
        self.repository = CommandeRepository()

    def __traitement(self, client: dict):
        return client
    
    def get_all_commandes(self, db: Session):
        return self.repository.get_all_commandes(db)
    
    def get_commande_by_id(self, db: Session, commande_id: int):
        return self.repository.get_commande_by_id(db, commande_id)
    
    def create_commande(self, db: Session, new_commande: CommandePost):
        new_commande = new_commande.model_dump()
        new_commande = self.__traitement(new_commande)
        return self.repository.create_commande(db, new_commande)
    
    def patch_commande(self, db: Session, commande_id: int, commande: CommandePatch):
        commande = commande.model_dump(exclude_unset=True)
        commande = self.__traitement(commande)
        return self.repository.patch_commande(db, commande_id, commande)
    
    def delete_commande(self, db: Session, commande_id: int):
        return self.repository.delete_commande(db, commande_id)