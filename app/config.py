import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "JWT_SECRET_KEY")




EMAIL_HOST = os.getenv("EMAIL_HOST", "EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "EMAIL_PORT"))  
EMAIL_USER = os.getenv("EMAIL_USER")           
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")   
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USER)
EMAIL_USE_TLS = True