"""
Schémas Pydantic pour WishList et WishListItem
"""
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal
from enum import Enum


# Enums
class WishListType(str, Enum):
    """Types de liste"""
    TO_RECEIVE = "to_receive"
    TO_GIVE = "to_give"
    MIXED = "mixed"


class WishListStatus(str, Enum):
    """Statuts de liste"""
    ACTIVE = "active"
    ARCHIVED = "archived"


class ItemPriority(str, Enum):
    """Priorités d'article"""
    MUST_HAVE = "must_have"
    WANTED = "wanted"
    BONUS = "bonus"


class ItemStatus(str, Enum):
    """Statuts d'article"""
    TO_BUY = "to_buy"
    PURCHASED = "purchased"


# === WishList Schemas ===

class WishListBase(BaseModel):
    """Champs de base pour une liste de souhaits"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    list_type: WishListType
    target_date: Optional[date] = None
    budget_allocated: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    status: WishListStatus = WishListStatus.ACTIVE


class WishListCreate(WishListBase):
    """Schéma pour créer une liste"""
    pass


class WishListUpdate(BaseModel):
    """Schéma pour mettre à jour une liste"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    list_type: Optional[WishListType] = None
    target_date: Optional[date] = None
    budget_allocated: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    status: Optional[WishListStatus] = None


class WishListRead(WishListBase):
    """Schéma pour lire une liste"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === WishListItem Schemas ===

class WishListItemBase(BaseModel):
    """Champs de base pour un article"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0, decimal_places=2)
    quantity: int = Field(default=1, ge=1)
    url: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    priority: ItemPriority = ItemPriority.WANTED
    status: ItemStatus = ItemStatus.TO_BUY
    recipient: Optional[str] = Field(None, max_length=100, description="Pour listes 'to_give'")
    sort_order: int = 0


class WishListItemCreate(WishListItemBase):
    """Schéma pour créer un article (wish_list_id fourni dans l'URL)"""
    pass


class WishListItemUpdate(BaseModel):
    """Schéma pour mettre à jour un article"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    quantity: Optional[int] = Field(None, ge=1)
    url: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    priority: Optional[ItemPriority] = None
    status: Optional[ItemStatus] = None
    recipient: Optional[str] = Field(None, max_length=100)
    sort_order: Optional[int] = None


class WishListItemRead(WishListItemBase):
    """Schéma pour lire un article"""
    id: int
    wish_list_id: int
    transaction_id: Optional[int] = None
    purchased_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === Schemas avec relations ===

class WishListWithItems(WishListRead):
    """Schéma de liste avec tous ses articles"""
    items: List[WishListItemRead] = []
    total_cost: Decimal = Field(description="Coût total de tous les articles")
    purchased_cost: Decimal = Field(description="Montant déjà dépensé")
    remaining_cost: Decimal = Field(description="Montant restant à acheter")
    
    model_config = ConfigDict(from_attributes=True)


class WishListSummary(BaseModel):
    """Résumé statistique d'une liste"""
    total_items: int
    purchased_items: int
    total_cost: Decimal
    purchased_cost: Decimal
    remaining_cost: Decimal
    completion_percent: float
