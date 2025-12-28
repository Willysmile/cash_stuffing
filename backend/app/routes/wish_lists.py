"""
Routes API pour les listes de souhaits (wish lists) et leurs articles
"""
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.wish_list import WishList
from app.models.wish_list_item import WishListItem
from app.models.user import User
from app.schemas.wish_list import (
    WishListCreate, WishListUpdate, WishListRead, WishListWithItems,
    WishListItemCreate, WishListItemUpdate, WishListItemRead,
    WishListType, WishListStatus, ItemStatus
)
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/wish_lists", tags=["wish_lists"])


@router.get("", response_model=List[WishListRead])
async def list_wish_lists(
    list_type: Optional[WishListType] = Query(None, description="Filtrer par type"),
    status: Optional[WishListStatus] = Query(None, description="Filtrer par statut"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste toutes les wish lists de l'utilisateur."""
    query = select(WishList).where(WishList.user_id == current_user.id)
    
    if list_type is not None:
        query = query.where(WishList.list_type == list_type)
    if status is not None:
        query = query.where(WishList.status == status)
    
    query = query.order_by(WishList.created_at.desc())
    
    result = await db.execute(query)
    wish_lists = result.scalars().all()
    
    return wish_lists


@router.post("", response_model=WishListRead, status_code=status.HTTP_201_CREATED)
async def create_wish_list(
    wish_list_data: WishListCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle wish list."""
    wish_list = WishList(
        user_id=current_user.id,
        **wish_list_data.model_dump()
    )
    
    db.add(wish_list)
    await db.commit()
    await db.refresh(wish_list)
    
    return wish_list


@router.get("/{wish_list_id}", response_model=WishListWithItems)
async def get_wish_list(
    wish_list_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère une wish list avec tous ses articles."""
    result = await db.execute(
        select(WishList)
        .options(selectinload(WishList.items))
        .where(
            and_(
                WishList.id == wish_list_id,
                WishList.user_id == current_user.id
            )
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish list not found"
        )
    
    # Calculer les statistiques
    total_cost = sum(item.price * item.quantity for item in wish_list.items)
    purchased_cost = sum(
        item.price * item.quantity 
        for item in wish_list.items 
        if item.status == ItemStatus.PURCHASED
    )
    remaining_cost = total_cost - purchased_cost
    
    # Convertir en dict et ajouter les stats
    wish_list_dict = {
        **{c.name: getattr(wish_list, c.name) for c in wish_list.__table__.columns},
        "items": wish_list.items,
        "total_cost": total_cost,
        "purchased_cost": purchased_cost,
        "remaining_cost": remaining_cost
    }
    
    return wish_list_dict


@router.put("/{wish_list_id}", response_model=WishListRead)
async def update_wish_list(
    wish_list_id: int,
    wish_list_data: WishListUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour une wish list."""
    result = await db.execute(
        select(WishList).where(
            and_(
                WishList.id == wish_list_id,
                WishList.user_id == current_user.id
            )
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish list not found"
        )
    
    # Appliquer les modifications
    update_data = wish_list_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(wish_list, key, value)
    
    await db.commit()
    await db.refresh(wish_list)
    
    return wish_list


@router.delete("/{wish_list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wish_list(
    wish_list_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime une wish list et tous ses articles."""
    result = await db.execute(
        select(WishList).where(
            and_(
                WishList.id == wish_list_id,
                WishList.user_id == current_user.id
            )
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish list not found"
        )
    
    await db.delete(wish_list)
    await db.commit()
    
    return None


# === Routes pour les articles (items) ===

@router.post("/{wish_list_id}/items", response_model=WishListItemRead, status_code=status.HTTP_201_CREATED)
async def create_wish_list_item(
    wish_list_id: int,
    item_data: WishListItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ajoute un article à une wish list."""
    # Vérifier que la wish list existe et appartient à l'utilisateur
    result = await db.execute(
        select(WishList).where(
            and_(
                WishList.id == wish_list_id,
                WishList.user_id == current_user.id
            )
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish list not found"
        )
    
    # Vérifier que le wish_list_id dans item_data correspond
    if item_data.wish_list_id != wish_list_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wish list ID mismatch"
        )
    
    item = WishListItem(**item_data.model_dump())
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item


@router.get("/{wish_list_id}/items", response_model=List[WishListItemRead])
async def list_wish_list_items(
    wish_list_id: int,
    item_status: Optional[ItemStatus] = Query(None, description="Filtrer par statut"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste tous les articles d'une wish list."""
    # Vérifier que la wish list existe et appartient à l'utilisateur
    result = await db.execute(
        select(WishList).where(
            and_(
                WishList.id == wish_list_id,
                WishList.user_id == current_user.id
            )
        )
    )
    wish_list = result.scalar_one_or_none()
    
    if not wish_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wish list not found"
        )
    
    query = select(WishListItem).where(WishListItem.wish_list_id == wish_list_id)
    
    if item_status is not None:
        query = query.where(WishListItem.status == item_status)
    
    query = query.order_by(WishListItem.sort_order, WishListItem.created_at)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return items


@router.put("/items/{item_id}", response_model=WishListItemRead)
async def update_wish_list_item(
    item_id: int,
    item_data: WishListItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un article d'une wish list."""
    # Récupérer l'article avec sa wish list
    result = await db.execute(
        select(WishListItem)
        .join(WishList)
        .where(
            and_(
                WishListItem.id == item_id,
                WishList.user_id == current_user.id
            )
        )
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    # Appliquer les modifications
    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    await db.commit()
    await db.refresh(item)
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wish_list_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime un article d'une wish list."""
    # Récupérer l'article avec sa wish list
    result = await db.execute(
        select(WishListItem)
        .join(WishList)
        .where(
            and_(
                WishListItem.id == item_id,
                WishList.user_id == current_user.id
            )
        )
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    await db.delete(item)
    await db.commit()
    
    return None


@router.post("/items/{item_id}/mark-purchased", response_model=WishListItemRead)
async def mark_item_as_purchased(
    item_id: int,
    purchased_date: Optional[str] = Query(None, description="Date d'achat (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Marque un article comme acheté."""
    from datetime import date
    
    # Récupérer l'article
    result = await db.execute(
        select(WishListItem)
        .join(WishList)
        .where(
            and_(
                WishListItem.id == item_id,
                WishList.user_id == current_user.id
            )
        )
    )
    item = result.scalar_one_or_none()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    item.status = ItemStatus.PURCHASED
    item.purchased_date = date.fromisoformat(purchased_date) if purchased_date else date.today()
    
    await db.commit()
    await db.refresh(item)
    
    return item
