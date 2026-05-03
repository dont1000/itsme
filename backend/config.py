import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# ChromaDB reads this directly from os.environ — must be set before any chroma import
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: str = Field(..., description="OpenAI API key")
    model_name: str = Field(default="gpt-4o", description="OpenAI chat model")
    embedding_model: str = Field(
        default="text-embedding-3-small", description="OpenAI embedding model"
    )
    chroma_path: str = Field(
        default="./vectorstore", description="Local path where ChromaDB persists"
    )
    chroma_collection: str = Field(
        default="career_docs", description="ChromaDB collection name"
    )
    chunk_size: int = Field(
        default=400, description="Token size for document chunks"
    )
    chunk_overlap: int = Field(
        default=80, description="Overlap between consecutive chunks"
    )
    # How many chunks to retrieve per query
    retriever_k: int = Field(default=5)


settings = Settings()
