import os
from sqlalchemy.orm import Session
from faker import Faker

from api.database import SessionLocal
from api.models.commune import Commune


def seed_communes():
    if os.getenv("SEED_COMMUNES", "false").lower() != "true":
        print("SEED_COMMUNES désactivé — seed communes ignoré")
        return

    nb = int(os.getenv("SEED_NB_COMMUNES", "50"))
    faker = Faker("fr_FR")

    db: Session = SessionLocal()
    try:
        count = db.query(Commune).count()
        if count > 0:
            print("Table commune déjà seedée")
            return

        communes = []
        for _ in range(nb):
            communes.append(
                Commune(
                    cp=faker.postcode(),
                    nom_commune=faker.city()[:100],
                    departement=faker.department()[:100],
                )
            )

        db.add_all(communes)
        db.commit()
        print(f"Seed communes terminé ({nb})")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
