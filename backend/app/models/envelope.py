"""
Modèle Envelope - Enveloppe budgétaire
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Envelope(Base):
    """Modèle représentant une enveloppe budgétaire"""
    __tablename__ = "envelopes"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Informations
    name = Column(String(100), nullable=False)
    
    # Budget
    monthly_budget = Column(Numeric(10, 2), default=0.00, nullable=False)
    current_balance = Column(Numeric(10, 2), default=0.00, nullable=False)
    
    # Personnalisation
    color = Column(String(7), nullable=True)
    icon = Column(String(50), nullable=True)
    
    # État
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="envelopes")
    bank_account = relationship("BankAccount", back_populates="envelopes")
    category = relationship("Category", back_populates="envelopes")
    transactions = relationship("Transaction", back_populates="envelope", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Envelope(id={self.id}, name='{self.name}', budget={self.monthly_budget})>"
