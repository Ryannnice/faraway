from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.responses import success_response
from app.db.base import Base
from app.db.session import engine
from app.modules.ai.router import router as ai_router
from app.modules.auth.router import router as auth_router
from app.modules.matches.router import router as matches_router
from app.modules.media.router import router as media_router
from app.modules.notifications.router import router as notifications_router
from app.modules.users.router import router as users_router

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings.resolved_local_media_dir.mkdir(parents=True, exist_ok=True)
if settings.auto_create_schema:
    Base.metadata.create_all(bind=engine)

app.mount(settings.media_url_prefix, StaticFiles(directory=settings.resolved_local_media_dir), name="media")

api_router = APIRouter(prefix=settings.api_prefix)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(ai_router)
api_router.include_router(matches_router)
api_router.include_router(media_router)
api_router.include_router(notifications_router)


@app.get("/healthz")
async def healthz() -> dict:
    return success_response({"status": "ok"})


app.include_router(api_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": str(exc.detail), "data": {}})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": "validation error", "data": {"errors": exc.errors()}},
    )
