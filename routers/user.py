from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..utility import oauth2
from ..config import database
from ..schemas import userSchemas
from .. import models

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get('/{id}', response_model=userSchemas.User)
def get_user(id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if not oauth2.isAdmin(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not admin")
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user



@router.get('/', response_model= List[userSchemas.User])
def get_user(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    if not oauth2.isAdmin(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not admin")
    userList = db.query(models.User).all()
    if len(userList) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user list")

    return userList
