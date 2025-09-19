from pathlib import Path 
from ai.ai_processor import process_file

def run_tests():
    data_dir = Path("data")
    pdfs = list(data_dir.glob("*.pdf"))

    if not pdfs:
        print("No PDFs found in data/. Please add sample_claim1.pdf etc.")
        return

    # satellite image path
    image_path = data_dir / "sample_satellite.png"

    for pdf in pdfs:
        print(f"\n=== Processing: {pdf.name} ===")
        result = process_file(str(pdf), str(image_path))
        print(result)

if __name__ == "__main__":
    run_tests()
