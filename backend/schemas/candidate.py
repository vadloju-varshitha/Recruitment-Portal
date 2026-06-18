from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CandidateProfileCreate(BaseModel):
    skills: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    projects: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    headline: Optional[str] = None


class CandidateProfileUpdate(BaseModel):
    skills: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    projects: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    headline: Optional[str] = None


class CandidateResponse(BaseModel):
    candidate_id: int
    user_id: int
    resume: Optional[str] = None
    skills: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    projects: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    headline: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
