from pydantic import BaseModel, constr


class TagBase(BaseModel):
    name: constr(max_length=50)


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: constr(max_length=12)

    class Config:
        orm_mode = True
