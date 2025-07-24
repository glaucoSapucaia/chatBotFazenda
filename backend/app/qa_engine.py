from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = ROOT / "data" / "chroma_db"

# Carrega apenas uma vez
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectordb = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embeddings)
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5},
)

llm = OllamaLLM(model="llama3")

prompt_template = """
Você é um assistente da Prefeitura especializado no preenchimento do BLAC.

Use apenas as informações abaixo para responder de forma clara, objetiva e em português.

Informações extraídas do documento:
{context}

Pergunta:
{question}

Resposta:
"""
prompt = PromptTemplate.from_template(prompt_template)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
)


def get_answer(query: str) -> str:
    result = qa.invoke({"query": query})
    return result["result"] if isinstance(result, dict) else str(result)
