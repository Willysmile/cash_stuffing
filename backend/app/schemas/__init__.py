"""
Schemas package - Export de tous les schémas Pydantic
"""
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserRead,
    UserLogin,
    Token,
    TokenData,
)
from app.schemas.category import (
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryRead,
    CategoryWithChildren,
)
from app.schemas.bank_account import (
    BankAccountBase,
    BankAccountCreate,
    BankAccountUpdate,
    BankAccountAdjustBalance,
    BankAccountRead,
)
from app.schemas.envelope import (
    EnvelopeBase,
    EnvelopeCreate,
    EnvelopeUpdate,
    EnvelopeReallocate,
    EnvelopeRead,
    EnvelopeWithStats,
)
from app.schemas.transaction import (
    TransactionType,
    TransactionPriority,
    TransactionBase,
    TransactionCreate,
    TransactionUpdate,
    TransactionRead,
    TransactionWithDetails,
    TransactionFilter,
)
from app.schemas.wish_list import (
    WishListType,
    WishListStatus,
    ItemPriority,
    ItemStatus,
    WishListBase,
    WishListCreate,
    WishListUpdate,
    WishListRead,
    WishListItemBase,
    WishListItemCreate,
    WishListItemUpdate,
    WishListItemRead,
    WishListWithItems,
    WishListSummary,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "UserLogin",
    "Token",
    "TokenData",
    # Category
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryRead",
    "CategoryWithChildren",
    # BankAccount
    "BankAccountBase",
    "BankAccountCreate",
    "BankAccountUpdate",
    "BankAccountAdjustBalance",
    "BankAccountRead",
    # Envelope
    "EnvelopeBase",
    "EnvelopeCreate",
    "EnvelopeUpdate",
    "EnvelopeReallocate",
    "EnvelopeRead",
    "EnvelopeWithStats",
    # Transaction
    "TransactionType",
    "TransactionPriority",
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionRead",
    "TransactionWithDetails",
    "TransactionFilter",
    # WishList
    "WishListType",
    "WishListStatus",
    "ItemPriority",
    "ItemStatus",
    "WishListBase",
    "WishListCreate",
    "WishListUpdate",
    "WishListRead",
    "WishListItemBase",
    "WishListItemCreate",
    "WishListItemUpdate",
    "WishListItemRead",
    "WishListWithItems",
    "WishListSummary",
]
