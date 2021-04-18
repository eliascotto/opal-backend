from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..utils import generate_rand_id
from .. import schemas
from ..models import (
    Resource,
    Article,
    ExternalResource,
    Note,
    Block,
    User
)


def generate_resource_id(db: Session):
    id = generate_rand_id()

    while (get_resource(db, id) != None):
        id = generate_rand_id()

    return id


def create_resource(db: Session, resource: schemas.ResourceCreate):
    db_resource = Resource(**{
        **resource.dict(),
        "id": generate_resource_id(db)
    })
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def create_resource_params(db: Session, resource_type: str, resource_id: str):
    db_schema = schemas.ResourceCreate(
        type=resource_type,
        resource_id=resource_id
    )

    return create_resource(db, db_schema)


def get_resource(db: Session, resource_id: str):
    return (
        db
        .query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )


def get_resource_from_resourceid(db: Session, resource_id: str):
    return (
        db
        .query(Resource)
        .filter(Resource.resource_id == resource_id)
        .first()
    )


def get_resource_mentions(db: Session, resource_id: str, url: str):
    return (
        db
        .query(Resource, Note, User, Article, Block)
        .filter(
            Block.properties.contains({ "links": [url] }) == True,
            Block.article_id == Article.id,
            Note.article_id == Article.id,
            Resource.resource_id == Note.id,
            User.id == Article.author
        )
        .all()
    )


def get_resource_by_article(db: Session, article_id: str):
    db_ext = (
        db
        .query(Resource, ExternalResource, Article)
        .filter(
            Article.id == article_id,
            ExternalResource.article_id == Article.id,
            Resource.resource_id == ExternalResource.id
        )
        .first()
    )

    if len(db_ext) == 0:
        return (
            db
            .query(Resource, Note, Article)
            .filter(
                Article.id == article_id,
                Note.article_id == Article.id,
                Resource.resource_id == Note.id
            )
            .first()
        )
    else:
        return db_ext
