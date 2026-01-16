from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from api.schemas.utilisateur_schema import LoginRequest, Token, UtilisateurRead
from api.services import auth_service
from api.routers.dependencies import get_current_utilisateur

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    access_token = auth_service.login(db, credentials.email, credentials.motDePasse)
    return Token(access_token=access_token)


@router.get("/me", response_model=UtilisateurRead)
def read_me(
    current_utilisateur=Depends(get_current_utilisateur),
) -> UtilisateurRead:
    return current_utilisateur
