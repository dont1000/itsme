"""
FastAPI application — career chatbot backend.

Endpoints:
  POST /chat          — streams a conversational RAG response
  GET  /health        — liveness check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from chain import stream_response

app = FastAPI(
    title="Career Chatbot API",
    description="RAG-powered chatbot grounded in personal career documents.",
    version="1.0.0",
)

# Allow the Vue frontend (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000","https://its-ralf.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    # Pass the full conversation so the chain can condense follow-ups correctly.
    # Alternating user/assistant pairs; omit for the first message.
    history: list[ChatMessage] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Stream a career-assistant response for `message`.

    The client receives a plain-text stream of tokens separated by no
    delimiter — the frontend should append each chunk to its buffer.
    """
    print(f"QUESTION: {request.message}", flush=True)
    history_dicts = [m.model_dump() for m in request.history]

    async def token_generator():
        try:
            async for token in stream_response(request.message, history_dicts):
                yield token
        except Exception as exc:
            # Surface errors as a final stream chunk so the client sees them
            yield f"\n\n[Error: {exc}]"

    return StreamingResponse(
        token_generator(),
        media_type="text/plain",
        headers={
            # Prevents Nginx / proxies from buffering the stream
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
        },
    )
