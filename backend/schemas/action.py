from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ActionCreate(BaseModel):
    """Schema for creating a new action"""
    contract_id: int
    action_type: str = Field(..., description="Type of action (approve, reject, reopen, flag)")
    action_note: Optional[str] = Field(None, description="Note describing the action")
    acted_by: str = Field(..., description="User who performed the action")


class ActionResponse(BaseModel):
    """Schema for action response"""
    action_id: int
    contract_id: int
    action_type: str
    action_note: Optional[str]
    acted_by: str
    acted_at: datetime
    prior_status: Optional[str] = None
    new_status: Optional[str] = None

    class Config:
        from_attributes = True
