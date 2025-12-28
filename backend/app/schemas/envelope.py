"""
Schémas Pydantic pour Envelope
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal


# Schéma de base
class EnvelopeBase(BaseModel):
    """Champs de base pour une enveloppe budgétaire"""
    name: str = Field(..., min_length=1, max_length=100)
    bank_account_id: Optional[int] = None
    category_id: Optional[int] = None
    target_amount: Decimal = Field(..., ge=0, decimal_places=2, description="Objectif à atteindre")
    description: Optional[str] = Field(None, max_length=255)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


# Schéma pour la création
class EnvelopeCreate(EnvelopeBase):
    """Schéma pour créer une nouvelle enveloppe"""
    pass


# Schéma pour la mise à jour
class EnvelopeUpdate(BaseModel):
    """Schéma pour mettre à jour une enveloppe"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    bank_account_id: Optional[int] = None
    category_id: Optional[int] = None
    target_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=255)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


# Schéma pour réallouer entre enveloppes
class EnvelopeReallocate(BaseModel):
    """Schéma pour transférer de l'argent entre enveloppes"""
    from_envelope_id: int
    to_envelope_id: int
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    description: Optional[str] = Field(None, max_length=255)


# Schéma pour la lecture
class EnvelopeRead(EnvelopeBase):
    """Schéma pour lire une enveloppe"""
    id: int
    user_id: int
    current_balance: Decimal
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schéma avec statistiques
class EnvelopeWithStats(EnvelopeRead):
    """Schéma avec statistiques de l'enveloppe"""
    progress_percent: float = Field(description="Pourcentage de l'objectif atteint")
    remaining_to_target: Decimal = Field(description="Montant restant pour atteindre l'objectif")
    is_goal_reached: bool = Field(description="Objectif atteint")
