"""
Vercel serverless function entry point for MYTA FastAPI backend
"""

import sys
import os
import traceback

# Add the parent directory to the Python path so we can import from App
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try to import the full FastAPI app
    from App.main import app
    print("✅ Successfully imported full MYTA FastAPI app")

except Exception as e:
    print(f"⚠️ Failed to import full app, falling back to enhanced simple app: {e}")
    traceback.print_exc()

    # Fallback to enhanced simple FastAPI app with basic functionality
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from .simple_routers import health_router, session_router, auth_router

    app = FastAPI(
        title="MYTA Backend API",
        version="1.0.0",
        description="""
        MYTA Backend API deployed on Vercel

        ## Features
        - Health monitoring endpoints
        - Basic authentication system
        - Session management
        - User registration and login

        This is a simplified version optimized for serverless deployment.
        """,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://myta-cew6m1h8v-mytas-projects.vercel.app",
            "https://myta-4rbwrdcfu-mytas-projects.vercel.app",
            "https://app.myytagent.app",
            "https://myytagent.app",
            "http://localhost:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(session_router)
    app.include_router(auth_router)

    @app.get("/")
    async def root():
        return {
            "message": "MYTA Backend API is running on Vercel!",
            "status": "success",
            "mode": "enhanced",
            "docs_url": "/docs",
            "health_url": "/api/health"
        }

# Export the app for Vercel
# Vercel will automatically handle ASGI apps like FastAPI
