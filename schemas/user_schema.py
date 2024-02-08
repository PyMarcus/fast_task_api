import datetime
from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: Optional[int]
    name: str
    password: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
