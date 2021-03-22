from typing import Optional, List
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import (
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError

from config import ENV_NAME

from .database import get_db, engine
from .security import (
    authenticate_user,
    get_password_hash,
    get_active_user,
    create_access_token
)
from . import crud, schemas, models
from .routes import (
    users,
    resources,
    articles,
    blocks,
    highlights,
    notes
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

if ENV_NAME == "development":
    origins = ["*"]
else:
    origins = [
        "https://opal-frontend.vercel.app/",
        "http://opal-frontend.vercel.app/"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# Routes
#
app.include_router(users.router)
app.include_router(resources.router)
app.include_router(articles.router)
app.include_router(blocks.router)
app.include_router(highlights.router)
app.include_router(notes.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"WTF: the client sent invalid data: {exc}")
    return await request_validation_exception_handler(request, exc)

#
# Root
#
@app.get("/")
async def root():
    return "Application loaded"

#
# Basic Security, see docs
#
@app.post("/auth")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(form_data.username)
    return { "access_token": access_token, "token_type": "bearer" }
