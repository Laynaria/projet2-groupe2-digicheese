from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from api.repositories import utilisateur_repository as repo
from api.services.security_service import verify_password, create_access_token

def authenticate_utilisateur(db: Session, email: str, password: str):
    user = repo.get_utilisateur_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.motDePasse):
        return None
    return user

def login(db: Session, email: str, password: str) -> str:
    user = authenticate_utilisateur(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    roles = [role.libelleRole for role in user.roles]
    token = create_access_token(user_id=user.idUtil, roles=roles)
    return token
