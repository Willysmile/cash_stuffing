"""
Routes API pour les transactions
"""
from typing import List, Optional
from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.transaction import Transaction
from app.models.bank_account import BankAccount
from app.models.envelope import Envelope
from app.models.category import Category
from app.models.user import User
from app.schemas.transaction import (
    TransactionCreate, TransactionUpdate, TransactionRead,
    TransactionType, TransactionPriority
)
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=List[TransactionRead])
async def list_transactions(
    bank_account_id: Optional[int] = Query(None, description="Filtrer par compte bancaire"),
    envelope_id: Optional[int] = Query(None, description="Filtrer par enveloppe"),
    category_id: Optional[int] = Query(None, description="Filtrer par catégorie"),
    transaction_type: Optional[TransactionType] = Query(None, description="Filtrer par type"),
    priority: Optional[TransactionPriority] = Query(None, description="Filtrer par priorité"),
    date_from: Optional[date] = Query(None, description="Date de début"),
    date_to: Optional[date] = Query(None, description="Date de fin"),
    min_amount: Optional[Decimal] = Query(None, description="Montant minimum"),
    max_amount: Optional[Decimal] = Query(None, description="Montant maximum"),
    search: Optional[str] = Query(None, description="Recherche dans description/payee"),
    is_recurring: Optional[bool] = Query(None, description="Transactions récurrentes uniquement"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste toutes les transactions de l'utilisateur avec filtres optionnels."""
    query = select(Transaction).where(Transaction.user_id == current_user.id)
    
    # Filtres
    if bank_account_id is not None:
        query = query.where(Transaction.bank_account_id == bank_account_id)
    if envelope_id is not None:
        query = query.where(Transaction.envelope_id == envelope_id)
    if category_id is not None:
        query = query.where(Transaction.category_id == category_id)
    if transaction_type is not None:
        query = query.where(Transaction.transaction_type == transaction_type)
    if priority is not None:
        query = query.where(Transaction.priority == priority)
    if date_from is not None:
        query = query.where(Transaction.date >= date_from)
    if date_to is not None:
        query = query.where(Transaction.date <= date_to)
    if min_amount is not None:
        query = query.where(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.where(Transaction.amount <= max_amount)
    if search is not None:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Transaction.description.ilike(search_pattern),
                Transaction.payee.ilike(search_pattern)
            )
        )
    if is_recurring is not None:
        query = query.where(Transaction.is_recurring == is_recurring)
    
    # Tri par date décroissante
    query = query.order_by(Transaction.date.desc(), Transaction.id.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    return transactions


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée une nouvelle transaction."""
    # Vérifier que le compte bancaire appartient à l'utilisateur
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == transaction_data.bank_account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    bank_account = result.scalar_one_or_none()
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    # Vérifier que la catégorie existe et appartient à l'utilisateur
    result = await db.execute(
        select(Category).where(
            and_(
                Category.id == transaction_data.category_id,
                Category.user_id == current_user.id
            )
        )
    )
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Si une enveloppe est spécifiée, vérifier qu'elle appartient à l'utilisateur
    if transaction_data.envelope_id is not None:
        result = await db.execute(
            select(Envelope).where(
                and_(
                    Envelope.id == transaction_data.envelope_id,
                    Envelope.user_id == current_user.id
                )
            )
        )
        envelope = result.scalar_one_or_none()
        if not envelope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Envelope not found"
            )
    
    # Créer la transaction
    transaction = Transaction(
        user_id=current_user.id,
        **transaction_data.model_dump()
    )
    
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    
    return transaction


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupère une transaction par son ID."""
    result = await db.execute(
        select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id
            )
        )
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour une transaction existante."""
    # Récupérer la transaction
    result = await db.execute(
        select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id
            )
        )
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Préparer les données à mettre à jour
    update_data = transaction_data.model_dump(exclude_unset=True)
    
    # Si le compte bancaire est modifié, vérifier qu'il appartient à l'utilisateur
    if "bank_account_id" in update_data:
        result = await db.execute(
            select(BankAccount).where(
                and_(
                    BankAccount.id == update_data["bank_account_id"],
                    BankAccount.user_id == current_user.id
                )
            )
        )
        bank_account = result.scalar_one_or_none()
        if not bank_account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bank account not found"
            )
    
    # Si la catégorie est modifiée, vérifier qu'elle appartient à l'utilisateur
    if "category_id" in update_data:
        result = await db.execute(
            select(Category).where(
                and_(
                    Category.id == update_data["category_id"],
                    Category.user_id == current_user.id
                )
            )
        )
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Si l'enveloppe est modifiée, vérifier qu'elle appartient à l'utilisateur
    if "envelope_id" in update_data and update_data["envelope_id"] is not None:
        result = await db.execute(
            select(Envelope).where(
                and_(
                    Envelope.id == update_data["envelope_id"],
                    Envelope.user_id == current_user.id
                )
            )
        )
        envelope = result.scalar_one_or_none()
        if not envelope:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Envelope not found"
            )
    
    # Appliquer les modifications
    for key, value in update_data.items():
        setattr(transaction, key, value)
    
    await db.commit()
    await db.refresh(transaction)
    
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime une transaction."""
    result = await db.execute(
        select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.user_id == current_user.id
            )
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
    
    return None


@router.get("/stats/summary", response_model=dict)
async def get_transaction_summary(
    date_from: Optional[date] = Query(None, description="Date de début"),
    date_to: Optional[date] = Query(None, description="Date de fin"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtient un résumé des transactions (revenus, dépenses, solde)."""
    query = select(Transaction).where(Transaction.user_id == current_user.id)
    
    if date_from:
        query = query.where(Transaction.date >= date_from)
    if date_to:
        query = query.where(Transaction.date <= date_to)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    total_income = Decimal("0")
    total_expense = Decimal("0")
    
    for transaction in transactions:
        if transaction.transaction_type == "income":
            total_income += transaction.amount
        elif transaction.transaction_type == "expense":
            total_expense += transaction.amount
    
    return {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance": float(total_income - total_expense),
        "transaction_count": len(transactions)
    }
