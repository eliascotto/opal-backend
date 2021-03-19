from uuid import UUID
from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import Highlight


def create_highlight(db: Session, highlight: schemas.HighlightCreate):
    db_highlight = Highlight(**highlight.dict())
    db.add(db_highlight)
    db.commit()
    db.refresh(db_highlight)
    return db_highlight


def get_highlight(db: Session, highlight_id: UUID):
    return (
        db
        .query(Highlight)
        .filter(Highlight.id == highlight_id)
        .first()
    )


def get_all_highglights_by_resource(db: Session, resource_id: str, user_id: str):
    return (
        db
        .query(Highlight)
        .filter(
            Highlight.resource_id == resource_id,
            Highlight.user_id == user_id
        )
        .all()
    )


def delete_highlight(db: Session, highlight_id: UUID):
    (
        db
        .query(Highlight)
        .filter(Highlight.id == highlight_id)
        .delete()
    )
    db.commit()
