"""
Modèle pour l'historique des ajustements des enveloppes
"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class EnvelopeHistory(Base):
    __tablename__ = "envelope_history"

    id = Column(Integer, primary_key=True, index=True)
    envelope_id = Column(Integer, ForeignKey("envelopes.id"), index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    balance_after = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relation
    envelope = relationship("Envelope", back_populates="history")
