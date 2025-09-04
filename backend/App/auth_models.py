"""
Authentication Models for Vidalytics
Secure user authentication with password hashing and session management
"""

from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext
import secrets
import uuid

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    remember_me: bool = False

class UserResponse(BaseModel):
    """User response model (safe for API responses)"""
    id: str
    email: str
    name: str
    is_verified: bool
    subscription_tier: str
    youtube_connected: bool
    created_at: datetime
    last_login: Optional[datetime]

class PasswordReset(BaseModel):
    """Password reset request model"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation model"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @validator('new_password')
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
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Ensure passwords match"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class ChangePassword(BaseModel):
    """Change password request model"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str
    
    @validator('new_password')
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
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Ensure passwords match"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

class User:
    """User model for database operations"""

    def __init__(self, email: str, name: str, password_hash: str,
                 user_id: str = None, is_verified: bool = False,
                 subscription_tier: str = "free", youtube_connected: bool = False,
                 created_at: datetime = None, last_login: datetime = None,
                 verification_token: str = None, reset_token: str = None,
                 reset_token_expires: datetime = None):
        self.id = user_id or str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.is_verified = is_verified
        self.subscription_tier = subscription_tier
        self.youtube_connected = youtube_connected
        self.created_at = created_at or datetime.utcnow()
        self.last_login = last_login
        self.verification_token = verification_token
        self.reset_token = reset_token
        self.reset_token_expires = reset_token_expires

    @classmethod
    def create_user(cls, email: str, name: str, password: str) -> 'User':
        """Create a new user with hashed password"""
        password_hash = pwd_context.hash(password)
        verification_token = secrets.token_urlsafe(32)
        return cls(
            email=email,
            name=name,
            password_hash=password_hash,
            verification_token=verification_token
        )

    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(password, self.password_hash)

    def update_password(self, new_password: str):
        """Update user password with new hash"""
        self.password_hash = pwd_context.hash(new_password)

    def generate_reset_token(self) -> str:
        """Generate password reset token"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        return self.reset_token

    def verify_reset_token(self, token: str) -> bool:
        """Verify password reset token"""
        if not self.reset_token or not self.reset_token_expires:
            return False
        if datetime.utcnow() > self.reset_token_expires:
            return False
        return self.reset_token == token

    def clear_reset_token(self):
        """Clear password reset token"""
        self.reset_token = None
        self.reset_token_expires = None

    def to_dict(self) -> dict:
        """Convert user to dictionary for database storage"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'password_hash': self.password_hash,
            'is_verified': self.is_verified,
            'subscription_tier': self.subscription_tier,
            'youtube_connected': self.youtube_connected,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'verification_token': self.verification_token,
            'reset_token': self.reset_token,
            'reset_token_expires': self.reset_token_expires.isoformat() if self.reset_token_expires else None
        }

    def to_response(self) -> UserResponse:
        """Convert user to safe response model"""
        return UserResponse(
            id=self.id,
            email=self.email,
            name=self.name,
            is_verified=self.is_verified,
            subscription_tier=self.subscription_tier,
            youtube_connected=self.youtube_connected,
            created_at=self.created_at,
            last_login=self.last_login
        )

# Utility functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(password, hashed)
