from fastapi import APIRouter, HTTPException
from backend.web.services.runs_service import RunsService

router = APIRouter()

@router.get("")
def get_runs():
    """
    Get test runs from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return RunsService.get_test_runs()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )