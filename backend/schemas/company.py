from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CompanyCreate(BaseModel):
    company_name: str = Field(..., min_length=2)
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    description: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    recruiter_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
