from fastapi import APIRouter, HTTPException
from backend.web.services.qa_batch_service import QABatchService
from backend.web.dtos import QABatch

router = APIRouter()

@router.get("")
def get_qa_batches():
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return QABatchService.get_qa_batches()
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )
        
@router.post("/add")
def add_qa_batch(request: QABatch):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        id = QABatchService.add_qa_batch(request.title, request.description)
        return {"status": "success", "_id": id}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )
        
@router.post("/delete")
def delete_qa_batch(request: QABatch):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        QABatchService.delete_qa_batch(request.id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )

@router.post("/update")
def update_qa_batch(request: QABatch):
    """
    Get test results from the JSON file.
    
    Returns:
        Dictionary containing the test results data
    """
    try:
        return QABatchService.update_qa_batch(request.id, request.title, request.description)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading JSON file: {e}"
        )