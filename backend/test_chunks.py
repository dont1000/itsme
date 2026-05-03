"""
Quick sanity check — query the vector store and print the top retrieved chunks.
Run from the backend/ directory after ingest.py has been executed.

Usage:
    python test_chunks.py "What are your main skills?"
"""

import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import settings

query = sys.argv[1] if len(sys.argv) > 1 else "Was hast du bisher mit Ai gemacht?"

embeddings = OpenAIEmbeddings(
    model=settings.embedding_model,
    openai_api_key=settings.openai_api_key,
)

vectorstore = Chroma(
    persist_directory=settings.chroma_path,
    collection_name=settings.chroma_collection,
    embedding_function=embeddings,
)

total = vectorstore._collection.count()
print(f"Total chunks in store: {total}\n")
print(f'Query: "{query}"\n{"─" * 60}')

results = vectorstore.similarity_search_with_score(query, k=3)
for i, (doc, score) in enumerate(results, 1):
    source = doc.metadata.get("source", "unknown")
    preview = doc.page_content[:300].replace("\n", " ")
    print(f"\n[{i}] score={score:.4f}  source={source}")
    print(f"    {preview}…")
