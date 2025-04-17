from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid

from ..config import database
from ..schemas import schemas, userSchemas
from ..utility.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..models import models
from ..config.config import settings
from ..utility.enums import UserRoleEnum

router = APIRouter( 
    prefix="/auth",
    tags=['Authentication'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=userSchemas.User)
def login(userRegisterObject: userSchemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if user already exists
    existingUser = db.query(models.User).filter(models.User.email == userRegisterObject.email).first()
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{userRegisterObject.email}' is already registered."
        )

    hashed_password = get_password_hash(userRegisterObject.password)

    # Create the user object to be stored in the "database"
    newUser = models.User(
        id= str(uuid.uuid4()),
        name=userRegisterObject.name,
        email=userRegisterObject.email,
        password=hashed_password,
        role= UserRoleEnum.USER,
        created_at= datetime.now(),
        updated_at=datetime.now(),
        disabled=False
    )

    # Add user to the database
    db.add(newUser)
    db.commit()
    return newUser

@router.post('/login', response_model=schemas.Token)
def login(userLoginObject: userSchemas.UserLoginObject, db: Session = Depends(database.get_db)):
    existingUser = db.query(models.User).filter(models.User.email == userLoginObject.email).first()
    
    if not existingUser or not verify_password(userLoginObject.password, existingUser.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if existingUser.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existingUser.id, "name": existingUser.name, "role": existingUser.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/token', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print('userCred',user_credentials)
    
    existingUser = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not existingUser or not verify_password(user_credentials.password, existingUser.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if existingUser.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": existingUser.id, "name": existingUser.name, "role": existingUser.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
