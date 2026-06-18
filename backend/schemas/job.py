from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobCreate(BaseModel):
    title: str = Field(..., min_length=2)
    description: str
    requirements: Optional[str] = None
    required_skills: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    required_skills: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class JobResponse(BaseModel):
    job_id: int
    title: str
    description: str
    requirements: Optional[str] = None
    required_skills: Optional[str] = None
    salary: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None
    company_id: int
    is_active: bool = True
    company_name: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobSearchParams(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    experience: Optional[str] = None
