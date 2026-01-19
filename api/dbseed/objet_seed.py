import os
import random
from decimal import Decimal
from sqlalchemy.orm import Session
from faker import Faker

from api.database import SessionLocal
from api.models import RelCond
from api.models.objet import Objet


def seed_objets():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé — seed ignoré")
        return

    nb = int(os.getenv("SEED_NB_OBJETS", "20"))
    faker = Faker("fr_FR")

    db: Session = SessionLocal()
    try:
        count = db.query(Objet).count()
        if count > 0:
            print("Table objet déjà seedée")
            return

        objets = []
        for _ in range(nb):
            obj = Objet(
                libelle=faker.word()[:50],
                taille=random.choice(["S", "M", "L", "XL"]),
                poids=Decimal(str(round(random.uniform(0.1, 50.0), 4))),
                bIndispo=random.randint(0, 1),
                points=random.randint(0, 100),
                relCond_id=random.choice([r.idRelCond for r in db.query(RelCond).all()])
            )
            objets.append(obj)

        db.add_all(objets)
        db.commit()
        print(f"Seed terminé")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
