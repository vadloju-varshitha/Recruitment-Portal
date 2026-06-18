from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from models.candidate import Candidate
from models.job import Job
from models.company import Company
from schemas.analytics import OfferLetterRequest, ExperienceLetterRequest, PayslipRequest
from utils.dependencies import require_roles
from pdf_generator.documents import generate_offer_letter, generate_experience_letter, generate_payslip
from email_service.email import notify_offer_letter
from telegram_service.bot import notify_offer_telegram

router = APIRouter(prefix="/pdf", tags=["PDF Generation"])


@router.post("/offer-letter")
async def create_offer_letter(
    data: OfferLetterRequest,
    current_user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    candidate = db.query(Candidate).filter(Candidate.candidate_id == data.candidate_id).first()
    job = db.query(Job).filter(Job.job_id == data.job_id).first()
    if not candidate or not job:
        return {"error": "Candidate or job not found"}

    company_name = job.company.company_name if job.company else "Company"
    user = candidate.user

    buffer = generate_offer_letter(
        candidate_name=user.name if user else "Candidate",
        company_name=company_name,
        position=data.position,
        salary=data.salary,
        start_date=data.start_date,
        template=data.template,
    )

    if user:
        notify_offer_letter(user.email, user.name, job.title)
        await notify_offer_telegram(user.name, job.title, company_name)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=offer_letter_{data.candidate_id}.pdf"},
    )


@router.post("/experience-letter")
def create_experience_letter(
    data: ExperienceLetterRequest,
    current_user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    candidate = db.query(Candidate).filter(Candidate.candidate_id == data.candidate_id).first()
    user = candidate.user if candidate else None

    buffer = generate_experience_letter(
        candidate_name=user.name if user else "Employee",
        company_name=data.company_name,
        position=data.position,
        start_date=data.start_date,
        end_date=data.end_date,
        responsibilities=data.responsibilities,
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=experience_letter_{data.candidate_id}.pdf"},
    )


@router.post("/payslip")
def create_payslip(
    data: PayslipRequest,
    current_user: User = Depends(require_roles(UserRole.RECRUITER, UserRole.ADMIN)),
):
    buffer = generate_payslip(
        employee_name=data.employee_name,
        employee_id=data.employee_id,
        month=data.month,
        year=data.year,
        basic_salary=data.basic_salary,
        hra=data.hra,
        allowances=data.allowances,
        deductions=data.deductions,
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=payslip_{data.employee_id}.pdf"},
    )


@router.get("/offer-templates")
def get_offer_templates():
    return {
        "templates": [
            {"id": "standard", "name": "Standard Offer Letter"},
            {"id": "executive", "name": "Executive Offer Letter"},
            {"id": "intern", "name": "Internship Offer Letter"},
        ]
    }
