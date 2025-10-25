import os
import re
from utils import read_pdf_text, read_docx_text, read_txt_text, simple_skill_list

DEGREE_KEYWORDS = [
    "B.E", "B.Tech", "BTech", "B Sc", "B.Sc", "BCA", "BCom", "B.Com",
    "M.E", "M.Tech", "MTech", "M Sc", "M.Sc", "MCA", "MBA", "PhD", "Diploma", "PUC", "12th", "10th"
]

def extract_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else ""

def extract_phone(text):
    # Indian formats + general; keeps only digits and '+'
    m = re.search(r"(\+?\d[\d\-\s]{8,}\d)", text)
    if not m:
        return ""
    phone = re.sub(r"[^+\d]", "", m.group(0))
    # Take last 12-13 chars if too long
    return phone[-13:] if len(phone) > 13 else phone

def guess_name(text):
    # Very naive: look for a line starting with letters and spaces (title case), exclude common headings
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    blacklist = {"resume", "curriculum vitae", "cv", "profile", "contact", "details"}
    for l in lines[:10]:  # top region
        pure = re.sub(r"[^A-Za-z\s\.]", "", l).strip()
        if not pure:
            continue
        if pure.lower() in blacklist:
            continue
        # Likely a name if 1-4 words, title case
        parts = pure.split()
        if 1 <= len(parts) <= 4 and all(p[0:1].isupper() for p in parts):
            return pure
    return ""

def extract_skills(text):
    skills = []
    base = set(s.lower() for s in simple_skill_list())
    text_l = text.lower()
    for s in base:
        # exact word match or with separators
        if re.search(rf"(?<![a-zA-Z0-9]){re.escape(s)}(?![a-zA-Z0-9])", text_l):
            skills.append(s)
    # normalize capitalization
    return sorted({s.upper() if s in {"c"} else s.title() for s in skills})

def extract_education(text):
    results = []
    for deg in DEGREE_KEYWORDS:
        if re.search(rf"\b{re.escape(deg)}\b", text, flags=re.IGNORECASE):
            results.append(deg.upper())
    return sorted(set(results))

def estimate_experience_years(text):
    # Look for patterns like "X years", "X+ years", "2019-2022" differences etc.
    years = 0
    for m in re.finditer(r"(\d{1,2})\s*\+?\s*years", text, flags=re.IGNORECASE):
        try:
            years = max(years, int(m.group(1)))
        except:
            pass
    # crude add based on ranges like 2019-2022
    for m in re.finditer(r"(20\d{2})\s*[-–]\s*(20\d{2}|Present|Current)", text, flags=re.IGNORECASE):
        start = int(m.group(1))
        end = m.group(2)
        end_year = 2025 if end.lower() in {"present", "current"} else int(end)
        years = max(years, max(0, end_year - start))
    return years if years else ""

def read_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return read_pdf_text(file_path)
    if ext == ".docx":
        return read_docx_text(file_path)
    if ext == ".txt":
        return read_txt_text(file_path)
    return ""

def parse_resume(file_path):
    text = read_text(file_path)
    if not text:
        return {"error": "Could not read text from file.", "raw_text": ""}

    name = guess_name(text)
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    exp_years = estimate_experience_years(text)

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience_years": exp_years,
        "raw_text": text
    }
