import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from models.company import Company
from models.job import Job
from models.application import Application, ApplicationStatus
from models.candidate import Candidate
from models.interview import Interview
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from schemas.job import JobCreate, JobUpdate, JobResponse
from schemas.application import ApplicationResponse, ApplicationStatusUpdate
from schemas.interview import InterviewCreate, InterviewResponse
from schemas.analytics import RecruiterAnalytics, InterviewQuestionsRequest, InterviewQuestionsResponse
from utils.dependencies import require_roles
from services.interview_questions import generate_interview_questions
from email_service.email import notify_shortlisted, notify_rejected, notify_interview_scheduled
from telegram_service.bot import (
    notify_shortlisted_telegram,
    notify_interview_telegram,
)

router = APIRouter(prefix="/recruiter", tags=["Recruiter"])


def _get_company(current_user: User, db: Session) -> Company:
    company = db.query(Company).filter(Company.recruiter_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not registered. Please register first.")
    return company


@router.post("/company", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def register_company(
    company_data: CompanyCreate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    existing = db.query(Company).filter(Company.recruiter_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already registered")

    company = Company(recruiter_id=current_user.id, **company_data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return CompanyResponse.model_validate(company)


@router.get("/company", response_model=CompanyResponse)
def get_company(
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    return CompanyResponse.model_validate(company)


@router.put("/company", response_model=CompanyResponse)
def update_company(
    company_data: CompanyUpdate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    for field, value in company_data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return CompanyResponse.model_validate(company)


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = Job(company_id=company.company_id, **job_data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return JobResponse(
        job_id=job.job_id,
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        required_skills=job.required_skills,
        salary=job.salary,
        experience=job.experience,
        location=job.location,
        company_id=job.company_id,
        is_active=job.is_active,
        company_name=company.company_name,
        created_at=job.created_at,
    )


@router.get("/jobs", response_model=list[JobResponse])
def get_my_jobs(
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    jobs = db.query(Job).filter(Job.company_id == company.company_id).all()
    return [
        JobResponse(
            job_id=j.job_id, title=j.title, description=j.description,
            requirements=j.requirements, required_skills=j.required_skills,
            salary=j.salary, experience=j.experience, location=j.location,
            company_id=j.company_id, is_active=j.is_active,
            company_name=company.company_name, created_at=j.created_at,
        )
        for j in jobs
    ]


@router.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = db.query(Job).filter(Job.job_id == job_id, Job.company_id == company.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for field, value in job_data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return JobResponse(
        job_id=job.job_id, title=job.title, description=job.description,
        requirements=job.requirements, required_skills=job.required_skills,
        salary=job.salary, experience=job.experience, location=job.location,
        company_id=job.company_id, is_active=job.is_active,
        company_name=company.company_name, created_at=job.created_at,
    )


@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = db.query(Job).filter(Job.job_id == job_id, Job.company_id == company.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


@router.get("/jobs/{job_id}/applicants", response_model=list[ApplicationResponse])
def get_applicants(
    job_id: int,
    sort_by: str = "match_score",
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = db.query(Job).filter(Job.job_id == job_id, Job.company_id == company.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    applications = db.query(Application).filter(Application.job_id == job_id).all()
    if sort_by == "match_score":
        applications.sort(key=lambda a: a.match_score, reverse=True)

    result = []
    for app in applications:
        candidate = app.candidate
        user = candidate.user if candidate else None
        result.append(ApplicationResponse(
            application_id=app.application_id,
            candidate_id=app.candidate_id,
            job_id=app.job_id,
            status=app.status,
            match_score=app.match_score,
            match_breakdown=app.match_breakdown,
            cover_letter=app.cover_letter,
            candidate_name=user.name if user else None,
            candidate_email=user.email if user else None,
            candidate_skills=candidate.skills if candidate else None,
            job_title=job.title,
            company_name=company.company_name,
            created_at=app.created_at,
            updated_at=app.updated_at,
        ))
    return result


@router.patch("/applications/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: int,
    status_data: ApplicationStatusUpdate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    application = db.query(Application).filter(Application.application_id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = db.query(Job).filter(
        Job.job_id == application.job_id, Job.company_id == company.company_id
    ).first()
    if not job:
        raise HTTPException(status_code=403, detail="Not authorized")

    application.status = status_data.status
    db.commit()
    db.refresh(application)

    candidate = application.candidate
    user = candidate.user if candidate else None
    if user:
        if status_data.status == ApplicationStatus.SHORTLISTED:
            notify_shortlisted(user.email, user.name, job.title)
            await notify_shortlisted_telegram(user.name, job.title, company.company_name)
        elif status_data.status == ApplicationStatus.REJECTED:
            notify_rejected(user.email, user.name, job.title)

    return ApplicationResponse(
        application_id=application.application_id,
        candidate_id=application.candidate_id,
        job_id=application.job_id,
        status=application.status,
        match_score=application.match_score,
        match_breakdown=application.match_breakdown,
        candidate_name=user.name if user else None,
        candidate_email=user.email if user else None,
        job_title=job.title,
        company_name=company.company_name,
        created_at=application.created_at,
        updated_at=application.updated_at,
    )


@router.post("/interviews", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
async def schedule_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = db.query(Job).filter(
        Job.job_id == interview_data.job_id, Job.company_id == company.company_id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    interview = Interview(**interview_data.model_dump())
    db.add(interview)

    application = db.query(Application).filter(
        Application.candidate_id == interview_data.candidate_id,
        Application.job_id == interview_data.job_id,
    ).first()
    if application:
        application.status = ApplicationStatus.INTERVIEW

    db.commit()
    db.refresh(interview)

    candidate = db.query(Candidate).filter(
        Candidate.candidate_id == interview_data.candidate_id
    ).first()
    user = candidate.user if candidate else None
    if user:
        notify_interview_scheduled(
            user.email, user.name, job.title,
            str(interview_data.date), str(interview_data.time),
            interview_data.meeting_link or "",
        )
        await notify_interview_telegram(
            user.name, job.title, str(interview_data.date), str(interview_data.time)
        )

    return InterviewResponse(
        interview_id=interview.interview_id,
        candidate_id=interview.candidate_id,
        job_id=interview.job_id,
        date=interview.date,
        time=interview.time,
        meeting_link=interview.meeting_link,
        notes=interview.notes,
        candidate_name=user.name if user else None,
        job_title=job.title,
        created_at=interview.created_at,
    )


@router.get("/interviews", response_model=list[InterviewResponse])
def get_interviews(
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job_ids = [j.job_id for j in db.query(Job).filter(Job.company_id == company.company_id).all()]
    interviews = db.query(Interview).filter(Interview.job_id.in_(job_ids)).all()

    result = []
    for iv in interviews:
        candidate = iv.candidate
        user = candidate.user if candidate else None
        result.append(InterviewResponse(
            interview_id=iv.interview_id,
            candidate_id=iv.candidate_id,
            job_id=iv.job_id,
            date=iv.date,
            time=iv.time,
            meeting_link=iv.meeting_link,
            notes=iv.notes,
            candidate_name=user.name if user else None,
            job_title=iv.job.title if iv.job else None,
            created_at=iv.created_at,
        ))
    return result


@router.post("/interview-questions", response_model=InterviewQuestionsResponse)
def get_interview_questions(
    request: InterviewQuestionsRequest,
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    job = db.query(Job).filter(
        Job.job_id == request.job_id, Job.company_id == company.company_id
    ).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidate = db.query(Candidate).filter(Candidate.candidate_id == request.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    user = candidate.user
    questions = generate_interview_questions(
        job.title, job.description, job.required_skills or "",
        candidate.skills or "", user.name if user else "Candidate",
    )
    return InterviewQuestionsResponse(
        questions=questions,
        job_title=job.title,
        candidate_name=user.name if user else "Candidate",
    )


@router.get("/analytics", response_model=RecruiterAnalytics)
def recruiter_analytics(
    current_user: User = Depends(require_roles(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    company = _get_company(current_user, db)
    jobs = db.query(Job).filter(Job.company_id == company.company_id).all()
    job_ids = [j.job_id for j in jobs]

    applications = db.query(Application).filter(Application.job_id.in_(job_ids)).all() if job_ids else []
    interviews = db.query(Interview).filter(Interview.job_id.in_(job_ids)).all() if job_ids else []

    status_counts = {}
    for app in applications:
        status_counts[app.status.value] = status_counts.get(app.status.value, 0) + 1

    hired = status_counts.get("hired", 0) + status_counts.get("offered", 0)
    total = len(applications) or 1

    return RecruiterAnalytics(
        total_jobs=len(jobs),
        active_jobs=len([j for j in jobs if j.is_active]),
        total_applications=len(applications),
        shortlisted=status_counts.get("shortlisted", 0),
        rejected=status_counts.get("rejected", 0),
        interviews_scheduled=len(interviews),
        hiring_rate=round((hired / total) * 100, 2),
        applications_by_status=status_counts,
    )
