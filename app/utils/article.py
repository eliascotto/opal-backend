from sqlalchemy.orm import Session
from typing import List, Optional, Dict

from .. import crud, schemas
from ..models import Block, Article
from .main import generate_uuid


def create_article_scheme(title: str, subtitle: str, user_id: str = None, properties: Dict = None):
    params = {
        "title": title,
        "subtitle": subtitle,
        "author": user_id,
        "properties": properties,
    }
    return schemas.ArticleCreate(**params)


def store_article(db: Session, article: schemas.ArticleCreate, blocks: List[Dict]):
    """
    Store a new article into the db, with all the blocks in different instances
    """

    # create new article
    new_article = Article(**{
        **article.dict(),
        "id": crud.generate_article_id(db),
    })
    db.add(new_article)
    db.flush()

    # list of blocks to push into the db
    new_blocks = []

    try:
        for block in blocks:
            # create blocks
            params = {
                **block.to_dict(),
                "id": generate_uuid(),
                "article_id": new_article.id
            }

            new_block = schemas.BlockCreate(**params)

            # ORM operation:
            #   add blocks to the db and commit at the end.
            #   if something fails, rollback and delete article
            db_block = Block(**new_block.dict())
            db.add(db_block)
            db.flush()

            new_blocks.append(db_block)

        db.commit()
        db.refresh(new_article)
    except Exception as e:
        print(e)
        db.rollback()

    return new_article
