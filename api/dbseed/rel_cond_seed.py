import os
from sqlalchemy.orm import Session
from faker import Faker

from api.database import SessionLocal
from api.models.rel_cond import RelCond


def seed_rel_cond():
    if os.getenv("SEED_DB", "false").lower() != "true":
        print("SEED_DB désactivé — seed ignoré")
        return

    nb = int(os.getenv("SEED_NB_REL_COND", "20"))
    faker = Faker("fr_FR")

    db: Session = SessionLocal()
    try:
        if db.query(RelCond).count() > 0:
            print("Table rel_cond déjà seedée")
            return

        rel_conds = [
            RelCond(quantiteObjet =faker.random_int(min=1, max=20))
            for _ in range(nb)
        ]

        db.add_all(rel_conds)
        db.commit()
        print("Seed rel_cond terminé")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
