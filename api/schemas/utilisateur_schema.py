from typing import List, Optional
from pydantic import BaseModel, EmailStr

class RoleRead(BaseModel):
    idRole: int
    libelleRole: str

    class Config:
        orm_mode = True

class UtilisateurBase(BaseModel):
    nomUtil: str
    prenomUtil: str
    emailUtil: EmailStr

class UtilisateurCreate(UtilisateurBase):
    motDePasse: str
    roles_ids: List[int] = []  # optionnel: rôles à affecter à la création

class UtilisateurUpdate(BaseModel):
    nomUtil: Optional[str] = None
    prenomUtil: Optional[str] = None
    emailUtil: Optional[EmailStr] = None
    motDePasse: Optional[str] = None
    roles_ids: Optional[List[int]] = None

class UtilisateurRead(UtilisateurBase):
    idUtil: int
    roles: List[RoleRead] = []

    class Config:
        orm_mode = True

# Schémas pour l’auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    idUtil: int
    roles: List[str] = []

class LoginRequest(BaseModel):
    email: EmailStr
    motDePasse: str