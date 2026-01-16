import os
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models.role import Role


def seed_roles():
    if os.getenv("SEED_ADMIN", "false").lower() != "true":
        print("SEED_ADMIN désactivé — seed roles ignoré")
        return

    roles_a_creer = ["Admin", "OP-colis", "OP-stocks"]

    db: Session = SessionLocal()
    try:
        # Idempotence: on regarde ce qui existe déjà
        existants = {
            r.libelleRole for r in db.query(Role).filter(Role.libelleRole.in_(roles_a_creer)).all()
        }

        manquants = [r for r in roles_a_creer if r not in existants]
        if not manquants:
            print("Rôles déjà seedés")
            return

        db.add_all([Role(libelleRole=lib) for lib in manquants])
        db.commit()
        print(f"Seed roles terminé: {len(manquants)} ajoutés")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
