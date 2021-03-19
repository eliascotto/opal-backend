from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import Vote


def create_vote_schema(user_id: str, resource_id: str):
    return schemas.VoteCreate(**{
        user_id: user_id,
        resource_id: resource_id
    })


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
