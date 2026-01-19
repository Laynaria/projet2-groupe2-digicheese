from typing import List
from sqlalchemy.orm import Session

from api.models.utilisateur import Utilisateur
from api.repositories import utilisateur_repository as repo
from api.schemas.utilisateur_schema import (
    UtilisateurCreate,
    UtilisateurUpdate,
)
from api.services.security_service import get_password_hash


def create_utilisateur(db: Session, utilisateur_in: UtilisateurCreate) -> Utilisateur:
    if repo.get_utilisateur_by_email(db, utilisateur_in.emailUtil):
        # à convertir en HTTPException dans le router
        raise ValueError("Email déjà utilisé")

    db_utilisateur = Utilisateur(
        nomUtil=utilisateur_in.nomUtil,
        prenomUtil=utilisateur_in.prenomUtil,
        emailUtil=utilisateur_in.emailUtil,
        motDePasse=get_password_hash(utilisateur_in.motDePasse),
    )
    db_utilisateur = repo.create_utilisateur(db, db_utilisateur)

    if getattr(utilisateur_in, "roles_ids", None):
        db_utilisateur = repo.set_roles_for_utilisateur(
            db, db_utilisateur, utilisateur_in.roles_ids
        )

    return db_utilisateur


def update_utilisateur(
    db: Session, utilisateur_id: int, utilisateur_in: UtilisateurUpdate
) -> Utilisateur:
    db_utilisateur = repo.get_utilisateur(db, utilisateur_id)
    if not db_utilisateur:
        raise ValueError("Utilisateur introuvable")

    if utilisateur_in.emailUtil is not None:
        existing = repo.get_utilisateur_by_email(db, utilisateur_in.emailUtil)
        if existing and existing.idUtil != db_utilisateur.idUtil:
            raise ValueError("Email déjà utilisé")
        db_utilisateur.emailUtil = utilisateur_in.emailUtil

    if utilisateur_in.nomUtil is not None:
        db_utilisateur.nomUtil = utilisateur_in.nomUtil
    if utilisateur_in.prenomUtil is not None:
        db_utilisateur.prenomUtil = utilisateur_in.prenomUtil
    if utilisateur_in.motDePasse is not None:
        db_utilisateur.motDePasse = get_password_hash(utilisateur_in.motDePasse)

    db.commit()
    db.refresh(db_utilisateur)

    if utilisateur_in.roles_ids is not None:
        db_utilisateur = repo.set_roles_for_utilisateur(
            db, db_utilisateur, utilisateur_in.roles_ids
        )

    return db_utilisateur


def delete_utilisateur(db: Session, utilisateur_id: int) -> None:
    db_utilisateur = repo.get_utilisateur(db, utilisateur_id)
    if not db_utilisateur:
        raise ValueError("Utilisateur introuvable")
    repo.delete_utilisateur(db, db_utilisateur)


def list_utilisateurs(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Utilisateur]:
    return repo.get_all_utilisateurs(db)
