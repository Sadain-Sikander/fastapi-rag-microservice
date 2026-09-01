"""
Configuration module for FastAPI RAG Microservice.
Loads environment variables and provides centralized configuration management.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    environment: str = "development"
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # LLM Provider Keys
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # ChromaDB Configuration
    chroma_collection_name: str = "pdf_docs"
    chroma_persist_directory: str = "./chroma_data"
    
    # LLM Model Configuration
    primary_llm_model: str = "gemini-2.0-flash"
    fallback_llm_model: str = "claude-3-5-sonnet-20241022"
    chunk_size: int = 500
    top_k_results: int = 3
    
    # System Prompt
    system_prompt: str = (
        "Use ONLY the provided context to answer the user's question. "
        "If the answer is not contained within the context, state that explicitly."
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
