import re
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Union, Tuple

from .. import crud, schemas, utils
from ..database import get_db, engine
from ..security import (
    authenticate_user,
    get_password_hash,
    get_active_user,
    get_user_or_none,
    create_access_token
)

# Regex for tags, not less than 3 chars
TAG_R = r'^[a-zA-Z0-9]{2,50}$'

router = APIRouter(
    prefix="/resources",
    tags=["resources"],
    dependencies=[],
    responses={
        404: { "description": "Resource not found" }
    }
)


@router.get("/{resource_id}", response_model=schemas.FullResource)
async def get_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_user_or_none)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_count_saved = crud.count_saved_resouce(db, resource_id=resource_id)

    votes = crud.get_votes_count(db, resource_id=resource_id)

    if user:
        user_vote = crud.get_vote(db, user_id=user.id, resource_id=resource_id)
    else:
        user_vote = None

    if db_resource.type == "note":
        # note
        db_note_article = crud.get_note_article(db, note_id=db_resource.resource_id)

        if db_note_article[0].private and (db_note_article[1].author != user.id or user is None):
            # check private note
            raise HTTPException(status_code=401, detail="User not allowed")

        model = schemas.FullResource(
            content=db_note_article,
            saved_count=db_count_saved,
            votes=votes,
            user_vote=user_vote
        )
    else:
        # external article
        db_ext_res_article = crud.get_external_resource_article(
            db,
            ext_resource_id=db_resource.resource_id
        )

        # we create a schemas to contain multiple models;
        # ExternalResource, Article, Optional[SavedResource]
        if user:
            # if the current user is logged, provide information about the saved resource
            db_saved = crud.get_saved_resource(db, resource_id=resource_id, user_id=user.id)

            model = schemas.FullResource(
                content=db_ext_res_article,
                saved=db_saved,
                saved_count=db_count_saved,
                votes=votes,
                user_vote=user_vote
            )
        else:
            model = schemas.FullResource(
                content=db_ext_res_article,
                saved_count=db_count_saved,
                votes=votes,
                user_vote=user_vote
            )

    return model


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    crud.delete_user_resource(db, resource_id=resource_id, user_id=user.id)


@router.get("/{resource_id}/article", response_model=schemas.ArticleWithExcerpt)
async def get_resource_article_exceprt(resource_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_user_or_none)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    if db_resource.type == "note":
        db_note = crud.get_note(db, note_id=db_resource.resource_id)
        article_id = db_note.article_id
    else:
        db_ext_res = crud.get_external_resource(db, ext_resource_id=db_resource.resource_id)
        article_id = db_ext_res.article_id

    db_article = crud.get_article_excerpt(db, article_id=article_id, limit=6)

    article = db_article[0][0]
    if db_resource.type == "note" and db_note.private and user.id != article.author:
        raise HTTPException(status_code=403, detail="Requested resource is private")

    schema = schemas.ArticleWithExcerpt(article=article, blocks=[a[1] for a in db_article])
    return schema


@router.post("externals/tweet")
async def create_tweet(
    tweet_url: str,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    match = utils.match_twitter_status_url(tweet_url=tweet_url)
    if not match:
        raise HTTPException(status_code=406, detail="Tweet status not valid")

    return utils.save_tweet(db, tweet_url=tweet_url, user=user)


@router.post("/externals/new", status_code=status.HTTP_201_CREATED)
async def create_extenal_resource(
    url: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    background_tasks.add_task(
        utils.create_extenal_resource_task,
        db=db, url=url, user=user
    )

    return { "message": "External resource has been added to queue" }


@router.get("/{resource_id}/notes", response_model=List[schemas.ArticleNoteWithExcerpt])
async def get_resource_notes(
    resource_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_user_or_none)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_notes = crud.get_all_notes_by_source(db, source_id=db_resource.id)

    notes_with_excerpt = []
    for collection in db_notes:
        note, article, user = collection

        article_excerpt = crud.get_article_excerpt(db, article_id=note.article_id, limit=6)
        article_excerpt_blocks = [a[1] for a in article_excerpt]

        resource = crud.get_resource_from_resourceid(db, resource_id=note.id)
        votes = crud.get_votes_count(db, resource_id=resource.id)

        if user:
            user_vote = crud.get_vote(db, user_id=user.id, resource_id=resource.id)
        else:
            user_vote = None

        schema = schemas.ArticleNoteWithExcerpt(
            note=note,
            article=article,
            user=user,
            blocks=article_excerpt_blocks,
            votes=votes,
            user_vote=user_vote
        )
        notes_with_excerpt.append(schema)

    return notes_with_excerpt


@router.get("/{resource_id}/mentions", response_model=List[schemas.ResourceMentions])
async def get_resource_mentions(resource_id: str, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    url = "/resource/{}".format(resource_id)
    db_mentions = crud.get_resource_mentions(db, resource_id=resource_id, url=url)

    mentions = []
    for collection in db_mentions:
        resource, note, user, article, block = collection
        # block_count = crud.get_blocks_count_by_article(db, article_id=article.id)
        # position = block.position

        # skip = position - 1
        # limit = 3
        # if position == 0:
        #     skip = 0
        # elif position == block_count - 1:
        #     skip = (position - limit) + 1

        # excerpt = crud.get_article_excerpt(db, article_id=article.id, skip=skip, limit=limit)
        # excerpt_blocks = [a[1] for a in excerpt]
        schema = schemas.ResourceMentions(
            resource=resource,
            user=user,
            article=article,
            blocks=[block],
        )
        mentions.append(schema)

    return mentions


@router.post(
    "/{resource_id}/notes/new",
    response_model=schemas.FullNote,
    status_code=status.HTTP_201_CREATED
)
async def add_note(
    resource_id: str,
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    # check if source-resource is present
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    # 1. create new article
    db_article = crud.create_article_with_user(db, article=article, user_id=user.id)

    # 2. create new note (default Private=False)
    db_note = crud.create_note_params(db, source_id=resource_id, article_id=db_article.id)

    # 3. create new resource as a note
    db_resource = crud.create_resource_params(db, resource_type="note", resource_id=db_note.id)

    # 4. save user resource
    crud.save_user_resource(db, resource_id=db_resource.id, user_id=user.id)

    return schemas.FullNote(note=db_note, article=db_article)


@router.get("/{resource_id}/tags", response_model=List[schemas.ResourceTagFull])
async def get_resource_tags(
    resource_id: str,
    db: Session = Depends(get_db),
    user = Depends(get_user_or_none)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    user_id = user.id if user else None

    db_tags_full = crud.get_tags_by_resource(db, resource_id=resource_id, user_id=user_id)

    tags_all = []
    for collection in db_tags_full:
        schema = schemas.ResourceTagFull(
            resource_tag=collection[0],
            tag=collection[1]
        )
        tags_all.append(schema)

    return tags_all


@router.post("/{resource_id}/tags/new", response_model=schemas.ResourceTag)
async def add_resource_tag(
    resource_id: str,
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    user = Depends(get_active_user)
):
    if not re.match(TAG_R, tag.name):
        raise HTTPException(status_code=406, detail="Tag not valid")

    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_tag = crud.get_tag_by_name(db, name=tag.name.lower())

    if db_tag:
        # tag already present
        db_res_tag = crud.get_resource_tag(
            db,
            resource_id=resource_id,
            tag_id=db_tag.id,
            user_id=user.id
        )

        if not db_res_tag:
            db_res_tag = utils.create_res_tag(
                db,
                resource_id=resource_id,
                tag_id=db_tag.id,
                user_id=user.id,
                raw=tag.name
            )
    else:
        # tag not present
        db_tag = crud.create_tag(db, tag_name=tag.name.lower())

        db_res_tag = utils.create_res_tag(
            db,
            resource_id=resource_id,
            tag_id=db_tag.id,
            user_id=user.id,
            raw=tag.name
        )

    return db_res_tag


@router.delete("/{resource_id}/tags", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    resource_id: str,
    tag: schemas.TagCreate,
    db: Session = Depends(get_db),
    user = Depends(get_active_user)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_tag = crud.get_tag_by_name(db, name=tag.name.lower())
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    crud.delete_resource_tag(
        db,
        resource_id=resource_id,
        tag_id=db_tag.id,
        user_id=user.id
    )


@router.post(
    "/{resource_id}/save",
    response_model=schemas.Article,
    status_code=status.HTTP_201_CREATED
)
async def save_resource(
    resource_id: str,
    delete: bool = False,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    if delete:
        crud.delete_user_resource(db, resource_id=resource_id, user_id=user.id)
    else:
        crud.save_user_resource(db, resource_id=resource_id, user_id=user.id)


@router.post("/{resource_id}/hide-saved", status_code=status.HTTP_204_NO_CONTENT)
async def hide_saved_resource(
    resource_id: str,
    hidden: bool = True,
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    db_res_saved = crud.get_saved_resource(db, resource_id=resource_id, user_id=user.id)
    if not db_res_saved:
        raise HTTPException(status_code=404, detail="Resource has not been saved yet")

    crud.set_saved_resource_private(db, resource_id=resource_id, user_id=user.id, private=hidden)


@router.post(
    "/{resource_id}/vote",
    response_model=schemas.Article,
    status_code=status.HTTP_201_CREATED
)
async def save_vote(
    resource_id: str,
    unvote: bool = Query(False),
    db: Session = Depends(get_db),
    user: schemas.User = Depends(get_active_user)
):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if not db_resource or db_resource.hidden:
        raise HTTPException(status_code=404, detail="Resource not found")

    if unvote:
        # delete vote
        return crud.delete_vote(db, user_id=user.id, resource_id=resource_id)

    vote = crud.get_vote(db, user_id=user.id, resource_id=resource_id)
    if vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vote already present"
        )

    vote_schema = schemas.VoteCreate(user_id=user.id, resource_id=resource_id)
    crud.create_vote(db, vote=vote_schema)


@router.get("/user/{user_id}")
async def get_user_resources(
    user_id: str,
    match: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 100,
    user = Depends(get_user_or_none),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_not_valid = (user is None) or (user.id != user_id)

    if tags:
        db_articles = crud.filter_user_articles_tags(
            db, user_id=user_id,
            filter_str=match,
            tags=tags,
            skip=skip,
            limit=limit,
            filter_private=user_not_valid
        )
        db_articles_count = crud.count_filter_user_articles_tags(
            db, user_id=user_id,
            filter_str=match,
            tags=tags,
            filter_private=user_not_valid
        )
    else:
        # filter all articles matching the string
        db_articles = crud.filter_user_articles(
            db, user_id=user_id,
            filter_str=match,
            skip=skip,
            limit=limit,
            filter_private=user_not_valid
        )
        db_articles_count = crud.count_filter_user_articles(
            db, user_id=user_id,
            filter_str=match,
            filter_private=user_not_valid
        )

    exs = get_articles_excerpts(db, db_articles)

    # all article
    db_note_articles = crud.get_user_notes_articles(
        db, user_id=user_id,
        filter_str=match,
        skip=skip,
        limit=limit,
        filter_user=user_not_valid
    )
    db_note_count = crud.count_user_notes_articles(
        db, user_id=user_id,
        filter_str=match,
        filter_user=user_not_valid
    )
    nts = get_articles_excerpts(db, db_note_articles)

    return {
        "externals": [db_articles, exs],
        "notes": [db_note_articles, nts],
        "info": {
            "external_count": db_articles_count,
            "notes_count": db_note_count
        }
    }


def get_articles_excerpts(db: Session, resources):
    """Extract excerpt from each article in resources"""
    excerpts = []

    for res in resources:
        article = res[0]
        article_excerpt = crud.get_article_excerpt(db, article_id=article.id)
        excerpts.append([block[1] for block in article_excerpt])

    return excerpts
