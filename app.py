from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from parser import parse_resume
import csv

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
CSV_PATH = "parsed_resumes.csv"

app = Flask(__name__)
app.secret_key = "resume-parser-secret"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "resume" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["resume"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            # Parse
            parsed = parse_resume(save_path)

            # Save to CSV (append mode)
            fieldnames = ["filename", "name", "email", "phone", "skills", "education", "experience_years", "raw_text_chars"]
            file_exists = os.path.isfile(CSV_PATH)
            with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    "filename": filename,
                    "name": parsed.get("name", ""),
                    "email": parsed.get("email", ""),
                    "phone": parsed.get("phone", ""),
                    "skills": ", ".join(parsed.get("skills", [])),
                    "education": "; ".join(parsed.get("education", [])),
                    "experience_years": parsed.get("experience_years", ""),
                    "raw_text_chars": len(parsed.get("raw_text", ""))
                })

            return render_template("result.html", data=parsed, filename=filename)
        else:
            flash("Unsupported file type. Please upload PDF, DOCX, or TXT.")
            return redirect(request.url)
    return render_template("index.html")

@app.route("/records")
def records():
    # Simple viewer for CSV records
    rows = []
    if os.path.isfile(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    return render_template("records.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
