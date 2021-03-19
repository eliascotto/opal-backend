from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..utils import generate_rand_id
from .. import schemas
from ..models import ExternalResource, Article


def generate_external_resource_id(db: Session):
    id = generate_rand_id()

    while (get_external_resource(db, id) != None):
        id = generate_rand_id()

    return id


def create_external_resource(db: Session, ext_resource: schemas.ExternalResourceCreate):
    db_ext_resource = ExternalResource(**{
        **ext_resource.dict(),
        "id": generate_external_resource_id(db)
    })
    db.add(db_ext_resource)
    db.commit()
    db.refresh(db_ext_resource)
    return db_ext_resource


def get_external_resource(db: Session, ext_resource_id: str):
    return (
        db
        .query(ExternalResource)
        .filter(ExternalResource.id == ext_resource_id)
        .first()
    )


def get_external_resource_article(db: Session, ext_resource_id: str):
    return (
        db
        .query(ExternalResource, Article)
        .filter(
            ExternalResource.id == ext_resource_id,
            ExternalResource.article_id == Article.id
        )
        .first()
    )


def get_resource_by_url(db: Session, resource_url: str):
    return (
        db
        .query(ExternalResource)
        .filter(ExternalResource.url == resource_url)
        .order_by(ExternalResource.date)
        .first()
    )
