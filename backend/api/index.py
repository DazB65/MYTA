"""
Production FastAPI backend for MYTA - Vercel deployment
Uses Supabase for data persistence and proper JWT authentication
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
import jwt
import bcrypt
import secrets
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to Python path for imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Create FastAPI app optimized for serverless
app = FastAPI(
    title="MYTA Production Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Updated for correct frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myta-app.vercel.app",  # Correct frontend URL
        "https://myytagent.app",       # Custom domain
        "http://localhost:3000"        # Development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables - Backend uses clean naming
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET") or os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32))

# Pydantic models with proper validation
class UserRegistration(BaseModel):
    """User registration request model with validation"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: str = Field(..., min_length=2, max_length=100)
    confirm_password: str

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Ensure passwords match"""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str

# Utility functions for authentication
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against bcrypt hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def generate_jwt_token(user_id: str, email: str) -> str:
    """Generate JWT token"""
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_jwt_token(token: str) -> Dict[str, Any]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Supabase HTTP client
class SupabaseClient:
    """Simple HTTP client for Supabase REST API"""

    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            logger.warning("Supabase credentials not found, using fallback storage")
            self.enabled = False
            return

        self.enabled = True
        self.url = SUPABASE_URL.rstrip('/')
        self.headers = {
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user in Supabase"""
        if not self.enabled:
            # Fallback to in-memory storage for development
            user_id = f"user_{secrets.token_urlsafe(16)}"
            return {
                "id": user_id,
                "email": user_data["email"],
                "name": user_data["name"],
                "created_at": datetime.utcnow().isoformat()
            }

        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/rest/v1/users",
                headers=self.headers,
                json=user_data
            )
            if response.status_code == 201:
                return response.json()[0]
            elif response.status_code == 409:
                raise HTTPException(status_code=400, detail="User already exists")
            else:
                error_detail = response.text
                logger.error(f"Supabase error: {response.status_code} - {error_detail}")
                raise HTTPException(status_code=500, detail=f"Failed to create user: {error_detail}")

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email from Supabase"""
        if not self.enabled:
            return None

        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.url}/rest/v1/users",
                headers=self.headers,
                params={"email": f"eq.{email}"}
            )
            if response.status_code == 200:
                users = response.json()
                return users[0] if users else None
            return None

# Initialize Supabase client
supabase = SupabaseClient()

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MYTA Production Backend",
        "status": "online",
        "version": "1.0.0",
        "timestamp": time.time(),
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "MYTA Production Backend",
        "platform": "Vercel Serverless",
        "supabase_enabled": supabase.enabled
    }

@app.post("/api/auth/register")
async def register_user(user_data: UserRegistration, request: Request):
    """Register a new user with Supabase persistence"""
    try:
        logger.info(f"Registration attempt for: {user_data.email}")

        # Check if user already exists
        existing_user = await supabase.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Hash password
        password_hash = hash_password(user_data.password)

        # Create user data
        user_record = {
            "email": user_data.email,
            "name": user_data.name,
            "password_hash": password_hash,
            "created_at": datetime.utcnow().isoformat(),
            "is_verified": True,
            "subscription_tier": "free"
        }

        # Create user in Supabase
        user = await supabase.create_user(user_record)

        # Generate JWT token
        token = generate_jwt_token(user["id"], user["email"])

        logger.info(f"User registered successfully: {user_data.email}")

        return {
            "status": "success",
            "message": "User registered successfully",
            "data": {
                "user_id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "token": token,
                "expires_in": 28800  # 8 hours
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/api/auth/login")
async def login_user(login_data: UserLogin):
    """Login user with Supabase authentication"""
    try:
        logger.info(f"Login attempt for: {login_data.email}")

        # Get user from Supabase
        user = await supabase.get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        if not verify_password(login_data.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT token
        token = generate_jwt_token(user["id"], user["email"])

        logger.info(f"User logged in successfully: {login_data.email}")

        return {
            "status": "success",
            "message": "Login successful",
            "data": {
                "user_id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "token": token,
                "expires_in": 28800  # 8 hours
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/api/youtube/auth-url")
async def youtube_auth_url(request_data: dict):
    """Generate YouTube OAuth URL (placeholder for now)"""
    user_id = request_data.get("userId", "default_user")

    return {
        "status": "success",
        "message": "YouTube OAuth placeholder",
        "authUrl": "https://accounts.google.com/oauth/authorize?placeholder=true",
        "state": f"mock_state_{user_id}"
    }
