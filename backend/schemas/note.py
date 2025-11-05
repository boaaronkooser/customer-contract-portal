from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class NoteBase(BaseModel):
    """Base note schema with common fields"""
    body: str = Field(..., min_length=1, description="Note content")
    parent_comment_id: Optional[int] = Field(None, description="Parent comment for threading")


class NoteCreate(NoteBase):
    """Schema for creating a new note"""
    contract_id: int
    created_by: str = Field(..., description="User who created the note")


class NoteUpdate(BaseModel):
    """Schema for updating a note"""
    body: Optional[str] = Field(None, min_length=1)
    edit_note: Optional[str] = Field(None, description="Note about the edit")


class NoteResponse(NoteBase):
    """Schema for note response"""
    note_id: int
    contract_id: int
    created_by: str
    created_at: datetime
    edited_at: Optional[datetime] = None
    edit_note: Optional[str] = None

    class Config:
        from_attributes = True

