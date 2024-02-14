import datetime
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from typing import Sequence
from schemas import TaskSchema
from commum import create_session
from models import Task


router: APIRouter = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def create_task(task: TaskSchema, db: AsyncSession = Depends(create_session)) -> TaskSchema:
    try:
        async with db as session:
            query = select(Task).filter(task.title == Task.title)
            result = await session.execute(query)
            if result.scalars().first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Error to try process this task"
                )

        new_task: Task = Task(
            title=task.title,
            user_id=task.user_id,
            created_at=datetime.datetime.now()
        )
        db.add(new_task)
        await db.commit()
        return new_task
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[TaskSchema])
async def get_all_tasks(db: AsyncSession = Depends(create_session)) -> Sequence[TaskSchema]:
    try:
        async with db as session:
            query = select(Task)
            response = await session.execute(query)
            return response.scalars().all()
    except Exception as e:
        print({e})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskSchema)
async def get_task(task_id: int, db: AsyncSession = Depends(create_session)) -> TaskSchema:
    try:
        async with db as session:
            query = select(Task).filter(task_id == Task.id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            if task:
                return task
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
