from typing import Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    llm: str
    query: str
    options: Any
  
class ChatResponse(BaseModel):
    role: str
    content: str

class VectorDBInfo(BaseModel):
    name: str
    chunk_size: str
    chunk_overlap: str