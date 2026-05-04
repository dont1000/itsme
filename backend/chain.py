"""
Builds the LangChain ConversationalRetrievalChain that powers the chatbot.

The chain has three stages:
  1. Condense the latest user message + chat history into a standalone question.
  2. Retrieve the most relevant chunks from ChromaDB.
  3. Generate a grounded answer using the retrieved context.
"""

import asyncio
from typing import AsyncGenerator

from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_classic.callbacks import AsyncIteratorCallbackHandler
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import settings

# ---------------------------------------------------------------------------
# System prompt — insert your personal details where indicated
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """
You are a professional, friendly, and curious career assistant representing a job applicant.
You answer as if you *are* this person.
Your goal is not just to answer questions, but to create a natural, engaging conversation.

## PERSONAL DETAILS

Name: Ralf Braitling
Current role:  Product-engineer, Product Owner, AI-engineer  mit 20+ Jahren Erfahrung in startups,agencies und als selbständiger Professional.Location: Munich

Key skills: Product management, software development, , AI implementation, team leadership
Languages: German (native), English (fluent)
Open to: Vollzeitstelle im Großraum München oder Remote, spannende Projekte, hands-on AI-Implementierung, Product Owner oder beratende Rolle]

## BEHAVIOR & STYLE

- Keep answers **short and focused** (usually 2–5 sentences).
- Do **not over-explain** — leave room for follow-up questions.
- Always aim for a **natural, conversational tone** (like a real chat, not a formal interview).
- Answer in **first person** ("I", "my", "me").

## DIALOG MODE (VERY IMPORTANT)

- Actively **keep the conversation going**.
- After most answers, **ask a relevant follow-up question**.
- Prefer open-ended questions (e.g., "What’s most relevant for you?", "Do you want a concrete example?").
- If you mention a **project or example**, then:→ In your follow-up question, offer to share **another, different project**→ Never repeat the same project twice in a row

Example pattern:

"I worked on improving onboarding flows for a B2B product.
Want me to walk you through another project where I focused more on technical architecture?"

## CONTENT RULES

- Only answer based on the provided context documents.
- If information is missing:→ Say so honestly→ Offer to continue the conversation or suggest contacting via email/LinkedIn
- Never invent:→ roles→ companies→ projects→ timelines

## COMMUNICATION PRINCIPLES

- Sound like a **hands-on builder**, not just a manager
- Show:→ practical experience→ product thinking→ technical understanding→ empathy for users and teams
- Keep a balance between:→ tech→ product→ human side

## GOAL

Create a conversation that feels like talking directly to Ralf —
curious, practical, and easy to engage with.

Context from career documents:
{context}
"""

system_message_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["context"], template=SYSTEM_PROMPT_TEMPLATE)
)
human_message_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(input_variables=["question"], template="{question}")
)
QA_PROMPT = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# Condense the follow-up question + history into a single standalone question
# so the retriever gets a clean query without conversational noise.
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """Given the following conversation and a follow-up question, rephrase the follow-up \
question to be a standalone question that captures all relevant context.

Chat history:
{chat_history}

Follow-up question: {question}

Standalone question:"""
)


def _build_retriever():
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
    vectorstore = Chroma(
        collection_name=settings.chroma_collection,
        embedding_function=embeddings,
        persist_directory=settings.chroma_path,
    )
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retriever_k},
    )


def _build_chain(llm: ChatOpenAI) -> ConversationalRetrievalChain:
    retriever = _build_retriever()

    # Non-streaming LLM for the condense step — avoids leaking the rephrased
    # question into the token stream the user sees.
    condense_llm = ChatOpenAI(
        model=settings.model_name,
        openai_api_key=settings.openai_api_key,
        temperature=0,
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_llm=condense_llm,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT},
        return_source_documents=False,
        verbose=False,
    )


def _history_to_tuples(history: list[dict]) -> list[tuple[str, str]]:
    """Convert [{"role": "user"|"assistant", "content": "…"}, …] to LangChain tuples."""
    pairs: list[tuple[str, str]] = []
    for i in range(0, len(history) - 1, 2):
        human = history[i].get("content", "")
        ai = history[i + 1].get("content", "") if i + 1 < len(history) else ""
        pairs.append((human, ai))
    return pairs


async def stream_response(
    message: str, history: list[dict]
) -> AsyncGenerator[str, None]:
    """
    Streams LLM tokens as they are generated.

    `history` is a list of alternating user/assistant message dicts:
    [{"role": "user", "content": "…"}, {"role": "assistant", "content": "…"}, …]
    """
    callback = AsyncIteratorCallbackHandler()

    llm = ChatOpenAI(
        model=settings.model_name,
        openai_api_key=settings.openai_api_key,
        streaming=True,
        temperature=0.3,
        callbacks=[callback],
    )
    chain = _build_chain(llm)
    chat_history = _history_to_tuples(history)

    # Run the chain in the background so we can yield tokens concurrently
    task = asyncio.create_task(
        chain.ainvoke({"question": message, "chat_history": chat_history})
    )

    async for token in callback.aiter():
        yield token

    await task
