from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class EventCreate(BaseModel):
    """Schema for creating a new event"""
    customer_id: int
    event_type: str = Field(..., description="Type of event (Login, Logout, Password Reset, etc.)")
    channel: str = Field(..., description="Channel (Web, Mobile, API)")
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = Field(None, max_length=500)
    metadata_json: Optional[Dict[str, Any]] = Field(None, description="Additional event metadata")
    correlation_id: Optional[str] = Field(None, max_length=100)


class EventResponse(BaseModel):
    """Schema for event response"""
    event_id: int
    customer_id: int
    event_type: str
    timestamp: datetime
    channel: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    metadata_json: Optional[Dict[str, Any]]
    correlation_id: Optional[str]

    class Config:
        from_attributes = True

