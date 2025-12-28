"""  
Routes API pour la gestion des comptes bancaires
"""
from typing import List, Optional
from decimal import Decimal
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.database import get_db
from app.models.bank_account import BankAccount
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.bank_account import (
    BankAccountCreate,
    BankAccountUpdate,
    BankAccountRead,
    BankAccountAdjustBalance
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/bank_accounts", tags=["Bank Accounts"])


@router.post("/{account_id}/recalculate", response_model=BankAccountRead)
async def recalculate_balance(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Recalcule le solde d'un compte à partir de son solde initial et de toutes ses transactions"""
    # Récupérer le compte
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    # Récupérer toutes les transactions du compte
    result = await db.execute(
        select(Transaction).where(Transaction.bank_account_id == account_id)
    )
    transactions = result.scalars().all()
    
    # Calculer le nouveau solde : solde initial + somme des transactions
    calculated_balance = account.initial_balance
    for t in transactions:
        if t.transaction_type == "income":
            calculated_balance += t.amount
        elif t.transaction_type == "expense":
            calculated_balance -= t.amount
    
    # Mettre à jour le solde
    account.current_balance = calculated_balance
    await db.commit()
    await db.refresh(account)
    
    return account


@router.get("/options", response_class=HTMLResponse)
async def get_bank_accounts_options(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne les options HTML pour le select des comptes bancaires"""
    query = select(BankAccount).where(BankAccount.user_id == current_user.id).order_by(BankAccount.name)
    result = await db.execute(query)
    accounts = result.scalars().all()
    
    html = '<option value="">💵 Espèces (sans compte)</option>\n'
    for account in accounts:
        html += f'<option value="{account.id}">{account.name}</option>\n'
    
    return HTMLResponse(content=html)


@router.get("", response_model=List[BankAccountRead])
async def get_bank_accounts(
    account_type: Optional[str] = Query(None, description="Filtrer par type de compte"),
    currency: Optional[str] = Query(None, description="Filtrer par devise"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Liste tous les comptes bancaires de l'utilisateur connecté
    
    Paramètres:
    - **account_type**: Filtrer par type de compte (ex: checking, savings)
    - **currency**: Filtrer par devise (ex: EUR, USD)
    
    Returns:
        Liste des comptes triés par nom
    """
    # Construction de la requête de base
    query = select(BankAccount).where(BankAccount.user_id == current_user.id)
    
    # Filtre type de compte
    if account_type:
        query = query.where(BankAccount.account_type == account_type)
    
    # Filtre devise
    if currency:
        query = query.where(BankAccount.currency == currency)
    
    # Tri par nom
    query = query.order_by(BankAccount.name)
    
    result = await db.execute(query)
    accounts = result.scalars().all()
    
    return accounts


@router.get("/{account_id}", response_model=BankAccountRead)
async def get_bank_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les détails d'un compte bancaire spécifique
    
    Paramètres:
    - **account_id**: ID du compte
    
    Returns:
        Détails du compte
    """
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found"
        )
    
    return account


@router.post("", response_model=BankAccountRead, status_code=status.HTTP_201_CREATED)
async def create_bank_account(
    account_data: BankAccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crée un nouveau compte bancaire
    
    Paramètres:
    - **name**: Nom du compte (requis)
    - **account_type**: Type de compte (ex: checking, savings)
    - **initial_balance**: Solde initial (défaut: 0)
    - **currency**: Devise (défaut: EUR)
    
    Note:
    - Le current_balance est automatiquement initialisé à initial_balance
    - Une transaction initiale est créée pour enregistrer le solde de départ
    
    Returns:
        Compte créé
    """
    # Créer le compte avec current_balance = initial_balance
    account_dict = account_data.model_dump()
    initial_balance = account_dict.get('initial_balance', Decimal('0'))
    account_dict['current_balance'] = initial_balance
    
    new_account = BankAccount(
        **account_dict,
        user_id=current_user.id
    )
    
    db.add(new_account)
    await db.flush()  # Flush pour obtenir l'ID du compte
    
    # Créer une transaction initiale si le solde n'est pas zéro
    if initial_balance != Decimal('0'):
        # Récupérer ou créer une catégorie "Solde initial"
        result = await db.execute(
            select(Category).where(
                and_(
                    Category.user_id == current_user.id,
                    Category.name == "Solde initial"
                )
            )
        )
        category = result.scalar_one_or_none()
        
        if not category:
            category = Category(
                user_id=current_user.id,
                name="Solde initial",
                color="#6c757d",
                icon="fa-flag",
                is_default=True
            )
            db.add(category)
            await db.flush()
        
        # Créer la transaction initiale
        initial_transaction = Transaction(
            user_id=current_user.id,
            bank_account_id=new_account.id,
            category_id=category.id,
            amount=abs(initial_balance),
            transaction_type="income" if initial_balance > 0 else "expense",
            date=date.today(),
            description=f"Solde initial du compte {new_account.name}",
            payee="Système",
            is_recurring=False
        )
        db.add(initial_transaction)
    
    await db.commit()
    await db.refresh(new_account)
    
    return new_account


@router.put("/{account_id}", response_model=BankAccountRead)
async def update_bank_account(
    account_id: int,
    account_data: BankAccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Met à jour un compte bancaire existant
    
    Paramètres:
    - **account_id**: ID du compte à modifier
    - Champs modifiables: name, account_type, currency
    
    Note:
    - Le solde ne peut pas être modifié via cette route
    - Utiliser POST /bank-accounts/{id}/adjust pour ajuster le solde
    
    Returns:
        Compte mis à jour
    """
    # Récupérer le compte
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found"
        )
    
    # Mettre à jour les champs (exclut les balances)
    update_data = account_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)
    
    await db.commit()
    await db.refresh(account)
    
    return account


@router.post("/{account_id}/adjust", response_model=BankAccountRead)
async def adjust_balance(
    account_id: int,
    adjustment_data: BankAccountAdjustBalance,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ajuste manuellement le solde d'un compte bancaire
    
    Utilisé pour corriger des erreurs ou synchroniser avec la banque
    
    Paramètres:
    - **account_id**: ID du compte
    - **new_balance**: Nouveau solde à définir
    - **reason**: Raison de l'ajustement (optionnel mais recommandé)
    
    Note:
    - Modifie directement current_balance
    - initial_balance reste inchangé
    - Un ajustement peut aussi être enregistré comme transaction type 'adjustment'
    
    Returns:
        Compte avec solde ajusté
    """
    # Récupérer le compte
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found"
        )
    
    # Ajuster le solde
    old_balance = account.current_balance
    account.current_balance = adjustment_data.new_balance
    
    await db.commit()
    await db.refresh(account)
    
    # Log l'ajustement (pour débogage)
    print(f"Balance adjustment: Account {account_id} ({account.name})")
    print(f"  Old balance: {old_balance} {account.currency}")
    print(f"  New balance: {adjustment_data.new_balance} {account.currency}")
    if adjustment_data.reason:
        print(f"  Reason: {adjustment_data.reason}")
    
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bank_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supprime un compte bancaire
    
    Paramètres:
    - **account_id**: ID du compte à supprimer
    
    Note:
    - La suppression échoue si le compte a des enveloppes liées (contrainte FK)
    - La suppression échoue si le compte a des transactions liées (contrainte FK)
    
    Returns:
        204 No Content si succès
    """
    # Récupérer le compte
    result = await db.execute(
        select(BankAccount).where(
            and_(
                BankAccount.id == account_id,
                BankAccount.user_id == current_user.id
            )
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bank account {account_id} not found"
        )
    
    # Vérifier si le compte a des enveloppes ou transactions
    # La contrainte FK en base empêchera la suppression
    
    try:
        await db.delete(account)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete bank account: it may have related envelopes or transactions. {str(e)}"
        )
    
    return None
