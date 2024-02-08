from typing import Optional, Generator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


__engine: Optional[AsyncEngine] = None


def create_engine() -> Optional[AsyncEngine]:
    global __engine

    conn_str: str = "postgresql+asyncpg://postgres:Xzone123@@@localhost:5432/postgres"
    __engine = create_async_engine(url=conn_str, echo=False)
    return __engine


async def create_session() -> Generator:
    global __engine

    if not __engine:
        create_engine()
    async_session = sessionmaker(__engine, expire_on_commit=False, class_=AsyncSession)
    session: AsyncSession = async_session()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()
