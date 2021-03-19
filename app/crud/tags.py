from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..utils import generate_rand_id
from .. import schemas
from ..models import Tag


def generate_tag_id(db: Session):
    id = generate_rand_id()

    while (get_tag(db, id) != None):
        id = generate_rand_id()

    return id


def create_tag(db: Session, tag_name: str):
    db_tag = Tag(
        name=tag_name,
        id=generate_tag_id(db)
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return (
        db
        .query(Tag)
        .filter(Tag.id == tag_id)
        .first()
    )


def get_tag_by_name(db: Session, name: str):
    return (
        db
        .query(Tag)
        .filter(Tag.name == name)
        .first()
    )
