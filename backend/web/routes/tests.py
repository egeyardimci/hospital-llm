from fastapi import APIRouter, HTTPException
from backend.web.services.tests_service import TestService
from backend.web.database.utils import remove_objectid
from backend.web.dtos import TestCase

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

@router.post("/add")
def add_test(test_data: TestCase):
    try:
        id = TestService.add_test(dict(remove_objectid(test_data)))
        return {"status": "success", "_id": id}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error adding test case: {e}"
        )

@router.post("/update")
def update_test(test_data: TestCase):
    try:
        TestService.update_test(test_data.id, dict(remove_objectid(test_data)))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating test case: {e}"
        )

@router.post("/delete")
def delete_test(test_data: TestCase):
    try:
        TestService.delete_test(test_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error deleting test case: {e}"
        )