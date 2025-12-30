from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from pathlib import Path

# Import des routes
from app.routes import (
    auth_router, 
    categories_router, 
    bank_accounts_router, 
    envelopes_router, 
    transactions_router, 
    wish_lists_router,
    payees_router
)
from app.routes.envelope_htmx import router as envelope_htmx_router
from app.routes.transaction_htmx import router as transaction_htmx_router
from app.routes.category_htmx import router as category_htmx_router
from app.routes.bank_account_htmx import router as bank_account_htmx_router
from app.routes.wish_list_htmx import router as wish_list_htmx_router
from app.routes.dashboard_htmx import router as dashboard_htmx_router
from app.routes.frontend import router as frontend_router

# Configuration des chemins
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    # Startup
    print("🚀 Démarrage de l'application Cash Stuffing")
    # Ici: initialisation de la base de données, connexions, etc.
    
    yield
    
    # Shutdown
    print("👋 Arrêt de l'application")
    # Ici: fermeture des connexions, nettoyage, etc.

# Création de l'application FastAPI
app = FastAPI(
    title="Cash Stuffing API",
    description="API pour la gestion de budget par enveloppes",
    version="1.0.0",
    lifespan=lifespan
)

# Gestionnaire d'erreurs de validation personnalisé
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gère les erreurs de validation et affiche des détails"""
    print(f"❌ Erreur de validation sur {request.method} {request.url.path}")
    print(f"Détails: {exc.errors()}")
    print(f"Body reçu: {exc.body}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montage des fichiers statiques
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR / "static")),
    name="static"
)

# Configuration des templates Jinja2
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Ajout de filtres personnalisés pour Jinja2
def format_currency(value):
    """Filtre pour formater les montants en euros"""
    return f"{value:,.2f} €".replace(",", " ").replace(".", ",")

templates.env.filters["currency"] = format_currency

# === Routes de l'API ===
app.include_router(auth_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(bank_accounts_router, prefix="/api")
app.include_router(envelopes_router, prefix="/api")
app.include_router(transactions_router, prefix="/api")
app.include_router(wish_lists_router, prefix="/api")
app.include_router(payees_router, prefix="/api")

# === Routes HTMX (montées après pour éviter les conflits) ===
app.include_router(envelope_htmx_router, prefix="/api")
app.include_router(transaction_htmx_router, prefix="/api")
app.include_router(category_htmx_router, prefix="/api")
app.include_router(bank_account_htmx_router, prefix="/api")
app.include_router(wish_list_htmx_router, prefix="/api")
app.include_router(dashboard_htmx_router, prefix="/api")

# === Routes du frontend ===
app.include_router(frontend_router)

# Route de santé
@app.get("/health")
async def health():
    """Endpoint de health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
