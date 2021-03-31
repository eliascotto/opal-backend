from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..utils import get_count
from .. import schemas
from ..models import Vote


def create_vote(db: Session, vote: schemas.VoteCreate):
    db_vote = Vote(**vote.dict())
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_vote(db: Session, user_id: str, resource_id: str):
    return (
        db
        .query(Vote)
        .filter(
            Vote.user_id == user_id,
            Vote.resource_id == resource_id
        )
        .first()
    )


def get_votes_count(db: Session, resource_id: str):
    query = (
        db
        .query(Vote)
        .filter(
            Vote.resource_id == resource_id
        )
    )

    return get_count(query)


def delete_vote(db: Session, user_id: str, resource_id: str):
    (
        db
        .query(Vote)
        .filter(
            Vote.user_id == user_id,
            Vote.resource_id == resource_id
        )
        .delete()
    )
    db.commit()
