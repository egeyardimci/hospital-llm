# Hospital LLM - Backend

FastAPI-based backend server providing REST APIs for RAG testing, evaluation, and document Q&A with support for multiple LLM models, embedding strategies, and database modes.

## Architecture

### Core Modules

```
backend/
├── web/                    # FastAPI application and routes
│   ├── main.py            # FastAPI app entry point
│   ├── database/          # MongoDB client (singleton pattern)
│   └── routes/            # API route handlers
├── ai/                    # AI and ML modules
│   ├── llm/              # LLM integrations
│   │   ├── rag.py        # RAG system implementation
│   │   ├── llm_as_a_judge/  # Evaluation system
│   │   ├── cross_encoder.py # Re-ranking
│   │   └── prompts.py    # System prompts
│   ├── testing/          # Test execution framework
│   │   ├── main.py       # Test runner
│   │   ├── io_utils.py   # Database I/O
│   │   └── models.py     # Pydantic models
│   ├── vectordb/         # ChromaDB management
│   │   ├── main.py       # Vector DB initialization
│   │   └── utils.py      # Vector DB utilities
│   └── graphdb/          # Neo4j integration
│       └── utils.py      # Graph DB utilities
├── common/               # Shared utilities
│   ├── constants.py      # Model names, DB options
│   ├── config.py         # Application config
│   └── paths.py          # Path definitions
└── utils/                # Helper utilities
    └── logger.py         # Logging configuration
```

## Getting Started

### Prerequisites

- Python 3.8 or higher (tested with Python 3.13.1)
- MongoDB instance (local or Atlas)
- Groq API key
- (Optional) Neo4j database for GraphDB features

### Installation

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   MONGO_DB_URI=mongodb+srv://username:password@cluster.mongodb.net/

   # Optional: For GraphDB features
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   NEO4J_DATABASE=neo4j
   AURA_INSTANCEID=your_instance_id
   AURA_INSTANCENAME=your_instance_name
   ```

   See `.env.example` for a template.

### Running the Server

**Development mode with auto-reload:**
```bash
uvicorn backend.web.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn backend.web.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Chat
- `POST /chat`: Send a query and get an AI-generated response with context

### Results
- `GET /results`: Fetch all test execution results

### Tests
- `GET /tests`: List all test configurations
- `POST /tests/add`: Create a new test case
- `POST /tests/update`: Update existing test case
- `POST /tests/delete`: Delete a test case
- `POST /tests/run`: Execute a test by test_id

### Runs
- `GET /runs`: Fetch run attributes grouped by run_count

### Q&A Management
- `GET /qa`: List all Q&A pairs
- `POST /qa/add`: Create a new Q&A pair
- `POST /qa/update`: Update existing Q&A pair
- `POST /qa/delete`: Delete a Q&A pair

### Q&A Batches
- `GET /qa-batches`: List all Q&A batches
- `POST /qa-batches/add`: Create a new batch
- `POST /qa-batches/update`: Update existing batch
- `POST /qa-batches/delete`: Delete a batch

### System Prompts
- `GET /system-prompts`: List all system prompts
- `POST /system-prompts/add`: Create a new system prompt
- `POST /system-prompts/update`: Update existing prompt
- `POST /system-prompts/delete`: Delete a prompt

### Vector Database
- `GET /vectordb/list`: List available vector databases
- `GET /vectordb/models`: List available embedding models
- `GET /vectordb/current`: Get currently loaded vector database
- `POST /vectordb/load`: Load a specific vector database
- `POST /vectordb/create`: Create a new vector database

### Configuration
- `GET /config`: Fetch application configuration

## MongoDB Collections

The application uses the following MongoDB collections in the `hospital` database:

### `results`
Stores test execution results with evaluation scores.

**Fields:**
- `test_id`: Reference to test configuration
- `run_count`: Unique identifier grouping related test runs
- `llm`: LLM model used
- `embedding_model`: Embedding model used
- `chunk_size`, `chunk_overlap`: Chunking parameters
- `similar_vector_count`: Number of vectors retrieved
- `query`, `expected_answer`, `response`: Q&A data
- `evaluation_score`, `evaluation`, `evaluation_reasoning`: Response evaluation
- `chunk_evaluation_score`, `chunk_evaluation`, `chunk_evaluation_reasoning`: Chunk evaluation
- `retrieved_chunks`: Retrieved document chunks
- `options`: Test options (e.g., cross-encoder config)
- `rag_database`: Database type (VectorDB/GraphDB/HybridDB)
- `time_stamp`: Execution timestamp
- `error`: Error message if test failed

### `runs`
Stores run attributes indexed by `run_count`.

**Fields:**
- `run_count`: Unique run identifier
- `test_id`: Reference to test configuration
- `llm`, `embedding_model`, `chunk_size`, etc.: Configuration snapshot
- `qa_batch_id`: Associated Q&A batch
- `rag_database`: Database type used

### `test_cases`
Test configurations.

**Fields:**
- `test_id`: Unique test identifier (string)
- `llm_name`: LLM model to use
- `embedding_model_name`: Embedding model
- `system_message`: System prompt text
- `chunk_size`, `chunk_overlap`: Chunking parameters
- `similar_vector_count`: Number of vectors to retrieve
- `options`: Array of test options
- `rag_database`: Database type (VectorDB/GraphDB/HybridDB)
- `qa_batch`: Reference to Q&A batch ObjectId

### `queries`
Individual Q&A pairs.

**Fields:**
- `query`: Question text
- `answer`: Expected answer

### `qa_batches`
Grouped Q&A sets.

**Fields:**
- `name`: Batch name
- `queries`: Array of ObjectIds referencing `queries` collection

### `system_prompts`
System prompt templates.

**Fields:**
- `name`: Prompt name
- `content`: Prompt text

### `config`
Application configuration and counters.

**Fields:**
- `name`: Config key (e.g., "run_count")
- `data`: Config value

## Running Tests

### Execute a Test Case

**Via API:**
```bash
curl -X POST "http://localhost:8000/tests/run" \
  -H "Content-Type: application/json" \
  -d '{"test_id": "your_test_id"}'
```

**Via Python Module:**
```bash
# From project root
python -m backend.ai.testing.main <test_id>
```

### Test Execution Flow

1. Load test configuration by `test_id`
2. Retrieve current global `run_count`
3. Load associated Q&A batch
4. For each Q&A pair:
   - Retrieve context using selected RAG database
   - Apply cross-encoder re-ranking if enabled
   - Generate answer using LLM
   - Evaluate response and chunks with LLM-as-judge
   - Save result to `results` collection with `run_count`
5. Save run attributes to `runs` collection
6. Increment global `run_count`

## RAG System

### Database Modes

**VectorDB Mode:**
- Uses ChromaDB for semantic similarity search
- Supports multiple embedding models
- Optional cross-encoder re-ranking
- Configurable number of retrieved chunks

**GraphDB Mode:**
- Uses Neo4j for knowledge graph queries
- Structured information retrieval
- Returns formatted context from graph relationships

**HybridDB Mode:**
- Combines vector and graph approaches
- Experimental feature

### Supported Models

**LLM Models (via Groq):**
- `deepseek-r1-distill-llama-70b`
- `llama-3.2-90b-vision-preview`
- `llama-3.3-70b-versatile`
- `meta-llama/llama-4-maverick-17b-128e-instruct`
- `mistral-saba-24b`
- `openai/gpt-oss-120b`

**Embedding Models:**
- `BAAI/bge-m3`
- `LaBSE`
- `Snowflake/snowflake-arctic-embed-l-v2.0`
- `emrecan/bert-base-turkish-cased-mean-nli-stsb-tr`
- `sentence-transformers/all-mpnet-base-v2`

**Cross-Encoder Models:**
- `cross-encoder/ms-marco-MiniLM-L6-v2`
- `mixedbread-ai/mxbai-rerank-base-v1`
- `BAAI/bge-reranker-v2-m3`
- `Alibaba-NLP/gte-multilingual-reranker-base`

See `backend/common/constants.py` for the full list.

## LLM-as-a-Judge

The evaluation system uses a separate LLM to score:

1. **Response Quality** (0-5 scale)
   - Compares generated answer to expected answer
   - Provides reasoning for the score
   - Returns feedback

2. **Chunk Relevance** (0-5 scale)
   - Evaluates if retrieved chunks contain answer
   - Provides reasoning
   - Returns feedback

Both evaluations use Pydantic models for structured output validation.

## Vector Database Management

### Creating a Vector Database

```python
from backend.ai.vectordb.utils import create_vectordb

# Create with specific embedding model and chunking
create_vectordb(
    embedding_model_name="BAAI/bge-m3",
    chunk_size=500,
    chunk_overlap=50
)
```

### Loading a Vector Database

```python
from backend.ai.vectordb.utils import load_vectordb

db = load_vectordb(
    embedding_model_name="BAAI/bge-m3",
    chunk_size=500,
    chunk_overlap=50
)
```

Vector databases are stored in `backend/ai/chroma_db/` directory.

## Logging

The application uses a colored logger configured in `backend/utils/logger.py`.

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages

## Cross-Encoder Re-Ranking

When enabled in test options, the system re-ranks retrieved chunks using a cross-encoder model for improved relevance.

**Configuration:**
```python
{
    "name": "CE",
    "is_enabled": true,
    "data": {
        "model_name": "cross-encoder/ms-marco-MiniLM-L6-v2",
        "top_k": 5
    }
}
```

## Error Handling

- All test execution errors are captured and stored in the `error` field of results
- Failed tests still create result records for tracking
- Evaluation errors are logged and stored separately
- RAG system errors prevent evaluation but log detailed messages

## Development

### Code Structure

- **Routes** (`web/routes/`): Keep API endpoints thin, delegate to service layer
- **Database** (`web/database/`): Use singleton MongoDB client
- **AI Modules** (`ai/`): Modular LLM, vector DB, and testing logic
- **Constants** (`common/constants.py`): Centralize model names and options
- **Type Safety**: Use Pydantic models for request/response validation

### Adding a New LLM Model

1. Add model name constant to `backend/common/constants.py`
2. Ensure Groq API supports the model
3. Update frontend constants if needed

### Adding a New Embedding Model

1. Add model name to `backend/common/constants.py`
2. Ensure model is available via Sentence Transformers
3. Create vector database with the new embedding
4. Update frontend constants

## Troubleshooting

### MongoDB Connection Issues
- Verify `MONGO_DB_URI` in `.env`
- Check network connectivity to MongoDB
- Ensure database user has proper permissions

### Groq API Errors
- Verify `GROQ_API_KEY` is valid
- Check API rate limits
- Ensure selected model is available

### Vector Database Not Found
- Create vector database first using `/vectordb/create` endpoint
- Verify embedding model name matches exactly
- Check `backend/ai/chroma_db/` directory exists

### Neo4j Connection Issues
- Verify Neo4j credentials in `.env`
- Ensure Neo4j instance is running
- Check network connectivity to Neo4j

### Import Errors
- Ensure you're running from project root
- Verify Python path includes backend directory
- Use `python -m backend.module.file` syntax

## Performance Considerations

- **Batch Processing**: Run multiple tests in a single batch for efficiency
- **Vector DB Caching**: Vector databases are loaded once and reused
- **MongoDB Indexing**: Consider adding indexes on frequently queried fields
- **Concurrent Execution**: Current implementation runs tests sequentially (see TODO.md for concurrency plans)

## Security Notes

- Never commit `.env` file to version control
- Rotate API keys regularly
- Use environment-specific MongoDB credentials
- Implement authentication for production deployments
- Sanitize user inputs in chat endpoints

## Future Enhancements

See issues page on Github for planned features and improvements.
