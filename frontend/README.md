# FastAPI RAG Frontend

Modern React/Next.js frontend for the FastAPI RAG Microservice with Cyber-Slate Dark Theme.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Update .env.local with your API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   ├── Header.tsx         # Navigation header
│   │   ├── Sidebar.tsx        # Left sidebar
│   │   ├── ChatView.tsx       # Chat interface
│   │   ├── DocumentUpload.tsx # PDF upload zone
│   │   ├── MessageBubble.tsx  # Message component
│   │   └── SourceInspector.tsx# Source viewer
│   ├── hooks/
│   │   ├── useChat.ts         # Chat logic
│   │   └── useDocuments.ts    # Document management
│   ├── services/
│   │   └── api.ts             # API client
│   ├── types/
│   │   └── index.ts           # TypeScript types
│   └── styles/
│       └── theme.css          # Design tokens
├── public/
│   └── favicon.ico
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── README.md
```

## 🎨 Design System

### Color Palette
- **Background**: `#090D16` (Cyber-Slate Dark)
- **Panels**: `#111827` (Card Surface)
- **Accent Cyan**: `#06B6D4` (Primary Interactive)
- **Accent Violet**: `#8B5CF6` (Secondary)
- **Success**: `#10B981` (Positive States)
- **Error**: `#EF4444` (Alert States)

### Typography
- **UI Font**: Inter / System-UI
- **Monospace**: JetBrains Mono / Fira Code

## 🧪 Testing

```bash
# Run tests
npm run test

# Run tests in watch mode
npm run test:watch
```

## 🔨 Building

```bash
# Build for production
npm run build

# Start production server
npm run start
```

## 📝 Environment Variables

Create `.env.local` with the following variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=RAG Studio
NEXT_PUBLIC_API_TIMEOUT=30000
NEXT_PUBLIC_ENABLE_DEBUG_MODE=true
```

## 🔗 API Integration

The frontend communicates with the FastAPI backend via REST API.

### Key Endpoints
- `POST /ingest` - Upload PDF
- `POST /query` - Query documents
- `GET /health` - Health check
- `GET /stats` - Get statistics

See `src/services/api.ts` for implementation.

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Deploy to Vercel
vercel deploy
```

### Docker

```bash
# Build Docker image
docker build -t fastapi-rag-frontend .

# Run container
docker run -p 3000:3000 fastapi-rag-frontend
```

## 📚 Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Lucide Icons](https://lucide.dev)

## 📄 License

MIT License - See LICENSE file for details.
