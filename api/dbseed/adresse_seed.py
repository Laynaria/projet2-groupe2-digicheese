import os
import random
from sqlalchemy.orm import Session
from faker import Faker

from api.database import SessionLocal
from api.models.adresse import Adresse
from api.models.commune import Commune
from api.models.client import Client


def seed_adresses():
    if os.getenv("SEED_ADRESSES", "false").lower() != "true":
        print("SEED_ADRESSES désactivé — seed adresses ignoré")
        return

    nb = int(os.getenv("SEED_NB_ADRESSES", "60"))
    faker = Faker("fr_FR")

    db: Session = SessionLocal()
    try:
        count = db.query(Adresse).count()
        if count > 0:
            print("Table adresse déjà seedée")
            return

        communes = db.query(Commune).all()
        clients = db.query(Client).all()

        if not communes:
            raise Exception("Aucune commune en base — seed_adresses impossible.")
        if not clients:
            raise Exception("Aucun client en base — seed_adresses impossible.")

        adresses = []
        for _ in range(nb):
            commune = random.choice(communes)
            client = random.choice(clients)

            adresses.append(
                Adresse(
                    compAdresse1=faker.secondary_address()[:255] if faker.boolean(chance_of_getting_true=25) else None,
                    compAdresse2=None,
                    compAdresse3=None,
                    numeroVoie=str(faker.building_number())[:10],
                    nomVoie=faker.street_name()[:255],
                    idCommune=commune.idCommune,
                    idClient=client.idClient,
                )
            )

        db.add_all(adresses)
        db.commit()
        print(f"Seed adresses terminé ({nb})")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
