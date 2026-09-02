from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from tasks.routes import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(
    lifespan=lifespan,
    title="Task Management API",
    description="a simple API for managing tasks ",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://127.0.0.1:8000", "description": "Development Server"},
    ],
    openapi_tags=[
        {
            "name": "tasks",
            "description": "Operations with tasks",
        }
    ]
)

app.include_router(tasks_router, prefix="/tasks")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)