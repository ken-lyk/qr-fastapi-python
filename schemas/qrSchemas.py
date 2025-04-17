# models.py
from pydantic import BaseModel, EmailStr
class QRBase(BaseModel):
    data : str
    path: str
    source: str

class QRCreate(QRBase):
    data : str

class QR(QRBase):
    id : str
    user_id  : str

    class Config:
        from_attributes = True