"""
Ultra-minimal Railway app - guaranteed to work
No complex imports or dependencies
"""

import os
from fastapi import FastAPI
from datetime import datetime

# Create the simplest possible FastAPI app
app = FastAPI(
    title="MYTA Railway Test",
    description="Minimal test app for Railway deployment",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "MYTA Railway deployment test",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "port": os.getenv("PORT", "8888")
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/test")
def test_endpoint():
    return {
        "test": "success",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "python_path": os.getenv("PYTHONPATH", "not_set")
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8888))
    uvicorn.run(app, host="0.0.0.0", port=port)
