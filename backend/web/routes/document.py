from fastapi import APIRouter, HTTPException
from backend.common.paths import SUT_JSON_PATH
import json

router = APIRouter()

@router.get("")
def get_document():
    """Serve the SUT document JSON"""
    try:
        with open(SUT_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading document: {e}")
