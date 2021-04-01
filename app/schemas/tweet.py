from pydantic import BaseModel, constr
from typing import List, Optional, Dict

from .external_resource import ExternalResource


class TweetBase(BaseModel):
    id: str
    resource_id: str
    content: Dict

class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):

    class Config:
        orm_mode = True


class TweetFull(BaseModel):
    tweet: Tweet
    resource: ExternalResource
