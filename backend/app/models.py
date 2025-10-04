from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator


class EvaluationCriteria(BaseModel):
    required_skills: List[str] = Field(default_factory=list, description="Exact skill names to look for")
    preferred_skills: List[str] = Field(default_factory=list, description="Nice-to-have skill names")
    min_years_experience: int = Field(ge=0, default=0, description="Minimum total years of experience")
    education_keywords: List[str] = Field(default_factory=list, description="Keywords indicating education level or degrees")

    @field_validator("required_skills", "preferred_skills", "education_keywords")
    @classmethod
    def normalize_keywords(cls, v: List[str]) -> List[str]:
        return [s.strip().lower() for s in v if s and s.strip()]


class CandidateProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    total_years_experience: Optional[float] = None
    skills: List[str] = Field(default_factory=list)
    education: Optional[str] = None
    raw_text: Optional[str] = None


class EvaluationResult(BaseModel):
    score: float
    breakdown: Dict[str, float]
    matched_required_skills: List[str] = Field(default_factory=list)
    matched_preferred_skills: List[str] = Field(default_factory=list)
    meets_min_experience: bool = False
    education_match: bool = False
    notes: List[str] = Field(default_factory=list)
