from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import ResourcesTag, Tag


def create_resource_tag(db: Session, r_tag: schemas.ResourceTagCreate):
    db_r_tag = ResourcesTag(**r_tag.dict())
    db.add(db_r_tag)
    db.commit()
    db.refresh(db_r_tag)
    return db_r_tag


def get_resource_tag(db: Session, resource_id: str, tag_id: str, user_id: str):
    return (
        db
        .query(ResourcesTag)
        .filter(
            ResourcesTag.resource_id == resource_id,
            ResourcesTag.tag_id == tag_id,
            ResourcesTag.user_id == user_id
        )
        .first()
    )


def get_tags_by_resource(db: Session, resource_id: str, user_id: str = None):
    db_tags = []

    # db_tags generated
    db_tags.extend(
        db
        .query(ResourcesTag, Tag)
        .filter(
            ResourcesTag.resource_id == resource_id,
            ResourcesTag.user_id == None,
            Tag.id == ResourcesTag.tag_id
        )
        .all()
    )

    if user_id:
        # add tags created by the user
        db_tags.extend(
            db
            .query(ResourcesTag, Tag)
            .filter(
                ResourcesTag.resource_id == resource_id,
                ResourcesTag.user_id == user_id,
                Tag.id == ResourcesTag.tag_id
            )
            .all()
        )

    return db_tags


def delete_resource_tag(db: Session, resource_id: str, tag_id: str, user_id: str):
    (
        db
        .query(ResourcesTag)
        .filter(
            ResourcesTag.resource_id == resource_id,
            ResourcesTag.tag_id == tag_id,
            ResourcesTag.user_id == user_id
        )
        .delete()
    )
    db.commit()
