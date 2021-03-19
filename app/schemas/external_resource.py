from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal


class ExternalResourceBase(BaseModel):
    url: str
    imported_by: constr(max_length=12)
    type: constr(max_length=15)
    raw: Optional[str]
    article_id: constr(max_length=12)


class ExternalResourceCreate(ExternalResourceBase):
    pass


class ExternalResource(ExternalResourceBase):
    id: constr(max_length=12)
    date: datetime

    class Config:
        orm_mode = True


class ExternalResourceRestricted(BaseModel):
    id: constr(max_length=12)
    url: str
    type: constr(max_length=15)
    article_id: constr(max_length=12)

    class Config:
        orm_mode = True
