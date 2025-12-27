"""
Modèle BankAccount - Compte bancaire
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class BankAccount(Base):
    """Modèle représentant un compte bancaire"""
    __tablename__ = "bank_accounts"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clé étrangère
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Informations
    name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)  # checking, savings, livret, etc.
    
    # Finances
    initial_balance = Column(Numeric(10, 2), default=0.00, nullable=False)
    current_balance = Column(Numeric(10, 2), default=0.00, nullable=False)
    currency = Column(String(3), default="EUR", nullable=False)
    
    # Personnalisation
    color = Column(String(7), nullable=True)
    icon = Column(String(50), nullable=True)
    
    # État
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="bank_accounts")
    envelopes = relationship("Envelope", back_populates="bank_account", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BankAccount(id={self.id}, name='{self.name}', balance={self.current_balance})>"
