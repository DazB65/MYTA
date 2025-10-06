"""
Supabase User Service for Vidalytics
Secure user management with Supabase PostgreSQL database operations
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from supabase import create_client, Client
from .auth_models import User, UserRegistration, UserLogin
from .database_security import generate_secure_id
import uuid

logger = logging.getLogger(__name__)

class SupabaseUserService:
    """Service for user management operations using Supabase"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment variables")
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        logger.info("Supabase user service initialized successfully")
    
    def create_user(self, registration: UserRegistration, ip_address: str = None,
                   user_agent: str = None) -> User:
        """Create a new user account with enhanced security"""
        try:
            # Check if user already exists
            existing_user = self.get_user_by_email(registration.email)
            if existing_user:
                raise ValueError("User with this email already exists")

            # Generate secure user ID (UUID for Supabase)
            secure_user_id = str(uuid.uuid4())

            # Create user object with secure ID
            user = User.create_user(
                email=registration.email,
                name=registration.name,
                password=registration.password
            )
            user.id = secure_user_id

            # Insert user into Supabase
            user_data = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "password_hash": user.password_hash,
                "is_verified": user.is_verified,
                "subscription_tier": user.subscription_tier,
                "youtube_connected": user.youtube_connected,
                "created_at": user.created_at.isoformat(),
                "verification_token": user.verification_token
            }

            result = self.supabase.table("users").insert(user_data).execute()
            
            if not result.data:
                raise Exception("Failed to create user in database")

            logger.info(f"User created successfully: {user.email}")
            return user

        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        try:
            result = self.supabase.table("users").select("*").eq("email", email).execute()
            
            if result.data and len(result.data) > 0:
                return self._row_to_user(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")
            raise
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            result = self.supabase.table("users").select("*").eq("id", user_id).execute()
            
            if result.data and len(result.data) > 0:
                return self._row_to_user(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Failed to get user by ID: {e}")
            raise
    
    def authenticate_user(self, login: UserLogin, ip_address: str = None,
                         user_agent: str = None) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            user = self.get_user_by_email(login.email)
            if not user:
                logger.warning(f"Login attempt for non-existent user: {login.email}")
                return None

            if not user.verify_password(login.password):
                logger.warning(f"Invalid password attempt for user: {login.email}")
                return None

            # Update last login
            user.last_login = datetime.utcnow()
            self.update_user(user)

            logger.info(f"User authenticated successfully: {user.email}")
            return user

        except Exception as e:
            logger.error(f"Failed to authenticate user: {e}")
            raise
    
    def update_user(self, user: User):
        """Update user in database"""
        try:
            update_data = {
                "name": user.name,
                "password_hash": user.password_hash,
                "is_verified": user.is_verified,
                "subscription_tier": user.subscription_tier,
                "youtube_connected": user.youtube_connected,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "verification_token": user.verification_token,
                "reset_token": user.reset_token,
                "reset_token_expires": user.reset_token_expires.isoformat() if user.reset_token_expires else None
            }

            result = self.supabase.table("users").update(update_data).eq("id", user.id).execute()
            
            if not result.data:
                raise Exception("Failed to update user in database")
                
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise
    
    def _row_to_user(self, row: dict) -> User:
        """Convert database row to User object"""
        return User(
            user_id=row['id'],
            email=row['email'],
            name=row['name'],
            password_hash=row['password_hash'],
            is_verified=bool(row['is_verified']) if row['is_verified'] is not None else False,
            subscription_tier=row['subscription_tier'] or 'free',
            youtube_connected=bool(row['youtube_connected']) if row['youtube_connected'] is not None else False,
            created_at=datetime.fromisoformat(row['created_at'].replace('Z', '+00:00')) if row['created_at'] else None,
            last_login=datetime.fromisoformat(row['last_login'].replace('Z', '+00:00')) if row['last_login'] else None,
            verification_token=row['verification_token'],
            reset_token=row['reset_token'],
            reset_token_expires=datetime.fromisoformat(row['reset_token_expires'].replace('Z', '+00:00')) if row['reset_token_expires'] else None
        )

# Global user service instance
supabase_user_service = SupabaseUserService()
