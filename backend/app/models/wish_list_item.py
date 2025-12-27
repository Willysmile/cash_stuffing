"""
Modèle WishListItem - Article d'une liste de souhaits
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class WishListItem(Base):
    """Modèle représentant un article dans une liste de souhaits"""
    __tablename__ = "wish_list_items"
    
    # Identifiant
    id = Column(Integer, primary_key=True, index=True)
    
    # Clé étrangère
    wish_list_id = Column(Integer, ForeignKey("wish_lists.id", ondelete="CASCADE"), nullable=False, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Informations
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Prix et quantité
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    
    # Liens externes
    url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    
    # Métadonnées
    priority = Column(String(20), default="wanted", nullable=False)  # must_have, wanted, bonus
    status = Column(String(20), default="to_buy", nullable=False)  # to_buy, purchased
    recipient = Column(String(100), nullable=True)  # Pour listes "to_give"
    
    # Achat
    purchased_date = Column(Date, nullable=True)
    
    # Ordre
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    wish_list = relationship("WishList", back_populates="items")
    transaction = relationship("Transaction", back_populates="wish_list_items")
    
    def __repr__(self):
        return f"<WishListItem(id={self.id}, name='{self.name}', price={self.price}, status='{self.status}')>"
