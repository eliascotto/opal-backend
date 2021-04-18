from uuid import UUID
from typing import List, Optional, Dict, Union
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal


class BlockBase(BaseModel):
    id: UUID
    article_id: constr(max_length=12)
    type: constr(max_length=25)
    position: int
    indent: int
    list: Optional[constr(max_length=1)]
    properties: Optional[Dict]
    content: Optional[Union[List[Dict], Dict]]


class BlockCreate(BlockBase):
    pass


class Block(BlockBase):
    date_created: datetime
    date_modified: Optional[datetime]

    class Config:
        orm_mode = True


class BlockUpdate(BaseModel):
    type: Optional[constr(max_length=25)]
    position: Optional[int]
    indent: Optional[int]
    list: Optional[constr(max_length=1)]
    properties: Optional[Dict]
    content: Optional[List[Dict]]


class BlockResourceId(BaseModel):
    block: Block
    resource_id: str
