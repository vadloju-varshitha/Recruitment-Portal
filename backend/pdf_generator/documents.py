from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime


OFFER_TEMPLATES = {
    "standard": {
        "header": "OFFER OF EMPLOYMENT",
        "intro": "We are pleased to offer you the position of {position} at our organization.",
    },
    "executive": {
        "header": "EXECUTIVE OFFER LETTER",
        "intro": "It is with great pleasure that we extend this executive offer for the role of {position}.",
    },
    "intern": {
        "header": "INTERNSHIP OFFER LETTER",
        "intro": "We are delighted to offer you an internship position as {position}.",
    },
}


def generate_offer_letter(
    candidate_name: str,
    company_name: str,
    position: str,
    salary: str,
    start_date: str,
    template: str = "standard",
) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1 * inch)
    styles = getSampleStyleSheet()
    story = []

    tmpl = OFFER_TEMPLATES.get(template, OFFER_TEMPLATES["standard"])

    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], alignment=TA_CENTER, spaceAfter=30
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], alignment=TA_JUSTIFY, spaceAfter=12, leading=16
    )

    story.append(Paragraph(tmpl["header"], title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Dear {candidate_name},", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(tmpl["intro"].format(position=position), body_style))
    story.append(Paragraph(
        f"We believe your skills and experience make you an excellent fit for our team. "
        f"This letter outlines the terms of your employment with {company_name}.",
        body_style,
    ))

    details = [
        ["Position:", position],
        ["Annual Salary:", salary],
        ["Start Date:", start_date],
        ["Company:", company_name],
    ]
    table = Table(details, colWidths=[2 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(Spacer(1, 20))
    story.append(table)
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "This offer is contingent upon successful completion of background verification. "
        "Please sign and return this letter to confirm your acceptance.",
        body_style,
    ))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Sincerely,", body_style))
    story.append(Paragraph(f"{company_name} HR Department", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_experience_letter(
    candidate_name: str,
    company_name: str,
    position: str,
    start_date: str,
    end_date: str,
    responsibilities: str,
) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1 * inch)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], alignment=TA_CENTER, spaceAfter=30
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], alignment=TA_JUSTIFY, spaceAfter=12, leading=16
    )

    story.append(Paragraph("EXPERIENCE CERTIFICATE", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("To Whom It May Concern,", body_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"This is to certify that <b>{candidate_name}</b> was employed with "
        f"<b>{company_name}</b> as <b>{position}</b> from <b>{start_date}</b> "
        f"to <b>{end_date}</b>.",
        body_style,
    ))
    story.append(Paragraph(
        f"During their tenure, {candidate_name} was responsible for: {responsibilities}",
        body_style,
    ))
    story.append(Paragraph(
        f"We found {candidate_name} to be diligent, hardworking, and a valuable team member. "
        f"We wish them all the best in their future endeavors.",
        body_style,
    ))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Authorized Signatory", body_style))
    story.append(Paragraph(f"{company_name}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_payslip(
    employee_name: str,
    employee_id: str,
    month: str,
    year: str,
    basic_salary: float,
    hra: float = 0,
    allowances: float = 0,
    deductions: float = 0,
) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    story = []

    gross = basic_salary + hra + allowances
    net = gross - deductions

    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], alignment=TA_CENTER, spaceAfter=20
    )

    story.append(Paragraph("SALARY PAYSLIP", title_style))
    story.append(Paragraph(f"Pay Period: {month} {year}", styles["Normal"]))
    story.append(Spacer(1, 20))

    info = [
        ["Employee Name:", employee_name, "Employee ID:", employee_id],
    ]
    info_table = Table(info, colWidths=[1.5 * inch, 2 * inch, 1.5 * inch, 2 * inch])
    info_table.setStyle(TableStyle([
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 20))

    earnings = [
        ["Earnings", "Amount (INR)", "Deductions", "Amount (INR)"],
        ["Basic Salary", f"{basic_salary:,.2f}", "Total Deductions", f"{deductions:,.2f}"],
        ["HRA", f"{hra:,.2f}", "", ""],
        ["Allowances", f"{allowances:,.2f}", "", ""],
        ["Gross Earnings", f"{gross:,.2f}", "Net Pay", f"{net:,.2f}"],
    ]
    pay_table = Table(earnings, colWidths=[2 * inch, 1.5 * inch, 2 * inch, 1.5 * inch])
    pay_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))
    story.append(pay_table)
    story.append(Spacer(1, 30))
    story.append(Paragraph("This is a computer-generated payslip.", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
