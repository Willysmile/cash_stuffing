"""
Schémas Pydantic pour BankAccount
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


# Schéma de base
class BankAccountBase(BaseModel):
    """Champs de base pour un compte bancaire"""
    name: str = Field(..., min_length=1, max_length=100)
    account_type: str = Field(..., max_length=50, description="Type: checking, savings, livret")
    currency: str = Field(default="EUR", pattern="^[A-Z]{3}$", description="Code devise ISO (EUR, USD, etc.)")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


# Schéma pour la création
class BankAccountCreate(BankAccountBase):
    """Schéma pour créer un nouveau compte bancaire"""
    initial_balance: Decimal = Field(..., decimal_places=2, description="Solde initial")


# Schéma pour la mise à jour
class BankAccountUpdate(BaseModel):
    """Schéma pour mettre à jour un compte bancaire"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_type: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


# Schéma pour ajuster manuellement le solde
class BankAccountAdjustBalance(BaseModel):
    """Schéma pour corriger le solde d'un compte"""
    new_balance: Decimal = Field(..., decimal_places=2)
    reason: Optional[str] = Field(None, max_length=255, description="Raison de l'ajustement")


# Schéma pour la lecture
class BankAccountRead(BankAccountBase):
    """Schéma pour lire un compte bancaire"""
    id: int
    user_id: int
    initial_balance: Decimal
    current_balance: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
