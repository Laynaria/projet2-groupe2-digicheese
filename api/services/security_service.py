from datetime import datetime, timedelta, timezone
from typing import List, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from api.schemas.utilisateur_schema import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(
        user_id: int, roles: List[str], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = {
        "sub": str(user_id),
        "roles": roles,
    }
    now = datetime.now(timezone.utc)
    if expires_delta is not None:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if user_id is None:
            raise JWTError()
        return TokenData(idUtil=int(user_id), roles=roles)
    except JWTError as e:
        raise e
