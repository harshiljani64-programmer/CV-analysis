from __future__ import annotations
from typing import List
import streamlit as st

from backend.app.models import EvaluationCriteria, CandidateProfile
from backend.app.services import parser
from backend.app.services.evaluator import evaluate_candidate


def parse_criteria(
    required_skills_text: str,
    preferred_skills_text: str,
    min_years_experience: int,
    education_keywords_text: str,
) -> EvaluationCriteria:
    required = [s.strip() for s in required_skills_text.split(",") if s.strip()]
    preferred = [s.strip() for s in preferred_skills_text.split(",") if s.strip()]
    education = [s.strip() for s in education_keywords_text.split(",") if s.strip()]
    return EvaluationCriteria(
        required_skills=required,
        preferred_skills=preferred,
        min_years_experience=min_years_experience,
        education_keywords=education,
    )


def build_profile_from_pdf(pdf_bytes: bytes) -> CandidateProfile:
    try:
        text = parser.extract_text_from_pdf(pdf_bytes)
    except Exception:
        try:
            text = pdf_bytes.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    text = parser.normalize_text(text)

    return CandidateProfile(
        name=parser.extract_name(text),
        email=parser.extract_email(text),
        phone=parser.extract_phone(text),
        total_years_experience=parser.estimate_total_experience_years(text),
        skills=parser.extract_skills(text),
        raw_text=text,
    )


st.set_page_config(page_title="CV Analysis", page_icon="📄", layout="centered")
st.title("📄 CV Analysis")
st.caption("Upload a PDF resume and evaluate against your criteria.")

with st.sidebar:
    st.header("Evaluation Criteria")
    required_skills_text = st.text_input(
        "Required skills (comma-separated)", value="python, fastapi, sql"
    )
    preferred_skills_text = st.text_input(
        "Preferred skills (comma-separated)", value="docker, aws"
    )
    min_years_experience = st.number_input(
        "Minimum years of experience", min_value=0, value=0, step=1
    )
    education_keywords_text = st.text_input(
        "Education keywords (comma-separated)", value="bachelor, master, phd"
    )

uploaded = st.file_uploader("Resume PDF", type=["pdf"], accept_multiple_files=False)

if uploaded is not None:
    with st.spinner("Parsing resume..."):
        pdf_bytes = uploaded.getvalue()
        profile = build_profile_from_pdf(pdf_bytes)

    st.subheader("Extracted Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Name**:", profile.name or "-")
        st.write("**Email**:", profile.email or "-")
        st.write("**Phone**:", profile.phone or "-")
    with col2:
        st.write("**Experience (years)**:", profile.total_years_experience or "-")
        st.write("**Skills (sample)**:", ", ".join(profile.skills[:20]) if profile.skills else "-")

    criteria = parse_criteria(
        required_skills_text,
        preferred_skills_text,
        int(min_years_experience),
        education_keywords_text,
    )

    if st.button("Evaluate Candidate", use_container_width=True):
        result = evaluate_candidate(profile, criteria)

        st.subheader("Evaluation Result")
        st.metric("Score", f"{result.score:.2f}")
        st.write("**Breakdown**")
        st.json(result.breakdown)

        st.write("**Matched required skills**")
        st.write(", ".join(result.matched_required_skills) or "-")
        st.write("**Matched preferred skills**")
        st.write(", ".join(result.matched_preferred_skills) or "-")

        st.write("**Meets minimum experience**:", "✅ Yes" if result.meets_min_experience else "❌ No")
        st.write("**Education match**:", "✅ Yes" if result.education_match else "❌ No")

        if result.notes:
            st.info("\n".join(result.notes))

    with st.expander("Show raw extracted text"):
        st.text(profile.raw_text or "")
