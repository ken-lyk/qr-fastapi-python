from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..utility import oauth2
from ..config import database
from ..schemas import userSchemas, schemas
from ..models import userModel

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

database_dependency: Session = Depends(database.get_db)

get_user_dependency: userModel.User = Depends(oauth2.get_current_user)

@router.get('/{id}', response_model=userSchemas.User)
def get_user(id: str, db = database_dependency, current_user = get_user_dependency):
    if not oauth2.isAdmin(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not admin")
    user = db.query(userModel.User).filter(userModel.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user



@router.get('/', response_model= List[userSchemas.User])
def get_user(filter_query: Annotated[schemas.FilterParams, Query()], db = database_dependency, current_user = get_user_dependency):
    if not oauth2.isAdmin(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not admin")
    userList = db.query(userModel.User).offset(filter_query.offset).limit(filter_query.limit).all()
    if len(userList) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user list")

    return userList

@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: str,db = database_dependency, current_user = get_user_dependency):
    if not oauth2.isAdmin(current_user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User is not admin")
    userQuery = db.query(userModel.User).filter(userModel.User.id == id)
    
    user = userQuery.first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    userQuery.delete(synchronize_session=False)
    db.commit()
    
    return "User deleted successfully"

