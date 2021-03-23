from os import environ, path

# ENV
ENV_NAME = environ.get("ENV_NAME")

# Database config
DATABASE_HOST = environ.get("DATABASE_HOST")
DATABASE_USERNAME = environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
DATABASE_PORT = environ.get("DATABASE_PORT")
DATABASE_NAME = environ.get("DATABASE_NAME")
DATABASE_URL = environ.get("DATABASE_URL")

# JWT Settings 
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

# general
FRONTEND_DOMAIN=environ.get('FRONTEND_DOMAIN')
