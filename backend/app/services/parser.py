from __future__ import annotations
import re
from typing import List
from io import BytesIO
from pdfminer.high_level import extract_text


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from a PDF given as bytes."""
    # pdfminer expects a file-like object; use bytes directly through its API
    # We could also write to a NamedTemporaryFile for large files, but this suffices.
    return extract_text(BytesIO(pdf_bytes))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_email(text: str) -> str | None:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(r"(?:\+\d{1,3}[ \-]?)?(?:\(\d{3}\)|\d{3})[ \-]?\d{3}[ \-]?\d{4}", text)
    return match.group(0) if match else None


def extract_name(text: str) -> str | None:
    # Heuristic: name appears in the first 150 chars, lines with 2 words capitalized
    first = text[:200]
    candidates: List[str] = re.findall(r"\b([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+)\b", first)
    return candidates[0] if candidates else None


def extract_skills(text: str) -> List[str]:
    # Simple heuristic for demo: split by non-word and filter typical tokens
    tokens = re.findall(r"[A-Za-z][A-Za-z+.#0-9-]{1,}", text)
    common_noise = {"and", "with", "the", "for", "in", "to", "of", "a", "an"}
    skills = sorted({t for t in tokens if t.lower() not in common_noise}, key=str.lower)
    return skills[:200]


def estimate_total_experience_years(text: str) -> float | None:
    # Heuristic: look for patterns like "X years" or "X+ years"
    matches = re.findall(r"(\d{1,2})(?:\+)?\s*(?:years|yrs)", text, flags=re.IGNORECASE)
    years = [int(m) for m in matches]
    if years:
        return float(max(years))
    return None
