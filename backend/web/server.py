from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
from backend.common.paths import REACT_BUILD_PATH, TEST_RESULTS_PATH
from backend.common.constants import *
from backend.ai.llm.sgk_agent.agent import sgk_agent
from backend.web.dtos import ChatRequest, ChatResponse
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB

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

# Serve the React build folder
app.mount("/", StaticFiles(directory=REACT_BUILD_PATH, html=True), name="static")