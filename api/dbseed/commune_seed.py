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

        for _ in range(nb):
            # Faker.department() peut renvoyer autre chose qu'une string
            departement = faker.department()
            departement = str(departement)[:100]

            commune = Commune(
                cp=faker.postcode(),
                nom_commune=faker.city()[:100],
                departement=departement,
            )

            # 👉 insertion UNE PAR UNE (évite bug MariaDB + RETURNING)
            db.add(commune)

        db.commit()
        print(f"Seed communes terminé ({nb})")

    except Exception as e:
        db.rollback()
        print("Erreur seed communes :", e)
        raise
    finally:
        db.close()
