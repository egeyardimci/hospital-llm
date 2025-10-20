# Hospital LLM

A comprehensive RAG (Retrieval-Augmented Generation) testing and evaluation platform that enables systematic testing and comparison of different LLM models, embedding models, and retrieval strategies on healthcare documents.

## Overview

Hospital LLM combines a React-based web interface with a FastAPI backend to provide:

- **Multi-Model Testing**: Compare different LLMs (Llama, Deepseek, Mistral, etc.) and embedding models
- **Multiple RAG Strategies**: Support for Vector databases (ChromaDB), Knowledge Graphs (Neo4j), and Hybrid approaches
- **Automated Evaluation**: LLM-as-a-judge for objective scoring of responses and retrieved chunks
- **Interactive Chat Interface**: Real-time Q&A with document-based context
- **Visual Analytics**: Dashboard for analyzing test results grouped by runs
- **Test Configuration**: Web-based UI for managing test cases, Q&A pairs, and system prompts

## Architecture

```
hospital-llm/
   backend/ # FastAPI server, AI modules, database
   frontend/ # React application with Redux
```

### Tech Stack

**Backend:**
- FastAPI for REST API
- MongoDB for data persistence
- ChromaDB for vector storage
- Neo4j for knowledge graphs
- LangChain for LLM orchestration
- Groq API for LLM inference
- Sentence Transformers for embeddings

**Frontend:**
- React 18 with Vite
- Redux Toolkit for state management
- Tailwind CSS for styling
- Recharts for data visualization
- React Select for enhanced dropdowns

## Quick Start

### Prerequisites

- Python 3.8+ (tested with Python 3.13.1)
- Node.js 16+ and npm (tested with Node v22.13.1, npm 10.9.2)
- MongoDB instance (local or Atlas)
- Groq API key
- (Optional) Neo4j instance for graph database features

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hospital-llm
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create `backend/.env` file:
   ```env
   GROQ_API_KEY=gsk_your_api_key
   MONGO_DB_URI=mongodb+srv://your_mongodb_uri
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   NEO4J_DATABASE=neo4j
   AURA_INSTANCEID=your_instance_id
   AURA_INSTANCENAME=your_instance_name
   ```

4. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn backend.web.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

Access the application at `http://localhost:5173`

The API will be available at `http://localhost:8000`

## Core Features

### 1. Test Configuration
- Define test cases with specific LLM and embedding model combinations
- Configure chunking parameters (size, overlap)
- Select RAG database type (Vector, Graph, or Hybrid)
- Enable/disable cross-encoder re-ranking
- Associate Q&A batches with test cases

### 2. Q&A Management
- Create and manage question-answer pairs
- Organize into batches for systematic testing
- Import/export Q&A data

### 3. Test Execution
- Run tests via UI or CLI
- Automatic evaluation using LLM-as-a-judge
- Results stored with detailed metadata
- Each test run assigned a unique `run_count` for grouping

### 4. Results Analysis
- Filter results by LLM, embedding model, run count, etc.
- View detailed evaluation scores and reasoning
- Compare retrieved chunks across different configurations
- Export results for further analysis

### 5. Data Visualization
- Group results by run count, LLM, embedding model, or other parameters
- View average scores and chunk evaluation scores
- Interactive charts with detailed tooltips
- Statistical summaries by configuration

### 6. Interactive Chat
- Real-time Q&A with document context
- Configurable LLM and retrieval settings
- View retrieved chunks and sources

## Key Concepts

### Run Count System
The `run_count` is a global counter that groups all tests executed together in a single batch. This allows:
- Tracking different experimental runs
- Comparing configurations across runs
- Historical analysis of test evolution
- Filtering dashboard data by specific runs

### RAG Database Modes
- **VectorDB**: Traditional semantic search using ChromaDB with configurable embeddings
- **GraphDB**: Knowledge graph queries using Neo4j for structured information retrieval
- **HybridDB**: Combination of vector and graph approaches (experimental)

### Evaluation Metrics
- **Response Score**: LLM-as-judge evaluation of the generated answer quality (0-5 scale)
- **Chunk Score**: LLM-as-judge evaluation of retrieved chunk relevance (0-5 scale)
- Both include reasoning for transparency

## Running Tests

### Via Web UI
1. Navigate to "Test Configurator" tab
2. Create or select a test case
3. Click "Run Test"
4. Monitor progress and view results in "Results" tab

### Via Command Line
```bash
# Run a specific test by test_id
python -m backend.ai.testing.main <test_id>
```

## Project Documentation

- See [backend/README.md](backend/README.md) for backend-specific documentation
- See [frontend/README.md](frontend/README.md) for frontend-specific documentation
- See [CLAUDE.md](CLAUDE.md) for detailed architecture and development guidance

## Development

### Backend Development
```bash
cd backend
# Start with auto-reload
uvicorn backend.web.main:app --reload
```

### Frontend Development
```bash
cd frontend
# Development server with hot reload
npm run dev

# Lint code
npm run lint

# Build for production
npm run build
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

### Backend (.env in backend/)
| Variable | Description | Required |
|----------|-------------|----------|
| GROQ_API_KEY | Groq API key for LLM access | Yes |
| MONGO_DB_URI | MongoDB connection string | Yes |
| NEO4J_URI | Neo4j database URI | No* |
| NEO4J_USERNAME | Neo4j username | No* |
| NEO4J_PASSWORD | Neo4j password | No* |
| NEO4J_DATABASE | Neo4j database name | No* |

*Required only if using GraphDB or HybridDB modes

### Frontend
API endpoint is configured in `frontend/src/constants/index.js` (default: `http://127.0.0.1:8000`)

## Troubleshooting

### Backend won't start
- Verify MongoDB connection string in `.env`
- Check if port 8000 is available
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Frontend won't start
- Verify Node.js version (16+)
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available

### Tests failing
- Verify GROQ_API_KEY is valid
- Check MongoDB connection and required collections exist
- Ensure vector database is initialized (if using VectorDB mode)
- For GraphDB mode, verify Neo4j connection

### No data in dashboard
- Dashboard only shows tests with `run_count` field
- Run some tests to generate data
- Check that backend is running and accessible

## Contributing

1. Create a feature branch
2. Make your changes
3. Run linters: `npm run lint` (frontend)
4. Test your changes thoroughly
5. Submit a pull request

## License

[Add your license here]

## Support

For issues, questions, or contributions, please open an issue on the repository.
