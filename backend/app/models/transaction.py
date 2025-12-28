"""
Modèle Transaction - Dépense ou revenu
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    """Modèle représentant une transaction (dépense ou revenu)"""
    __tablename__ = "transactions"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    envelope_id = Column(Integer, ForeignKey("envelopes.id", ondelete="SET NULL"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=False, index=True)
    payee_id = Column(Integer, ForeignKey("payees.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Informations financières
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # expense, income, transfer, adjustment
    
    # Informations de transaction
    date = Column(Date, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    # Métadonnées
    priority = Column(String(20), nullable=True)  # vital, comfort, pleasure
    is_recurring = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="transactions")
    bank_account = relationship("BankAccount", back_populates="transactions")
    envelope = relationship("Envelope", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    payee = relationship("Payee", back_populates="transactions")
    wish_list_items = relationship("WishListItem", back_populates="transaction")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.transaction_type}', amount={self.amount}, date={self.date})>"
