"""
Routes HTMX pour les comptes bancaires
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pathlib import Path
from decimal import Decimal

from app.database import get_db
from app.models import User, BankAccount
from app.utils.dependencies import get_current_user

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


@router.post("", response_class=HTMLResponse)
async def create_account_htmx(
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


@router.post("", response_class=HTMLResponse)
async def create_account_htmx(
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


@router.get("/{account_id}/edit", response_class=HTMLResponse)
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


@router.put("/{account_id}", response_class=HTMLResponse)
async def update_account_htmx(
    account_id: int,
    name: str,
    account_number: str = None,
    balance: float = 0,
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
    
    account.name = name
    account.account_number = account_number
    account.balance = Decimal(str(balance))
    await db.commit()
    
    result = await db.execute(
        select(BankAccount).where(BankAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    return templates.TemplateResponse(
        "components/accounts_table.html",
        {"request": request, "accounts": accounts}
    )


@router.delete("/{account_id}", response_class=HTMLResponse)
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
        "components/accounts_table.html",
        {"request": request, "accounts": accounts}
    )
