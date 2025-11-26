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
    first_name: str
    last_name: str
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orrm_model = True

# step 1.4




# step 2.3

class Token(BaseModel):
    access_token : str
    token_type : str

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