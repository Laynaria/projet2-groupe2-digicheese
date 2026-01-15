from datetime import datetime, timedelta
from typing import List, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from api.schemas.utilisateur_schema import TokenData