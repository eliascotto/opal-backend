from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal

from .tag import Tag


class ResourceTagBase(BaseModel):
    resource_id: constr(max_length=12)
    tag_id: constr(max_length=12)
    user_id: constr(max_length=12)
    raw: Optional[constr(max_length=50)]


class ResourceTagCreate(ResourceTagBase):
    pass


class ResourceTag(ResourceTagBase):

    class Config:
        orm_mode = True


class ResourceTagFull(BaseModel):
    resource_tag: ResourceTag

    class Config:
        orm_mode = True
