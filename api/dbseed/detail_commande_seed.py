import os
import random
from sqlalchemy.orm import Session
from faker import Faker
import uuid

from ..database import SessionLocal
from ..models import DetailCommande, Commande

def seed_detail_commande():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé - seed ignoré")
        return
    
    nb = int(os.getenv("SEED_NB_DETAIL_COMMANDES", "20"))
    faker = Faker("fr_FR")
    db: Session = SessionLocal()

    try:
        count = db.query(DetailCommande).count()
        if count > 0:
            print("Table detail_commande déjà seedée")
            return
        
        commandes: list[Commande] = db.query(Commande)

        detail_commandes = []
        for i in range(nb):
            new_detail_commande = DetailCommande(
                quantite=random.randint(1, 10),
                colis=str(uuid.uuid4()).replace("-", "").upper()[0:20],
                commentaire=faker.word()[:255],
                commande_id=commandes[i].idCommande
            )
            detail_commandes.append(new_detail_commande)

        db.add_all(detail_commandes)
        db.commit()
        print(f"Seed terminé")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()