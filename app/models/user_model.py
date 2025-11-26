# step 1.3

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from ..database import Base


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False, index= True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable= False)
    is_verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'))


# step 1.3