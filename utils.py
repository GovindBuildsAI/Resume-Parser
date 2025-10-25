from io import StringIO
from pdfminer.high_level import extract_text
import docx2txt

def read_pdf_text(path):
    try:
        return extract_text(path) or ""
    except Exception:
        return ""

def read_docx_text(path):
    try:
        return docx2txt.process(path) or ""
    except Exception:
        return ""

def read_txt_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""

def simple_skill_list():
    # Small, demonstrative list; expand easily
    return [
        "python","java","c","c++","javascript","html","css","sql","mysql","postgresql",
        "mongodb","flask","django","react","node.js","tensorflow","pytorch","scikit-learn",
        "nlp","computer vision","data analysis","pandas","numpy","matplotlib","git","docker",
        "linux","aws","azure","gcp","kubernetes","fastapi","oop","dsa"
    ]
