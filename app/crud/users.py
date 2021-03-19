from datetime import datetime
from sqlalchemy.orm import Session

from ..utils import generate_rand_id
from .. import schemas
from ..models import User


def generate_user_id(db: Session):
    id = generate_rand_id()

    while (get_user(db, id) != None):
        id = generate_rand_id()

    return id


def create_user(
    db: Session,
    user: schemas.UserCreate,
    password_hashed: str
):
    db_user = User(
        id=generate_user_id(db),
        email=user.email,
        password=password_hashed,
        name=user.name,
        display_name=user.name,
        last_login=datetime.now(),
        blocked=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return (
        db
        .query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_name(db: Session, user_name: str):
    return (
        db
        .query(User)
        .filter(User.name == user_name)
        .first()
    )


def get_user_by_email(db: Session, email: str):
    return (
        db
        .query(User)
        .filter(User.email == email)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db
        .query(User)
        .order_by(User.date_created)
        .offset(skip)
        .limit(limit)
        .all()
    )
