from fastapi import HTTPException, status, Depends, APIRouter
from .. import database
from .. models import user_model
from .. utils import hashing, jwt_handler, otp_sender
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm=Depends(), db:Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    
    if not hashing.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    
    access_token = jwt_handler.create_access_token(
        data={"user_id":user.id},
        expires_delta=timedelta(minutes=jwt_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {'access_token': access_token, 'token_type': "bearer"}



@router.post("/forgot-password")
def forgot_password(user_credentials : OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    otp = otp_sender.generate_otp()
    user.otp = otp
    db.commit()
    return {"message": "OTP sent to email", "otp": otp}


@router.post("/verify-otp")
def verify(user_credentials : OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==user_credentials.username).first()
    if user.otp != user_credentials.otp:
        return {"error": "Invalid OTP"}
    return {"message": "OTP verified"}


@router.post("/reset-password/{email}")
def reset(user_credentials : OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==user_credentials.username).first()

    hashed_password = hashing.hash_password(user.password)
    user.password =hashed_password
    user.otp = None
    db.commit()

    return {"message": "Password updated"}







