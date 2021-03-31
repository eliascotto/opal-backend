from pydantic import BaseModel, constr

from .external_resource import ExternalResource


class TweetBase(BaseModel):
    id: int
    resource_id: str

class TweetCreate(TweetBase):
    pass


class Tweet(TweetBase):

    class Config:
        orm_mode = True


class TweetFull(BaseModel):
    tweet: Tweet
    resource: ExternalResource
