from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from typing import Sequence
from schemas import UserSchema
from commum import create_session
from commum import hash_password
from models import User


router: APIRouter = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema, response_model_exclude={"password"})
async def create_user(user: UserSchema, db: AsyncSession = Depends(create_session)) -> UserSchema:
    try:
        async with db as session:
            query = select(User).filter(user.name == User.name)
            result = await session.execute(query)
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error to try process this user"
                )

        new_user: User = User(
            name=user.name,
            password=hash_password(user.password)
        )
        db.add(new_user)
        await db.commit()
        return new_user
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema], response_model_exclude={"password"})
async def get_all_users(db: AsyncSession = Depends(create_session)) -> Sequence[UserSchema]:
    try:
        async with db as session:
            query = select(User)
            response = await session.execute(query)
            return response.scalars().all()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
