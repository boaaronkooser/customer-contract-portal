from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Action(Base):
    """Action model for contract lifecycle actions"""
    __tablename__ = "actions"

    action_id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False, index=True)
    action_type = Column(String(30), nullable=False)
    action_note = Column(String(500), nullable=True)
    acted_by = Column(String(100), nullable=False)
    acted_at = Column(DateTime(timezone=True), server_default=func.now())
    prior_status = Column(String(30), nullable=True)
    new_status = Column(String(30), nullable=True)

    # Relationships
    contract = relationship("Contract", back_populates="actions")
