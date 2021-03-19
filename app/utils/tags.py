from sqlalchemy.orm import Session

from .. import crud, schemas
from ..models import Block, Article


def create_res_tag(
    db: Session,
    resource_id: str,
    tag_id: str, 
    user_id: str,
    raw: str
):
    schema = schemas.ResourceTagCreate(
        resource_id=resource_id,
        tag_id=tag_id,
        user_id=user_id,
        raw=raw
    )

    return crud.create_resource_tag(db, r_tag=schema)
