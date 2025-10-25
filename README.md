# Resume Parser AI — Basic (CSV)

A minimal, college‑friendly resume parser built with Flask. Upload a PDF/DOCX/TXT resume, parse basic fields, and save to `parsed_resumes.csv`.

## Features
- Upload PDF / DOCX / TXT
- Extract Name, Email, Phone, Skills, Education, Experience (years*)
- Save results to CSV
- View saved records at `/records`

*Experience years are heuristics based on text patterns and year ranges; it's intentionally simple for clarity during viva.*

## Tech Stack
- Python, Flask
- `pdfminer.six` for PDFs
- `docx2txt` for DOCX
- No heavy NLP models to keep setup simple

## Setup
```bash
# 1) Create venv (recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run
python app.py
# Open http://127.0.0.1:5000
```

## Project Structure
```
ResumeParserAI/
├── app.py
├── parser.py
├── utils.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── records.html
├── static/
│   └── style.css
├── sample_resumes/
│   └── sample_resume.txt
├── requirements.txt
└── README.md
```

## Notes for Presentation
- Emphasize **problem** (manual screening slow, error-prone) and **solution** (automated parsing).
- Walk through **flow**: Upload → Extract → Display → Save CSV → Records.
- Explain **limitations**: regex-based extraction is simple; future work can add spaCy/TF‑IDF matching, job description upload, better skill ontology.

## Future Improvements (if asked)
- Add TF‑IDF cosine similarity for JD matching
- Use spaCy NER for more robust names/ORG/EDU extraction
- SQLite storage and admin dashboard
