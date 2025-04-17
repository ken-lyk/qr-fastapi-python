from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, File, UploadFile, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..utility import oauth2, qrUtil
from ..config import database
from ..schemas import qrSchemas
from .. import models
from ..utility.enums import QRSourceEnum

router = APIRouter(
    prefix="/qr",
    tags=['QR']
)

@router.get('/{id}', response_model=qrSchemas.QR)
def get_qr(id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    isAdmin = oauth2.isAdmin(current_user)
    if isAdmin:  
        qr = db.query(models.QR).filter(models.QR.id == id).first()
    else:
        qr = db.query(models.QR).filter(models.QR.id == id & models.QR.user_id == current_user.id).first()
    
    if not qr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return qr

@router.get('/', response_model= List[qrSchemas.QR])
def get_qr(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    isAdmin = oauth2.isAdmin(current_user)
    if isAdmin:  
        qrList = db.query(models.QR).all()
    else:
        qrList = db.query(models.QR).filter(models.QR.user_id == current_user.id).all()
        
    if len(qrList) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No QR list")

    return qrList

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=qrSchemas.QR)
def create_qr(qr: qrSchemas.QRBase, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    newQr = models.QR(
        id=str(uuid.uuid4()),
        path=qr.path,
        data=qr.data,
        created_at= datetime.now(),
        updated_at=datetime.now(),
        # user=current_user,
        user_id=current_user.id,
        source=QRSourceEnum.DIRECT_VALUE,
        disabled=False
    )
    db.add(newQr)
    db.commit()
    return newQr

@router.post('/qr-image-data', status_code=status.HTTP_201_CREATED, response_model=qrSchemas.QR)
def create_qr_image_data(qr: qrSchemas.QRBase, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    qrData = ''
    try:
        qrData = qrUtil.decode_qr_from_base64(qr.data + '==')
    except Exception as e: 
        print('error', e)
    
    print('qrData', qrData)
    if qrData != '' and len(qrData) > 0:
        newQr = models.QR(
            id=str(uuid.uuid4()),
            path=qr.path,
            data=qrData,
            created_at= datetime.now(),
            updated_at=datetime.now(),
            user_id=current_user.id,
            source=QRSourceEnum.IMAGE_DATA,
            disabled=False
        )
        db.add(newQr)
        db.commit()
        return newQr
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"QR Data is not valid. Please try encode QR string without header.")
        
        
@router.post('/qr-image-file', status_code=status.HTTP_201_CREATED, response_model=qrSchemas.QR)
def create_qr_image_file(file: Annotated[UploadFile, File(description="Only Image file")] = None, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    print('file from url',file)
    qrData = ''
    try:
        contents = file.file.read()
        qrData = qrUtil.decode_qr_from_file_content(contents)
    except Exception as e: 
        print('error', e)
    
    if qrData != '' and len(qrData) > 0:
        newQr = models.QR(
            id=str(uuid.uuid4()),
            path=file.filename,
            data=qrData,
            created_at= datetime.now(),
            updated_at=datetime.now(),
            # user=current_user,
            user_id=current_user.id,
            source=QRSourceEnum.IMAGE_FILE,
            disabled=False
        )
        db.add(newQr)
        db.commit()
        return newQr
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"QR Image is not valid. Please try with other QR.")
        
        