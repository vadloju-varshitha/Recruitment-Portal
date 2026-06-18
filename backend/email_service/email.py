import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_settings

settings = get_settings()


def send_email(to_email: str, subject: str, body: str) -> bool:
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[EMAIL MOCK] To: {to_email} | Subject: {subject}")
        return True

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email send failed: {e}")
        return False


def notify_application_submitted(candidate_email: str, candidate_name: str, job_title: str):
    subject = f"Application Submitted - {job_title}"
    body = f"""
    <h2>Application Received</h2>
    <p>Dear {candidate_name},</p>
    <p>Your application for <strong>{job_title}</strong> has been successfully submitted.</p>
    <p>We will review your profile and get back to you soon.</p>
    <p>Best regards,<br>Recruitment Portal Team</p>
    """
    send_email(candidate_email, subject, body)


def notify_shortlisted(candidate_email: str, candidate_name: str, job_title: str):
    subject = f"Congratulations! You've been shortlisted - {job_title}"
    body = f"""
    <h2>You've Been Shortlisted!</h2>
    <p>Dear {candidate_name},</p>
    <p>Great news! You have been shortlisted for the position of <strong>{job_title}</strong>.</p>
    <p>Our team will contact you shortly for the next steps.</p>
    <p>Best regards,<br>Recruitment Portal Team</p>
    """
    send_email(candidate_email, subject, body)


def notify_rejected(candidate_email: str, candidate_name: str, job_title: str):
    subject = f"Application Update - {job_title}"
    body = f"""
    <h2>Application Update</h2>
    <p>Dear {candidate_name},</p>
    <p>Thank you for your interest in the <strong>{job_title}</strong> position.</p>
    <p>After careful consideration, we have decided to move forward with other candidates.</p>
    <p>We encourage you to apply for other openings that match your profile.</p>
    <p>Best regards,<br>Recruitment Portal Team</p>
    """
    send_email(candidate_email, subject, body)


def notify_interview_scheduled(
    candidate_email: str,
    candidate_name: str,
    job_title: str,
    date: str,
    time: str,
    meeting_link: str = "",
):
    subject = f"Interview Scheduled - {job_title}"
    link_html = f"<p>Meeting Link: <a href='{meeting_link}'>{meeting_link}</a></p>" if meeting_link else ""
    body = f"""
    <h2>Interview Scheduled</h2>
    <p>Dear {candidate_name},</p>
    <p>Your interview for <strong>{job_title}</strong> has been scheduled.</p>
    <p><strong>Date:</strong> {date}</p>
    <p><strong>Time:</strong> {time}</p>
    {link_html}
    <p>Please be prepared and join on time.</p>
    <p>Best regards,<br>Recruitment Portal Team</p>
    """
    send_email(candidate_email, subject, body)


def notify_offer_letter(candidate_email: str, candidate_name: str, job_title: str):
    subject = f"Offer Letter - {job_title}"
    body = f"""
    <h2>Offer Letter Generated</h2>
    <p>Dear {candidate_name},</p>
    <p>Congratulations! An offer letter for the position of <strong>{job_title}</strong> has been generated.</p>
    <p>Please check your dashboard to download the offer letter.</p>
    <p>Best regards,<br>Recruitment Portal Team</p>
    """
    send_email(candidate_email, subject, body)
