"""
Schémas Pydantic pour User
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


# Schéma de base (champs communs)
class UserBase(BaseModel):
    """Champs de base pour un utilisateur"""
    email: EmailStr


# Schéma pour la création d'un utilisateur
class UserCreate(UserBase):
    """Schéma pour créer un nouvel utilisateur"""
    password: str = Field(..., min_length=8, description="Mot de passe (min 8 caractères)")


# Schéma pour la mise à jour d'un utilisateur
class UserUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


# Schéma pour la lecture d'un utilisateur (réponse API)
class UserRead(UserBase):
    """Schéma pour lire un utilisateur (sans le mot de passe)"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Schéma pour la connexion
class UserLogin(BaseModel):
    """Schéma pour la connexion utilisateur"""
    email: EmailStr
    password: str


# Schéma pour le token JWT
class Token(BaseModel):
    """Schéma pour le token d'authentification"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Données extraites du token JWT"""
    user_id: Optional[int] = None
    email: Optional[str] = None
