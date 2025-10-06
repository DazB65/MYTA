"""
Working FastAPI backend for MYTA - Vercel compatible
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Dict
import time
import secrets
import hashlib

# Create FastAPI app
app = FastAPI(title="MYTA Backend", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myta-kgvke4oeq-mytas-projects.vercel.app",
        "https://myytagent.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_db = {}

# Models
class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Utility functions
def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}:{pwd_hash.hex()}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, pwd_hash = hashed.split(':')
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex() == pwd_hash
    except:
        return False

# Routes
@app.get("/")
async def root():
    return {"message": "MYTA Backend is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/auth/register")
async def register(user_data: UserRegistration):
    # Basic validation
    if user_data.password != user_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Check if user exists
    if user_data.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user
    user_id = f"user_{secrets.token_urlsafe(16)}"
    hashed_password = hash_password(user_data.password)
    
    users_db[user_data.email] = {
        "user_id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hashed_password,
        "created_at": time.time()
    }
    
    token = f"jwt_token_{user_id}_{int(time.time())}"
    
    return {
        "status": "success",
        "message": "User registered successfully",
        "data": {
            "user_id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "token": token,
            "expires_in": 28800
        }
    }

@app.post("/api/auth/login")
async def login(login_data: UserLogin):
    if login_data.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[login_data.email]
    
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = f"jwt_token_{user['user_id']}_{int(time.time())}"
    
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

@app.post("/api/youtube/auth-url")
async def youtube_auth_url(request_data: Dict[str, str]):
    user_id = request_data.get("userId", "default_user")
    return {
        "status": "success",
        "message": "YouTube OAuth placeholder",
        "authUrl": "https://accounts.google.com/oauth/authorize?placeholder=true",
        "state": f"mock_state_{user_id}"
    }
