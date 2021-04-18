from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/blocks",
    tags=["blocks"],
    dependencies=[],
    responses={
        404: { "description": "Block not found" }
    }
)


@router.get("/{block_id}", response_model=schemas.BlockResourceId)
async def get_article(block_id: UUID, db: Session = Depends(get_db)):
    """
    Return a single block with a resource included
    """
    db_block = crud.get_block(db, block_id=block_id)
    if not db_block:
        raise HTTPException(status_code=404, detail="Block not found")
    db_resource = crud.get_resource_by_article(db, article_id=db_block.article_id)[0]
    return schemas.BlockResourceId(block=db_block, resource_id=db_resource.id)
