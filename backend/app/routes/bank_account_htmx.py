"""
Routes HTMX pour les comptes bancaires
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from decimal import Decimal

from app.database import get_db
from app.models import User, BankAccount
from app.models.transaction import Transaction
from app.utils.dependencies import get_current_user
from datetime import date

templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/bank-accounts/htmx", tags=["accounts-htmx"])


@router.get("/create", response_class=HTMLResponse)
async def create_account_modal(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal pour créer un nouveau compte bancaire."""
    return templates.TemplateResponse(
        "components/account_create_modal.html",
        {"request": request}
    )


@router.get("", response_class=HTMLResponse)
async def list_accounts_htmx(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les comptes bancaires de l'utilisateur."""
    result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/accounts_table.html",
        {"request": request, "accounts": accounts}
    )


@router.get("/rows", response_class=HTMLResponse)
async def list_accounts_rows_htmx(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne seulement les lignes du tableau pour HTMX."""
    result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/accounts_rows.html",
        {"request": request, "accounts": accounts}
    )


@router.post("", response_class=HTMLResponse)
async def create_account_htmx(
    name: str = Form(...),
    account_number: str = Form(None),
    balance: float = Form(0),
    account_type: str = Form("checking"),
    currency: str = Form("EUR"),
    color: str = Form(None),
    icon: str = Form(None),
    is_active: str = Form("true"),
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau compte bancaire."""
    try:
        # Convertir is_active string en booléen
        is_active_bool = is_active.lower() in ('true', 'on', 'yes', '1')
        
        account = BankAccount(
            user_id=current_user.id,
            name=name,
            account_type=account_type,
            account_number=account_number,
            initial_balance=Decimal(str(balance)),
            current_balance=Decimal(str(balance)),
            currency=currency,
            color=color,
            icon=icon,
            is_active=is_active_bool
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
        
        # Créer une transaction initiale si le solde > 0
        if balance > 0:
            initial_transaction = Transaction(
                user_id=current_user.id,
                bank_account_id=account.id,
                category_id=1,  # Catégorie par défaut (à ajuster selon vos besoins)
                amount=Decimal(str(balance)),
                transaction_type="income",
                date=date.today(),
                description=f"Solde initial du compte {name}",
                is_recurring=False
            )
            db.add(initial_transaction)
            await db.commit()
        
        result = await db.execute(
            select(BankAccount).where(BankAccount.user_id == current_user.id)
        )
        accounts = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/accounts_rows.html",
            {"request": request, "accounts": accounts}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_class=HTMLResponse)
async def create_account_htmx_dup(
    name: str,
    account_number: str = None,
    balance: float = 0,
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crée un nouveau compte bancaire."""
    try:
        account = BankAccount(
            user_id=current_user.id,
            name=name,
            account_number=account_number,
            balance=Decimal(str(balance))
        )
        db.add(account)
        await db.commit()
        
        result = await db.execute(
            select(BankAccount).where(BankAccount.user_id == current_user.id)
        )
        accounts = result.scalars().all()
        
        return templates.TemplateResponse(
            "components/accounts_table.html",
            {"request": request, "accounts": accounts}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{account_id:int}/edit", response_class=HTMLResponse)
async def account_edit_modal(
    account_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modal d'édition d'un compte bancaire."""
    result = await db.execute(
        select(BankAccount).where(
            BankAccount.id == account_id,
            BankAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return templates.TemplateResponse(
        "components/account_edit_modal.html",
        {"request": request, "account": account}
    )


@router.put("/{account_id:int}", response_class=HTMLResponse)
async def update_account_htmx(
    account_id: int,
    name: str = Form(None),
    account_type: str = Form(None),
    account_number: str = Form(None),
    current_balance: float = Form(None),
    color: str = Form(None),
    icon: str = Form(None),
    is_active: str = Form(None),
    request: Request = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met à jour un compte bancaire."""
    result = await db.execute(
        select(BankAccount).where(
            BankAccount.id == account_id,
            BankAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if name is not None:
        account.name = name
    if account_type is not None:
        account.account_type = account_type
    if account_number is not None:
        account.account_number = account_number
    if current_balance is not None:
        account.current_balance = Decimal(str(current_balance))
    if color is not None:
        account.color = color
    if icon is not None:
        account.icon = icon
    if is_active is not None:
        # Convertir is_active string en booléen
        account.is_active = is_active.lower() in ('true', 'on', 'yes', '1')
    await db.commit()
    
    result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/accounts_rows.html",
        {"request": request, "accounts": accounts}
    )


@router.delete("/{account_id:int}", response_class=HTMLResponse)
async def delete_account_htmx(
    account_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Supprime un compte bancaire."""
    result = await db.execute(
        select(BankAccount).where(
            BankAccount.id == account_id,
            BankAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    await db.delete(account)
    await db.commit()
    
    result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/accounts_rows.html",
        {"request": request, "accounts": accounts}
    )
