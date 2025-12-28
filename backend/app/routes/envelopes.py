"""
Routes API pour les enveloppes budgétaires
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from decimal import Decimal
from pathlib import Path

from app.database import get_db
from app.models import User, Envelope, BankAccount, Category
from app.schemas.envelope import (
    EnvelopeCreate,
    EnvelopeUpdate,
    EnvelopeRead,
    EnvelopeReallocate,
    EnvelopeWithStats
)
from app.utils.dependencies import get_current_user

# Templates pour rendu HTML
templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


router = APIRouter(prefix="/envelopes", tags=["envelopes"])


@router.get("", response_model=List[EnvelopeRead])
async def list_envelopes(
    bank_account_id: Optional[int] = Query(None, description="Filtrer par compte bancaire"),
    category_id: Optional[int] = Query(None, description="Filtrer par catégorie"),
    is_active: Optional[bool] = Query(None, description="Filtrer par statut actif"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Liste toutes les enveloppes de l'utilisateur
    
    Filtres disponibles :
    - **bank_account_id**: ID du compte bancaire
    - **category_id**: ID de la catégorie
    - **is_active**: Actif ou inactif
    """
    query = select(Envelope).where(Envelope.user_id == current_user.id)
    
    # Appliquer les filtres
    if bank_account_id is not None:
        query = query.where(Envelope.bank_account_id == bank_account_id)
    if category_id is not None:
        query = query.where(Envelope.category_id == category_id)
    if is_active is not None:
        query = query.where(Envelope.is_active == is_active)
    
    # Tri par nom
    query = query.order_by(Envelope.name)
    
    result = await db.execute(query)
    envelopes = result.scalars().all()
    
    return envelopes


@router.get("/html", response_class=HTMLResponse)
async def get_envelopes_html(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
    bank_account_id: Optional[int] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = None
):
    """Retourne les enveloppes sous forme de fragment HTML pour HTMX"""
    # Récupérer les enveloppes avec jointures
    query = (
        select(Envelope)
        .options(
            selectinload(Envelope.category),
            selectinload(Envelope.bank_account)
        )
        .where(Envelope.user_id == current_user.id)
    )
    
    # Appliquer les filtres
    if bank_account_id is not None:
        query = query.where(Envelope.bank_account_id == bank_account_id)
    if category_id is not None:
        query = query.where(Envelope.category_id == category_id)
    if is_active is not None:
        query = query.where(Envelope.is_active == is_active)
    
    # Tri par nom
    query = query.order_by(Envelope.name)
    
    result = await db.execute(query)
    envelopes = result.scalars().all()
    
    # Rendu du template
    templates = Jinja2Templates(directory=templates_dir)
    return templates.TemplateResponse(
        "components/envelope_cards.html",
        {"request": request, "envelopes": envelopes}
    )


@router.get("/{envelope_id}", response_model=EnvelopeRead)
async def get_envelope(
    envelope_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Récupère une enveloppe spécifique
    """
    result = await db.execute(
        select(Envelope).where(
            Envelope.id == envelope_id,
            Envelope.user_id == current_user.id
        )
    )
    envelope = result.scalar_one_or_none()
    
    if not envelope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found"
        )
    
    return envelope


@router.post("", response_model=EnvelopeRead, status_code=status.HTTP_201_CREATED)
async def create_envelope(
    envelope_data: EnvelopeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Crée une nouvelle enveloppe budgétaire
    
    L'enveloppe doit être liée à un compte bancaire existant.
    La catégorie est optionnelle.
    Le solde initial est à 0.
    """
    # Vérifier que le compte bancaire existe et appartient à l'utilisateur
    result = await db.execute(
        select(BankAccount).where(
            BankAccount.id == envelope_data.bank_account_id,
            BankAccount.user_id == current_user.id
        )
    )
    bank_account = result.scalar_one_or_none()
    
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Vérifier la catégorie si fournie
    if envelope_data.category_id:
        result = await db.execute(
            select(Category).where(
                Category.id == envelope_data.category_id,
                Category.user_id == current_user.id
            )
        )
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Créer l'enveloppe
    envelope = Envelope(
        user_id=current_user.id,
        **envelope_data.model_dump()
    )
    
    db.add(envelope)
    await db.commit()
    await db.refresh(envelope)
    
    return envelope


@router.put("/{envelope_id}", response_model=EnvelopeRead)
async def update_envelope(
    envelope_id: int,
    envelope_data: EnvelopeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Met à jour une enveloppe existante
    
    Seuls les champs fournis sont modifiés.
    Le solde actuel ne peut pas être modifié via cette route.
    """
    # Récupérer l'enveloppe
    result = await db.execute(
        select(Envelope).where(
            Envelope.id == envelope_id,
            Envelope.user_id == current_user.id
        )
    )
    envelope = result.scalar_one_or_none()
    
    if not envelope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found"
        )
    
    # Vérifier le compte bancaire si modifié
    if envelope_data.bank_account_id:
        result = await db.execute(
            select(BankAccount).where(
                BankAccount.id == envelope_data.bank_account_id,
                BankAccount.user_id == current_user.id
            )
        )
        bank_account = result.scalar_one_or_none()
        
        if not bank_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
    
    # Vérifier la catégorie si modifiée
    if envelope_data.category_id:
        result = await db.execute(
            select(Category).where(
                Category.id == envelope_data.category_id,
                Category.user_id == current_user.id
            )
        )
        category = result.scalar_one_or_none()
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Mettre à jour les champs
    update_data = envelope_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(envelope, field, value)
    
    await db.commit()
    await db.refresh(envelope)
    
    return envelope


@router.delete("/{envelope_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_envelope(
    envelope_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Supprime une enveloppe
    
    La suppression échoue si des transactions sont liées à cette enveloppe.
    """
    # Récupérer l'enveloppe
    result = await db.execute(
        select(Envelope).where(
            Envelope.id == envelope_id,
            Envelope.user_id == current_user.id
        )
    )
    envelope = result.scalar_one_or_none()
    
    if not envelope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found"
        )
    
    # Supprimer l'enveloppe
    # Les contraintes FK empêcheront la suppression si des transactions existent
    try:
        await db.delete(envelope)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete envelope with existing transactions"
        )
    
    return None


@router.post("/{envelope_id}/reallocate", response_model=EnvelopeRead)
async def reallocate_funds(
    envelope_id: int,
    reallocation: EnvelopeReallocate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Transfère de l'argent entre deux enveloppes
    
    - Retire le montant de l'enveloppe source
    - Ajoute le montant à l'enveloppe destination
    - Les deux enveloppes doivent appartenir à l'utilisateur
    """
    # Vérifier que les IDs sont différents
    if reallocation.from_envelope_id == reallocation.to_envelope_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination envelopes must be different"
        )
    
    # Récupérer les deux enveloppes
    result = await db.execute(
        select(Envelope).where(
            Envelope.id.in_([reallocation.from_envelope_id, reallocation.to_envelope_id]),
            Envelope.user_id == current_user.id
        )
    )
    envelopes = result.scalars().all()
    
    if len(envelopes) != 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or both envelopes not found"
        )
    
    # Identifier source et destination
    from_envelope = next((e for e in envelopes if e.id == reallocation.from_envelope_id), None)
    to_envelope = next((e for e in envelopes if e.id == reallocation.to_envelope_id), None)
    
    # Vérifier que l'enveloppe source a assez de fonds
    if from_envelope.current_balance < reallocation.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds in source envelope. Available: {from_envelope.current_balance}"
        )
    
    # Effectuer le transfert
    from_envelope.current_balance -= reallocation.amount
    to_envelope.current_balance += reallocation.amount
    
    await db.commit()
    await db.refresh(from_envelope)
    
    # Retourner l'enveloppe source mise à jour
    return from_envelope
