"""
Schémas Pydantic pour Transaction
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from enum import Enum


# Enums pour les types
class TransactionType(str, Enum):
    """Types de transaction"""
    EXPENSE = "expense"
    INCOME = "income"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class TransactionPriority(str, Enum):
    """Priorités de dépense"""
    VITAL = "vital"
    COMFORT = "comfort"
    PLEASURE = "pleasure"


# Schéma de base
class TransactionBase(BaseModel):
    """Champs de base pour une transaction"""
    bank_account_id: int
    envelope_id: Optional[int] = None
    category_id: int
    amount: Decimal = Field(..., decimal_places=2, description="Montant de la transaction")
    transaction_type: TransactionType
    date: date
    description: Optional[str] = Field(None, max_length=255)
    payee: Optional[str] = Field(None, max_length=100, description="Bénéficiaire ou fournisseur")
    priority: Optional[TransactionPriority] = None
    is_recurring: bool = False


# Schéma pour la création
class TransactionCreate(TransactionBase):
    """Schéma pour créer une nouvelle transaction"""
    pass


# Schéma pour la mise à jour
class TransactionUpdate(BaseModel):
    """Schéma pour mettre à jour une transaction"""
    bank_account_id: Optional[int] = None
    envelope_id: Optional[int] = None
    category_id: Optional[int] = None
    amount: Optional[Decimal] = Field(None, decimal_places=2)
    transaction_type: Optional[TransactionType] = None
    date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=255)
    payee: Optional[str] = Field(None, max_length=100)
    priority: Optional[TransactionPriority] = None
    is_recurring: Optional[bool] = None


# Schéma pour la lecture
class TransactionRead(TransactionBase):
    """Schéma pour lire une transaction"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Schéma avec relations expanded
class TransactionWithDetails(TransactionRead):
    """Schéma avec détails complets (catégorie, compte, enveloppe)"""
    category_name: Optional[str] = None
    bank_account_name: Optional[str] = None
    envelope_name: Optional[str] = None


# Schéma pour les filtres de recherche
class TransactionFilter(BaseModel):
    """Schéma pour filtrer les transactions"""
    bank_account_id: Optional[int] = None
    envelope_id: Optional[int] = None
    category_id: Optional[int] = None
    transaction_type: Optional[TransactionType] = None
    priority: Optional[TransactionPriority] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    search: Optional[str] = Field(None, description="Recherche dans description/payee")
    is_recurring: Optional[bool] = None
