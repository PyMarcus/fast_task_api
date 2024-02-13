from fastapi import FastAPI
from api.v1.api import api_router


app: FastAPI = FastAPI(
    title="Get users and tasks!",
    description="An API to recover users and yours tasks!")

app.include_router(api_router, prefix="/api/v1")


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=True
    )
