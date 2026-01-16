import os
from sqlalchemy.orm import Session

from api.database import SessionLocal
from api.models.utilisateur import Utilisateur
from api.models.role import Role
from api.models.utilisateur_role import UtilisateurRole
from api.services.security_service import get_password_hash


def seed_admin_user():
    if os.getenv("SEED_ADMIN", "false").lower() != "true":
        print("SEED_ADMIN désactivé — seed admin ignoré")
        return

    email = os.getenv("ADMIN_EMAIL", "admin@digicheese.local")
    password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    nom = os.getenv("ADMIN_NOM", "Root")
    prenom = os.getenv("ADMIN_PRENOM", "Admin")

    db: Session = SessionLocal()
    try:
        admin = db.query(Utilisateur).filter(Utilisateur.emailUtil == email).first()
        if admin:
            print("Admin déjà présent")
            return

        role_admin = db.query(Role).filter(Role.libelleRole == "Admin").first()
        if not role_admin:
            raise Exception("Rôle 'Admin' introuvable.")

        admin = Utilisateur(
            nomUtil=nom,
            prenomUtil=prenom,
            emailUtil=email,
            motDePasse=get_password_hash(password),
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        lien = db.query(UtilisateurRole).filter(
            UtilisateurRole.idUtil == admin.idUtil,
            UtilisateurRole.idRole == role_admin.idRole
        ).first()

        if not lien:
            db.add(UtilisateurRole(idUtil=admin.idUtil, idRole=role_admin.idRole))
            db.commit()

        print("Seed admin terminé")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
