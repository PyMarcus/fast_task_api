import bcrypt
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from models import User
from datetime import timedelta, datetime
from .database import create_session
from pytz import timezone
import jwt


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login"
)


async def auth(name: str, password: str, db: AsyncSession) -> Optional[User]:
    async with db as session:
        query = select(User).filter(User.name == name)
        result = await session.execute(query)
        user_model: User = result.scalars().unique().one_or_none()
        if not user_model:
            return None

        if not _check_password(password, user_model.password):
            return None

        return user_model


def _check_password(password: str, storage_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), storage_password.encode('utf-8'))


def _create_token(type: str, time: timedelta, user: str) -> str:
    tz = timezone("America/Sao_Paulo")
    expire = datetime.now(tz=tz) + time
    payload = {
        "type": type,
        "expiration": expire.isoformat(),
        "iat": datetime.now(tz=tz).timestamp(),
        "user": user
    }
    return jwt.encode(payload,
                  "qS96E1oCfq5gEZH-ngD91NC2qkcl0cffhNTIDGpF4pw",
                  algorithm="HS256"
                  )


def create_token(obj: str) -> str:
    return _create_token("access_token", timedelta(minutes=60*24*7), obj)


oauth2_scheme2 = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme2), db=Depends(create_session)) -> User:

    try:
        payload = jwt.decode(
            token,
            "qS96E1oCfq5gEZH-ngD91NC2qkcl0cffhNTIDGpF4pw",
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        username = payload.get("user")

        if username is None:
            error: HTTPException = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid tokenÇ {username}",
                headers={"WWW-Authenticate": "Bearer"},
            )
            raise error
    except jwt.PyJWTError as e:
        error2: HTTPException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise error2

    async with db as session:
        query = select(User).filter(
            User.id == int(username))
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()
        print("OK3")

        if user is None:
            raise error
    return user


