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
from fastapi import Request
import httpx



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




@router.get("/google/login")
def google_login():
    
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(database.get_db)):
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No code provided by Google"
        )

    async with httpx.AsyncClient() as client:
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = await client.post(GOOGLE_TOKEN_URL, data=token_data)
        if token_res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve access token from Google"
            )

        token_json = token_res.json()
        access_token = token_json.get("access_token")

        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_res = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        if userinfo_res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve user info from Google"
            )

        userinfo = userinfo_res.json()

    google_email = userinfo.get("email")
    name = userinfo.get("name", "Google User")

    if not google_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no email"
        )

    user = db.query(user_model.User).filter(
        user_model.User.email == google_email
    ).first()

    if not user:
        user = user_model.User(
            name=name,
            email=google_email,
            password=hashing.hash_password("GOOGLE_AUTH_USER"),  # dummy/pass
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = jwt_handler.create_access_token(
        data={"user_id": user.id, "email": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email,
        "name": user.name,
        "login_provider": "google"
    }







