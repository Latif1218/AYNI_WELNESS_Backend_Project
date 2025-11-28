# step 1.1 

from fastapi import FastAPI
from . routes import user, auth
from . database import Base, engine
from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)


app = FastAPI()
# step 1.1

app.include_router(user.router)    
app.include_router(auth.router)    
