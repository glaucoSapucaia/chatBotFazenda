from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

import pdfplumber
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "backend" / "data" / "DLDT 02_2021 BLAC.pdf"
TXT_PATH = ROOT / "backend" / "data" / "texto_extraido.txt"
CHROMA_PATH = ROOT / "backend" / "data" / "chroma_db"


def extract_text_with_pdfplumber(pdf_path: Path, txt_path: Path):
    print("Extraindo texto do PDF...")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n\n--- Página {i + 1} ---\n\n" + page_text

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Texto extraído e salvo como .txt")


def ingest_pdf(txt_path: Path):
    print("Carregando texto e dividindo em chunks...")
    loader = TextLoader(str(txt_path), encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, chunk_overlap=300, separators=["\n\n", "\n", ".", ":", " "]
    )
    docs = splitter.split_documents(documents)

    print(f"Total de chunks gerados: {len(docs)}")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectordb = Chroma.from_documents(
        documents=docs, embedding=embeddings, persist_directory=str(CHROMA_PATH)
    )

    print("PDF processado e vetores salvos no banco vetorial.")


if __name__ == "__main__":
    extract_text_with_pdfplumber(PDF_PATH, TXT_PATH)
    ingest_pdf(TXT_PATH)
