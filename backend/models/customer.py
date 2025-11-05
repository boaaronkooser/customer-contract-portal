from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=False)
    segment = Column(String(50), nullable=False)
    risk_level = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    contracts = relationship("Contract", back_populates="customer", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="customer", cascade="all, delete-orphan")
