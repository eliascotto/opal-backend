from fastapi import APIRouter, Depends, HTTPException, status, Query
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

    [db_note, db_article, db_resource] = db_note_art

    if db_note.private and (not user or user.id != db_article.author):
        raise HTTPException(status_code=403, detail="Note is private")

    return schemas.FullNote(note=db_note, article=db_article, resource_id=db_resource.id)


@router.post(
    "/new",
    response_model=schemas.FullNote,
    status_code=status.HTTP_201_CREATED
)
async def add_note(
    article: schemas.ArticleCreate,
    resource_id: str = Query(None),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    """
    Create a new note, with or without `resource_id` as a source
    """
    if resource_id:
        if len(resource_id) != 12:
            raise HTTPException(status_code=404, detail="Resource id field not valid")

        # check if source-resource is present
        db_resource = crud.get_resource(db, resource_id=resource_id)
        if not db_resource or db_resource.hidden:
            raise HTTPException(status_code=404, detail="Resource not found")

    # 1. create new article
    db_article = crud.create_article_with_user(db, article=article, user_id=user.id)

    # 2. create new note (default Private=False)
    db_note = crud.create_note_params(db, source_id=resource_id, article_id=db_article.id)

    # 3. create new resource as a note
    db_resource_new = crud.create_resource_params(db, resource_type="note", resource_id=db_note.id)

    # 4. save user resource
    crud.save_user_resource(db, resource_id=db_resource_new.id, user_id=user.id)

    return schemas.FullNote(note=db_note, article=db_article, resource_id=db_resource_new.id)


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
