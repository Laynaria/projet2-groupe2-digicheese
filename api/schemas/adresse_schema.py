from typing import Optional
from pydantic import BaseModel


class AdresseBase(BaseModel):
    compAdresse1: Optional[str] = None
    compAdresse2: Optional[str] = None
    compAdresse3: Optional[str] = None
    numeroVoie: str
    nomVoie: str
    idCommune: int
    idClient: int


class AdresseCreate(AdresseBase):
    """Données nécessaires à la création d'une adresse."""
    pass


class AdresseUpdate(BaseModel):
    """Champs modifiables pour une adresse."""
    compAdresse1: Optional[str] = None
    compAdresse2: Optional[str] = None
    compAdresse3: Optional[str] = None
    numeroVoie: Optional[str] = None
    nomVoie: Optional[str] = None
    idCommune: Optional[int] = None
    idClient: Optional[int] = None


class AdresseRead(AdresseBase):
    """Adresse renvoyée par l'API."""
    idAdresse: int

    class Config:
        from_attributes = True
