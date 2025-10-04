from __future__ import annotations
from io import BytesIO
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import EvaluationCriteria, CandidateProfile
from .services.parser import (
    normalize_text,
    extract_email,
    extract_name,
    extract_phone,
    extract_skills,
    estimate_total_experience_years,
)
from .services.evaluator import evaluate_candidate

app = FastAPI(title="CV Analysis")

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
templates = Jinja2Templates(directory="backend/app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/evaluate", response_class=JSONResponse)
async def evaluate(
    file: UploadFile = File(...),
    required_skills: str = Form(""),
    preferred_skills: str = Form(""),
    min_years_experience: int = Form(0),
    education_keywords: str = Form(""),
):
    pdf_bytes = await file.read()

    # Extract text using pdfminer; if it fails, fall back to naive decode
    # Note: pdfminer.six usually accepts a file path or fp. We'll wrap bytes in BytesIO.
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(BytesIO(pdf_bytes))
    except Exception:
        try:
            text = pdf_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    text = normalize_text(text)

    profile = CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        total_years_experience=estimate_total_experience_years(text),
        skills=extract_skills(text),
        education=None,
        raw_text=text,
    )

    criteria = EvaluationCriteria(
        required_skills=[s.strip() for s in required_skills.split(",") if s.strip()],
        preferred_skills=[s.strip() for s in preferred_skills.split(",") if s.strip()],
        min_years_experience=min_years_experience,
        education_keywords=[s.strip() for s in education_keywords.split(",") if s.strip()],
    )

    result = evaluate_candidate(profile, criteria)

    return JSONResponse(
        {
            "profile": profile.model_dump(),
            "criteria": criteria.model_dump(),
            "result": result.model_dump(),
        }
    )
