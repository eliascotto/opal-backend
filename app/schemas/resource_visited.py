from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal


class ResourceVisitedBase(BaseModel):
    user_id: constr(max_length=12)
    resource_id: constr(max_length=12)


class ResourceVisitedCreate(ResourceVisitedBase):
    pass


class ResourceVisited(ResourceVisitedBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
