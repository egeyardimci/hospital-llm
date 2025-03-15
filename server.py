from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from main import run_one_test

app = FastAPI()

# Set the allowed origins - update these as needed
origins = [
    "http://localhost:3000",  # React app default port
    "http://localhost:8000",
]

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
        with open("./results.json", "r", encoding="utf-8", errors="replace") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading JSON file: {e}")

# Define a Pydantic model for the POST request data
class ChatRequest(BaseModel):
    llm: str
    embedding_model: str
    system_message: str
    query: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        result = run_one_test(
            request.llm, 
            request.embedding_model, 
            request.system_message, 
            request.query,
            500, 50, 10
        )
        
        response = {
            "role": "assistant",
            "content": result
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {e}")

# Serve the React build folder
app.mount("/", StaticFiles(directory="react_build", html=True), name="static")
