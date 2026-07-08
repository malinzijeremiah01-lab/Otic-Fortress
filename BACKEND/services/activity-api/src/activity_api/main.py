from fastapi import FastAPI
from .records.routes import router as records_router

app = FastAPI(title="Fortress Activity API")
app.include_router(records_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "activity-api"}
