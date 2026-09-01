"""
Pydantic models for request/response validation and API contracts.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


# ============ REQUEST MODELS ============

class IngestRequest(BaseModel):
    """Schema for document ingestion endpoint."""
    pass  # File is handled separately in FastAPI as UploadFile


class ChatRequest(BaseModel):
    """Schema for chat/query endpoint."""
    question: str = Field(..., min_length=1, max_length=1000, description="User question")
    top_k: Optional[int] = Field(default=3, ge=1, le=10, description="Number of context chunks to retrieve")


# ============ RESPONSE MODELS ============

class IngestResponse(BaseModel):
    """Schema for document ingestion response."""
    status: str = Field(..., description="Status of ingestion (success/error)")
    file: str = Field(..., description="Name of the ingested file")
    chunks_indexed: int = Field(..., ge=0, description="Number of chunks indexed")
    message: Optional[str] = Field(None, description="Additional message or error details")


class ChatResponse(BaseModel):
    """Schema for chat/query response."""
    question: str = Field(..., description="The user's question")
    answer: str = Field(..., description="The LLM-generated answer")
    sources_used: int = Field(..., ge=0, description="Number of context chunks used")
    model_used: str = Field(..., description="Which LLM model was used")
    message: Optional[str] = Field(None, description="Additional information or warnings")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Health status (healthy/unhealthy)")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment (development/production)")
    message: Optional[str] = Field(None, description="Additional status information")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    detail: Optional[str] = Field(None, description="Detailed error information")
