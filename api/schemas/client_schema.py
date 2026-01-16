from typing import Optional
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    nomClient: str
    prenomClient: str
    genre: Optional[str] = None
    emailClient: EmailStr
    telephone: Optional[str] = None


class ClientCreate(ClientBase):
    """Données nécessaires à la création d'un client."""
    pass


class ClientUpdate(BaseModel):
    """Champs modifiables pour un client."""
    nomClient: Optional[str] = None
    prenomClient: Optional[str] = None
    genre: Optional[str] = None
    emailClient: Optional[EmailStr] = None
    telephone: Optional[str] = None


class ClientRead(ClientBase):
    """Client renvoyé par l'API."""
    idClient: int

    class Config:
        from_attributes = True
