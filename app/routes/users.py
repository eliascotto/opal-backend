from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from email_validator import validate_email, EmailNotValidError

from .. import crud, schemas
from ..database import get_db, engine
from ..security import (
    authenticate_user,
    get_password_hash,
    get_active_user,
    get_user_or_none,
    create_access_token
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={
        404: { "description": "User not found" }
    },
)


@router.get("/me", response_model=schemas.User)
async def read_current_user(user: schemas.User = Depends(get_active_user)):
    return user


@router.get("/{user_id}", response_model=schemas.UserRestricted)
async def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/new", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Validate.
        valid = validate_email(user.email)
        # Update with the normalized form.
        user.email  = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        raise HTTPException(status_code=400, detail=str(e))

    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = get_password_hash(user.password)
    new_user = crud.create_user(db, user, password)
    
    return new_user


@router.post("/onboard", status_code=status.HTTP_204_NO_CONTENT)
async def set_user_onboard(
    user: schemas.User = Depends(get_active_user),
    db: Session = Depends(get_db)
):
    crud.set_user_onboard(db, user_id=user.id, onboard=True)
