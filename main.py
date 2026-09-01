"""
Main FastAPI application for RAG Microservice.
Defines all API endpoints for document ingestion and querying.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from models import IngestRequest, ChatRequest, IngestResponse, ChatResponse, HealthResponse, ErrorResponse
from document_processor import document_processor
from vector_store import vector_store
from llm_adapter import llm_adapter


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============ LIFESPAN EVENTS ============

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("🚀 RAG Microservice starting...")
    try:
        stats = vector_store.get_collection_stats()
        logger.info(f"Vector store initialized: {stats}")
    except Exception as e:
        logger.warning(f"Vector store warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 RAG Microservice shutting down...")


# ============ APP INITIALIZATION ============

app = FastAPI(
    title="FastAPI RAG Microservice",
    description="A Retrieval-Augmented Generation service with multi-LLM support",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ HEALTH CHECK ENDPOINTS ============

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Check API health and status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=settings.environment,
        message="RAG Microservice is running"
    )


@app.get("/stats", tags=["Info"])
async def get_stats():
    """Get vector store statistics."""
    try:
        return vector_store.get_collection_stats()
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============ DOCUMENT INGESTION ENDPOINTS ============

@app.post("/ingest", response_model=IngestResponse, tags=["Documents"])
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a PDF document into the vector store.
    
    - **file**: PDF file to be processed and indexed
    
    Returns:
        IngestResponse with status, filename, and chunks indexed
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read file content
        content = await file.read()
        logger.info(f"Processing file: {file.filename}")
        
        # Extract and chunk document
        chunks, chunk_ids = document_processor.process_document(content, file.filename)
        logger.info(f"Generated {len(chunks)} chunks from {file.filename}")
        
        # Add to vector store
        metadatas = [{"source": file.filename, "chunk_index": i} for i in range(len(chunks))]
        vector_store.add_documents(chunks, chunk_ids, metadatas)
        logger.info(f"Indexed {len(chunks)} chunks for {file.filename}")
        
        return IngestResponse(
            status="success",
            file=file.filename,
            chunks_indexed=len(chunks),
            message=f"Successfully indexed {len(chunks)} chunks from {file.filename}"
        )
    
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")


# ============ QUERY ENDPOINTS ============

@app.post("/query", response_model=ChatResponse, tags=["Chat"])
async def query_documents(request: ChatRequest):
    """
    Query the vector store and get RAG-based response.
    
    - **question**: User's question or query
    - **top_k**: Number of context chunks to retrieve (1-10, default 3)
    
    Returns:
        ChatResponse with answer, sources used, and model information
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Query vector store for relevant chunks
        logger.info(f"Querying: {request.question}")
        results = vector_store.query(request.question, n_results=request.top_k)
        
        if not results["documents"] or len(results["documents"][0]) == 0:
            logger.warning("No relevant documents found")
            return ChatResponse(
                question=request.question,
                answer="No relevant documents found in the knowledge base to answer your question.",
                sources_used=0,
                model_used=llm_adapter.get_active_model(),
                message="No matching documents found"
            )
        
        # Extract retrieved documents
        retrieved_docs = results["documents"][0]  # ChromaDB returns nested list
        num_sources = len(retrieved_docs)
        logger.info(f"Retrieved {num_sources} relevant documents")
        
        # Generate response using LLM with retrieved context
        response_text, model_used = llm_adapter.generate_rag_response(
            question=request.question,
            context=retrieved_docs
        )
        logger.info(f"Generated response using {model_used}")
        
        return ChatResponse(
            question=request.question,
            answer=response_text,
            sources_used=num_sources,
            model_used=model_used,
            message="Response generated successfully"
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Alias endpoint for /query for convenience.
    Same functionality as /query.
    """
    return await query_documents(request)


# ============ ADMIN ENDPOINTS ============

@app.delete("/reset", tags=["Admin"])
async def reset_database():
    """Reset the vector store collection (WARNING: Deletes all indexed documents)."""
    try:
        vector_store.delete_collection()
        logger.warning("Vector store collection reset")
        return {
            "status": "success",
            "message": "Vector store collection has been reset"
        }
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset database: {str(e)}")


# ============ ROOT ENDPOINT ============

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "FastAPI RAG Microservice",
        "version": "1.0.0",
        "description": "Retrieval-Augmented Generation service with multi-LLM support",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "ingest": "POST /ingest",
            "query": "POST /query",
            "stats": "GET /stats",
            "reset": "DELETE /reset"
        }
    }


# ============ ERROR HANDLERS ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
