from fastapi import APIRouter, HTTPException
from backend.web.services.qa_service import QAService
from backend.web.dtos import QAInfo

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
        
@router.post("/add")
def add_qa(request: QAInfo):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        id = QAService.add_qa_pair(request.query, request.answer,request.batch_id, request.path)
        return {"status": "success", "_id": id}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )
        
@router.post("/delete")
def delete_qa(request: QAInfo):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        QAService.delete_qa_pair(request.id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )

@router.post("/update")
def update_qa(request: QAInfo):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return QAService.update_qa_pair(request.id, request.query, request.answer, request.batch_id, request.path)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )