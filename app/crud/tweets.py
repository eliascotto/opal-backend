from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .. import schemas
from ..models import Tweet


def create_tweet(db: Session, tweet = schemas.TweetCreate):
    db_tweet = Tweet(**tweet.dict())
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


def get_tweet(db: Session, tweet_id: int):
    return (
        db
        .query(Tweet)
        .filter(Tweet.id == tweet_id)
        .first()
    )

