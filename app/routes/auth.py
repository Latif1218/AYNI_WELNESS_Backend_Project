from fastapi import HTTPException, status, Depends, APIRouter
from .. import database
from .. models import user_model
from .. schemas import user_schema
from .. utils import hashing, jwt_handler, otp_sender, email_sender
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from ..config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_AUTH_URL, GOOGLE_TOKEN_URL, GOOGLE_USERINFO_URL
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
from .. database import get_db
from fastapi import Request
from typing import Annotated
import httpx



router = APIRouter(
    tags=['Authentication']
)


@router.post('/token', response_model=user_schema.Token)
async def login_for_access_token(
    user_credentials : Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db),):
    user = jwt_handler.authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_handler.create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(minutes=jwt_handler.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return user_schema.Token(access_token=access_token, token_type="bearer")



@router.get("/", status_code=status.HTTP_200_OK)
async def user(user: Session = Depends(jwt_handler.get_current_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Faild"
        )
    return {"User": user}



@router.post("/forgot_password")
def forgot_password(payload: user_schema.ForgotPassword, db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid credential"
        )
    otp = otp_sender.generate_otp()
    user.otp = otp
    db.commit()

    try:
        email_sender.send_otp_email(user.email, otp)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Faild to send OTP email"
        )

    return {"message": "OTP sent to email"}


@router.post("/verify-otp")
def verify_otp(payload: user_schema.VerifyOtp, db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OTP set for this user"
        )
    if user.otp != payload.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    user.is_verified = True
    user.otp = None
    db.commit()
    db.refresh(user)
        
    return {
        "message": "OTP verified successfully",
        "email":user.email,
        "is_verified": user.is_verified
    }


@router.post("/reset-password/{email}")
def reset_password(email: str, payload: user_schema.ResetPassword, db: Session = Depends(database.get_db)):
    user = db.query(user_model.User).filter(user_model.User.email==email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    hashed_password = hashing.hash_password(payload.new_password)
    user.password =hashed_password
    user.otp = None
    db.commit()

    return {"message": "Password updated successfully"}









