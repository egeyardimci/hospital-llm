from fastapi import APIRouter, HTTPException
from backend.web.services.results_service import ResultsService

router = APIRouter()

@router.get("")
def get_results():
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return ResultsService.get_test_results()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )