import sqlalchemy as sa
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Task(Base):
    __tablename__: str = "task"

    id: Optional[int] = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title: str = sa.Column(sa.String(100), nullable=False)
    user_id: int = sa.Column(sa.Integer, nullable=False)
    created_at: Optional[datetime] = sa.Column(sa.DateTime, default=datetime.now, index=True)
