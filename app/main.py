from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.summarizer import extract_text_from_pdf, summarize_text

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/summarize-pdf/")
async def summarize_pdf(file: UploadFile = File(...)):
    with open(f"temp_{file.filename}", "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(f.name)
    summary = summarize_text(text)

    return {"summary": summary}
