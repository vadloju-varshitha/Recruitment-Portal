from typing import List
from config import get_settings

settings = get_settings()


def generate_interview_questions(
    job_title: str,
    job_description: str,
    required_skills: str,
    candidate_skills: str,
    candidate_name: str,
) -> List[str]:
    if settings.GEMINI_API_KEY:
        try:
            return _generate_with_gemini(
                job_title, job_description, required_skills, candidate_skills, candidate_name
            )
        except Exception:
            pass

    return _generate_fallback_questions(job_title, required_skills, candidate_skills)


def _generate_with_gemini(
    job_title: str,
    job_description: str,
    required_skills: str,
    candidate_skills: str,
    candidate_name: str,
) -> List[str]:
    import google.generativeai as genai

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Generate 8 technical interview questions for the following scenario:

Job Title: {job_title}
Job Description: {job_description[:500]}
Required Skills: {required_skills}
Candidate Skills: {candidate_skills}
Candidate Name: {candidate_name}

Return only the questions, one per line, numbered 1-8. Mix behavioral and technical questions."""

    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")
    questions = [line.strip().lstrip("0123456789.) ") for line in lines if line.strip()]
    return questions[:8]


def _generate_fallback_questions(
    job_title: str, required_skills: str, candidate_skills: str
) -> List[str]:
    skills = required_skills.split(",") if required_skills else ["general programming"]
    skills = [s.strip() for s in skills if s.strip()][:3]

    questions = [
        f"Tell us about your experience relevant to the {job_title} role.",
        "Describe a challenging project you worked on and how you overcame obstacles.",
        "How do you stay updated with industry trends and new technologies?",
        f"Explain your proficiency in {skills[0] if skills else 'your primary skill'}.",
        "Describe a situation where you had to work under tight deadlines.",
        "How do you approach debugging complex issues?",
        "Tell us about a time you collaborated with a cross-functional team.",
        "Where do you see yourself professionally in the next 3 years?",
    ]
    return questions
