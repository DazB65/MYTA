"""
Minimal test endpoint to verify Vercel deployment works
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def read_root():
    return JSONResponse({
        "status": "ok",
        "message": "MYTA Backend is running!",
        "service": "test-endpoint"
    })

@app.get("/health")
def health():
    return JSONResponse({
        "status": "healthy",
        "service": "MYTA Backend Test"
    })

# Export for Vercel
handler = app

