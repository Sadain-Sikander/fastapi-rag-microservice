# FastAPI RAG Microservice

A production-ready **Retrieval-Augmented Generation (RAG)** microservice built with FastAPI, ChromaDB, and multi-LLM support (Google Gemini & Anthropic Claude).

## 🌟 Features

- **📄 Document Ingestion**: Upload and automatically process PDF documents
- **🔍 Semantic Search**: Powered by ChromaDB with vector embeddings
- **🤖 Multi-LLM Support**: Primary (Gemini), Fallback (Claude) with automatic failover
- **⚡ FastAPI Framework**: Modern async Python web framework
- **🔐 Environment Configuration**: Secure .env-based configuration
- **📊 Collection Statistics**: Monitor indexed documents and embeddings
- **🏥 Health Checks**: Built-in health monitoring endpoints
- **🚀 Production Ready**: Logging, error handling, and CORS support

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API Key (or Anthropic Claude API Key)
- pip package manager

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/Sadain-Sikander/fastapi-rag-microservice.git
cd fastapi-rag-microservice
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=development
DEBUG=True
```

### 5. Run the Service

```bash
python main.py
```

The API will be available at `http://localhost:8000`

**Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)

## 📚 API Endpoints

### Health & Info

#### `GET /health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "message": "RAG Microservice is running"
}
```

#### `GET /stats`
Get vector store statistics.

**Response:**
```json
{
  "collection_name": "pdf_docs",
  "document_count": 42,
  "embedding_model": "default"
}
```

#### `GET /`
API information and available endpoints.

---

### Document Management

#### `POST /ingest`
Upload and index a PDF document.

**Request:**
- `file` (UploadFile): PDF file to process

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "file": "document.pdf",
  "chunks_indexed": 125,
  "message": "Successfully indexed 125 chunks from document.pdf"
}
```

---

### Query & Chat

#### `POST /query`
Query the indexed documents with RAG.

**Request Body:**
```json
{
  "question": "What is machine learning?",
  "top_k": 3
}
```

**Parameters:**
- `question` (string, required): User's question
- `top_k` (integer, optional): Number of context chunks to retrieve (1-10, default 3)

**Response:**
```json
{
  "question": "What is machine learning?",
  "answer": "Machine learning is a subset of artificial intelligence...",
  "sources_used": 3,
  "model_used": "gemini-2.0-flash",
  "message": "Response generated successfully"
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "top_k": 3
  }'
```

#### `POST /chat`
Alias for `/query` endpoint (same functionality).

---

### Admin Operations

#### `DELETE /reset`
⚠️ **WARNING**: Deletes all indexed documents from the vector store.

**Response:**
```json
{
  "status": "success",
  "message": "Vector store collection has been reset"
}
```

## 📁 Project Structure

```
fastapi-rag-microservice/
├── main.py                 # FastAPI application & endpoints
├── config.py              # Configuration management
├── models.py              # Pydantic request/response schemas
├── document_processor.py   # PDF extraction & chunking
├── vector_store.py        # ChromaDB integration
├── llm_adapter.py         # Multi-LLM provider abstraction
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

```env
# API Configuration
ENVIRONMENT=development          # development or production
DEBUG=True                       # Enable debug mode
API_HOST=0.0.0.0               # API server host
API_PORT=8000                  # API server port

# LLM Provider Keys
GEMINI_API_KEY=xxx             # Google Gemini API key
ANTHROPIC_API_KEY=xxx          # Anthropic Claude API key

# ChromaDB Configuration
CHROMA_COLLECTION_NAME=pdf_docs              # Collection name
CHROMA_PERSIST_DIRECTORY=./chroma_data       # Storage directory

# LLM Model Configuration
PRIMARY_LLM_MODEL=gemini-2.0-flash           # Primary model
FALLBACK_LLM_MODEL=claude-3-5-sonnet-20241022  # Fallback model
CHUNK_SIZE=500                 # Text chunk size in characters
TOP_K_RESULTS=3                # Default retrieval count

# System Prompt
SYSTEM_PROMPT="Use ONLY..."    # Instruction for LLM
```

## 🤖 LLM Providers

### Google Gemini
- **Model**: `gemini-2.0-flash` (primary)
- **API Key**: `GEMINI_API_KEY`
- **Docs**: https://ai.google.dev/

### Anthropic Claude
- **Model**: `claude-3-5-sonnet-20241022` (fallback)
- **API Key**: `ANTHROPIC_API_KEY`
- **Docs**: https://docs.anthropic.com/

## 🔄 Processing Pipeline

```
PDF Upload
    ↓
PDF Extraction (PyPDF)
    ↓
Text Chunking (500 chars default)
    ↓
Vector Embedding (ChromaDB)
    ↓
Vector Storage
    ↓
User Query
    ↓
Semantic Search (ChromaDB)
    ↓
Context Retrieval (top-k chunks)
    ↓
LLM Response Generation (Gemini/Claude)
    ↓
RAG Response to User
```

## 📦 Dependencies

Key dependencies:

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **ChromaDB**: Vector database
- **PyPDF**: PDF processing
- **google-generativeai**: Gemini API
- **anthropic**: Claude API
- **pydantic**: Data validation
- **pydantic-settings**: Configuration management
- **python-multipart**: File upload support

See `requirements.txt` for complete list.

## 🧪 Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test Ingestion

```bash
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@sample.pdf"
```

### Test Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 3
  }'
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY not configured"
- Ensure `.env` file exists and contains `GEMINI_API_KEY`
- Check API key is valid at https://aistudio.google.com

### "No relevant documents found"
- Ensure documents have been ingested via `/ingest`
- Check `/stats` endpoint to verify document count
- Try `/reset` and re-ingest documents

### Vector Store Connection Issues
- Verify `CHROMA_PERSIST_DIRECTORY` is writable
- Check disk space availability
- Restart the service

### LLM API Errors
- Verify API keys are correct
- Check API rate limits
- Monitor API quota usage in respective dashboards

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV ENVIRONMENT=production
CMD ["python", "main.py"]
```

### Environment Variables (Production)

Set environment variables securely:
- Use container secrets management
- Use cloud provider secret managers (AWS Secrets Manager, GCP Secret Manager)
- Never commit `.env` with real API keys

## 📊 Monitoring

The service provides:

- Structured logging to console
- Health check endpoint (`/health`)
- Collection statistics (`/stats`)
- Error tracking and logging

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues and questions:
- Open a GitHub Issue
- Check existing documentation
- Review API docs at `/docs`

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- ChromaDB for vector database capabilities
- Google Gemini and Anthropic Claude for LLM APIs
- PyPDF for PDF processing

---

**Built with ❤️ by Sadain Sikander**

Last Updated: September 2024
