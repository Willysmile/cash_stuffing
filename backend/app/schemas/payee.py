"""
Schémas Pydantic pour Payee
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PayeeBase(BaseModel):
    """Champs de base pour un bénéficiaire"""
    name: str = Field(..., min_length=1, max_length=100, description="Nom du bénéficiaire")


class PayeeCreate(PayeeBase):
    """Schéma pour créer un bénéficiaire"""
    pass


class PayeeUpdate(BaseModel):
    """Schéma pour mettre à jour un bénéficiaire"""
    name: str | None = Field(None, min_length=1, max_length=100)


class PayeeRead(PayeeBase):
    """Schéma pour lire un bénéficiaire"""
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
