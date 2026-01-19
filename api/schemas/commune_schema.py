from typing import Optional
from pydantic import BaseModel


class CommuneBase(BaseModel):
    cp: str
    nom_commune: str
    departement: Optional[str] = None


class CommuneCreate(CommuneBase):
    """Données nécessaires à la création d'une commune."""
    pass


class CommuneUpdate(BaseModel):
    """Champs modifiables pour une commune."""
    cp: Optional[str] = None
    nom_commune: Optional[str] = None
    departement: Optional[str] = None


class CommuneRead(CommuneBase):
    """Commune renvoyée par l'API."""
    idCommune: int

    class Config:
        from_attributes = True
