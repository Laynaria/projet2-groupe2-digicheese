from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError

from api.services.security_service import decode_access_token
from api.repositories import utilisateur_repository as repo
from ..database import get_db

bearer_scheme = HTTPBearer()


def get_current_utilisateur(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = decode_access_token(token)
    except JWTError:
        raise credentials_exception

    utilisateur = repo.get_utilisateur(db, token_data.idUtil)
    if utilisateur is None:
        raise credentials_exception

    return utilisateur


def require_roles(*roles_required: str):
    def dependency(current_utilisateur=Depends(get_current_utilisateur)):
        utilisateur_roles = {role.libelleRole for role in current_utilisateur.roles}
        if not utilisateur_roles.intersection(roles_required):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès refusé : rôle insuffisant",
            )
        return current_utilisateur

    return dependency