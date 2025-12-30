"""
Routes HTMX pour les enveloppes budgétaires
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal
from datetime import datetime
from pathlib import Path

from app.database import get_db
from app.models import User, Envelope, Category, BankAccount, EnvelopeHistory
from app.utils.dependencies import get_current_user

# Templates
templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/envelopes/htmx", tags=["envelopes-htmx"])


@router.get("", response_class=HTMLResponse)
async def list_envelopes_htmx(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les enveloppes de l'utilisateur sous forme de cards."""
    result = await db.execute(
        select(Envelope)
        .where(Envelope.user_id == current_user.id)
        .options(
            selectinload(Envelope.category),
            selectinload(Envelope.bank_account)
        )
    )
    envelopes = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/envelope_cards.html",
        {"request": request, "envelopes": envelopes}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_envelope_modal(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal pour créer une nouvelle enveloppe."""
    # Récupérer les options pour les selects
    categories_result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = categories_result.scalars().all()
    
    bank_accounts_result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    bank_accounts = bank_accounts_result.scalars().all()
    
    return templates.TemplateResponse(
        "components/envelope_create_modal.html",
        {
            "request": request,
            "categories": categories,
            "bank_accounts": bank_accounts
        }
    )


@router.post("", response_class=HTMLResponse)
async def create_envelope_htmx(
    name: str,
    target_amount: float,
    category_id: int,
    bank_account_id: int = None,
    description: str = None,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle enveloppe."""
    try:
        envelope = Envelope(
            user_id=current_user.id,
            name=name,
            target_amount=Decimal(str(target_amount)),
            category_id=category_id,
            bank_account_id=bank_account_id,
            description=description
        )
        db.add(envelope)
        await db.commit()
        
        result = await db.execute(
            select(Envelope)
            .where(Envelope.user_id == current_user.id)
            .options(
                selectinload(Envelope.category),
                selectinload(Envelope.bank_account)
            )
        )
        envelopes = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/envelope_cards.html",
            {"request": request, "envelopes": envelopes}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{envelope_id:int}/adjust", response_class=HTMLResponse)
async def adjust_envelope_htmx(
    envelope_id: int,
    amount: float,
    direction: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour ajuster le solde d'une enveloppe.
    Retourne le composant envelope_card mis à jour.
    """
    try:
        adjustment = Decimal(str(amount)) * Decimal(direction)
    except:
        raise HTTPException(status_code=400, detail="Montant invalide")
    
    # Récupérer l'enveloppe avec ses relations
    result = await db.execute(
        select(Envelope)
        .where(
            Envelope.id == envelope_id,
            Envelope.user_id == current_user.id
        )
        .options(
            selectinload(Envelope.category),
            selectinload(Envelope.bank_account)
        )
    )
    envelope = result.scalar_one_or_none()
    
    if not envelope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found"
        )
    
    # Vérifier qu'on a assez d'argent pour retirer
    if adjustment < 0 and envelope.current_balance + adjustment < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solde insuffisant (actuellement: {envelope.current_balance}€)"
        )
    
    # Effectuer l'ajustement
    envelope.current_balance += adjustment
    
    # Créer un historique
    history = EnvelopeHistory(
        envelope_id=envelope_id,
        amount=adjustment,
        balance_after=envelope.current_balance,
        created_at=datetime.utcnow()
    )
    db.add(history)
    await db.commit()
    await db.refresh(envelope)
    
    # Rendre le composant mis à jour
    return templates.TemplateResponse(
        "components/envelope_cards.html",
        {
            "request": request,
            "envelopes": [envelope]
        }
    )


@router.get("/{envelope_id:int}/detail", response_class=HTMLResponse)
async def envelope_detail_modal(
    envelope_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour afficher le détail d'une enveloppe en modal.
    """
    result = await db.execute(
        select(Envelope)
        .where(
            Envelope.id == envelope_id,
            Envelope.user_id == current_user.id
        )
        .options(
            selectinload(Envelope.category),
            selectinload(Envelope.bank_account),
            selectinload(Envelope.transactions)
        )
    )
    envelope = result.scalar_one_or_none()
    
    if not envelope:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Envelope not found"
        )
    
    # Récupérer l'historique
    history_result = await db.execute(
        select(EnvelopeHistory)
        .where(EnvelopeHistory.envelope_id == envelope_id)
        .order_by(EnvelopeHistory.created_at.desc())
        .limit(10)
    )
    history = history_result.scalars().all()
    
    return templates.TemplateResponse(
        "components/envelope_detail_modal.html",
        {
            "request": request,
            "envelope": envelope,
            "history": history
        }
    )


@router.get("/{envelope_id:int}/edit", response_class=HTMLResponse)
async def envelope_edit_modal(
    envelope_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour afficher le formulaire d'édition d'une enveloppe.
    """
    result = await db.execute(
        select(Envelope)
        .where(
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
    
    # Récupérer les options pour les selects
    categories_result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = categories_result.scalars().all()
    
    bank_accounts_result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    bank_accounts = bank_accounts_result.scalars().all()
    
    return templates.TemplateResponse(
        "components/envelope_edit_modal.html",
        {
            "request": request,
            "envelope": envelope,
            "categories": categories,
            "bank_accounts": bank_accounts
        }
    )
