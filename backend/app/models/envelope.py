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
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Informations
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    
    # Objectif d'épargne
    target_amount = Column(Numeric(10, 2), default=0.00, nullable=False)  # Objectif à atteindre
    current_balance = Column(Numeric(10, 2), default=0.00, nullable=False)  # Solde actuel accumulé
    
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
    history = relationship("EnvelopeHistory", back_populates="envelope", cascade="all, delete-orphan")
