from fastapi import APIRouter, HTTPException
from backend.web.dtos import ChatRequest, ChatResponse
from backend.web.services.chat_service import ChatService

router = APIRouter()

@router.post("", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Process a chat request and return the assistant's response.
    
    Args:
        request: ChatRequest containing the user's query and options
        
    Returns:
        ChatResponse with the assistant's response
    """
    try:
        print(f"Chat request: {request}")
        response = ChatService.process_chat_request(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing chat request: {e}"
        )