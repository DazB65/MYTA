"""
Simplified routers for Vercel serverless deployment
Contains basic versions of key endpoints without complex dependencies
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os

# Simple response models
class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str

# Create routers
health_router = APIRouter(prefix="/api/health", tags=["health"])
session_router = APIRouter(prefix="/api/session", tags=["session"])
auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

# Health endpoints
@health_router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="myta-backend",
        version="1.0.0",
        environment=os.getenv("VERCEL_ENV", "development")
    )

@health_router.get("/detailed")
async def detailed_health():
    """Detailed health check with system info"""
    return {
        "status": "healthy",
        "service": "myta-backend",
        "version": "1.0.0",
        "environment": os.getenv("VERCEL_ENV", "development"),
        "region": os.getenv("VERCEL_REGION", "unknown"),
        "deployment_id": os.getenv("VERCEL_DEPLOYMENT_ID", "unknown"),
        "timestamp": "2024-01-01T00:00:00Z"  # Would use datetime in real implementation
    }

# Session endpoints (simplified)
@session_router.post("/login")
async def login(credentials: Dict[str, str]):
    """Simplified login endpoint"""
    # In real implementation, this would validate credentials and create session
    email = credentials.get("email")
    password = credentials.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Mock successful login
    return StandardResponse(
        status="success",
        message="Login successful",
        data={
            "user_id": "mock_user_123",
            "email": email,
            "session_token": "mock_session_token_123"
        }
    )

@session_router.post("/logout")
async def logout():
    """Simplified logout endpoint"""
    return StandardResponse(
        status="success",
        message="Logout successful"
    )

@session_router.get("/me")
async def get_current_user():
    """Get current user info (simplified)"""
    # In real implementation, this would validate session and return user data
    return StandardResponse(
        status="success",
        message="User data retrieved",
        data={
            "user_id": "mock_user_123",
            "email": "user@example.com",
            "name": "Mock User",
            "subscription_status": "active"
        }
    )

# Auth endpoints (simplified)
@auth_router.post("/register")
async def register(user_data: Dict[str, str]):
    """Simplified user registration"""
    email = user_data.get("email")
    password = user_data.get("password")
    name = user_data.get("name")
    
    if not all([email, password, name]):
        raise HTTPException(status_code=400, detail="Email, password, and name required")
    
    # Mock successful registration
    return StandardResponse(
        status="success",
        message="Registration successful",
        data={
            "user_id": "mock_user_new_123",
            "email": email,
            "name": name
        }
    )

@auth_router.post("/forgot-password")
async def forgot_password(email_data: Dict[str, str]):
    """Simplified password reset"""
    email = email_data.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email required")
    
    # Mock password reset
    return StandardResponse(
        status="success",
        message="Password reset email sent"
    )
