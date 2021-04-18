from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, conint, constr
from typing_extensions import Literal

from .article import Article
from .block import Block
from .user import UserRestricted
from .vote import Vote


class NoteBase(BaseModel):
    source_id: Optional[constr(max_length=12)]
    article_id: constr(max_length=12)
    private: bool = False


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: constr(max_length=12)

    class Config:
        orm_mode = True


class NotePrivateUpdate(BaseModel):
    private: bool


class NoteWithExcerpt(NoteBase):
    article: List[Dict]


class FullNote(BaseModel):
    note: Note
    article: Article
    resource_id: str


class ArticleNoteWithExcerpt(BaseModel):
    note: Note
    article: Article
    user: UserRestricted
    blocks: List[Block]
    votes: int
    user_vote: Optional[Vote]
