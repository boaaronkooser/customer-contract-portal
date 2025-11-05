from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ContractBase(BaseModel):
    """Base contract schema with common fields"""
    type: str = Field(..., min_length=1, max_length=50, description="Contract type")
    status: str = Field(..., description="Contract status (Draft, Pending Approval, Approved, Rejected)")
    effective_date: datetime
    expiration_date: Optional[datetime] = None
    terms_ref: Optional[str] = Field(None, description="Reference to terms document")
    attachments_ref: Optional[str] = Field(None, description="Reference to attachments")


class ContractCreate(ContractBase):
    """Schema for creating a new contract"""
    customer_id: int
    created_by: str = Field(..., description="User who created the contract")
    updated_by: str = Field(..., description="User who last updated the contract")


class ContractUpdate(BaseModel):
    """Schema for updating contract information"""
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = None
    effective_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    terms_ref: Optional[str] = None
    attachments_ref: Optional[str] = None
    updated_by: Optional[str] = None


class ContractResponse(ContractBase):
    """Schema for contract response"""
    contract_id: int
    customer_id: int
    created_by: str
    updated_by: str
    last_action_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

