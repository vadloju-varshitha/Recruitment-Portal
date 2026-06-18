import json
from typing import List, Dict, Tuple


def parse_skills(skills_text: str) -> List[str]:
    if not skills_text:
        return []
    separators = [",", ";", "|", "\n"]
    skills = [skills_text]
    for sep in separators:
        new_skills = []
        for s in skills:
            new_skills.extend(s.split(sep))
        skills = new_skills
    return list({s.strip().lower() for s in skills if s.strip()})


def calculate_match_score(
    job_skills: str, candidate_skills: str
) -> Tuple[float, Dict]:
    required = parse_skills(job_skills)
    candidate = parse_skills(candidate_skills)

    if not required:
        return 100.0, {
            "matched_skills": candidate,
            "missing_skills": [],
            "total_required": 0,
            "total_matched": len(candidate),
            "match_percentage": 100.0,
        }

    matched = [s for s in required if s in candidate]
    missing = [s for s in required if s not in candidate]
    percentage = round((len(matched) / len(required)) * 100, 2)

    breakdown = {
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required": len(required),
        "total_matched": len(matched),
        "match_percentage": percentage,
    }
    return percentage, breakdown


def analyze_skill_gap(job_skills: str, candidate_skills: str, job_title: str) -> Dict:
    percentage, breakdown = calculate_match_score(job_skills, candidate_skills)
    recommendations = []
    for skill in breakdown["missing_skills"]:
        recommendations.append(f"Learn or improve {skill.title()} to better match this role")

    if not recommendations:
        recommendations.append("Great match! Focus on interview preparation.")

    return {
        "job_title": job_title,
        "required_skills": parse_skills(job_skills),
        "candidate_skills": parse_skills(candidate_skills),
        "matched_skills": breakdown["matched_skills"],
        "missing_skills": breakdown["missing_skills"],
        "match_percentage": percentage,
        "recommendations": recommendations,
    }
