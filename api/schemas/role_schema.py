from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    libelleRole: str


class RoleCreate(RoleBase):
    """Données nécessaires à la création d'un rôle."""
    pass


class RoleUpdate(BaseModel):
    """Champs modifiables pour un rôle."""
    libelleRole: Optional[str] = None


class RoleRead(RoleBase):
    """Rôle renvoyé par l'API."""
    idRole: int

    class Config:
        from_attributes = True
