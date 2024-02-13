import sqlalchemy as sa
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__: str = "user"

    id: Optional[int] = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String(100), nullable=False)
    password: str = sa.Column(sa.String(900), nullable=False)
    created_at: Optional[datetime] = sa.Column(sa.DateTime, default=datetime.now, index=True)
