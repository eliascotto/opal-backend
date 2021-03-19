from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import ResourcesSaved


def create_resource_saved(db: Session, a_saved: schemas.ResourceSavedCreate):
    db_a_saved = ResourcesSaved(**a_saved.dict())
    db.add(db_a_saved)
    db.commit()
    db.refresh(db_a_saved)
    return db_a_saved


def save_user_resource(db: Session, resource_id: str, user_id: str):
    schema = schemas.ResourceSavedCreate(
        user_id=user_id,
        resource_id=resource_id
    )
    return create_resource_saved(db, schema)


def delete_user_resource(db: Session, resource_id: str, user_id: str):
    (
        db
        .query(ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == resource_id
        )
        .delete()
    )
    db.commit()


def get_saved_resource(db: Session, resource_id: str, user_id: str):
    return (
        db
        .query(ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == resource_id
        )
        .first()
    )


def count_saved_resouce(db: Session, resource_id: str):
    return (
        db
        .query(ResourcesSaved)
        .filter(
            ResourcesSaved.resource_id == resource_id,
            ResourcesSaved.private == False,
        )
        .count()
    )


def get_saved_by_resource(db: Session, resource_id: str):
    return (
        db
        .query(ResourcesSaved)
        .filter(ResourcesSaved.resource_id == resource_id)
        .all()
    )


def get_saved_by_user(db: Session, user_id: str):
    return (
        db
        .query(ResourcesSaved)
        .filter(ResourcesSaved.user_id == user_id)
        .all()
    )


def set_saved_resource_private(db: Session, resource_id: str, user_id: str, private: bool):
    (
        db
        .query(ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == resource_id
        )
        .update({ "private": private })
    )
    db.commit()
