from typing import Any
from pydantic import BaseModel, Field

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
    
class QAInfo(BaseModel):
    id: str = Field(alias='_id')
    query: str
    answer: str
    class Config:
        populate_by_name = True

class SystemPromptInfo(BaseModel):
    id: str = Field(alias='_id')
    title: str
    content: str
    class Config:
        populate_by_name = True
