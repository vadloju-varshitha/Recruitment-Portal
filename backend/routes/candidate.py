import os
import shutil
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.candidate import Candidate
from models.application import Application
from models.job import Job
from schemas.candidate import CandidateProfileCreate, CandidateProfileUpdate, CandidateResponse
from schemas.application import ApplicationCreate, ApplicationResponse
from schemas.analytics import SkillGapAnalysis
from utils.dependencies import get_current_user, require_roles
from models.user import UserRole
from services.match_service import calculate_match_score, analyze_skill_gap
from services.resume_parser import parse_resume
from email_service.email import notify_application_submitted
from config import get_settings

router = APIRouter(prefix="/candidate", tags=["Candidate"])
settings = get_settings()


def _candidate_response(candidate: Candidate, user: User) -> CandidateResponse:
    return CandidateResponse(
        candidate_id=candidate.candidate_id,
        user_id=candidate.user_id,
        resume=candidate.resume,
        skills=candidate.skills,
        education=candidate.education,
        experience=candidate.experience,
        projects=candidate.projects,
        phone=candidate.phone,
        location=candidate.location,
        headline=candidate.headline,
        name=user.name,
        email=user.email,
        created_at=candidate.created_at,
    )


def _get_candidate_profile(current_user: User, db: Session) -> Candidate:
    candidate = db.query(Candidate).filter(Candidate.user_id == current_user.id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    return candidate


@router.get("/profile", response_model=CandidateResponse)
def get_profile(
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    return _candidate_response(candidate, current_user)


@router.put("/profile", response_model=CandidateResponse)
def update_profile(
    profile_data: CandidateProfileUpdate,
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(candidate, field, value)
    db.commit()
    db.refresh(candidate)
    return _candidate_response(candidate, current_user)


@router.post("/profile", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_data: CandidateProfileCreate,
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = db.query(Candidate).filter(Candidate.user_id == current_user.id).first()
    if not candidate:
        candidate = Candidate(user_id=current_user.id)
        db.add(candidate)
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(candidate, field, value)
    db.commit()
    db.refresh(candidate)
    return _candidate_response(candidate, current_user)


@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    candidate = _get_candidate_profile(current_user, db)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, f"{candidate.candidate_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    parsed = parse_resume(file_path)
    candidate.resume = file_path
    if parsed.get("skills"):
        existing_skills = candidate.skills or ""
        new_skills = ", ".join(parsed["skills"])
        candidate.skills = f"{existing_skills}, {new_skills}".strip(", ") if existing_skills else new_skills
    if parsed.get("education") and not candidate.education:
        candidate.education = parsed["education"]
    if parsed.get("experience") and not candidate.experience:
        candidate.experience = parsed["experience"]
    if parsed.get("projects") and not candidate.projects:
        candidate.projects = parsed["projects"]

    db.commit()
    return {
        "message": "Resume uploaded successfully",
        "parsed_data": parsed,
        "file_path": file_path,
    }


@router.get("/jobs")
def search_jobs(
    query: str = "",
    location: str = "",
    experience: str = "",
    db: Session = Depends(get_db),
):
    jobs_query = db.query(Job).filter(Job.is_active == True)
    if query:
        jobs_query = jobs_query.filter(
            Job.title.ilike(f"%{query}%") | Job.description.ilike(f"%{query}%")
        )
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f"%{location}%"))
    if experience:
        jobs_query = jobs_query.filter(Job.experience.ilike(f"%{experience}%"))

    jobs = jobs_query.all()
    result = []
    for job in jobs:
        result.append({
            "job_id": job.job_id,
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements,
            "required_skills": job.required_skills,
            "salary": job.salary,
            "experience": job.experience,
            "location": job.location,
            "company_id": job.company_id,
            "company_name": job.company.company_name if job.company else None,
            "created_at": job.created_at,
        })
    return result


@router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    application_data: ApplicationCreate,
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    job = db.query(Job).filter(Job.job_id == application_data.job_id, Job.is_active == True).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = db.query(Application).filter(
        Application.candidate_id == candidate.candidate_id,
        Application.job_id == application_data.job_id,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied for this job")

    score, breakdown = calculate_match_score(
        job.required_skills or "", candidate.skills or ""
    )

    application = Application(
        candidate_id=candidate.candidate_id,
        job_id=application_data.job_id,
        cover_letter=application_data.cover_letter,
        match_score=score,
        match_breakdown=json.dumps(breakdown),
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    notify_application_submitted(current_user.email, current_user.name, job.title)

    return ApplicationResponse(
        application_id=application.application_id,
        candidate_id=application.candidate_id,
        job_id=application.job_id,
        status=application.status,
        match_score=application.match_score,
        match_breakdown=application.match_breakdown,
        cover_letter=application.cover_letter,
        candidate_name=current_user.name,
        job_title=job.title,
        company_name=job.company.company_name if job.company else None,
        created_at=application.created_at,
    )


@router.get("/applications", response_model=list[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    applications = db.query(Application).filter(
        Application.candidate_id == candidate.candidate_id
    ).all()

    result = []
    for app in applications:
        result.append(ApplicationResponse(
            application_id=app.application_id,
            candidate_id=app.candidate_id,
            job_id=app.job_id,
            status=app.status,
            match_score=app.match_score,
            match_breakdown=app.match_breakdown,
            cover_letter=app.cover_letter,
            job_title=app.job.title if app.job else None,
            company_name=app.job.company.company_name if app.job and app.job.company else None,
            created_at=app.created_at,
            updated_at=app.updated_at,
        ))
    return result


@router.get("/dashboard")
def candidate_dashboard(
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    applications = db.query(Application).filter(
        Application.candidate_id == candidate.candidate_id
    ).all()

    status_counts = {}
    for app in applications:
        status_counts[app.status.value] = status_counts.get(app.status.value, 0) + 1

    return {
        "total_applications": len(applications),
        "status_breakdown": status_counts,
        "recent_applications": [
            {
                "application_id": a.application_id,
                "job_title": a.job.title if a.job else None,
                "company_name": a.job.company.company_name if a.job and a.job.company else None,
                "status": a.status.value,
                "match_score": a.match_score,
                "created_at": a.created_at,
            }
            for a in sorted(applications, key=lambda x: x.created_at or "", reverse=True)[:5]
        ],
    }


@router.get("/skill-gap/{job_id}", response_model=SkillGapAnalysis)
def get_skill_gap(
    job_id: int,
    current_user: User = Depends(require_roles(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    candidate = _get_candidate_profile(current_user, db)
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    result = analyze_skill_gap(
        job.required_skills or "", candidate.skills or "", job.title
    )
    return SkillGapAnalysis(**result)
