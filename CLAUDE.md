# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hospital LLM is a RAG (Retrieval-Augmented Generation) testing and evaluation platform that combines a React frontend with a FastAPI backend. The system allows testing different LLM models and embedding models on documents, evaluates results using LLM-as-a-judge, and visualizes performance metrics.

## Architecture

### Backend (`backend/`)

**Core Components:**
- **FastAPI Server** (`backend/web/main.py`): Main API server with CORS configured for local development
- **MongoDB Database** (`backend/web/database/main.py`): Singleton pattern MongoDB client managing collections:
  - `results`: Test execution results with scores
  - `runs`: Run attributes and metadata grouped by `run_count`
  - `queries`: Q&A pairs for testing
  - `qa_batches`: Grouped Q&A sets
  - `test_cases`: Test configurations
  - `system_prompts`: System messages for LLMs
  - `config`: Application configuration

**AI Modules:**
- **RAG System** (`backend/ai/llm/rag.py`): Supports three database modes:
  - `VectorDB`: ChromaDB-based vector similarity search
  - `GraphDB`: Neo4j knowledge graph queries
  - `HybridDB`: Combination of vector and graph retrieval
- **Testing Framework** (`backend/ai/testing/main.py`):
  - `run_test_case_by_test_id()`: Main entry point for running tests
  - Tracks test runs with `run_count` - a monotonically increasing counter serving as a unique identifier for grouping related test executions
  - Saves results to MongoDB with evaluation scores
- **LLM as Judge** (`backend/ai/llm/llm_as_a_judge/`): Evaluates responses and retrieved chunks separately
- **Vector DB** (`backend/ai/vectordb/`): ChromaDB management with different embeddings
- **Graph DB** (`backend/ai/graphdb/`): Neo4j integration for knowledge graph queries
- **Cross-Encoder** (`backend/ai/llm/cross_encoder.py`): Re-ranks retrieved chunks for improved relevance

**API Routes** (`backend/web/routes/`):
- `/chat`: Chatbot interactions
- `/results`: Test results retrieval
- `/tests`: Test case CRUD and execution
- `/runs`: Run attributes by run_count
- `/qa`, `/qa-batches`: Q&A management
- `/system-prompts`: System prompt templates
- `/vectordb`: Vector database operations
- `/config`: Application configuration

### Frontend (`frontend/`)

**Redux Store** (`frontend/src/store/`):
- `results`: Test execution results (filtered data)
- `runs`: Run attributes indexed by `run_count`
- `tests`: Test configurations
- `qa` / `qaBatches`: Q&A data management
- `systemPrompts`: System prompt templates
- `vectorDBs`: Available vector databases
- `config`: App configuration
- `filters`: Result filtering state
- `chat`: Chatbot state
- `toast`: Notification system

**Feature Modules** (`frontend/src/features/`):
- `dashboard/`: Data visualization with charts (grouped by `run_count`)
  - **Important**: Dashboard components filter out any test data without `run_count` field
- `results/`: Test results display and filtering
- `chat/`: Interactive chatbot interface
- `testing/`: Test configuration UI
- `vectordb/`: Vector database management
- `qa-editor/`: Q&A pair editor
- `system-prompts/`: System prompt management
- `settings/`: Application settings

**Key Concepts:**
- Uses Vite for fast development builds
- Redux Toolkit for state management with async thunks
- React Select for dropdowns
- Recharts for data visualization
- Tailwind CSS for styling

## Development Commands

### Backend

Start the FastAPI server:
```bash
cd backend
uvicorn backend.web.main:app --reload --host 0.0.0.0 --port 8000
```

Run a single test by test_id (from project root):
```bash
python -m backend.ai.testing.main <test_id>
```

### Frontend

Development server (from `frontend/` directory):
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

Lint code:
```bash
npm run lint
```

Auto-fix linting issues:
```bash
npm run lint:fix
```

Preview production build:
```bash
npm run preview
```

## Environment Setup

### Backend Environment Variables (`.env` in `backend/`)
```
GROQ_API_KEY=gsk_...
MONGO_DB_URI=mongodb+srv://...
NEO4J_URI=...
NEO4J_USERNAME=...
NEO4J_PASSWORD=...
NEO4J_DATABASE=...
AURA_INSTANCEID=...
AURA_INSTANCENAME=...
```

### Frontend Configuration
API endpoint is configured in `frontend/src/constants/index.js` (default: `http://127.0.0.1:8000`)

## Key Implementation Details

### Run Count System
- `run_count` is a global counter stored in MongoDB that increments with each test batch execution
- All test results from a single execution share the same `run_count` value
- Run attributes (LLM, embedding model, chunk size, etc.) are stored in the `runs` collection indexed by `run_count`
- The dashboard and visualization features group data by `run_count` instead of the legacy `test_id`
- Tests without `run_count` are filtered out from dashboard visualizations

### Test Execution Flow
1. Load test case by `test_id` from MongoDB
2. Retrieve current `run_count` from config collection
3. Load associated Q&A batch
4. For each Q&A pair:
   - Retrieve context using selected RAG database (Vector/Graph/Hybrid)
   - Apply cross-encoder re-ranking if enabled
   - Generate answer using selected LLM
   - Evaluate with LLM-as-judge (response + chunks)
   - Save result to MongoDB with `run_count`
5. Store run attributes in `runs` collection
6. Increment global `run_count`

### RAG Database Options
- **VectorDB**: Uses ChromaDB with similarity search, supports cross-encoder re-ranking
- **GraphDB**: Uses Neo4j for knowledge graph queries, returns structured context
- **HybridDB**: Combines both approaches (implementation may vary)

### Constants and Configuration
- LLM models: Deepseek, Llama, Mistral, GPT variants (see `backend/common/constants.py`)
- Embedding models: BGE-M3, LaBSE, Arctic Embed, Turkish BERT variants
- Cross-encoders: MS-MARCO, mxbai, BGE reranker, GTE multilingual
- CORS origins: `http://localhost:5173`, `http://127.0.0.1:5173`

## Common Patterns

### Adding a New Redux Slice
1. Create slice file in `frontend/src/store/slices/`
2. Import and add reducer to `frontend/src/store/index.js`
3. Use `useAppSelector` hook to access state in components

### Adding a New API Endpoint
1. Create route handler in `backend/web/routes/`
2. Include router in `backend/web/main.py`
3. Add endpoint constant to `frontend/src/constants/index.js`
4. Create async thunk in corresponding Redux slice

### Working with Test Data
- Always check for `run_count` existence when working with dashboard/visualization features
- Use Redux store's `runs` slice to access run attributes
- Filter out tests without `run_count` when grouping or visualizing data

## Database Schema Highlights

**Test Results** (`results` collection):
- Contains: `test_id`, `run_count`, `llm`, `embedding_model`, `chunk_size`, `evaluation_score`, `chunk_evaluation_score`, `retrieved_chunks`, `options`, `rag_database`, etc.

**Run Attributes** (`runs` collection):
- Indexed by `run_count`
- Contains: test configuration snapshot (LLM, embeddings, chunk settings, QA batch reference)

**Test Cases** (`test_cases` collection):
- Contains: `test_id`, LLM config, embedding config, chunking params, system prompt, QA batch reference, RAG database type
