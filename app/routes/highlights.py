from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from .. import crud, schemas
from ..database import get_db
from ..security import get_active_user

router = APIRouter(
    prefix="/highlights",
    tags=["highlights"],
    dependencies=[],
    responses={
        404: { "description": "Highlight not found" }
    }
)

# QUESTION
# Now is possible to create and delete only.
# So, if I update an highlight, I will need to delete first and recreate a new one after.
# Implement update to avoid UUID collision could be helpful?

@router.get("/{highlight_id}", response_model=schemas.Highlight)
async def get_highlight(highlight_id: UUID, db: Session = Depends(get_db)):
    db_highlight = crud.get_highlight(db, highlight_id=highlight_id)
    if not db_highlight:
        raise HTTPException(status_code=404, detail="Highlight not found")
    return db_highlight


@router.get("/resource/{resource_id}/{user_id}", response_model=List[schemas.Highlight])
async def get_all_highlights(
    resource_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return crud.get_all_highglights_by_resource(db, resource_id=resource_id, user_id=user_id)


@router.post("/new", response_model=schemas.Highlight)
async def create_highlight(
    highlight: schemas.HighlightCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_highlight = crud.get_highlight(db, highlight_id=highlight.id)
    if db_highlight:
        raise HTTPException(status_code=404, detail="Highlight already exists")
    if user.id != highlight.user_id:
        raise HTTPException(status_code=403, detail="You don't have right to add highlight")

    return crud.create_highlight(db, highlight=highlight)


@router.delete("/{highlight_id}", response_model=schemas.Highlight)
async def delete_highlight(
    highlight_id: UUID,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_highlight = crud.get_highlight(db, highlight_id=highlight_id)
    if not db_highlight:
        raise HTTPException(status_code=404, detail="Highlight not found")

    return crud.delete_highlight(db, highlight_id=highlight_id)
