import datetime
from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    password: str

    class Config:
        from_attributes = True
