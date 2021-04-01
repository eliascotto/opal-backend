from typing import List, Optional, Dict, Union, Tuple
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal

from .article import Article
from .note import Note
from .external_resource import ExternalResource, ExternalResourceRestricted
from .resource_saved import ResourceSaved
from .block import Block
from .user import UserRestricted
from .vote import Vote
from .tweet import Tweet


class ResourceBase(BaseModel):
    type: constr(max_length=20)
    resource_id: constr(max_length=12)


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: constr(max_length=12)
    hidden: bool = False

    class Config:
        orm_mode = True


class FullResource(BaseModel):
    resource: Union[Note, ExternalResourceRestricted]
    content: Union[Article, Tweet]
    saved: Optional[ResourceSaved] = None
    saved_count: int
    votes: int
    user_vote: Optional[Vote]


class ResourceMentions(BaseModel):
    resource: Resource
    user: UserRestricted
    article: Article
    blocks: List[Block]
