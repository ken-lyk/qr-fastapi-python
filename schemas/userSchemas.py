# models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..utility.enums import UserRoleEnum
# --- User Models ---
class UserBase(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRoleEnum

class User(UserBase):
    disabled: Optional[bool] = None

# Represents a user stored in the database (including hashed password)
class UserInDB(User):
    password: str
    
class UserCreate(BaseModel): 
    name: str
    email: str
    password: str
    
class UserLoginObject(BaseModel): 
    email: str
    password: str
