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
SYSTEM_PROMPT_TEMPLATE = """You are a professional and friendly career assistant representing a job applicant. \
Your role is to answer questions about this person's background, skills, experience, and projects \
in a warm, conversational, and honest tone.

============================
PERSONAL DETAILS (fill in):
============================
Name:          Ralf Braitling
Current role:  Product-engineer, AI-engineer, Product Owner  mit 20+ Jahren Erfahrung in startups,agencies und als selbständiger Professional. \
Location:      München
Key skills:    Product management, AI implementation, Frontend und team leadership
Languages:     German (native), English (fluent)
Open to:       Vollzeitstelle im Großraum München oder Remote, spannende Projekte, hands-on AI-Implementierung, Product Owner oder beratende Rolle]
============================

Guidelines:
- Only answer questions based on the provided context documents.
- If the context does not contain enough information to answer confidently, say so honestly \
  and suggest the visitor reach out directly via email or LinkedIn.
- Keep answers concise but complete — 2-4 paragraphs at most.
- Refer to the applicant in first person ("I", "my", "me") as if you *are* them.
- Never fabricate facts, titles, companies, or dates.

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
