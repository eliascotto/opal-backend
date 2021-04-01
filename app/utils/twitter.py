import re
import tweepy
from sqlalchemy.orm import Session
from typing import Dict

from config import (
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)

from .. import schemas, crud
from .resource import store_resource, store_external_resource

TWITTER_R = r'^https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)'


def check_url_tweet(url: str):
    print(type(url))
    return re.match(TWITTER_R, url)


def get_tweet(tweet_id: int):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    status = api.get_status(tweet_id, tweet_mode="extended")

    info = {
        "text": status.full_text,
        "author": status.author._json,
        "entities": status.entities,
    }

    if hasattr(status, "extended_entities"):
        info["extended_entities"] = status.extended_entities

    return info


def get_tweet_id(tweet_url: str):
    match = check_url_tweet(url=tweet_url)

    if match:
        return match.groups()[2]
    return None


def create_ext_resource_scheme(url: str, raw: str, user_id: str):
    return schemas.ExternalResourceCreate(
        url=url,
        imported_by=user_id,
        type="tweet",
        raw=raw
    )


def store_external_resource(db: Session, url: str, raw: str, user_id: str):
    ext_resource_scheme = create_ext_resource_scheme(url, raw, user_id)
    
    new_ext_resource = crud.create_external_resource(db, ext_resource=ext_resource_scheme)
    return new_ext_resource


def create_tweet_scheme(tweet_id: int, tweet_info: Dict, resource_id: str):
    return schemas.TweetCreate(
        id=tweet_id,
        resource_id=resource_id,
        content=tweet_info
    )


def save_tweet(db: Session, tweet_url: str, user: schemas.User):
    tweet_id = get_tweet_id(tweet_url=tweet_url)

    db_tweet = crud.get_tweet(db, tweet_id)

    if db_tweet:
        # tweet already present, save to user collection
        resource = crud.get_resource_from_resourceid(db, resource_id=db_tweet.resource_id)
        ext_resource = crud.get_external_resource(db, ext_resource_id=db_tweet.resource_id)

        if not crud.get_saved_resource(db, user_id=user.id, resource_id=resource.id):
            # save resource inside the user collection
            crud.save_user_resource(db, resource_id=resource.id, user_id=user.id)

        return {
            "tweet": db_tweet,
            "resource": ext_resource,
        }

    tweet_info = get_tweet(tweet_id=tweet_id)

    tweet_ext_resource = store_external_resource(
        db, 
        url=tweet_url,
        raw=str(tweet_info),
        user_id=user.id
    )

    tweet_scheme = create_tweet_scheme(
        tweet_id=tweet_id,
        tweet_info=tweet_info,
        resource_id=tweet_ext_resource.id
    )

    tweet = crud.create_tweet(db, tweet=tweet_scheme)

    resource = store_resource(db, resource_id=tweet_ext_resource.id)

    crud.save_user_resource(db, resource_id=resource.id, user_id=user.id)

    return {
        "tweet": tweet_scheme,
        "resource": tweet_ext_resource,
    }


def clean_tweet_object(tweet_obj):
    tweet_obj.id = str(tweet_obj.id)
    return tweet_obj
