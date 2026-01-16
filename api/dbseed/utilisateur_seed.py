import os
from faker import Faker
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models.utilisateur import Utilisateur
from api.models.role import Role
from api.services.security_service import get_password_hash

fake = Faker("fr_FR")

def seed_utilisateurs(nb_users: int = 10):
    if os.getenv("SEED_USERS", "false").lower() != "true":
        print("SEED_USERS désactivé")
        return

    db: Session = SessionLocal()
    try:
        roles = ["OP-colis", "OP-stocks"]

        for _ in range(nb_users):
            email = fake.unique.email()

            if db.query(Utilisateur).filter(Utilisateur.emailUtil == email).first():
                continue

            user = Utilisateur(
                nomUtil=fake.last_name(),
                prenomUtil=fake.first_name(),
                emailUtil=email,
                motDePasse=get_password_hash("User123!"),
            )

            role_label = fake.random_element(elements=roles)
            role_obj = db.query(Role).filter(Role.libelleRole == role_label).first()
            if not role_obj:
                raise Exception(f"Rôle introuvable.")

            user.roles = [role_obj]   

            db.add(user)

        db.commit()
        print("Seed utilisateurs terminé")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
