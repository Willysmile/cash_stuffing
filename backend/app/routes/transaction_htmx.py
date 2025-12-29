"""
Routes HTMX pour les transactions
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime, date
from pathlib import Path

from app.database import get_db
from app.models import User, Transaction, Envelope, BankAccount, Category
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.utils.dependencies import get_current_user

# Templates
templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/transactions/htmx", tags=["transactions-htmx"])


@router.get("", response_class=HTMLResponse)
async def list_transactions_htmx(
    bank_account_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    transaction_type: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour lister les transactions avec filtres.
    Retourne le tableau des transactions mis à jour.
    """
    # Construire la query avec filtres
    query = select(Transaction).where(
        Transaction.user_id == current_user.id
    )
    
    if bank_account_id:
        query = query.where(Transaction.bank_account_id == bank_account_id)
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if transaction_type:
        query = query.where(Transaction.type == transaction_type)
    if date_from:
        query = query.where(Transaction.date >= date_from)
    if date_to:
        query = query.where(Transaction.date <= date_to)
    
    query = query.order_by(Transaction.date.desc())
    result = await db.execute(query.options(
        selectinload(Transaction.category),
        selectinload(Transaction.bank_account),
        selectinload(Transaction.envelope)
    ))
    transactions = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/transactions_table.html",
        {
            "request": request,
            "transactions": transactions
        }
    )


@router.post("", response_class=HTMLResponse)
async def create_transaction_htmx(
    amount: float,
    type: str,
    description: str,
    category_id: int,
    bank_account_id: int,
    envelope_id: Optional[int] = None,
    transaction_date: Optional[str] = None,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour créer une transaction.
    Retourne le tableau mise à jour ou une erreur.
    """
    try:
        if not transaction_date:
            transaction_date = datetime.now().date()
        else:
            transaction_date = datetime.fromisoformat(transaction_date).date()
        
        # Créer la transaction
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            type=type,
            description=description,
            category_id=category_id,
            bank_account_id=bank_account_id,
            envelope_id=envelope_id,
            date=transaction_date
        )
        
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        
        # Recharger la liste
        result = await db.execute(
            select(Transaction)
            .where(Transaction.user_id == current_user.id)
            .order_by(Transaction.date.desc())
            .options(
                selectinload(Transaction.category),
                selectinload(Transaction.bank_account),
                selectinload(Transaction.envelope)
            )
        )
        transactions = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/transactions_table.html",
            {
                "request": request,
                "transactions": transactions
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{transaction_id}/detail", response_class=HTMLResponse)
async def transaction_detail_modal(
    transaction_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour afficher le détail d'une transaction en modal.
    """
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
        .options(
            selectinload(Transaction.category),
            selectinload(Transaction.bank_account),
            selectinload(Transaction.envelope)
        )
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return templates.TemplateResponse(
        "components/transaction_detail_modal.html",
        {
            "request": request,
            "transaction": transaction
        }
    )


@router.get("/{transaction_id}/edit", response_class=HTMLResponse)
async def transaction_edit_modal(
    transaction_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour afficher le formulaire d'édition d'une transaction.
    """
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Récupérer les options
    categories = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    categories = categories.scalars().all()
    
    bank_accounts = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    bank_accounts = bank_accounts.scalars().all()
    
    envelopes = await db.execute(
        select(Envelope).where(Envelope.user_id == current_user.id)
    )
    envelopes = envelopes.scalars().all()
    
    return templates.TemplateResponse(
        "components/transaction_edit_modal.html",
        {
            "request": request,
            "transaction": transaction,
            "categories": categories,
            "bank_accounts": bank_accounts,
            "envelopes": envelopes
        }
    )


@router.delete("/{transaction_id}", response_class=HTMLResponse)
async def delete_transaction_htmx(
    transaction_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint HTMX pour supprimer une transaction.
    Retourne le tableau mise à jour.
    """
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id
        )
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    await db.delete(transaction)
    await db.commit()
    
    # Recharger la liste
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.date.desc())
        .options(
            selectinload(Transaction.category),
            selectinload(Transaction.bank_account),
            selectinload(Transaction.envelope)
        )
    )
    transactions = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/transactions_table.html",
        {
            "request": request,
            "transactions": transactions
        }
    )
