"""
Modèle SQLAlchemy pour Payee (Bénéficiaire)
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Payee(Base):
    """Modèle pour un bénéficiaire/fournisseur"""
    __tablename__ = "payees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="payees")
    transactions = relationship("Transaction", back_populates="payee")
