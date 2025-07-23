from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHROMA_PATH = ROOT / "data" / "chroma_db"

# Load vetores
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectordb = Chroma(persist_directory=str(CHROMA_PATH), embedding_function=embeddings)
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5},
)

# Modelo LLM
llm = OllamaLLM(model="llama3")

template = """
Você é um assistente da Prefeitura especializado no preenchimento do BLAC.

Use apenas as informações abaixo para responder de forma clara, objetiva e em português.

Informações extraídas do documento:
{context}

Pergunta:
{question}

Resposta:
"""

prompt = PromptTemplate.from_template(template)

# RetrievalQA com prompt customizado que usa 'context'
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
)

# Teste
resposta = qa.invoke(
    {
        "query": "No terreno, tem duas casas, um barracão e um galpão. Uma família vive em uma casa, outra família na segunda casa, e uma terceira família no barracão. O galpão é usado como uma oficina mecânica. Quantos BLAC devo fazer, e como devo preencher os dados?"
    }
)

print("\nResposta:\n", resposta)
