import os
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from faker import Faker

from ..database import SessionLocal
from ..models.conditionnement import Conditionnement

def seed_conditionnement():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé — seed ignoré")
        return

    nb = int(os.getenv("SEED_NB_CONDITIONNEMENTS", "20"))
    faker = Faker("fr_FR")
    db: Session = SessionLocal()
    
    try:
        count = db.query(Conditionnement).count()
        if count > 0:
            print("Table conditionnement déjà seedée")
            return

        conditionnements = []
        for _ in range(nb):
            new_conditionnement = Conditionnement(
                libelle=faker.word()[:50],
                poidsConditionnement=Decimal(str(round(random.uniform(0.1, 50.0), 4))),
                ordreImpression=random.randint(0, 10),
            )
            conditionnements.append(new_conditionnement)

        db.add_all(conditionnements)
        db.commit()
        print(f"Seed terminé")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
