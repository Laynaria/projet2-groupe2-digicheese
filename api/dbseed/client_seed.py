import os
from sqlalchemy.orm import Session
from faker import Faker

from api.database import SessionLocal
from api.models.client import Client


def seed_clients():
    if os.getenv("SEED_CLIENTS", "false").lower() != "true":
        print("SEED_CLIENTS désactivé — seed clients ignoré")
        return

    nb = int(os.getenv("SEED_NB_CLIENTS", "30"))
    faker = Faker("fr_FR")

    db: Session = SessionLocal()
    try:
        count = db.query(Client).count()
        if count > 0:
            print("Table client déjà seedée")
            return

        clients = []
        for _ in range(nb):
            clients.append(
                Client(
                    nomClient=faker.last_name()[:100],
                    prenomClient=faker.first_name()[:100],
                    genre=faker.random_element(elements=["F", "M", "NB", None]),
                    emailClient=faker.unique.email()[:255],
                    telephone=faker.phone_number()[:30],
                )
            )

        db.add_all(clients)
        db.commit()
        print(f"Seed clients terminé ({nb})")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
