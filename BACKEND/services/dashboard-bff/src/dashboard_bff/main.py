from fastapi import FastAPI

app = FastAPI(title="Fortress Dashboard BFF")

@app.get("/health")
def health():
    return {"status": "ok", "service": "dashboard-bff"}
