"""
Routes package - Export de tous les routers
"""
from app.routes.auth import router as auth_router

__all__ = [
    "auth_router",
]
