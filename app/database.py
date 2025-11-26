# step 1.2

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:4321@localhost/ayni'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
seasionlocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = seasionlocal()
    try:
        yield db
    finally:
        db.close()

# step 1.2