from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.web.dtos import VectorDBInfo
from backend.web.services.vectordb_service import VectorDBService

router = APIRouter()

@router.get("/list")
def get_vectordbs():
    """
    Get list of available vector databases.
    
    Returns:
        List of vector database information
    """
    try:
        return VectorDBService.get_available_vectordbs()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving vector databases: {e}"
        )

@router.post("/create")
def create_vectordb_request(request: VectorDBInfo):
    """
    Create a new vector database.
    
    Args:
        request: VectorDBInfo containing database parameters
        
    Returns:
        Success message
    """
    try:
        VectorDBService.create_vectordb(request)
        return {"detail": "Vector database created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating vector database: {e}"
        )

@router.post("/load")
def load_vectordb_request(request: VectorDBInfo):
    """
    Load an existing vector database.
    
    Args:
        request: VectorDBInfo containing database parameters
        
    Returns:
        Success message
    """
    try:
        VectorDBService.load_vectordb(request)
        return {"detail": "Vector database loaded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading vector database: {e}"
        )

@router.get("/models")
def get_vectordb_models():
    """
    Get list of available embedding models.
    
    Returns:
        List of available embedding model names
    """
    try:
        return VectorDBService.get_available_models()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving embedding models: {e}"
        )

@router.get("/current")
def get_current_vectordb():
    """
    Get the currently loaded vector database name.
    
    Returns:
        Name of the current vector database
    """
    try:
        return VectorDBService.get_current_vectordb()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error retrieving current vector database: {e}"
        )