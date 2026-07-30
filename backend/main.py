from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ingest import ingest
from agent import ask_agent


ingest()

app = FastAPI(
    title="Agentic RAG + Text-to-SQL Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def health():
    return {
        "status": "healthy",
        "message": "Chatbot API is running."
    }


@app.post("/chat")
def chat(request: ChatRequest):

    try:

        response = ask_agent(request.question)

        return response

    except Exception as e:

        return {
            "tool": "ERROR",
            "answer": str(e)
        }