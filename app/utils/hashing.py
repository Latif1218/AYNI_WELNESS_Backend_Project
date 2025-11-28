# step 1.5

from pwdlib import PasswordHash
from .. schemas import user_schema

password_hash = PasswordHash.recommended()

def hash_password(password: str):
    return password_hash.hash(password)


# step 1.5


# step 2.1

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

# step 2.1


