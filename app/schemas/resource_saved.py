from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal


class ResourceSavedBase(BaseModel):
    resource_id: constr(max_length=12)
    user_id: constr(max_length=12)


class ResourceSavedCreate(ResourceSavedBase):
    pass


class ResourceSaved(ResourceSavedBase):
    date: datetime
    private: bool = False

    class Config:
        orm_mode = True
