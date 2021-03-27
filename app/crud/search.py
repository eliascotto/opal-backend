from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Union, Tuple

from ..utils import get_count
from .. import schemas
from ..models import (
    ResourcesSaved, Resource, ExternalResource,
    Article, ResourcesTag, Tag
)


def filter_user_articles(
    db: Session,
    user_id: str,
    filter_str: Optional[str],
    skip: int = 0,
    limit: int = 100,
    filter_private: bool = False
):
    query = (
        db
        .query(Article, ExternalResource, Resource, ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == Resource.id,
            Resource.resource_id == ExternalResource.id,
            ExternalResource.article_id == Article.id
        )
    )

    if filter_private:
        query = query.filter(Article.private == False)

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return (
        query
        .order_by(ResourcesSaved.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def filter_user_articles_tags(
    db: Session,
    user_id: str,
    filter_str: Optional[str],
    tags: List[str],
    skip: int = 0,
    limit: int = 100,
    filter_private: bool = False
):
    query = (
        db
        .query(Article, ExternalResource, Resource, ResourcesSaved, ResourcesTag, Tag)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == Resource.id,
            Resource.resource_id == ExternalResource.id,
            ExternalResource.article_id == Article.id,
            ResourcesTag.user_id == user_id,
            ResourcesTag.resource_id == Resource.id,
            Tag.id == ResourcesTag.tag_id
        )
    )

    if filter_private:
        query = query.filter(Article.private == False)

    for tag in tags:
        query = query.filter(Tag.name.ilike(f'%{tag}%'))

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return (
        query
        .order_by(ResourcesSaved.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def count_filter_user_articles(
    db: Session,
    user_id: str,
    filter_str: Optional[str],
    filter_private: bool = False
):
    query = (
        db
        .query(Article, ExternalResource, Resource, ResourcesSaved)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == Resource.id,
            Resource.resource_id == ExternalResource.id,
            ExternalResource.article_id == Article.id
        )
    )

    if filter_private:
        query = query.filter(Article.private == False)

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return get_count(query)


def count_filter_user_articles_tags(
    db: Session,
    user_id: str,
    filter_str: Optional[str],
    tags: List[str],
    filter_private: bool = False
):
    query = (
        db
        .query(Article, ExternalResource, Resource, ResourcesSaved, ResourcesTag, Tag)
        .filter(
            ResourcesSaved.user_id == user_id,
            ResourcesSaved.resource_id == Resource.id,
            Resource.resource_id == ExternalResource.id,
            ExternalResource.article_id == Article.id,
            ResourcesTag.user_id == user_id,
            ResourcesTag.resource_id == Resource.id,
            Tag.id == ResourcesTag.tag_id
        )
    )

    if filter_private:
        query = query.filter(Article.private == False)

    for tag in tags:
        query = query.filter(Tag.name.ilike(f'%{tag}%'))

    if filter_str:
        query = query.filter(Article.title.ilike(f'%{filter_str}%'))

    return get_count(query)
