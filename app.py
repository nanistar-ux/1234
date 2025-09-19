# app.py
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import shutil
from pathlib import Path

from ai.ai_processor import process_file

app = FastAPI(title="SIH2025_AI - FRA Claim Processor")

# Directory to save uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Define your API key here (give this key to the backend)
API_KEY = "YOUR_SECRET_API_KEY_HERE"

# Dependency to verify API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")

@app.post("/api/process_claim")
async def process_claim(file: UploadFile = File(...), x_api_key: str = Header(...)):
    # Verify API key
    verify_api_key(x_api_key)

    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run AI processor
        result = process_file(str(file_path))

        return JSONResponse(content={"status": "success", "result": result})

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)},
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
