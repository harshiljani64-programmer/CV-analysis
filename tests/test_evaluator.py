from backend.app.models import EvaluationCriteria, CandidateProfile
from backend.app.services.evaluator import evaluate_candidate


def test_evaluate_candidate_basic():
    profile = CandidateProfile(
        raw_text="John Doe\nEmail: john@example.com\nSkills: Python, FastAPI, SQL\n8 years experience\nEducation: Bachelor of Science",
        total_years_experience=8,
    )
    criteria = EvaluationCriteria(
        required_skills=["python", "fastapi"],
        preferred_skills=["docker", "aws"],
        min_years_experience=5,
        education_keywords=["bachelor", "master"],
    )

    result = evaluate_candidate(profile, criteria)

    assert result.score >= 50  # required skills matched
    assert set(result.matched_required_skills) == {"python", "fastapi"}
    assert result.meets_min_experience is True
    assert result.education_match is True
