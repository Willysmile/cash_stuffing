"""
Modèle Category - Catégorie et sous-catégorie de dépenses/revenus
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Category(Base):
    """Modèle représentant une catégorie ou sous-catégorie"""
    __tablename__ = "categories"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Informations
    name = Column(String(100), nullable=False)
    color = Column(String(7), nullable=True)  # Format hex: #FF5733
    icon = Column(String(50), nullable=True)
    
    # Métadonnées
    is_default = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relations
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="children")
    envelopes = relationship("Envelope", back_populates="category")
    transactions = relationship("Transaction", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"
