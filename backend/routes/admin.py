from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from database import get_db
from models.user import User, UserRole
from models.company import Company
from models.job import Job
from models.candidate import Candidate
from models.application import Application, ApplicationStatus
from models.interview import Interview
from schemas.user import UserResponse, UserUpdate
from schemas.company import CompanyResponse
from schemas.job import JobResponse
from schemas.candidate import CandidateResponse
from schemas.application import ApplicationResponse
from schemas.analytics import AnalyticsOverview, TimeToHireData
from utils.dependencies import require_roles
from utils.security import get_password_hash

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/analytics", response_model=AnalyticsOverview)
def admin_analytics(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    total_jobs = db.query(Job).count()
    total_candidates = db.query(Candidate).count()
    total_applications = db.query(Application).count()
    shortlisted = db.query(Application).filter(
        Application.status == ApplicationStatus.SHORTLISTED
    ).count()
    rejected = db.query(Application).filter(
        Application.status == ApplicationStatus.REJECTED
    ).count()
    hired = db.query(Application).filter(
        Application.status.in_([ApplicationStatus.HIRED, ApplicationStatus.OFFERED])
    ).count()
    total_companies = db.query(Company).count()
    total_recruiters = db.query(User).filter(User.role == UserRole.RECRUITER).count()

    hiring_rate = round((hired / total_applications) * 100, 2) if total_applications else 0

    return AnalyticsOverview(
        total_jobs=total_jobs,
        total_candidates=total_candidates,
        total_applications=total_applications,
        shortlisted_candidates=shortlisted,
        rejected_candidates=rejected,
        hired_candidates=hired,
        hiring_rate=hiring_rate,
        total_companies=total_companies,
        total_recruiters=total_recruiters,
    )


@router.get("/analytics/time-to-hire", response_model=list[TimeToHireData])
def time_to_hire(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    hired_apps = db.query(Application).filter(
        Application.status.in_([ApplicationStatus.HIRED, ApplicationStatus.OFFERED])
    ).all()

    monthly_data = {}
    for app in hired_apps:
        if app.created_at and app.updated_at:
            days = (app.updated_at - app.created_at).days
            month_key = app.updated_at.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"days": [], "hires": 0}
            monthly_data[month_key]["days"].append(days)
            monthly_data[month_key]["hires"] += 1

    result = []
    for month, data in sorted(monthly_data.items()):
        avg_days = sum(data["days"]) / len(data["days"]) if data["days"] else 0
        result.append(TimeToHireData(
            month=month,
            avg_days=round(avg_days, 1),
            hires=data["hires"],
        ))
    return result


@router.get("/companies", response_model=list[CompanyResponse])
def get_all_companies(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return [CompanyResponse.model_validate(c) for c in db.query(Company).all()]


@router.get("/candidates", response_model=list[CandidateResponse])
def get_all_candidates(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    candidates = db.query(Candidate).all()
    result = []
    for c in candidates:
        user = c.user
        result.append(CandidateResponse(
            candidate_id=c.candidate_id, user_id=c.user_id,
            resume=c.resume, skills=c.skills, education=c.education,
            experience=c.experience, projects=c.projects,
            phone=c.phone, location=c.location, headline=c.headline,
            name=user.name if user else None,
            email=user.email if user else None,
            created_at=c.created_at,
        ))
    return result


@router.get("/recruiters", response_model=list[UserResponse])
def get_all_recruiters(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    recruiters = db.query(User).filter(User.role == UserRole.RECRUITER).all()
    return [UserResponse.model_validate(r) for r in recruiters]


@router.get("/jobs", response_model=list[JobResponse])
def get_all_jobs(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).all()
    return [
        JobResponse(
            job_id=j.job_id, title=j.title, description=j.description,
            requirements=j.requirements, required_skills=j.required_skills,
            salary=j.salary, experience=j.experience, location=j.location,
            company_id=j.company_id, is_active=j.is_active,
            company_name=j.company.company_name if j.company else None,
            created_at=j.created_at,
        )
        for j in jobs
    ]


@router.get("/applications", response_model=list[ApplicationResponse])
def get_all_applications(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    applications = db.query(Application).all()
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
            candidate_name=user.name if user else None,
            candidate_email=user.email if user else None,
            job_title=app.job.title if app.job else None,
            company_name=app.job.company.company_name if app.job and app.job.company else None,
            created_at=app.created_at,
            updated_at=app.updated_at,
        ))
    return result


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return [UserResponse.model_validate(u) for u in db.query(User).all()]


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@router.delete("/jobs/{job_id}")
def admin_delete_job(
    job_id: int,
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


@router.get("/reports")
def generate_report(
    report_type: str = "summary",
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    if report_type == "summary":
        return {
            "report_type": "summary",
            "generated_at": datetime.now().isoformat(),
            "total_users": db.query(User).count(),
            "total_companies": db.query(Company).count(),
            "total_jobs": db.query(Job).count(),
            "total_candidates": db.query(Candidate).count(),
            "total_applications": db.query(Application).count(),
            "applications_by_status": {
                status.value: db.query(Application).filter(Application.status == status).count()
                for status in ApplicationStatus
            },
        }
    elif report_type == "hiring":
        hired = db.query(Application).filter(
            Application.status.in_([ApplicationStatus.HIRED, ApplicationStatus.OFFERED])
        ).all()
        return {
            "report_type": "hiring",
            "generated_at": datetime.now().isoformat(),
            "total_hired": len(hired),
            "details": [
                {
                    "application_id": a.application_id,
                    "candidate": a.candidate.user.name if a.candidate and a.candidate.user else None,
                    "job": a.job.title if a.job else None,
                    "company": a.job.company.company_name if a.job and a.job.company else None,
                    "match_score": a.match_score,
                }
                for a in hired
            ],
        }
    raise HTTPException(status_code=400, detail="Invalid report type")
