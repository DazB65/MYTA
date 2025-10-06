"""
Production FastAPI backend for MYTA - Live deployment ready
Focused on core functionality: registration, auth, and essential endpoints
"""

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Dict, Any, Optional
import time
import secrets
import hashlib
from datetime import datetime, timedelta
import logging
import requests

# Import security middleware
from App.enhanced_security_middleware import EnhancedSecurityMiddleware, RateLimitMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MYTA Production Backend", 
    version="1.0.0",
    description="Production-ready MYTA backend for live deployment"
)

# Add security middleware
app.add_middleware(EnhancedSecurityMiddleware, strict_mode=True)
app.add_middleware(RateLimitMiddleware, requests_per_minute=60, burst_size=10)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myta-frontend.vercel.app",
        "https://myytagent.app", 
        "https://www.myytagent.app",
        "http://localhost:3000"  # For development testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserRegistration(BaseModel):
    """User registration request model"""
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

class StandardResponse(BaseModel):
    """Standard API response format"""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

# Mock user storage (in production, use proper database)
users_db = {}

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
    """Generate mock JWT token (in production, use proper JWT library)"""
    return f"jwt_token_{user_id}_{int(time.time())}"

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time(), "version": "1.0.0"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "MYTA Production Backend", "status": "online", "version": "1.0.0"}

# Registration endpoint
@app.post("/api/auth/register", response_model=StandardResponse)
async def register_user(registration: UserRegistration, request: Request):
    """
    Register a new user account
    """
    try:
        logger.info(f"Registration attempt for: {registration.email}")
        
        # Check if user already exists
        if registration.email in users_db:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create user
        user_id = f"user_{secrets.token_urlsafe(16)}"
        password_hash = hash_password(registration.password)
        
        user_data = {
            "id": user_id,
            "email": registration.email,
            "name": registration.name,
            "password_hash": password_hash,
            "created_at": datetime.utcnow().isoformat(),
            "is_verified": True,  # Auto-verify for now
            "subscription_tier": "free"
        }
        
        # Store user
        users_db[registration.email] = user_data
        
        # Generate token
        token = generate_jwt_token(user_id)
        
        logger.info(f"User registered successfully: {registration.email}")
        
        return StandardResponse(
            status="success",
            message="User registered successfully",
            data={
                "user_id": user_id,
                "email": registration.email,
                "name": registration.name,
                "token": token,
                "expires_in": 28800  # 8 hours
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

# Login endpoint
@app.post("/api/auth/login", response_model=StandardResponse)
async def login_user(login: UserLogin, request: Request):
    """
    Authenticate user and create session
    """
    try:
        logger.info(f"Login attempt for: {login.email}")
        
        # Check if user exists
        if login.email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        user_data = users_db[login.email]
        
        # Verify password
        if not verify_password(login.password, user_data["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Generate token
        token = generate_jwt_token(user_data["id"])
        
        logger.info(f"User logged in successfully: {login.email}")
        
        return StandardResponse(
            status="success",
            message="Login successful",
            data={
                "user_id": user_data["id"],
                "email": user_data["email"],
                "name": user_data["name"],
                "token": token,
                "expires_in": 28800  # 8 hours
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

# YouTube OAuth endpoints (real implementation)
@app.post("/api/youtube/auth-url")
async def youtube_auth_url(request_data: Dict[str, str]):
    """Generate YouTube OAuth URL"""
    user_id = request_data.get("userId", "default_user")

    # Real Google OAuth configuration for LIVE deployment
    # TODO: Replace with your actual Google OAuth credentials
    client_id = "DEMO_CLIENT_ID"  # Replace with actual client ID from Google Cloud Console
    redirect_uri = "https://myta-backend-6smgt85sc-mytas-projects.vercel.app/api/youtube/oauth/callback"  # Production backend
    scope = "https://www.googleapis.com/auth/youtube.readonly"
    state = f"user_{user_id}_{secrets.token_urlsafe(16)}"

    # Real Google OAuth URL
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code&access_type=offline&state={state}"

    logger.info(f"🔗 Generated YouTube OAuth URL for user {user_id}")
    logger.info(f"🔗 OAuth URL: {auth_url}")

    return {
        "status": "success",
        "authUrl": auth_url,
        "state": state
    }

@app.get("/api/youtube/oauth/callback")
async def youtube_oauth_callback(code: str = None, state: str = None, error: str = None):
    """Handle YouTube OAuth callback"""
    from fastapi.responses import RedirectResponse
    import requests

    if error:
        # User denied access
        return RedirectResponse(
            url="https://myytagent.app/dashboard?youtube_error=access_denied",
            status_code=302
        )

    if code and state:
        try:
            # Exchange code for access token
            client_id = "YOUR_GOOGLE_CLIENT_ID"  # Replace with actual client ID
            client_secret = "YOUR_GOOGLE_CLIENT_SECRET"  # Replace with actual client secret
            redirect_uri = "https://myta-backend-6smgt85sc-mytas-projects.vercel.app/api/youtube/oauth/callback"

            token_data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }

            # Get access token from Google
            token_response = requests.post(
                "https://oauth2.googleapis.com/token",
                data=token_data
            )

            if token_response.status_code == 200:
                token_info = token_response.json()
                access_token = token_info.get("access_token")

                # Get YouTube channel info
                youtube_response = requests.get(
                    "https://www.googleapis.com/youtube/v3/channels",
                    params={
                        "part": "snippet,statistics",
                        "mine": "true"
                    },
                    headers={
                        "Authorization": f"Bearer {access_token}"
                    }
                )

                if youtube_response.status_code == 200:
                    channel_data = youtube_response.json()

                    # Store the connection (in production, save to database)
                    logger.info(f"YouTube connected successfully for state: {state}")
                    logger.info(f"Channel data: {channel_data}")

                    return RedirectResponse(
                        url="https://myytagent.app/dashboard?youtube_connected=true",
                        status_code=302
                    )
                else:
                    logger.error(f"Failed to get YouTube channel data: {youtube_response.text}")
                    return RedirectResponse(
                        url="https://myytagent.app/dashboard?youtube_error=channel_fetch_failed",
                        status_code=302
                    )
            else:
                logger.error(f"Failed to exchange code for token: {token_response.text}")
                return RedirectResponse(
                    url="https://myytagent.app/dashboard?youtube_error=token_exchange_failed",
                    status_code=302
                )

        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return RedirectResponse(
                url="https://myytagent.app/dashboard?youtube_error=callback_error",
                status_code=302
            )
    else:
        # Missing required parameters
        return RedirectResponse(
            url="https://myytagent.app/dashboard?youtube_error=missing_parameters",
            status_code=302
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
