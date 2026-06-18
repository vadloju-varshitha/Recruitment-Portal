from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class MatchBreakdown(BaseModel):
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    total_required: int = 0
    total_matched: int = 0
    match_percentage: float = 0.0


class ApplicationResponse(BaseModel):
    application_id: int
    candidate_id: int
    job_id: int
    status: ApplicationStatus
    match_score: float
    match_breakdown: Optional[str] = None
    cover_letter: Optional[str] = None
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_skills: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
