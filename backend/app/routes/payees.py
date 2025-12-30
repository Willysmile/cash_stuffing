"""
Routes API pour la gestion des bénéficiaires
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models.payee import Payee
from app.models.user import User
from app.schemas.payee import PayeeCreate, PayeeUpdate, PayeeRead
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/payees", tags=["Payees"])


@router.get("", response_model=List[PayeeRead])
async def get_payees(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste tous les bénéficiaires de l'utilisateur"""
    result = await db.execute(
        select(Payee)
        .where(Payee.user_id == current_user.id)
        .order_by(Payee.name)
    )
    payees = result.scalars().all()
    return payees


@router.post("", response_model=PayeeRead, status_code=status.HTTP_201_CREATED)
async def create_payee(
    payee_data: PayeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau bénéficiaire"""
    # Vérifier si le nom existe déjà
    result = await db.execute(
        select(Payee).where(
            and_(
                Payee.user_id == current_user.id,
                Payee.name == payee_data.name
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A payee with this name already exists"
        )
    
    payee = Payee(user_id=current_user.id, **payee_data.model_dump())
    db.add(payee)
    await db.commit()
    await db.refresh(payee)
    return payee


@router.put("/{payee_id:int}", response_model=PayeeRead)
async def update_payee(
    payee_id: int,
    payee_data: PayeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un bénéficiaire"""
    result = await db.execute(
        select(Payee).where(
            and_(
                Payee.id == payee_id,
                Payee.user_id == current_user.id
            )
        )
    )
    payee = result.scalar_one_or_none()
    
    if not payee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payee not found"
        )
    
    update_data = {k: v for k, v in payee_data.model_dump().items() if v is not None}
    for key, value in update_data.items():
        setattr(payee, key, value)
    
    await db.commit()
    await db.refresh(payee)
    return payee


@router.delete("/{payee_id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payee(
    payee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime un bénéficiaire"""
    result = await db.execute(
        select(Payee).where(
            and_(
                Payee.id == payee_id,
                Payee.user_id == current_user.id
            )
        )
    )
    payee = result.scalar_one_or_none()
    
    if not payee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payee not found"
        )
    
    await db.delete(payee)
    await db.commit()
