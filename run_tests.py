# tests/run_tests.py
from ai.ai_processor import process_text, recommend_schemes

samples = [
    {
        "name": "small tribal example",
        "text": "Name: Ramesh Singh\nVillage: Baripada\nState: Odisha\nArea: 0.5 ha\nThis claimant is from a Scheduled Tribe family."
    },
    {
        "name": "missing coords example",
        "text": "Applicant Name: Sita Kumari\nVillage: DemoVillage\nArea: 3 hectares\n(Handwritten scanned form)"
    },
    {
        "name": "coords in text",
        "text": "Name: Arun Kumar\nCoords: 21.9400, 86.7293\nArea: 6 acres"
    }
]

for s in samples:
    ex = process_text(s["text"])
    rec = recommend_schemes(ex)
    print("=== SAMPLE:", s["name"])
    print("EXTRACT:", ex)
    print("RECOMMEND:", rec)
    print()
