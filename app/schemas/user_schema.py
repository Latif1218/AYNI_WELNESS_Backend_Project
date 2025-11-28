# step 1.4

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orrm_model = True

# step 1.4


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    disabled: bool 
    created_at : datetime




class UserInDB(User):
    hashed_password: str





# step 2.3

class Token(BaseModel):
    access_token : str
    token_type : str

    class Config:
        orm_mode = True

# step 2.3




# step 2.4

class UserLogin(BaseModel):
    email : EmailStr
    password : str 


# step 2.4



# step 2.5

class TokenData(BaseModel):
    id : Optional[int] = None


# step 2.5



# step 3.2

class ForgotPassword(BaseModel):
    email: EmailStr

# step 3.2


# step 4.2

class VerifyOtp(BaseModel):
    email: EmailStr
    otp: str

# step 4.2


# step 5.2

class ResetPassword(BaseModel):
    new_password: str