"""
Minimal FastAPI backend for MYTA - Live deployment ready
No complex imports, just core functionality
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, validator
from typing import Dict, Any
import time
import secrets
import hashlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MYTA Minimal Backend", 
    version="1.0.0",
    description="Minimal MYTA backend for live deployment"
)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myta-kgvke4oeq-mytas-projects.vercel.app",  # Current frontend
        "https://myytagent.app", 
        "https://www.myytagent.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory user storage (for testing)
users_db = {}

# Pydantic models
class UserRegistration(BaseModel):
    """User registration request model"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str

# Utility functions
def hash_password(password: str) -> str:
    """Hash password securely"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pwd_hash.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        salt, pwd_hash = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex() == pwd_hash
    except:
        return False

def generate_jwt_token(user_id: str) -> str:
    """Generate mock JWT token"""
    return f"jwt_token_{user_id}_{int(time.time())}"

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MYTA Minimal Backend is running!",
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "timestamp": time.time(), 
        "version": "1.0.0",
        "service": "MYTA Minimal Backend"
    }

@app.post("/api/auth/register")
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    try:
        logger.info(f"Registration attempt for: {user_data.email}")
        
        # Check if user already exists
        if user_data.email in users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Generate user ID
        user_id = f"user_{secrets.token_urlsafe(16)}"
        
        # Store user
        users_db[user_data.email] = {
            "user_id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "password_hash": hashed_password,
            "created_at": time.time()
        }
        
        # Generate token
        token = generate_jwt_token(user_id)
        
        logger.info(f"User registered successfully: {user_data.email}")
        
        return {
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "user_id": user_id,
                "email": user_data.email,
                "name": user_data.name,
                "token": token,
                "expires_in": 28800  # 8 hours
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/login")
async def login_user(login_data: UserLogin):
    """Login user"""
    try:
        logger.info(f"Login attempt for: {login_data.email}")
        
        # Check if user exists
        if login_data.email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = users_db[login_data.email]
        
        # Verify password
        if not verify_password(login_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Generate token
        token = generate_jwt_token(user["user_id"])
        
        logger.info(f"User logged in successfully: {login_data.email}")
        
        return {
            "status": "success",
            "message": "Login successful",
            "data": {
                "user_id": user["user_id"],
                "email": user["email"],
                "name": user["name"],
                "token": token,
                "expires_in": 28800
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/youtube/auth-url")
async def youtube_auth_url(request_data: Dict[str, str]):
    """Generate YouTube OAuth URL (simplified)"""
    user_id = request_data.get("userId", "default_user")
    
    # For now, return a placeholder response
    return {
        "status": "success",
        "message": "YouTube OAuth not implemented yet",
        "authUrl": "https://accounts.google.com/oauth/authorize?placeholder=true",
        "state": f"mock_state_{user_id}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
