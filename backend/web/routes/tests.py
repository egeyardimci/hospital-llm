from fastapi import APIRouter, HTTPException
from backend.web.services.tests_service import TestService

router = APIRouter()

@router.get("")
def get_tests():
    try:
        return TestService.get_tests()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )