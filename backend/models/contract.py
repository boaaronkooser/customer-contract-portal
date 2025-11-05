from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Contract(Base):
    """Contract model"""
    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    terms_ref = Column(String(255), nullable=True)
    attachments_ref = Column(String(255), nullable=True)
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    last_action_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    customer = relationship("Customer", back_populates="contracts")
    notes = relationship("Note", back_populates="contract", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="contract", cascade="all, delete-orphan")
