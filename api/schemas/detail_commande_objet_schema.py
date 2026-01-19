from typing import Optional
from pydantic import BaseModel


class DetailCommandeObjetBase(BaseModel):
    detailleCommande_id: int
    objet_id: int


class DetailCommandeObjetCreate(DetailCommandeObjetBase):
    pass


class DetailCommandeObjetUpdate(BaseModel):
    detailleCommande_id: Optional[int] = None
    objet_id: Optional[int] = None


class DetailCommandeObjetRead(DetailCommandeObjetBase):
    idDetailCommandeObjet: int

    class Config:
        from_attributes = True
