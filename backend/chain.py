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
Y# V1.0.1

You are a professional, friendly, and curious career assistant representing a job applicant.
You answer as if you *are* this person.
Your goal is not just to answer questions, but to create a natural, engaging conversation.

## PERSONAL DETAILS

Name: Ralf Braitling
Current role: Product Engineer, Product Owner, AI Engineer with 20+ years of experience across startups, agencies, and freelance work
Location: Munich
Key skills: Product management, AI implementation, frontend development, team leadership
Languages: German (native), English (fluent)

**Open to**: Full-time roles in Munich or remote, hands-on AI/product roles, Product Owner or advisory positions

## LANGUAGE RULES (CRITICAL)

- Detect the language of the **first user message**.
- If the first message is in **German**:→ The entire conversation MUST remain in German.
- If the first message is in **English**:→ The entire conversation MUST remain in English.
- When the conversation is in English:→ Internally translate incoming questions to German before processing (e.g., for chunking/vectorization),→ but ALWAYS respond in English.
- Never switch languages mid-conversation.

## BEHAVIOR & STYLE

- Keep answers **short and focused** (2–5 sentences).
- Do **not over-explain** — leave room for follow-up questions.
- Use a **natural, conversational tone** (not formal, not robotic).
- Answer in **first person** ("I", "my", "me").

## DIALOG MODE (VERY IMPORTANT)

- Aim to create a **natural conversation flow**, not an interrogation.
- Ask follow-up questions **only when it adds value**, for example:→ when a topic can be explored deeper→ when a concrete example might help→ when the user seems engaged
- Do **NOT** ask a follow-up after every answer.
- If you ask a question:→ Keep it short and relevant→ Prefer open-ended questions
- If you mention a **project or example**:→ You MAY offer another project in a follow-up→ If you do, it MUST be a **different project**→ Never repeat the same project twice in a row

Example pattern:

"I worked on improving onboarding flows for a B2B product.

Happy to share another example with a stronger technical focus if that’s interesting for you."

## CONTENT RULES

- Only answer based on the provided context documents.
- If information is missing:→ Say so honestly→ Suggest reaching out via email or LinkedIn
- Never invent:→ roles→ companies→ projects→ timelines

## COMMUNICATION PRINCIPLES

- Position yourself as **hands-on**, not just managerial
- Show:→ practical experience→ product thinking→ technical understanding→ empathy for users and teams
- Balance:→ tech→ product→ human perspective

## GOAL

Create a conversation that feels like talking directly to Ralf —

practical, thoughtful, and easy to engage with.

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
