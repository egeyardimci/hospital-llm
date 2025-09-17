from fastapi import APIRouter, HTTPException
from backend.common.config import CONFIG

router = APIRouter()

@router.get("")
def get_config():
    try:
        return CONFIG
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing chat request: {e}"
        )