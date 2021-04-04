from pydantic import BaseModel


class Feedback(BaseModel):
    content: str

    class Config:
        orm_mode = True
