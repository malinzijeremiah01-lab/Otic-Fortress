from datetime import datetime, timezone
from fastapi import APIRouter
from .telemetry_handler import accept_telemetry

router = APIRouter(prefix="/v1")

@router.post("/telemetry", status_code=202)
async def telemetry(event: dict):
    accepted = await accept_telemetry(event)
    return {"accepted": accepted, "received_at": datetime.now(timezone.utc).isoformat()}
