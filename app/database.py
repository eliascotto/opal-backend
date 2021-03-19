from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import (
    DATABASE_HOST,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_NAME,
)

DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME
)

# postgresql engine
engine = create_engine(DATABASE_URL, encoding='utf-8', echo=False)

# create a session if necessary
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# return a db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
