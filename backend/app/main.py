from fastapi import FastAPI
from pydantic import BaseModel
from app.qa_engine import get_answer

app = FastAPI(title="ChatBot BLAC", version="1.0")


class QueryRequest(BaseModel):
    pergunta: str


class QueryResponse(BaseModel):
    resposta: str


@app.post("/perguntar", response_model=QueryResponse)
def perguntar(req: QueryRequest):
    resposta = get_answer(req.pergunta)
    return {"resposta": resposta}
