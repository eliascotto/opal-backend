from sqlalchemy.orm import Session
from urllib.parse import unquote

from ..web2markdown import webpage2blocks
from ..models import Resource
from .. import schemas, crud

from .main import generate_uuid, compare_raw_str
from .article import store_article, create_article_scheme


def create_resource_scheme(db: Session, resource_id: str):
    params = {
        "type": "external_resource",
        "resource_id": resource_id
    }
    return schemas.ResourceCreate(**params)


def store_resource(db: Session, resource_id: str):
    resource_scheme = create_resource_scheme(db, resource_id)
    
    new_resource = crud.create_resource(db, resource=resource_scheme)
    return new_resource


def create_ext_resource_scheme(db: Session, url: str, raw: str, article_id: str, user_id: str):
    params = {
        "url": url,
        "imported_by": user_id,
        "type": "article",
        "raw": raw,
        "article_id": article_id
    }
    return schemas.ExternalResourceCreate(**params)


def store_external_resource(
    db: Session,
    url: str,
    raw: str,
    article_id: str,
    user_id: str
):
    ext_resource_scheme = create_ext_resource_scheme(db, url, raw, article_id, user_id)
    
    new_ext_resource = crud.create_external_resource(db, ext_resource=ext_resource_scheme)
    return new_ext_resource


def check_for_duplicates(db: Session, url: str):
    # get the external resource with the url
    duplicated_resource = crud.get_resource_by_url(db, url)

    if duplicated_resource:
        # resource with url is duplicated, check for raw content if the same
        # if compare_raw_str(duplicated_resource.raw, raw):
        return duplicated_resource

    return None


def upload_resource_with_url(db: Session, url: str, user_id: str):
    duplicated = check_for_duplicates(db, url=url)

    if duplicated:
        # WARNING is returning an ExternalResource
        return (duplicated, None)

    article = webpage2blocks(url)

    article_json = article["raw"]

    # create ARTICLE first
    title = article_json["title"] if "title" in article_json else ""
    subtitle = article_json["subtitle"] if "subtitle" in article_json else ""
    scheme = create_article_scheme(title, subtitle, properties=article["meta"])

    article = store_article(db, article=scheme, blocks=article["blocks"])

    # create EXT_RESOURCE with article link
    ext_resource = store_external_resource(db, url, article_json["content"], article.id, user_id)

    return (ext_resource, article)


def create_extenal_resource_task(db: Session, url: str, user: schemas.User):
    decoded_url = unquote(url)
    # celery background tasl
    db_ext_resource, db_article = upload_resource_with_url(db, url=decoded_url, user_id=user.id)

    if db_article:
        # create RESOURCE with resource id
        resource = store_resource(db, resource_id=db_ext_resource.id)
    else:
        # get resource already present
        resource = crud.get_resource_from_resourceid(db, resource_id=db_ext_resource.id)

    if not crud.get_saved_resource(db, user_id=user.id, resource_id=resource.id):
        # save resource inside the user collection
        crud.save_user_resource(db, resource_id=resource.id, user_id=user.id)
