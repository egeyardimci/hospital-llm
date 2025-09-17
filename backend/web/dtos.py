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
    batch_id: str
    class Config:
        populate_by_name = True
        
class QABatch(BaseModel):
    id: str = Field(alias='_id')
    title: str
    description: str
    class Config:
        populate_by_name = True


class SystemPromptInfo(BaseModel):
    id: str = Field(alias='_id')
    title: str
    content: str
    class Config:
        populate_by_name = True

class TestCase(BaseModel):
    id: str = Field(alias='_id')
    test_id: int
    test_description: str
    llm_name: str
    system_message: str
    qa_batch: str
    similar_vector_count: int
    chunk_size: int
    chunk_overlap: int
    embedding_model_name: str
    options: Any
    class Config:
        populate_by_name = True