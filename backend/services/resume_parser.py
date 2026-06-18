import re
from typing import Dict, List, Optional
from PyPDF2 import PdfReader


SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "react", "angular", "vue",
    "node.js", "django", "flask", "fastapi", "sql", "postgresql", "mysql",
    "mongodb", "redis", "docker", "kubernetes", "aws", "azure", "gcp",
    "machine learning", "deep learning", "tensorflow", "pytorch", "nlp",
    "data analysis", "pandas", "numpy", "scikit-learn", "git", "linux",
    "html", "css", "tailwind", "rest api", "graphql", "microservices",
    "agile", "scrum", "c++", "c#", "go", "rust", "ruby", "php", "spring",
    "express", "next.js", "devops", "ci/cd", "jenkins", "terraform",
    "power bi", "tableau", "excel", "spark", "hadoop", "kafka",
]


def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception:
        return ""


def extract_keywords(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for keyword in SKILL_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword.title())
    return list(set(found))


def extract_emails(text: str) -> List[str]:
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def extract_phones(text: str) -> List[str]:
    pattern = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    return re.findall(pattern, text)


def extract_entities_spacy(text: str) -> List[str]:
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text[:10000])
        entities = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT", "SKILL")]
        return list(set(entities))[:20]
    except Exception:
        return []


def parse_resume(file_path: str) -> Dict:
    text = extract_text_from_pdf(file_path)
    if not text:
        return {"skills": [], "keywords": [], "emails": [], "phones": [], "raw_text": ""}

    keywords = extract_keywords(text)
    spacy_entities = extract_entities_spacy(text)
    if spacy_entities:
        keywords = list(set(keywords + spacy_entities))
    emails = extract_emails(text)
    phones = extract_phones(text)

    education_section = _extract_section(text, ["education", "qualification", "academic"])
    experience_section = _extract_section(text, ["experience", "employment", "work history"])
    projects_section = _extract_section(text, ["projects", "portfolio"])

    return {
        "skills": keywords,
        "keywords": keywords,
        "emails": emails,
        "phones": [p if isinstance(p, str) else "".join(p) for p in phones],
        "education": education_section[:500] if education_section else "",
        "experience": experience_section[:500] if experience_section else "",
        "projects": projects_section[:500] if projects_section else "",
        "raw_text": text[:2000],
    }


def _extract_section(text: str, headers: List[str]) -> str:
    text_lower = text.lower()
    for header in headers:
        idx = text_lower.find(header)
        if idx != -1:
            return text[idx : idx + 500].strip()
    return ""
