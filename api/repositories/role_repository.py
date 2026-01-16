from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.role import Role
from api.models.utilisateur_role import UtilisateurRole


def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.idRole == role_id).first()


def get_role_by_name(db: Session, libelle_role: str) -> Optional[Role]:
    return db.query(Role).filter(Role.libelleRole == libelle_role).first()


def list_roles(db: Session) -> List[Role]:
    return db.query(Role).order_by(Role.idRole).all()


def create_role(db: Session, role: Role) -> Role:
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role: Role, new_libelle: str) -> Role:
    role.libelleRole = new_libelle
    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role: Role) -> None:
    # Vérifier que le rôle n'est pas utilisé par des utilisateurs
    count_links = (
        db.query(UtilisateurRole)
        .filter(UtilisateurRole.idRole == role.idRole)
        .count()
    )
    if count_links > 0:
        raise ValueError("Impossible de supprimer un rôle déjà utilisé par des utilisateurs")

    db.delete(role)
    db.commit()
