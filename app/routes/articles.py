from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas
from ..database import get_db, engine
from ..security import (
    authenticate_user,
    get_password_hash,
    get_active_user,
    get_user_or_none,
    create_access_token
)

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    dependencies=[],
    responses={
        404: { "description": "Article not found" }
    },
)


@router.get("/{article_id}", response_model=schemas.Article)
async def get_article(article_id: str, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router.patch("/{article_id}", response_model=schemas.Article)
async def update_article(
    article_id: str,
    article: schemas.ArticleBase,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author != user.id:
        raise HTTPException(status_code=404, detail="Cannot edit article not owned by the user")
    
    article_updates = article.dict(exclude_unset=True)
    return crud.update_article(db, article_id=article_id, article_updates=article_updates)


@router.delete("/{article_id}", status_code=status.HTTP_200_OK)
async def delete_article(
    article_id: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if db_article.author != user.id:
        raise HTTPException(status_code=404, detail="Cannot delete article not owned by the user")

    return crud.delete_article(db, article_id=article_id)


@router.get("/{article_id}/blocks", response_model=List[schemas.Block])
async def get_blocks(article_id: str, db: Session = Depends(get_db)):
    return crud.get_blocks_by_article(db, article_id=article_id)


@router.post("/{article_id}/blocks", status_code=status.HTTP_201_CREATED)
async def create_block(
    article_id: str,
    block: schemas.BlockCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not db_article.author:
        raise HTTPException(status_code=404, detail="Article not editable")
    if user.id != db_article.author:
        raise HTTPException(status_code=403, detail="Cannot create blocks for article not owned by the user")

    # create block
    new_block = crud.create_block(db, block=block)
    # shift all the others based on the new block position
    return crud.shift_blocks(db, block=new_block)


@router.patch("/{article_id}/blocks/{block_id}", status_code=status.HTTP_200_OK)
async def update_block(
    article_id: str,
    block_id: str,
    block: schemas.BlockUpdate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not db_article.author:
        raise HTTPException(status_code=404, detail="Article not editable")
    if user.id != db_article.author:
        raise HTTPException(status_code=403, detail="Cannot update blocks for article not owned by the user")

    db_block = crud.get_block(db, block_id=block_id)

    if db_block:
        # remove the default parameters in schemas.BlockUpdate not present in the request body
        block_updates = block.dict(exclude_unset=True)
        db_block = crud.update_block(db, block=db_block, block_updates=block_updates)
    else:
        # create new block
        db_block = crud.create_block(db, block=block)

    return db_block


@router.delete("/{article_id}/blocks/{block_id}", status_code=status.HTTP_200_OK)
async def delete_block(
    article_id: str,
    block_id: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_article = crud.get_article(db, article_id=article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    if not db_article.author:
        raise HTTPException(status_code=404, detail="Article not editable")
    if user.id != db_article.author:
        raise HTTPException(status_code=403, detail="Cannot delete blocks for article not owned by the user")

    db_block = crud.get_block(db, block_id=block_id)
    crud.shift_blocks(db, block=db_block, decrement=True)

    return crud.delete_block(db, block_id=block_id)
