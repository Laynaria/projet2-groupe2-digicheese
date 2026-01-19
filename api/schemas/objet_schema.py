from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ObjetBase(BaseModel):
    libelle: Optional[str] = None
    taille: Optional[str] = None
    poids: Optional[Decimal] = 0
    bIndispo: Optional[int] = 0
    points: Optional[int] = 0
    relCond_id: Optional[int] = None


class ObjetPost(ObjetBase):
    pass


class ObjetPatch(ObjetBase):
    libelle: Optional[str] = None
    taille: Optional[str] = None
    poids: Optional[Decimal] = None
    bIndispo: Optional[int] = None
    points: Optional[int] = None
    relCond_id: Optional[int] = None


class ObjetInDB(ObjetBase):
    idObjet: int


class Config:
    from_attributes = True
