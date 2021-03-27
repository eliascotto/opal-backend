from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from typing import Optional

from ..utils import generate_rand_id, get_count
from .. import schemas
from ..models import (
    Article, ResourcesSaved,
    Resource, ExternalResource,
    Note, Block,
)


def generate_article_id(db: Session):
    id = generate_rand_id()

    while (get_article(db, id) != None):
        id = generate_rand_id()

    return id


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = Article(**{
        **article.dict(),
        "id": generate_article_id(db),
    })
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def create_article_with_user(db: Session, article: schemas.ArticleCreate, user_id: str):
    db_article = Article(**{
        **article.dict(),
        "author": user_id,
        "id": generate_article_id(db),
    })
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article(db: Session, article_id: int):
    return (
        db
        .query(Article)
        .filter(Article.id == article_id)
        .first()
    )


def get_article_by_url(db: Session, article_url: str):
    return (
        db
        .query(Article)
        .filter(Article.url == article_url)
        .order_by(desc(Article.date_created))
        .first()
    )


def get_similar_article(db: Session, article: schemas.ArticleCreate):
    return (
        db
        .query(Article)
        .filter(
            Article.author == article.author,
            Article.title == article.title
        )
        .order_by(desc(Article.date_created))
        .first()
    )


def get_user_external_articles(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    filter_user: bool = False
):
    conditions = [
        ResourcesSaved.user_id == user_id,
        Resource.id == ResourcesSaved.resource_id,
        ExternalResource.id == Resource.resource_id,
        Article.id == ExternalResource.article_id,
    ]

    if filter_user:
        conditions.append(ResourcesSaved.private == False)

    return (
        db
        .query(Article, ExternalResource, Resource, ResourcesSaved)
        .filter(*conditions)
        .order_by(ResourcesSaved.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_notes_articles(
    db: Session,
    user_id: int,
    filter_str: Optional[str],
    skip: int = 0,
    limit: int = 100,
    filter_user: bool = False
):
    query = (
        db
        .query(Article, Note, Resource, ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            Resource.id == ResourcesSaved.resource_id,
            Note.id == Resource.resource_id,
            Article.id == Note.article_id
        )
    )

    if filter_user:
        query = query.filter(ResourcesSaved.private == False)

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return (
        query
        .order_by(ResourcesSaved.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_user_notes_articles(
    db: Session,
    user_id: int,
    filter_str: Optional[str],
    filter_user: bool = False
):
    query = (
        db
        .query(Article, Note, Resource, ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            Resource.id == ResourcesSaved.resource_id,
            Note.id == Resource.resource_id,
            Article.id == Note.article_id
        )
    )

    if filter_user:
        query = query.filter(ResourcesSaved.private == False)

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return get_count(query)


def get_article_excerpt(
    db: Session,
    article_id: str,
    skip: int = 0,
    limit: int = 5,
):
    return (
        db
        .query(Article, Block)
        .filter(
            Article.id == article_id,
            Block.article_id == Article.id
        )
        .order_by(Block.position)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_article(db: Session, article_id: int, article_updates: dict):
    db_article = db.query(Article).get(article_id)

    for field in article_updates:
        setattr(db_article, field, article_updates[field])

    setattr(db_article, "date_modified", datetime.now())

    db.commit()
    db.flush()
    return db_article


def delete_article(db: Session, article_id: int):
    (
        db
        .query(Article)
        .filter(Article.id == article_id)
        .update({ "hidden": True })
    )
    db.commit()
