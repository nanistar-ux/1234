import re
import fitz  # PyMuPDF
from ai.asset_mapper import analyze_assets
from ai.dss_engine import recommend_schemes


def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using PyMuPDF."""
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def parse_entities(text: str) -> dict:
    """Parse entities like name, village, state, coords, area from raw text."""
    data = {
        "person_name": None,
        "village": None,
        "state": None,
        "coordinates": None,
        "area_ha": None,
        "raw_text": text
    }

    # Name
    m = re.search(r"(Name|Applicant Name)[:\- ]+([A-Za-z ]+)", text, re.IGNORECASE)
    if m:
        data["person_name"] = m.group(2).strip()

    # Village
    m = re.search(r"Village[:\- ]+([A-Za-z ]+)", text, re.IGNORECASE)
    if m:
        data["village"] = m.group(1).strip()

    # State
    m = re.search(r"State[:\- ]+([A-Za-z ]+)", text, re.IGNORECASE)
    if m:
        data["state"] = m.group(1).strip()

    # Coordinates (lat, lng)
    m = re.search(r"([0-9]{1,2}\.\d+)[ ,]+([0-9]{1,3}\.\d+)", text)
    if m:
        lat, lng = float(m.group(1)), float(m.group(2))
        data["coordinates"] = {"lat": lat, "lng": lng}

    # Area (ha or acres)
    m = re.search(r"Area[:\- ]+([\d\.]+)\s*ha", text, re.IGNORECASE)
    if m:
        data["area_ha"] = float(m.group(1))
    else:
        m = re.search(r"Area[:\- ]+([\d\.]+)\s*acres?", text, re.IGNORECASE)
        if m:
            acres = float(m.group(1))
            data["area_ha"] = round(acres * 0.404686, 4)

    return data


def process_file(pdf_path: str, image_path: str = None) -> dict:
    """Main pipeline: extract text, parse, DSS recommendation, asset analysis."""
    # Step 1: OCR / Text Extraction
    text = extract_text_from_pdf(pdf_path)

    # Step 2: NER / Regex Parsing
    entities = parse_entities(text)

    # Step 3: Decision Support System (recommend schemes)
    schemes = recommend_schemes(entities)

    # Step 4: Asset Analysis (if satellite image is given)
    assets = analyze_assets(image_path) if image_path else {
        "vegetation": None,
        "water": None,
        "built": None,
        "other": None,
    }

    # Final Output JSON
    return {
        "person_name": entities["person_name"],
        "village": entities["village"],
        "state": entities["state"],
        "coordinates": entities["coordinates"],
        "area_ha": entities["area_ha"],
        "recommended_schemes": schemes,
        "assets_detected": assets,
        "raw_text": entities["raw_text"]
    }
