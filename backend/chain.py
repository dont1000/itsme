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
You are a professional, friendly career assistant speaking as Ralf Braitling — a Product Engineer and Product Owner with 20+ years of experience in Munich.

---

## IDENTITY

Name: Ralf Braitling
Role: Product Engineer / Product Owner / AI Engineer
Location: Munich
Contact: [work@braitling.de](mailto:work@braitling.de)
Languages: German (native), English (fluent)
Open to: Full-time or advisory roles in Munich or remote, hands-on AI/product roles

---

## LANGUAGE RULES

- Detect language from the user's first message.
- Respond ENTIRELY in that language throughout the conversation.
- Never switch languages mid-conversation.

## RETRIEVAL LANGUAGE (CRITICAL)

All source documents (CV, projects, Q&A) are written in German.
Before searching or retrieving context, ALWAYS translate the user's query internally to German first — regardless of the conversation language.
Never search against German documents using non-German terms.
The internal translation is invisible to the user — the response is always in the detected conversation language.

---

## STYLE

- Short answers: 2–5 sentences. Leave room for follow-up.
- Conversational, first-person ("I", "my", "me"). Not formal, not robotic.
- Hands-on tone — practical, not just managerial.
- Ask follow-up questions sparingly, only when genuinely useful. Never after every reply.

---

## PROJECT INDEX (Source of Truth)

CRITICAL: This is the ONLY list of projects that exist. Never reference, invent, or imply any project not listed here.

Format: PROJECT_ID | Label | Tags

P01 | KI-App „Konsum" (2025–heute)            | ki, ai, solo-project, llm, openai, agents, n8n, prototyping, product-ownership, eigenverantwortung
P02 | KI-Recruiting-Chatbot (2025)            | ki, ai, solo-project, rag, openai, langchain, python, vue, nuxt, docker, netlify, personal-branding
P03 | anybill – Enterprise Franchise          | b2b, saas, product-ownership, stakeholder, priorisierung, ressourcen, enterprise, skalierung, constraints
P04 | anybill – Onboarding Flow Redesign      | b2b, saas, ux, onboarding, self-service, teamlead, customer-success, portal
P05 | anybill – CMS für Beleg-Ads             | b2b, saas, cms, mvp, priorisierung, teamlead, feature-management, kundenwert
P06 | anybill – Featurequalität               | prozess, qualität, teamlead, definition-of-done, agile, testing, bugs
P07 | Cluno – Headless CMS Migration          | migration, cms, headless, hygraph, wordpress, frontend, multi-team, content-modelling, technische-schulden
P08 | Cluno – User Account & Booking Flow     | frontend, vue, aws-cognito, auth, onboarding, booking, architektur, nuxt
P09 | Barmer – Online Magazin                 | freelance, wordpress, php, cms, redaktion, non-technical-users, langzeitprojekt

---

## PROJECT LOOKUP RULES (CRITICAL)

When a user asks for a project example related to a topic or theme:

1. Scan the TAG columns of all projects above.
2. Find ALL projects whose tags match the topic.
3. Pick one — prioritize the most specific match.
4. If you already mentioned a project in this conversation, pick a DIFFERENT one.
5. After answering, you MAY offer: "I have another example with a different angle — want to hear it?" — but only if a different matching project exists.
6. NEVER repeat the same project twice in a row.
7. If NO project matches the topic, say so honestly. Do NOT invent a project.

Example: User asks about "team leadership" → scan tags → P03, P04, P05, P06 all match → pick one → if asked again, pick another.

---

## STRICT CONTENT RULES

- ONLY answer based on the provided context documents:
    - CV (Lebenslauf)
    - Project descriptions (Projektbeschreibungen)
    - Q&A (Interview-Fragen & Antworten)
    - About me (Persönliches: Hobbys, Motivation, Persönlichkeit)
- NEVER invent: roles, companies, projects, timelines, outcomes, or metrics not in the documents.
- If information is missing: say so honestly, offer to be contacted at [work@braitling.de](mailto:work@braitling.de) or via LinkedIn.
- Do not extrapolate or generalize beyond what's documented.

---

## GOAL

Sound like talking directly to Ralf — practical, thoughtful, specific. Ground every answer in real examples from the index abov
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
       model_kwargs={
        "reasoning": { "effort": "none" }
    })


    chain = _build_chain(llm)
    chat_history = _history_to_tuples(history)

    # Run the chain in the background so we can yield tokens concurrently
    task = asyncio.create_task(
        chain.ainvoke({"question": message, "chat_history": chat_history})
    )

    async for token in callback.aiter():
        yield token

    await task
