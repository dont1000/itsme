# Career Chatbot — Backend

RAG-based career chatbot. Python/FastAPI backend that answers questions about the owner's
professional background using documents stored in ChromaDB.

## Stack
- **FastAPI** — HTTP server, streaming endpoint
- **LangChain 1.x + langchain-classic** — ConversationalRetrievalChain (condense → retrieve → answer)
- **ChromaDB** — local vector store, persisted in `./vectorstore/`
- **OpenAI** — `gpt-4o` for chat, `text-embedding-3-small` for embeddings
- **Pydantic v2** — settings (`config.py`) and request/response models (`main.py`)

## Key files
| File | Purpose |
|------|---------|
| `config.py` | All settings loaded from `.env` via `pydantic-settings` |
| `ingest.py` | One-shot script: load → chunk → embed → store |
| `chain.py` | Builds the chain; `stream_response()` is the main entry point |
| `main.py` | FastAPI app; `POST /chat` streams tokens back to the client |
| `data/` | Drop PDF/MD/TXT career docs here; re-run `ingest.py` after changes |
| `vectorstore/` | ChromaDB persistence directory — never commit, excluded in `.gitignore` |

## Workflow
```
# First time setup
cp .env.example .env          # fill in OPENAI_API_KEY
pip install -r requirements.txt
python ingest.py               # indexes /data documents

# Start the server
uvicorn main:app --reload

# After updating documents in /data
python ingest.py               # re-index (overwrites the collection)
```

## /chat API
```
POST /chat
Content-Type: application/json

{
  "message": "What languages do you speak?",
  "history": [
    { "role": "user",      "content": "Tell me about yourself." },
    { "role": "assistant", "content": "Sure! I'm a software engineer …" }
  ]
}
```
Response: `text/plain` stream of tokens.

## Conventions
- Settings are always read from `config.settings` — never hardcode keys or paths.
- `ingest.py` always **recreates** the ChromaDB collection (`from_documents`), so it is safe
  to run repeatedly without accumulating duplicates.
- The system prompt persona lives in `chain.py::SYSTEM_PROMPT_TEMPLATE`.
  Look for the `# TODO` comment to insert personal details.
- CORS origins are set in `main.py` — add the production frontend URL before deploying.
- Chat history format: list of `{"role": "user"|"assistant", "content": "…"}` dicts,
  alternating, oldest first.

## Personal details placeholder
Open `chain.py` and search for `# TODO` — that block is where you insert your name,
current role, location, skills, and open-to statement. This text is injected into every
LLM call as part of the system prompt.
