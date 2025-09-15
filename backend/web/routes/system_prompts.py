from fastapi import APIRouter, HTTPException
from backend.web.services.system_prompts_service import SystemPromptsService
from backend.web.dtos import SystemPromptInfo

router = APIRouter()

@router.get("")
def get_system_prompts():
    """
    Get system prompts from the database.
    
    Returns:
        Dictionary containing the system prompts data
    """
    try:
        return SystemPromptsService.get_system_prompts()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading system prompts: {e}"
        )
        
@router.post("/add")
def add_system_prompt(request: SystemPromptInfo):
    """
    Add a new system prompt to the database.
    
    Returns:
        Dictionary containing the success status and ID
    """
    try:
        id = SystemPromptsService.add_system_prompt(request.title, request.content)
        return {"status": "success", "_id": id}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error adding system prompt: {e}"
        )
        
@router.post("/delete")
def delete_system_prompt(request: SystemPromptInfo):
    """
    Delete a system prompt from the database.
    
    Returns:
        Dictionary containing the success status
    """
    try:
        SystemPromptsService.delete_system_prompt(request.id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting system prompt: {e}"
        )

@router.post("/update")
def update_system_prompt(request: SystemPromptInfo):
    """
    Update a system prompt in the database.
    
    Returns:
        Dictionary containing the success status
    """
    try:
        SystemPromptsService.update_system_prompt(request.id, request.title, request.content)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating system prompt: {e}"
        )