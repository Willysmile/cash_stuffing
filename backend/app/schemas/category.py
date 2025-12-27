"""
Schémas Pydantic pour Category
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# Schéma de base
class CategoryBase(BaseModel):
    """Champs de base pour une catégorie"""
    name: str = Field(..., min_length=1, max_length=100)
    parent_id: Optional[int] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", description="Couleur hex (#RRGGBB)")
    icon: Optional[str] = Field(None, max_length=50)
    is_default: bool = False
    sort_order: int = 0


# Schéma pour la création
class CategoryCreate(CategoryBase):
    """Schéma pour créer une nouvelle catégorie"""
    pass


# Schéma pour la mise à jour
class CategoryUpdate(BaseModel):
    """Schéma pour mettre à jour une catégorie"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    parent_id: Optional[int] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[int] = None


# Schéma pour la lecture
class CategoryRead(CategoryBase):
    """Schéma pour lire une catégorie"""
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schéma avec sous-catégories (nested)
class CategoryWithChildren(CategoryRead):
    """Schéma avec la liste des sous-catégories"""
    children: List['CategoryRead'] = []
    
    model_config = ConfigDict(from_attributes=True)
