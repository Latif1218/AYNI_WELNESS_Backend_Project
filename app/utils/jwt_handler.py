import jwt
from datetime import datetime, timedelta, timezone
from .. schemas import user_schema
from .. models import user_model
from .. database import get_db 
from .. config import SECRET_KEY
from . hashing import verify_password
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from typing import Optional


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def get_user(db: Session, username: str):
    user = db.query(user_model.User).filter(user_model.User.email == username).first()
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = user_schema.TokenData(id = id)

    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db = Depends(get_db) , username=token_data.id)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(
    current_user: Annotated[user_schema.User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
