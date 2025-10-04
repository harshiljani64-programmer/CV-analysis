from __future__ import annotations
from typing import Dict, List

from .parser import normalize_text
from ..models import EvaluationCriteria, CandidateProfile, EvaluationResult


def evaluate_candidate(profile: CandidateProfile, criteria: EvaluationCriteria) -> EvaluationResult:
    text = normalize_text(profile.raw_text or "")
    text_lower = text.lower()

    required_hits: List[str] = []
    preferred_hits: List[str] = []

    # Required skills: each contributes equally up to 50 points total
    if criteria.required_skills:
        per_required = 50.0 / len(criteria.required_skills)
        for skill in criteria.required_skills:
            if skill in text_lower:
                required_hits.append(skill)
    else:
        per_required = 0.0

    required_score = per_required * len(required_hits)

    # Preferred skills: share 30 points total
    if criteria.preferred_skills:
        per_preferred = 30.0 / len(criteria.preferred_skills)
        for skill in criteria.preferred_skills:
            if skill in text_lower:
                preferred_hits.append(skill)
    else:
        per_preferred = 0.0

    preferred_score = per_preferred * len(preferred_hits)

    # Experience: 15 points if meets/exceeds minimum
    meets_experience = False
    experience_score = 0.0
    if criteria.min_years_experience and profile.total_years_experience is not None:
        meets_experience = profile.total_years_experience >= criteria.min_years_experience
        experience_score = 15.0 if meets_experience else 0.0

    # Education: 5 points if any keyword present
    education_match = False
    education_score = 0.0
    if criteria.education_keywords:
        education_match = any(k in text_lower for k in criteria.education_keywords)
        education_score = 5.0 if education_match else 0.0

    breakdown: Dict[str, float] = {
        "required_skills": round(required_score, 2),
        "preferred_skills": round(preferred_score, 2),
        "experience": experience_score,
        "education": education_score,
    }

    total_score = round(sum(breakdown.values()), 2)

    notes: List[str] = []
    if criteria.required_skills and not required_hits:
        notes.append("No required skills matched")
    if criteria.preferred_skills and not preferred_hits:
        notes.append("No preferred skills matched")
    if criteria.min_years_experience and not meets_experience:
        notes.append("Minimum years of experience not met")
    if criteria.education_keywords and not education_match:
        notes.append("No education keyword matched")

    return EvaluationResult(
        score=total_score,
        breakdown=breakdown,
        matched_required_skills=required_hits,
        matched_preferred_skills=preferred_hits,
        meets_min_experience=meets_experience,
        education_match=education_match,
        notes=notes,
    )
