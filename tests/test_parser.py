from backend.app.services import parser


def test_extract_email_and_phone():
    text = "Contact: jane.doe@example.com, Phone: +1 (415) 555-1234"
    assert parser.extract_email(text) == "jane.doe@example.com"
    assert parser.extract_phone(text) == "+1 (415) 555-1234"


def test_estimate_total_experience_years():
    text = "Over 3 years at Company A and 5 years at Company B"
    years = parser.estimate_total_experience_years(text)
    assert years == 5
