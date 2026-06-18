import httpx
from config import get_settings

settings = get_settings()


async def send_telegram_message(message: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print(f"[TELEGRAM MOCK] {message}")
        return True

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10)
            return response.status_code == 200
    except Exception as e:
        print(f"Telegram send failed: {e}")
        return False


async def notify_shortlisted_telegram(candidate_name: str, job_title: str, company_name: str):
    message = (
        f"⭐ <b>Candidate Shortlisted</b>\n"
        f"Candidate: {candidate_name}\n"
        f"Job: {job_title}\n"
        f"Company: {company_name}"
    )
    await send_telegram_message(message)


async def notify_interview_telegram(
    candidate_name: str, job_title: str, date: str, time: str
):
    message = (
        f"📅 <b>Interview Scheduled</b>\n"
        f"Candidate: {candidate_name}\n"
        f"Job: {job_title}\n"
        f"Date: {date}\n"
        f"Time: {time}"
    )
    await send_telegram_message(message)


async def notify_offer_telegram(candidate_name: str, job_title: str, company_name: str):
    message = (
        f"🎉 <b>Offer Letter Generated</b>\n"
        f"Candidate: {candidate_name}\n"
        f"Job: {job_title}\n"
        f"Company: {company_name}"
    )
    await send_telegram_message(message)
