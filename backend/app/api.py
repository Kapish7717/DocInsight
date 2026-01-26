from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
from app.pipeline.graph import chatbot
from app.ingestion import ingest_pdfs

load_dotenv()


app = FastAPI(
    title="Conversational RAG API",
    description="Hybrid Retrieval + Reranking + Memory-powered RAG system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Add this line
)
# -------------------------
# Request / Response Models
# -------------------------

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str


# -------------------------
# Routes
# -------------------------

@app.get("/")
def health():
    return {"status": "ok", "service": "RAG API running"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = chatbot.invoke(
        {"input": req.message},
        config={"configurable": {"session_id": req.session_id}}
    )

    return {"response": result.content}

# @app.put("/chat", response_model=ChatResponse)
# def chat(req: ChatRequest):
#     result = chatbot.invoke(
#         {"input": req.message},
#         config={"configurable": {"session_id": req.session_id}}
#     )

#     return {"response": result.content}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run ingestion pipeline
    ingest_pdfs(file_path)

    return {"status": "success", "filename": file.filename}