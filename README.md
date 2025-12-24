# Intelligent Document Service

An AI-powered backend system for document ingestion, processing, and semantic search.

The service allows authenticated users to upload documents, extract text page-wise, process them asynchronously, generate embeddings, store them in a vector database (Qdrant), and query documents using semantic similarity.

---

## Architecture Overview

### Tech Stack

- **API**: FastAPI (async)
- **Auth**: JWT (access tokens)
- **Database**: PostgreSQL (JSONB for page-wise text storage)
- **Background Processing**: Celery + Redis
- **Vector DB**: Qdrant
- **Embeddings**: DeepInfra Embeddings (LangChain)
- **PDF Processing**: PyMuPDF (fitz)

### High-Level Flow
```
Client
  ↓
FastAPI (Auth, Upload, Query)
  ↓
PostgreSQL (raw extracted text, metadata)
  ↓
Celery Worker (async processing)
  ↓
Qdrant (vector embeddings)
```

---

## Features

- ✅ JWT-based authentication (register / login)
- ✅ Secure document upload
- ✅ Page-wise text extraction from PDFs
- ✅ JSONB storage (no per-page tables)
- ✅ Asynchronous background processing
- ✅ Chunking with overlap
- ✅ Vector embeddings + semantic search
- ✅ Stateless, horizontally scalable services

---

## Project Structure
```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   ├── users.py
│       │   ├── documents.py
│       │   └── query.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── responses.py
│   ├── exceptions.py
│   └── celery_app.py
│
├── db/
│   ├── base.py
│   ├── postgres.py
│   └── vector_db.py
│
├── models/
│   ├── user.py
│   └── document.py
│
├── repositories/
│   ├── user_repository.py
│   └── document_repository.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   ├── document_service.py
│   ├── chunking_service.py
│   └── embedding_service.py
│
├── tasks/
│   └── document_tasks.py
│
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── document.py
│   └── query.py
│
├── main.py
│
alembic/
│   ├── env.py
│   └── versions/
│
.env
README.md
requirements.txt
```

---

## Environment Variables

Create a `.env` file at the project root:
```env
# App
APP_NAME=Intelligent Document Service
ENV=development
SECRET_KEY=super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/intelligent_doc_service

# Redis (Celery)
REDIS_URL=redis://localhost:6379/0

# Qdrant
QDRANT_URL=https://<qdrant-host>:6333
QDRANT_API_KEY=your_qdrant_api_key

# Embeddings (DeepInfra)
API_KEY=your_deepinfra_api_key
EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## Installation

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Database Setup

### 1. Create Database
```sql
CREATE DATABASE intelligent_doc_service;
```

### 2. Run Migrations
```bash
alembic upgrade head
```

**Verify tables:**
```bash
psql -d intelligent_doc_service -c "\dt"
```

---

## Running the Application

### Start FastAPI (Development)
```bash
fastapi dev app/main.py
```

**API will be available at:**
- http://127.0.0.1:8000

**Swagger docs:**
- http://127.0.0.1:8000/docs

### Running Celery Worker

Celery must be running separately.
```bash
celery -A app.core.celery_app worker -l info
```

> **Note:** Ensure Redis is running before starting Celery.

---

## API Usage

### Authentication Flow

#### Register
```http
POST /api/v1/auth/register
```

#### Login
```http
POST /api/v1/auth/login
```

Returns JWT access token.

#### Authenticated Requests

Add header:
```
Authorization: Bearer <access_token>
```

---

### Document Upload
```http
POST /api/v1/documents/upload
```

**Features:**
- Accepts PDF file
- Extracts text page-wise
- Stores JSON in PostgreSQL
- Triggers background Celery task

**Response includes:**
- `document_id`
- `filename`
- `status`
- Page-wise extracted text

---

### Document Processing (Async)

Handled by Celery worker:

1. Chunk text per page
2. Apply overlap
3. Generate embeddings
4. Ensure Qdrant collection exists
5. Store vectors with metadata

> FastAPI never blocks on embeddings.

---

### Semantic Query
```http
POST /api/v1/query
```

**Input:**
- `document_id`
- `query` text
- `top_k`

**Flow:**
1. Embed query
2. Vector search in Qdrant
3. Return ranked text chunks with scores

---

## Design Decisions

### PostgreSQL over MongoDB
- Strong consistency
- JSONB indexing
- Lower infra complexity

### Celery for async work
- Decouples heavy processing

### Qdrant for vectors
- High-performance similarity search

### No per-page tables
- Faster ingestion
- Simpler schema

### Scalability
- FastAPI scales horizontally
- Celery workers scale independently
- Qdrant handles vector load
- PostgreSQL stores only raw text + metadata

---

## Production Notes

- Use `fastapi run` instead of `dev`
- Use a process manager (systemd / Docker / Kubernetes)
- Run Celery with multiple workers
- Enable SSL for Qdrant & Postgres
- Rotate JWT secret periodically

---

## License