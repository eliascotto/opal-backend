from uuid import UUID
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, conint, constr
from typing_extensions import Literal


class HighlightBase(BaseModel):
    id: UUID
    resource_id: constr(max_length=12)
    user_id: constr(max_length=12)
    block_id: UUID
    content: Dict


class HighlightCreate(HighlightBase):
    pass


class Highlight(HighlightBase):
    date: datetime

    class Config:
        orm_mode = True
