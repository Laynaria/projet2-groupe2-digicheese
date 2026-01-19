from typing import List
from sqlalchemy.orm import Session

from api.models.role import Role
from api.repositories import role_repository as repo
from api.schemas.role_schema import RoleCreate, RoleUpdate


def create_role(db: Session, role_in: RoleCreate) -> Role:
    if repo.get_role_by_name(db, role_in.libelleRole):
        raise ValueError("Un rôle avec ce libellé existe déjà")

    db_role = Role(libelleRole=role_in.libelleRole)
    return repo.create_role(db, db_role)


def list_roles(db: Session) -> List[Role]:
    return repo.list_roles(db)


def update_role(db: Session, role_id: int, role_in: RoleUpdate) -> Role:
    db_role = repo.get_role(db, role_id)
    if not db_role:
        raise ValueError("Rôle introuvable")

    if role_in.libelleRole is not None:
        existing = repo.get_role_by_name(db, role_in.libelleRole)
        if existing and existing.idRole != db_role.idRole:
            raise ValueError("Un rôle avec ce libellé existe déjà")

        db_role = repo.update_role(db, db_role, role_in.libelleRole)

    return db_role


def delete_role(db: Session, role_id: int) -> None:
    db_role = repo.get_role(db, role_id)
    if not db_role:
        raise ValueError("Rôle introuvable")

    repo.delete_role(db, db_role)
