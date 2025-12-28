"""
Routes pour servir les templates HTML du frontend
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Configuration du moteur de templates
templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Page d'accueil - redirige vers le dashboard (auth temporairement désactivée)"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Page de connexion"""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Page d'inscription"""
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Page du tableau de bord"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/transactions", response_class=HTMLResponse)
async def transactions_page(request: Request):
    """Page des transactions"""
    return templates.TemplateResponse("transactions.html", {"request": request})


@router.get("/envelopes", response_class=HTMLResponse)
async def envelopes_page(request: Request):
    """Page des enveloppes"""
    return templates.TemplateResponse("envelopes_htmx.html", {"request": request})


@router.get("/accounts", response_class=HTMLResponse)
async def accounts_page(request: Request):
    """Page des comptes bancaires"""
    return templates.TemplateResponse("accounts.html", {"request": request})


@router.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    """Page des catégories"""
    return templates.TemplateResponse("categories.html", {"request": request})


@router.get("/wish-lists", response_class=HTMLResponse)
async def wish_lists_page(request: Request):
    """Page des listes de souhaits"""
    return templates.TemplateResponse("wish_lists.html", {"request": request})
