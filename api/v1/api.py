from fastapi import APIRouter
from .routes import user_route
from .routes import task_route


api_router: APIRouter = APIRouter()
api_router.include_router(user_route.router, prefix="/users", tags=["User"])
api_router.include_router(task_route.router, prefix="/tasks", tags=["Task"])
