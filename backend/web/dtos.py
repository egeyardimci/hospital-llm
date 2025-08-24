from typing import Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    llm: str
    query: str
    options: Any
  
class ChatResponse(BaseModel):
    role: str
    content: str