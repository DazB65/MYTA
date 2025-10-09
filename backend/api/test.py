"""
FastAPI test endpoint for Vercel serverless
"""

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="MYTA Backend Test")

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "MYTA Backend with FastAPI is running on Vercel!",
        "framework": "FastAPI"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MYTA Backend"
    }

# Mangum handler for Vercel
handler = Mangum(app, lifespan="off")

