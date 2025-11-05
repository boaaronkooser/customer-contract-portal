from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class CustomerBase(BaseModel):
    """Base customer schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=1, max_length=20)
    segment: str = Field(..., description="Customer segment (e.g., Retail, Corporate)")
    risk_level: str = Field(..., description="Risk level (Low, Medium, High)")
    status: str = Field(default="Active", description="Customer status")


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating customer information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    segment: Optional[str] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response"""
    customer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2 compatibility with SQLAlchemy

