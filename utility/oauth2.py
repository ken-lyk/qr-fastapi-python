from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from . import enums

from ..config import database

from ..schemas import schemas

from ..models import models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..config.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# SECRET_KEY
# Algorithm
# Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # Default expiration
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        name: str = payload.get("name")
        role: str = payload.get("role")
        print('id', id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, role=role, name=name)
    except JWTError as e:
        print('JWTError',e)
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == str(token.id)).first()
    return user

def isAdmin(user: models.User):
    return user.role == enums.UserRoleEnum.ADMIN