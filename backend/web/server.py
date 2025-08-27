import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from backend.common.paths import REACT_BUILD_PATH, TEST_RESULTS_PATH
from backend.common.constants import *
from backend.ai.llm.sgk_agent.agent import sgk_agent
from backend.web.dtos import ChatRequest, ChatResponse
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

@app.get("/vectordbs/list")
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

# Serve the React build folder
app.mount("/", StaticFiles(directory=REACT_BUILD_PATH, html=True), name="static")