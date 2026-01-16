import os
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models.role import Role


def seed_roles():
    if os.getenv("SEED_ADMIN", "false").lower() != "true":
        print("SEED_ADMIN désactivé — seed roles ignoré")
        return

    roles = ["Admin", "OP-colis", "OP-stocks"]

    db: Session = SessionLocal()
    try:
        existing = {
            r.libelleRole for r in db.query(Role).filter(Role.libelleRole.in_(roles)).all()
        }

        misssing = [r for r in roles if r not in existing]
        if not misssing:
            print("Rôles déjà seedés")
            return

        db.add_all([Role(libelleRole=lib) for lib in misssing])
        db.commit()
        print(f"Seed roles terminé")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
