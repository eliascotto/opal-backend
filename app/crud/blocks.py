from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from typing import List

from .. import schemas
from ..models import Block, Article


def create_block(db: Session, block: schemas.BlockCreate):
    # block.id is created externally, most of the time client side
    db_block = Block(**block.dict())
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block


def get_block(db: Session, block_id: str):
    return (
        db
        .query(Block)
        .filter(Block.id == block_id)
        .first()
    )


def get_blocks_by_article(db: Session, article_id: str):
    return (
        db
        .query(Block)
        .filter(Block.article_id == article_id)
        .order_by(Block.position)
        .all()
    )


def get_blocks_with_reference(db: Session, article_id: str):
    return (
        db
        .query(Article, Block)
        .filter(
            Article.id == article_id,
            Block.article_id == Article.id,
            Block.properties
        )
        .order_by(Block.position)
        .all()
    )


def update_block(db: Session, block: schemas.Block, block_updates: dict):
    for field in block_updates:
        setattr(block, field, block_updates[field])

    setattr(block, "date_modified", datetime.now())

    db.commit()
    db.flush()
    return block


def delete_block(db: Session, block_id: str):
    (
        db
        .query(Block)
        .filter(Block.id == block_id)
        .delete()
    )
    db.commit()


def shift_blocks(db: Session, block: schemas.Block, decrement: bool=False):
    position = block.position

    update_obj = {
        "position": Block.position - 1
    } if decrement else {
        "position": Block.position + 1
    }

    # increment position of all the consecutive blocks
    (
        db
        .query(Block)
        .filter(Block.position > position)
        .update(update_obj)
    )
    db.commit()


def get_blocks_count_by_article(db, article_id: str):
    def get_count(q):
        count_q = q.statement.with_only_columns([func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    q = (
        db
        .query(Block.id)
        .filter(
            Block.article_id == article_id
        )
    )

    return get_count(q)
