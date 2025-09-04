from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import users


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    return app

app = create_app()
