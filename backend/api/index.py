"""
Vercel serverless function entry point for MYTA FastAPI backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create a simple FastAPI app for testing
app = FastAPI(
    title="MYTA Backend API",
    version="1.0.0",
    description="MYTA Backend API deployed on Vercel"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MYTA Backend API is running on Vercel!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "myta-backend"}

# Export the app for Vercel
# Vercel will automatically handle ASGI apps like FastAPI
