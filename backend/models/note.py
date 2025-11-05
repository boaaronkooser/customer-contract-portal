from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Note(Base):
    """Note model for contract comments"""
    __tablename__ = "notes"

    note_id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False, index=True)
    body = Column(String(1000), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("notes.note_id"), nullable=True)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    edited_at = Column(DateTime(timezone=True), nullable=True)
    edit_note = Column(String(255), nullable=True)

    # Relationships
    contract = relationship("Contract", back_populates="notes")
    parent = relationship("Note", remote_side=[note_id], backref="replies")
