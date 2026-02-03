from fastapi import APIRouter

from app.api.routes import admin, auth, links

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(links.router, tags=["links"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
