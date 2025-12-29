"""
Routes HTMX pour les listes de souhaits
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pathlib import Path

from app.database import get_db
from app.models import User, WishList, WishListItem
from app.utils.dependencies import get_current_user

templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/wish-lists/htmx", tags=["wish-lists-htmx"])


@router.get("/create", response_class=HTMLResponse)
async def create_wish_list_modal(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal pour créer une nouvelle liste de souhaits."""
    return templates.TemplateResponse(
        "components/wish_list_create_modal.html",
        {"request": request}
    )


@router.post("", response_class=HTMLResponse)
async def create_wish_list_htmx(
    name: str,
    description: str = "",
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle liste de souhaits."""
    try:
        wish_list = WishList(
            user_id=current_user.id,
            name=name,
            description=description
        )
        db.add(wish_list)
        await db.commit()
        
        result = await db.execute(
            select(WishList)
            .where(WishList.user_id == current_user.id)
            .options(selectinload(WishList.items))
        )
        wish_lists = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/wish_lists_table.html",
            {"request": request, "wish_lists": wish_lists}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_class=HTMLResponse)
async def list_wish_lists_htmx(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les listes de souhaits de l'utilisateur."""
    result = await db.execute(
        select(WishList)
        .where(WishList.user_id == current_user.id)
        .options(selectinload(WishList.items))
    )
    wish_lists = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/wish_lists_table.html",
        {"request": request, "wish_lists": wish_lists}
    )


@router.get("/{list_id}/detail", response_class=HTMLResponse)
async def wish_list_detail_modal(
    list_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal de détail d'une liste de souhaits avec ses items."""
    result = await db.execute(
        select(WishList)
        .where(WishList.id == list_id, WishList.user_id == current_user.id)
        .options(selectinload(WishList.items))
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(status_code=404, detail="Wish list not found")
    
    return templates.TemplateResponse(
        "components/wish_list_detail_modal.html",
        {"request": request, "wish_list": wish_list}
    )


@router.get("/{list_id}/edit", response_class=HTMLResponse)
async def wish_list_edit_modal(
    list_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal d'édition d'une liste de souhaits."""
    result = await db.execute(
        select(WishList).where(
            WishList.id == list_id,
            WishList.user_id == current_user.id
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(status_code=404, detail="Wish list not found")
    
    return templates.TemplateResponse(
        "components/wish_list_edit_modal.html",
        {"request": request, "wish_list": wish_list}
    )


@router.put("/{list_id}", response_class=HTMLResponse)
async def update_wish_list_htmx(
    list_id: int,
    name: str,
    description: str = "",
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour une liste de souhaits."""
    result = await db.execute(
        select(WishList).where(
            WishList.id == list_id,
            WishList.user_id == current_user.id
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(status_code=404, detail="Wish list not found")
    
    wish_list.name = name
    wish_list.description = description
    await db.commit()
    
    result = await db.execute(
        select(WishList)
        .where(WishList.user_id == current_user.id)
        .options(selectinload(WishList.items))
    )
    wish_lists = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/wish_lists_table.html",
        {"request": request, "wish_lists": wish_lists}
    )


@router.delete("/{list_id}", response_class=HTMLResponse)
async def delete_wish_list_htmx(
    list_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime une liste de souhaits."""
    result = await db.execute(
        select(WishList).where(
            WishList.id == list_id,
            WishList.user_id == current_user.id
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(status_code=404, detail="Wish list not found")
    
    await db.delete(wish_list)
    await db.commit()
    
    result = await db.execute(
        select(WishList)
        .where(WishList.user_id == current_user.id)
        .options(selectinload(WishList.items))
    )
    wish_lists = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/wish_lists_table.html",
        {"request": request, "wish_lists": wish_lists}
    )


@router.patch("/{list_id}/items/{item_id}/purchase", response_class=HTMLResponse)
async def toggle_item_purchase_htmx(
    list_id: int,
    item_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Bascule le statut d'achat d'un item."""
    result = await db.execute(
        select(WishListItem).where(
            WishListItem.id == item_id,
            WishListItem.wish_list_id == list_id
        ).options(
            selectinload(WishListItem.wish_list).selectinload(WishList.user)
        )
    )
    item = result.scalar_one_or_none()
    
    if not item or item.wish_list.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.is_purchased = not item.is_purchased
    await db.commit()
    
    result = await db.execute(
        select(WishList)
        .where(WishList.id == list_id, WishList.user_id == current_user.id)
        .options(selectinload(WishList.items))
    )
    wish_list = result.scalar_one_or_none()
    
    return templates.TemplateResponse(
        "components/wish_list_detail_modal.html",
        {"request": request, "wish_list": wish_list}
    )
