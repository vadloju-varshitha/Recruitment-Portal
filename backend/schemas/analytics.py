from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AnalyticsOverview(BaseModel):
    total_jobs: int
    total_candidates: int
    total_applications: int
    shortlisted_candidates: int
    rejected_candidates: int
    hired_candidates: int
    hiring_rate: float
    total_companies: int
    total_recruiters: int


class TimeToHireData(BaseModel):
    month: str
    avg_days: float
    hires: int


class RecruiterAnalytics(BaseModel):
    total_jobs: int
    active_jobs: int
    total_applications: int
    shortlisted: int
    rejected: int
    interviews_scheduled: int
    hiring_rate: float
    applications_by_status: Dict[str, int]


class SkillGapAnalysis(BaseModel):
    job_title: str
    required_skills: List[str]
    candidate_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    match_percentage: float
    recommendations: List[str]


class InterviewQuestionsRequest(BaseModel):
    job_id: int
    candidate_id: int


class InterviewQuestionsResponse(BaseModel):
    questions: List[str]
    job_title: str
    candidate_name: str


class ReportRequest(BaseModel):
    report_type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class OfferLetterRequest(BaseModel):
    candidate_id: int
    job_id: int
    template: str = "standard"
    salary: str
    start_date: str
    position: str


class ExperienceLetterRequest(BaseModel):
    candidate_id: int
    company_name: str
    position: str
    start_date: str
    end_date: str
    responsibilities: str


class PayslipRequest(BaseModel):
    employee_name: str
    employee_id: str
    month: str
    year: str
    basic_salary: float
    hra: float = 0
    allowances: float = 0
    deductions: float = 0
