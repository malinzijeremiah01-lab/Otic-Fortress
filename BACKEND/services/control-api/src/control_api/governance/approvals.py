from fastapi import APIRouter

router = APIRouter(prefix="/v1/approvals", tags=["approvals"])

@router.get("/")
def list_approvals():
    return []
