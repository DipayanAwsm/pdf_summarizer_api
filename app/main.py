import os
import subprocess
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.summarizer import extract_text_from_pdf, summarize_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMMARY_DIR = os.path.join(BASE_DIR, "summaries")
os.makedirs(SUMMARY_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    try:
        original_filename = file.filename
        temp_pdf_path = os.path.join(SUMMARY_DIR, original_filename)
        
        with open(temp_pdf_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(temp_pdf_path)
        if not text:
            return {"summary": "No readable text found in PDF."}

        summary = summarize_text(text)
        summary_path = os.path.join(SUMMARY_DIR, f"{original_filename}_summary.txt")

        with open(summary_path, "w") as f:
            f.write(summary)

        subprocess.run(["git", "add", temp_pdf_path, summary_path])
        subprocess.run(["git", "commit", "-m", f"Add summary for {original_filename}"])
        subprocess.run(["git", "push"])

        return {"summary": summary}
    except Exception as e:
        return {"summary": f"Error: {str(e)}"}
