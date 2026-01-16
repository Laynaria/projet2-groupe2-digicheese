from typing import List, Optional
from sqlalchemy.orm import Session

from api.models.utilisateur import Utilisateur
from api.models.role import Role
from api.models.utilisateur_role import UtilisateurRole

def get_utilisateur_by_email(db: Session, email: str) -> Optional[Utilisateur]:
    return db.query(Utilisateur).filter(Utilisateur.emailUtil == email).first()

def get_utilisateur(db: Session, user_id: int) -> Optional[Utilisateur]:
    return db.query(Utilisateur).filter(Utilisateur.idUtil == user_id).first()

def get_all_utilisateurs(db: Session) -> List[Utilisateur]:
    return db.query(Utilisateur).all()

def create_utilisateur(db: Session, user: Utilisateur) -> Utilisateur:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def patch_utilisateur(db: Session, user: Utilisateur, updates) -> Utilisateur:
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_utilisateur(db: Session, user: Utilisateur) -> None:
    db.delete(user)
    db.commit()

def get_role_by_name(db: Session, libelle_role: str) -> Optional[Role]:
    return db.query(Role).filter(Role.libelleRole == libelle_role).first()

def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.idRole == role_id).first()

def set_roles_for_utilisateur(db: Session, user: Utilisateur, role_ids: List[int]) -> Utilisateur:
    db.query(UtilisateurRole).filter(UtilisateurRole.idUtil == user.idUtil).delete()
    for rid in role_ids:
        db.add(UtilisateurRole(idUtil=user.idUtil, idRole=rid))
    db.commit()
    db.refresh(user)
    return user
