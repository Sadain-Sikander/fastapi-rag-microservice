# FastAPI RAG Microservice - Full Stack

A production-ready **Retrieval-Augmented Generation (RAG)** system combining a FastAPI backend with a modern Next.js frontend, featuring dual LLM support (Google Gemini & Claude), PDF document processing, and vector search capabilities.

## 📁 Project Structure

```
fastapi-rag-microservice/
├── backend/                    # FastAPI Application
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration & environment variables
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── routes.py      # API endpoints
│   │   │   └── models.py      # Pydantic models
│   │   ├── services/
│   │   │   ├── pdf_processor.py
│   │   │   ├── vector_store.py
│   │   │   └── llm_service.py
│   │   └── utils/
│   │       └── helpers.py
│   ├── chroma_data/           # Vector database (local)
│   └── uploads/               # Uploaded PDF files
│
├── frontend/                   # Next.js React Application
│   ├── package.json           # Node dependencies
│   ├── next.config.js         # Next.js configuration
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # Tailwind CSS config
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Main page
│   │   │   └── globals.css    # Global styles
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── ChatView.tsx
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── SourceInspector.tsx
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   └── useDocuments.ts
│   │   ├── services/
│   │   │   └── api.ts         # API client
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript types
│   │   └── styles/
│   │       └── theme.css      # Design tokens
│   └── .env.local.example
│
├── docker-compose.yml         # Multi-container orchestration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # Main documentation
├── DESIGN.md                 # UI/UX specifications
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT License
```

## 🌟 Features

- **📄 Document Ingestion**: Upload and automatically process PDF documents
- **🔍 Semantic Search**: Powered by ChromaDB with vector embeddings
- **🤖 Multi-LLM Support**: Primary (Gemini), Fallback (Claude) with automatic failover
- **⚡ FastAPI Backend**: Modern async Python web framework
- **🎨 Modern Frontend**: Next.js with Tailwind CSS and Cyber-Slate Dark Theme
- **🔐 Environment Configuration**: Secure .env-based configuration
- **📊 Real-time Chat Interface**: Interactive conversation with AI
- **🏥 Health Checks**: Built-in health monitoring endpoints
- **🚀 Production Ready**: Docker support, logging, error handling, and CORS

## 🚀 Quick Start (Local Development)

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **npm or yarn**
- **Git**

### Option 1: Run Backend Only

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cd ..
cp .env.example .env
# Edit .env with your API keys

# 5. Run the backend server
cd backend
python main.py
```

**Backend available at**: `http://localhost:8000`
**API Docs**: `http://localhost:8000/docs`

### Option 2: Run Frontend Only

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Setup environment variables
cp .env.local.example .env.local
# Add NEXT_PUBLIC_API_URL=http://localhost:8000

# 4. Run the development server
npm run dev
```

**Frontend available at**: `http://localhost:3000`

### Option 3: Run Both (Recommended for Full Stack)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Now open `http://localhost:3000` in your browser!

---

## 🐳 Docker Deployment

### Using Docker Compose (Both Services)

```bash
# Build and run both backend and frontend
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Individual Docker Commands

```bash
# Backend only
cd backend
docker build -t fastapi-rag-backend .
docker run -p 8000:8000 --env-file ../.env fastapi-rag-backend

# Frontend only
cd frontend
docker build -t fastapi-rag-frontend .
docker run -p 3000:3000 fastapi-rag-frontend
```

---

## 📚 API Documentation

### Endpoints

#### 1. **Upload PDF**
```bash
POST /ingest
Content-Type: multipart/form-data

Request:
- file: PDF file

Response (201):
{
  "status": "success",
  "file": "document.pdf",
  "chunks_indexed": 125,
  "message": "Successfully indexed 125 chunks from document.pdf"
}
```

#### 2. **Query Documents**
```bash
POST /query
Content-Type: application/json

Request:
{
  "question": "What is this document about?",
  "top_k": 3
}

Response (200):
{
  "question": "What is this document about?",
  "answer": "Based on the context...",
  "sources_used": 3,
  "model_used": "gemini-2.0-flash",
  "message": "Response generated successfully"
}
```

#### 3. **Health Check**
```bash
GET /health

Response (200):
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "message": "RAG Microservice is running"
}
```

#### 4. **Get Stats**
```bash
GET /stats

Response (200):
{
  "collection_name": "pdf_docs",
  "document_count": 42,
  "embedding_model": "default"
}
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# === API Configuration ===
ENVIRONMENT=development
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# === LLM Provider Keys ===
GEMINI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# === ChromaDB Configuration ===
CHROMA_COLLECTION_NAME=pdf_docs
CHROMA_PERSIST_DIRECTORY=./chroma_data

# === LLM Model Configuration ===
PRIMARY_LLM_MODEL=gemini-2.0-flash
FALLBACK_LLM_MODEL=claude-3-5-sonnet-20241022
CHUNK_SIZE=500
TOP_K_RESULTS=3
```

### Frontend Environment (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RAG Studio
```

---

## 📊 Tech Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Vector DB**: ChromaDB
- **LLM APIs**: Google Gemini, Anthropic Claude
- **PDF Processing**: PyPDF
- **Validation**: Pydantic
- **Container**: Docker

### Frontend
- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Animations**: Framer Motion
- **HTTP Client**: Axios / React Query
- **Language**: TypeScript

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't start | Check Python version (3.11+), activate venv, install requirements |
| Frontend won't start | Check Node version (18+), install dependencies, check .env.local |
| API connection error | Verify NEXT_PUBLIC_API_URL in frontend .env.local |
| Port already in use | Change API_PORT or NEXT_PUBLIC_API_URL in .env files |
| PDF upload fails | Check file size, format, and backend logs |
| Vector search returns no results | Verify ChromaDB is running, documents are indexed |

---

## 📖 Documentation

- **[Backend Setup](./backend/README.md)** - Python/FastAPI specific docs
- **[Frontend Setup](./frontend/README.md)** - React/Next.js specific docs
- **[DESIGN.md](./DESIGN.md)** - UI/UX specification
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - How to contribute

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file for details

---

## 👨‍💻 Author

**Sadain Sikander** - [GitHub](https://github.com/Sadain-Sikander)

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## ⭐ Support

If you find this project helpful, please consider giving it a star! ⭐
