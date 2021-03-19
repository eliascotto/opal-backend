from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, schemas
from ..database import get_db
from ..security import get_user_or_none, get_active_user

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    dependencies=[],
    responses={
        404: { "description": "Note not found" }
    }
)

# QUESTION
# Now is possible to create and delete only.
# So, if I update an highlight, I will need to delete first and recreate a new one after.
# Implement update to avoid UUID collision could be helpful?

@router.get("/{note_id}", response_model=schemas.FullNote)
async def get_note(
    note_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_user_or_none)
):
    db_note_art = crud.get_note_article(db, note_id=note_id)
    if not db_note_art:
        raise HTTPException(status_code=404, detail="Note not found")

    [db_note, db_article] = db_note_art

    if db_note.private and (not user or user.id != db_article.author):
        raise HTTPException(status_code=403, detail="Note is private")

    return schemas.FullNote(note=db_note, article=db_article)


@router.post("/{note_id}/set", response_model=schemas.Note)
async def set_note_private(
    note_id: str,
    private_upd: schemas.NotePrivateUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_active_user)
):
    db_note = crud.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_article = crud.get_article(db, article_id=db_note.article_id)
    if db_article.author != user.id:
        raise HTTPException(status_code=403, detail="Note edit not permitted")

    crud.set_note_private(db, note_id=note_id, private=private_upd.private)

    return db_note


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_note = crud.get_note(db, note_id=note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    db_article = crud.get_article(db, article_id=db_note.article_id)
    if db_article.author != user.id:
        raise HTTPException(status_code=403, detail="Note delete not permitted")

    crud.delete_note(db, note_id=note_id)
