"""
Routes package - Export de tous les routers
"""
from app.routes.auth import router as auth_router
from app.routes.categories import router as categories_router
from app.routes.bank_accounts import router as bank_accounts_router
from app.routes.envelopes import router as envelopes_router
from app.routes.transactions import router as transactions_router

__all__ = [
    "auth_router",
    "categories_router",
    "bank_accounts_router",
    "envelopes_router",
    "transactions_router",
]
