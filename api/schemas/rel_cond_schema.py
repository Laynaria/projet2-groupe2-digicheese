from typing import Optional
from pydantic import BaseModel


class RelCondBase(BaseModel):
    quantiteObjet: int


class RelCondCreate(RelCondBase):
    pass


class RelCondUpdate(BaseModel):
    quantiteObjet: Optional[int] = None


class RelCondRead(RelCondBase):
    idRelCond: int

    class Config:
        from_attributes = True
