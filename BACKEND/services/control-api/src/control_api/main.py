from fastapi import FastAPI
from .governance.approvals import router as approvals_router

app = FastAPI(title="Fortress Control API")
app.include_router(approvals_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "control-api"}
