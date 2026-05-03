"""
Run this script once (and whenever you update /data) to load, chunk,
embed, and persist your career documents into ChromaDB.

Usage:
    python ingest.py
"""

import sys
from pathlib import Path

import chromadb

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings

DATA_DIR = Path(__file__).parent / "data"
SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}


def load_documents():
    docs = []
    files = [f for f in DATA_DIR.rglob("*") if f.suffix in SUPPORTED_EXTENSIONS]

    if not files:
        print(f"No documents found in {DATA_DIR}. Add PDF or Markdown files and retry.")
        sys.exit(1)

    for path in files:
        print(f"  Loading: {path.name}")
        try:
            if path.suffix == ".pdf":
                loader = PyPDFLoader(str(path))
            else:
                # Handles both .md and .txt with UTF-8 fallback
                loader = TextLoader(str(path), encoding="utf-8")
            docs.extend(loader.load())
        except Exception as exc:
            print(f"  WARNING: Could not load {path.name}: {exc}")

    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        # Keep paragraphs and sentences intact when possible
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(docs)


def ingest():
    print("=== Career Chatbot — Document Ingestion ===\n")

    print("Step 1/3  Loading documents from /data …")
    docs = load_documents()
    print(f"          Loaded {len(docs)} page(s) / document(s).\n")

    print("Step 2/3  Splitting into chunks …")
    chunks = split_documents(docs)
    print(f"          Created {len(chunks)} chunks.\n")

    print("Step 3/3  Embedding and storing in ChromaDB …")
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )

    # Delete the existing collection so re-runs don't accumulate duplicates
    client = chromadb.PersistentClient(path=settings.chroma_path)
    client.delete_collection(settings.chroma_collection)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_path,
        collection_name=settings.chroma_collection,
    )
    print(f"          Stored {len(chunks)} chunks in '{settings.chroma_path}'.\n")
    print("Done! You can now start the API server.")
    return vectorstore


if __name__ == "__main__":
    ingest()
