"""
Minimal test endpoint to verify Vercel deployment works
Using Vercel's Python ASGI handler
"""

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "MYTA Backend is running!",
        "service": "test-endpoint"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MYTA Backend Test"
    }

# Mangum adapter for AWS Lambda/Vercel
handler = Mangum(app)

