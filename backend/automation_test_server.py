"""
Simple test server for automation endpoints
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import the simple automation router
from App.simple_automation_router import router as automation_router

app = FastAPI(title="MYTA Automation Test Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include automation router
app.include_router(automation_router)

@app.get("/")
async def root():
    return {"message": "MYTA Automation Test Server", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "automation_endpoints": "available"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
