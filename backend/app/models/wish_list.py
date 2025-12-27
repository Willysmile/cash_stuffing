"""
Modèle WishList - Liste de souhaits/cadeaux
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class WishList(Base):
    """Modèle représentant une liste de souhaits ou cadeaux"""
    __tablename__ = "wish_lists"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clé étrangère
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Informations
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    list_type = Column(String(20), nullable=False)  # to_receive, to_give, mixed
    
    # Planning
    target_date = Column(Date, nullable=True)
    budget_allocated = Column(Numeric(10, 2), nullable=True)
    
    # État
    status = Column(String(20), default="active", nullable=False)  # active, archived
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="wish_lists")
    items = relationship("WishListItem", back_populates="wish_list", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<WishList(id={self.id}, name='{self.name}', type='{self.list_type}')>"
