from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int
    date: date
    time: time
    meeting_link: Optional[str] = None
    notes: Optional[str] = None


class InterviewUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[time] = None
    meeting_link: Optional[str] = None
    notes: Optional[str] = None


class InterviewResponse(BaseModel):
    interview_id: int
    candidate_id: int
    job_id: int
    date: date
    time: time
    meeting_link: Optional[str] = None
    notes: Optional[str] = None
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
