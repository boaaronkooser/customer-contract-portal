from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Event(Base):
    """Event model for logging customer activities"""
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    channel = Column(String(50), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    correlation_id = Column(String(100), nullable=True, index=True)

    # Relationships
    customer = relationship("Customer", back_populates="events")
