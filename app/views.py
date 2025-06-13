from django.shortcuts import render

# Create your views here.
# app/views.py

from django.http import HttpResponse

def home(request):
    return render(request,'home.html')



import json
from django.shortcuts import render, redirect
from .models import Job, ResumeMatch
from .lyzr_client import extract_skills_from_resume_via_lyzr

AGENT_ID = "684bbacbe5203d8a7b64bdc2"
SESSION_ID = "684bbacbe5203d8a7b64bdc2-n3qo951m6vh"
from django.shortcuts import render, redirect
from .models import Job

def job_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        skills = request.POST.get("skills", "")  # comma-separated
        if title and skills:
            Job.objects.create(title=title, description=description, skills=skills)
            return redirect("find_job")  # Redirect to job list or find page
        else:
            error = "Title and skills are required."
            return render(request, "create-job.html", {"error": error})

    return render(request, "create-job.html")
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import Job
from .lyzr_client import extract_skills_from_resume_via_lyzr
from PyPDF2 import PdfReader
import docx

AGENT_ID = "684bbacbe5203d8a7b64bdc2"
SESSION_ID = "684bbacbe5203d8a7b64bdc2-n3qo951m6vh"

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def find_job(request):
    matched_jobs = []
    error = None

    if request.method == "POST":
        uploaded_file = request.FILES.get("resume")
        if not uploaded_file:
            error = "Please upload your resume file."
        else:
            filename = uploaded_file.name.lower()
            try:
                if filename.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(uploaded_file)
                elif filename.endswith(".docx"):
                    resume_text = extract_text_from_docx(uploaded_file)
                elif filename.endswith(".txt"):
                    try:
                        resume_text = uploaded_file.read().decode('utf-8')
                    except UnicodeDecodeError:
                        resume_text = uploaded_file.read().decode('latin-1', errors='ignore')
                else:
                    error = "Unsupported file type. Please upload PDF, DOCX or TXT."
                    resume_text = ""
            except Exception as e:
                error = f"Failed to extract text: {str(e)}"
                resume_text = ""

            if resume_text:
                try:
                    extracted_skills = extract_skills_from_resume_via_lyzr(
                        user_id="rudrampanchal@gmail.com",
                        agent_id=AGENT_ID,
                        session_id=SESSION_ID,
                        resume_text=resume_text
                    )
                except Exception as e:
                    error = f"Error extracting skills: {str(e)}"
                    extracted_skills = []

                if extracted_skills:
                    # Debug print to see extracted skills
                    print("Extracted skills from resume:", extracted_skills)

                    resume_skills = [s.strip().lower() for s in extracted_skills if s.strip()]
                    all_jobs = Job.objects.all()

                    for job in all_jobs:
                        job_skills = job.get_skill_list()
                        if not job_skills:
                            continue

                        match_count = len(set(resume_skills) & set(job_skills))
                        match_percent = (match_count / len(job_skills)) * 100

                        if match_percent >= 50:
                            matched_jobs.append((job, round(match_percent, 1)))

                    if not matched_jobs:
                        error = error or "No matching jobs found for your skills."
                else:
                    error = error or "No skills found in the resume."
            else:
                error = error or "No resume text extracted."

    return render(request, "find-job.html", {
        "matched_jobs": matched_jobs,
        "error": error,
    })
