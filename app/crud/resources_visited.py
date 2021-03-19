from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import ResourcesVisited


def create_resource_visited(db: Session, a_read: schemas.ResourceVisitedCreate):
    db_a_read = ResourcesVisited(**a_read.dict())
    db.add(db_a_read)
    db.commit()
    db.refresh(db_a_read)
    return db_a_read


def get_resource_visited(db: Session, resource_visited_id: int):
    return (
        db
        .query(ResourcesVisited)
        .filter(ResourcesVisited.id == resource_visited_id)
        .first()
    )


def get_read_by_resource(db: Session, resource_id: str):
    return (
        db
        .query(ResourcesVisited)
        .filter(ResourcesVisited.resource_id == resource_id)
        .all()
    )


def get_read_by_user(db: Session, user_id: str):
    return (
        db
        .query(ResourcesVisited)
        .filter(ResourcesVisited.user_id == user_id)
        .all()
    )
