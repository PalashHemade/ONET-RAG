from fastapi import FastAPI, UploadFile, File
import tempfile

from app.schemas import CareerQuery, CareerResponse
from app.rag import explain_careers
from app.pdf_utils import parse_pdf_resume

app = FastAPI(
    title="Career Recommendation RAG API",
    version="1.0.0"
)


@app.post("/career/query", response_model=CareerResponse)
def career_from_text(payload: CareerQuery):
    answer = explain_careers(payload.query)
    return {"answer": answer}


@app.post("/career/resume", response_model=CareerResponse)
async def career_from_resume(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    resume_text = parse_pdf_resume(tmp_path)

    query = f"""
Candidate Resume:
{resume_text}

Based on this profile, suggest suitable careers.
"""

    answer = explain_careers(query)
    return {"answer": answer}
