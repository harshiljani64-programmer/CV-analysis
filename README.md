# CV Analysis

CV Analysis is a lightweight web app that lets you upload PDF resumes, extract relevant information, and evaluate candidates against customizable criteria.

## Project overview

- **Upload resumes**: Simple web UI to upload a PDF.
- **Extract information**: Email, phone, estimated years of experience, skills, and text.
- **Evaluate candidates**: Scoring based on required skills, preferred skills, minimum years of experience, and education keywords.

### Tech stack
- **Backend**: FastAPI
- **Parsing**: pdfminer.six (basic text extraction) with simple heuristics
- **Templating**: Jinja2 for a minimal UI
- **Frontend**: Vanilla JS + CSS
- **Tests**: Pytest

## Installation instructions

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/` in your browser.

### Alternatively: Run the Streamlit app

```bash
streamlit run streamlit_app.py
# If streamlit isn't on PATH:
python3 -m streamlit run streamlit_app.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Usage examples

- Fill in `Required skills` with comma-separated values like `python, fastapi, sql`.
- Optionally add `Preferred skills`, `Minimum years of experience`, and `Education keywords`.
- Upload a PDF resume and click `Evaluate`.
- The JSON output includes the parsed `profile`, the `criteria` used, and the `result` with score and breakdown.

## Explanation of the code structure

```
backend/
  app/
    main.py            # FastAPI app, endpoints, and UI route
    models.py          # Pydantic models (criteria, profile, result)
    services/
      parser.py        # PDF parsing and heuristic extractors
      evaluator.py     # Candidate scoring logic
    templates/
      index.html       # Upload form + client-side fetch
    static/
      styles.css       # Minimal dark UI styling

requirements.txt       # Python dependencies
README.md              # Project documentation (this file)
tests/
  test_parser.py       # Parser unit tests
  test_evaluator.py    # Evaluator unit tests
```

## Contribution guidelines

- Create a feature branch for your change.
- Add or update tests when modifying parsing or evaluation.
- Ensure `pytest` passes before pushing.
- Use clear commit messages and follow existing code style (readable, explicit names).

## Notes and limitations

- PDF text extraction varies by source; some PDFs may need OCR. You can integrate Tesseract or other OCR tools if needed.
- Skill detection and experience estimation are heuristic and simple by design; refine for your domain.
- For production, consider authentication, persistence, and better parsing (e.g., `spacy`, ML-based NER).
