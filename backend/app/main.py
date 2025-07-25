from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.qa_engine import get_answer

app = FastAPI(title="ChatBot BLAC", version="1.0")

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    pergunta: str


class QueryResponse(BaseModel):
    resposta: str


@app.post("/perguntar", response_model=QueryResponse)
def perguntar(req: QueryRequest):
    resposta = get_answer(req.pergunta)
    return {"resposta": resposta}
