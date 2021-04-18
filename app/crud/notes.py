from datetime import datetime
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..utils import generate_rand_id
from .. import schemas
from ..models import Note, Article, User, Resource
from .articles import generate_article_id


def generate_note_id(db: Session):
    id = generate_rand_id()

    while (get_note(db, id) != None):
        id = generate_rand_id()

    return id


def create_note(db: Session, note: schemas.NoteCreate):
    db_note = Note(**{
        **note.dict(),
        "id": generate_note_id(db)
    })
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def create_note_params(db: Session, source_id: str, article_id: str, private: bool = False):
    db_schema = schemas.NoteCreate(
        source_id=source_id,
        article_id=article_id,
        private=private
    )

    return create_note(db, db_schema)


def get_note(db: Session, note_id: str):
    return (
        db
        .query(Note)
        .filter(Note.id == note_id)
        .first()
    )


def get_note_article(db: Session, note_id: str):
    return (
        db
        .query(Note, Article, Resource)
        .filter(
            Note.id == note_id,
            Article.id == Note.article_id,
            Resource.resource_id == Note.id
        )
        .first()
    )


def get_all_notes_by_source(db: Session, source_id: str):
    return (
        db
        .query(Note, Article, User)
        .filter(
            Note.source_id == source_id,
            Note.article_id == Article.id,
            Article.author == User.id,
            Note.private == False
        )
        .all()
    )


def get_all_notes_by_user(db: Session, user_id: str):
    return (
        db
        .query(Note, Article)
        .filter(
            Article.author == user_id,
            Note.article_id == Article.id
        )
        .all()
    )


def count_all_notes_by_user(db: Session, user_id: str, private: bool = False):
    return (
        db
        .query(Note, Article)
        .filter(
            Article.author == user_id,
            Note.article_id == Article.id,
            Note.private == private
        )
        .count()
    ) 


def set_note_private(db: Session, note_id: str, private: bool):
    (
        db
        .query(Note)
        .filter(Note.id == note_id)
        .update({ "private": private })
    )
    db.commit()


def delete_note(db: Session, note_id: str):
    (
        db
        .query(Note)
        .filter(Note.id == note_id)
        .delete()
    )
    db.commit()
