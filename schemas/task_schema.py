import datetime
from typing import Optional
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: Optional[int]
    title: str
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
