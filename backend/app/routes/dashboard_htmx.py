"""
Routes HTMX pour le dashboard
Endpoints retournant des fragments HTML pour HTMX
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from pathlib import Path
from decimal import Decimal

from app.database import get_db
from app.models import User, Envelope, Transaction, BankAccount
from app.utils.dependencies import get_current_user

templates_dir = Path(__file__).parent.parent.parent.parent / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

router = APIRouter(prefix="/dashboard/htmx", tags=["dashboard-htmx"])


@router.get("/stats", response_class=HTMLResponse)
async def dashboard_stats(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne les statistiques du dashboard."""
    # Total des enveloppes
    envelopes_result = await db.execute(
        select(func.sum(Envelope.allocated_amount)).where(
            Envelope.user_id == current_user.id
        )
    )
    total_allocated = envelopes_result.scalar() or Decimal(0)

    # Solde total des comptes
    accounts_result = await db.execute(
        select(func.sum(BankAccount.balance)).where(
            BankAccount.user_id == current_user.id
        )
    )
    total_balance = accounts_result.scalar() or Decimal(0)

    # Total des transactions
    transactions_result = await db.execute(
        select(func.count(Transaction.id)).where(
            Transaction.user_id == current_user.id
        )
    )
    total_transactions = transactions_result.scalar() or 0

    # Enveloppes
    envelopes_data = await db.execute(
        select(Envelope).where(Envelope.user_id == current_user.id)
    )
    envelopes = envelopes_data.scalars().all()

    return templates.TemplateResponse(
        "components/dashboard_stats.html",
        {
            "request": request,
            "total_allocated": total_allocated,
            "total_balance": total_balance,
            "total_transactions": total_transactions,
            "envelopes": envelopes
        }
    )


@router.get("/recent-transactions", response_class=HTMLResponse)
async def dashboard_recent_transactions(
    request: Request,
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne les transactions récentes."""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.date.desc())
        .limit(limit)
    )
    transactions = result.scalars().all()

    return templates.TemplateResponse(
        "components/dashboard_recent_transactions.html",
        {"request": request, "transactions": transactions}
    )
