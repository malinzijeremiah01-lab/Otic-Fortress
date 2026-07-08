from fastapi import APIRouter
router = APIRouter(prefix="/v1/activity-records", tags=["activity-records"])

@router.get("/")
def list_records():
    return []
