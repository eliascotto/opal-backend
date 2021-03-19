from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, constr

from .block import Block


class ArticleBase(BaseModel):
    """
    url: is the external resource url from where the article has been imported
    raw: is the raw rapresentation of the article
    """
    title: constr(max_length=200)
    subtitle: Optional[constr(max_length=60)]
    author: Optional[constr(max_length=12)]
    properties: Optional[Dict]


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: constr(max_length=12)
    date_created: datetime
    date_modified: Optional[datetime]

    class Config:
        orm_mode = True


class ArticleWithExcerpt(BaseModel):
    article: Article
    blocks: List[Block]
