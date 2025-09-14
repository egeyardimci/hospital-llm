from fastapi import APIRouter, HTTPException
from backend.web.services.qa_service import QAService

router = APIRouter()

@router.get("")
def get_qas():
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return QAService.get_qa_pairs()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )