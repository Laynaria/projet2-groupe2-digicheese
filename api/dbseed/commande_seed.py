import os
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from faker import Faker
from datetime import datetime

from ..database import SessionLocal
from ..models import Commande, Client, Conditionnement

def seed_commande():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé - seed ignoré")
        return
    
    nb = int(os.getenv("SEED_NB_COMMANDES", "20"))
    faker = Faker("fr_FR")
    db: Session = SessionLocal()

    try:
        count = db.query(Commande).count()
        if count > 0:
            print("Table commande déjà seedée")
            return
        
        clients: list[Client] = db.query(Client)
        countClient: int = db.query(Client).count()
        conditionnements: list[Conditionnement] = db.query(Conditionnement)
        countConditionnement: int = db.query(Conditionnement).count()

        if countClient == 0 or countConditionnement == 0:
            print("Erreur: Les tables clients et conditionnement ne sont pas seed")
            return
        
        commandes = []
        for _ in range(nb):
            new_commande = Commande(
                date=datetime.now(),
                timbreClient=Decimal(str(round(random.uniform(0.1, 50.0), 4))),
                timbreCode=Decimal(str(round(random.uniform(0.1, 50.0), 4))),
                chequeClient=Decimal(str(round(random.uniform(0.1, 50.0), 4))),
                commentaireCommande=faker.word()[:255],
                nbColis=random.randint(1, 10),
                bArchive=random.randint(0, 1),
                client_id=clients[random.randint(1, countClient - 1)].idClient,
                conditionnement_id=conditionnements[random.randint(1, countConditionnement - 1)].idConditionnement
            )
            commandes.append(new_commande)

        db.add_all(commandes)
        db.commit()
        print(f"Seed terminé")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()