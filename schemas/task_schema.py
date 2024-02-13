import datetime
from typing import Optional
from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    user_id: int

    class Config:
        from_attributes = True
