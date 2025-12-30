"""
Routes HTMX pour les catégories
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pathlib import Path

from app.database import get_db
from app.models import User, Category
from app.utils.dependencies import get_current_user

templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/categories/htmx", tags=["categories-htmx"])


@router.get("/create", response_class=HTMLResponse)
async def create_category_modal(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal pour créer une nouvelle catégorie."""
    return templates.TemplateResponse(
        "components/category_create_modal.html",
        {"request": request}
    )


@router.get("", response_class=HTMLResponse)
async def list_categories_htmx(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les catégories de l'utilisateur."""
    result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/categories_table.html",
        {"request": request, "categories": categories}
    )


@router.post("", response_class=HTMLResponse)
async def create_category_htmx(
    name: str,
    color: str = "#3273dc",
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle catégorie."""
    try:
        category = Category(user_id=current_user.id, name=name, color=color)
        db.add(category)
        await db.commit()
        
        result = await db.execute(
            select(Category).where(Category.user_id == current_user.id)
        )
        categories = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/categories_table.html",
            {"request": request, "categories": categories}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_class=HTMLResponse)
async def create_category_htmx(
    name: str,
    color: str = "#3273dc",
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle catégorie."""
    try:
        category = Category(user_id=current_user.id, name=name, color=color)
        db.add(category)
        await db.commit()
        
        result = await db.execute(
            select(Category).where(Category.user_id == current_user.id)
        )
        categories = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/categories_table.html",
            {"request": request, "categories": categories}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{category_id:int}/edit", response_class=HTMLResponse)
async def category_edit_modal(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal d'édition d'une catégorie."""
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == current_user.id
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return templates.TemplateResponse(
        "components/category_edit_modal.html",
        {"request": request, "category": category}
    )


@router.put("/{category_id:int}", response_class=HTMLResponse)
async def update_category_htmx(
    category_id: int,
    name: str,
    color: str = "#3273dc",
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour une catégorie."""
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == current_user.id
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.name = name
    category.color = color
    await db.commit()
    
    result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/categories_table.html",
        {"request": request, "categories": categories}
    )


@router.delete("/{category_id:int}", response_class=HTMLResponse)
async def delete_category_htmx(
    category_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime une catégorie."""
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == current_user.id
        )
    )
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.delete(category)
    await db.commit()
    
    result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/categories_table.html",
        {"request": request, "categories": categories}
    )
