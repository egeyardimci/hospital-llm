import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from backend.common.paths import REACT_BUILD_PATH, TEST_RESULTS_PATH
from backend.common.constants import *
from backend.ai.llm.sgk_agent.agent import sgk_agent
from backend.web.dtos import ChatRequest, ChatResponse, VectorDBInfo
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB
from backend.common.paths import *

GLOBAL_VECTOR_DB.load_db(GLOBAL_VECTOR_DB_INITIAL_EMBEDDING_MODEL,GLOBAL_VECTOR_DB_INITIAL_CHUNK_SIZE,GLOBAL_VECTOR_DB_INITIAL_CHUNK_OVERLAP)

app = FastAPI()

# Set the allowed origins - update these as needed
origins = ALLOWED_CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/results")
def get_results():
    try:
        with open(TEST_RESULTS_PATH, "r", encoding="utf-8", errors="replace") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading JSON file: {e}")

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        print(request)
        result = sgk_agent(request.llm, request.query, request.options)
        response = ChatResponse(role="assistant", content=result.content)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {e}")

@app.get("/vectordb/list")
def get_vectordbs():
    try:
        vectordbs_info = []
        chroma_path = Path(CHROMA_DB_DIR)
        
        # Pattern to match names ending with one or more digits
        number_pattern = re.compile(r'\d+$')
        # Pattern to match UUID-like strings (optional, for extra filtering)
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
        
        for item in chroma_path.rglob("*"):
            if (item.is_dir() and 
                item != chroma_path and 
                number_pattern.search(item.name)):
                
                rel_path = item.relative_to(chroma_path)
                
                if uuid_pattern.match(item.name):
                    continue
                    
                name = item.name
                
                if(name.startswith("chroma_db_")):
                    name = name[len("chroma_db_"):]
                else:
                    # Create the normalized path outside the f-string
                    normalized_path = str(rel_path).replace('\\', '/')
                    name = normalized_path[len('chroma_db_'):]

                vectordbs_info.append({
                    "name": name.split('_')[0],
                    "chunk_size": name.split('_')[1],
                    "chunk_overlap": name.split('_')[2],
                })
        
        return vectordbs_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving vector databases: {e}")

@app.post("/vectordb/create")
def create_vectordb_request(request: VectorDBInfo):
    try:
        from backend.ai.vectordb.utils import create_vectordb
        create_vectordb(
            embedding_model_name=request.name,
            chunk_size=int(request.chunk_size),
            chunk_overlap=int(request.chunk_overlap)
        )
        return {"detail": "Vector database created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating vector database: {e}")

@app.post("/vectordb/load")
def load_vectordb_request(request: VectorDBInfo):
    try:
        GLOBAL_VECTOR_DB.load_db(
            embedding_model=request.name,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        return {"detail": "Vector database loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading vector database: {e}")


@app.get("/vectordb/models")
def get_vectordbs():
    try:
        return VECTOR_DB_EMBEDDING_MODELS
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving vector databases: {e}")

@app.get("/vectordb/current")
def get_current_vectordb():
    try:
        return GLOBAL_VECTOR_DB.get_db_name()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving vector databases: {e}")
    
# Serve the React build folder
app.mount("/", StaticFiles(directory=REACT_BUILD_PATH, html=True), name="static")