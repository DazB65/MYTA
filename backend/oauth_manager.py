"""
OAuth 2.0 Token Management for CreatorMate
Handles YouTube OAuth flow, token storage, and refresh mechanisms
"""

import os
import json
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urlencode, parse_qs, urlparse
import sqlite3
import asyncio
from contextlib import asynccontextmanager

import httpx
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class OAuthToken:
    """OAuth token data structure"""
    user_id: str
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: str
    created_at: datetime
    updated_at: datetime
    
    def is_expired(self) -> bool:
        """Check if token is expired with 5-minute buffer"""
        return datetime.now() >= (self.expires_at - timedelta(minutes=5))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['expires_at'] = self.expires_at.isoformat()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OAuthToken':
        """Create from dictionary"""
        data['expires_at'] = datetime.fromisoformat(data['expires_at'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)

@dataclass
class OAuthState:
    """OAuth state for security"""
    state: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    
    def is_expired(self) -> bool:
        """Check if state is expired"""
        return datetime.now() >= self.expires_at

class OAuthManager:
    """Manages OAuth 2.0 flow for YouTube API access"""
    
    def __init__(self, db_path: str = "creatormate.db"):
        self.db_path = db_path
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("OAUTH_REDIRECT_URI")
        
        # OAuth scopes for YouTube access
        self.scopes = [
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/yt-analytics.readonly",
            "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"
        ]
        
        # In-memory state storage (for development)
        self._oauth_states: Dict[str, OAuthState] = {}
        
        # Initialize database
        self._init_database()
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            logger.warning("OAuth credentials not fully configured. Check .env file.")
    
    def _init_database(self):
        """Initialize OAuth tokens table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS oauth_tokens (
                        user_id TEXT PRIMARY KEY,
                        access_token TEXT NOT NULL,
                        refresh_token TEXT NOT NULL,
                        token_type TEXT NOT NULL,
                        expires_at TEXT NOT NULL,
                        scope TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                conn.commit()
                logger.info("OAuth database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize OAuth database: {e}")
    
    def generate_authorization_url(self, user_id: str) -> Tuple[str, str]:
        """Generate OAuth authorization URL"""
        try:
            # Create state for security
            state = secrets.token_urlsafe(32)
            oauth_state = OAuthState(
                state=state,
                user_id=user_id,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(minutes=10)
            )
            
            # Store state (in production, use Redis or database)
            self._oauth_states[state] = oauth_state
            
            # Create Flow object
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            
            flow.redirect_uri = self.redirect_uri
            
            # Generate authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state,
                prompt='consent'  # Force consent to get refresh token
            )
            
            logger.info(f"Generated OAuth URL for user {user_id}")
            return auth_url, state
            
        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {e}")
            raise
    
    async def handle_callback(self, code: str, state: str) -> Optional[OAuthToken]:
        """Handle OAuth callback and exchange code for tokens"""
        try:
            # Validate state
            if state not in self._oauth_states:
                logger.error(f"Invalid OAuth state: {state}")
                return None
            
            oauth_state = self._oauth_states[state]
            if oauth_state.is_expired():
                logger.error(f"Expired OAuth state: {state}")
                del self._oauth_states[state]
                return None
            
            user_id = oauth_state.user_id
            
            # Exchange code for tokens
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes,
                state=state
            )
            
            flow.redirect_uri = self.redirect_uri
            
            # Fetch tokens
            flow.fetch_token(code=code)
            
            # Extract token information
            credentials = flow.credentials
            # Convert expiry to naive datetime if it has timezone info
            if credentials.expiry.tzinfo is not None:
                expires_at = credentials.expiry.replace(tzinfo=None)
            else:
                expires_at = credentials.expiry
            
            # Create token object
            oauth_token = OAuthToken(
                user_id=user_id,
                access_token=credentials.token,
                refresh_token=credentials.refresh_token,
                token_type="Bearer",
                expires_at=expires_at,
                scope=" ".join(self.scopes),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Store token in database
            await self._store_token(oauth_token)
            
            # Fetch and store the user's actual channel information
            await self._fetch_and_store_channel_info(oauth_token)
            
            # Clean up state
            del self._oauth_states[state]
            
            logger.info(f"Successfully stored OAuth token for user {user_id}")
            return oauth_token
            
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            return None
    
    async def _store_token(self, token: OAuthToken):
        """Store OAuth token in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO oauth_tokens 
                    (user_id, access_token, refresh_token, token_type, expires_at, scope, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    token.user_id,
                    token.access_token,
                    token.refresh_token,
                    token.token_type,
                    token.expires_at.isoformat(),
                    token.scope,
                    token.created_at.isoformat(),
                    token.updated_at.isoformat()
                ))
                conn.commit()
                logger.info(f"Stored OAuth token for user {token.user_id}")
        except Exception as e:
            logger.error(f"Failed to store OAuth token: {e}")
            raise
    
    async def _fetch_and_store_channel_info(self, token: OAuthToken):
        """Fetch user's actual channel information and store it"""
        try:
            # Create credentials for YouTube API
            credentials = Credentials(
                token=token.access_token,
                refresh_token=token.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes
            )
            
            # Build YouTube service
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Get user's channel information
            channels_response = youtube.channels().list(
                part='snippet,statistics,contentDetails',
                mine=True
            ).execute()
            
            if channels_response['items']:
                channel = channels_response['items'][0]
                channel_id = channel['id']
                channel_title = channel['snippet']['title']
                
                # Get statistics
                stats = channel['statistics']
                subscriber_count = int(stats.get('subscriberCount', 0))
                video_count = int(stats.get('videoCount', 0))
                view_count = int(stats.get('viewCount', 0))
                
                # Calculate average views per video
                avg_view_count = view_count // video_count if video_count > 0 else 0
                
                # Update channel info in database
                from ai_services import update_user_context
                
                channel_info = {
                    "name": channel_title,  # Real channel name
                    "channel_id": channel_id,  # YouTube channel ID
                    "niche": "Unknown",  # Keep existing or set default
                    "content_type": "Unknown",
                    "subscriber_count": subscriber_count,
                    "avg_view_count": avg_view_count,
                    "total_view_count": view_count,
                    "video_count": video_count,
                    "ctr": 0.0,
                    "retention": 0.0,
                    "upload_frequency": "Unknown",
                    "video_length": "Unknown",
                    "monetization_status": "Unknown",
                    "primary_goal": "Unknown",
                    "notes": f"Auto-fetched via OAuth on {datetime.now().strftime('%Y-%m-%d')}"
                }
                
                # Store the real channel information
                update_user_context(token.user_id, "channel_info", channel_info)
                
                logger.info(f"✅ Fetched and stored real channel info for {token.user_id}: {channel_title} (ID: {channel_id})")
                
            else:
                logger.warning(f"No channel found for user {token.user_id}")
                
        except Exception as e:
            logger.error(f"Failed to fetch channel info for user {token.user_id}: {e}")
            # Don't raise - OAuth should still succeed even if channel fetch fails
    
    async def get_token(self, user_id: str) -> Optional[OAuthToken]:
        """Get OAuth token for user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT user_id, access_token, refresh_token, token_type, expires_at, scope, created_at, updated_at
                    FROM oauth_tokens WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if not row:
                    return None
                
                token_data = {
                    'user_id': row[0],
                    'access_token': row[1],
                    'refresh_token': row[2],
                    'token_type': row[3],
                    'expires_at': row[4],
                    'scope': row[5],
                    'created_at': row[6],
                    'updated_at': row[7]
                }
                
                return OAuthToken.from_dict(token_data)
                
        except Exception as e:
            logger.error(f"Failed to get OAuth token for user {user_id}: {e}")
            return None
    
    async def refresh_token(self, user_id: str) -> Optional[OAuthToken]:
        """Refresh OAuth token for user"""
        try:
            token = await self.get_token(user_id)
            if not token:
                logger.error(f"No token found for user {user_id}")
                return None
            
            # Create credentials object
            credentials = Credentials(
                token=token.access_token,
                refresh_token=token.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=token.scope.split()
            )
            
            # Refresh the token
            credentials.refresh(Request())
            
            # Update token data
            token.access_token = credentials.token
            if credentials.refresh_token:
                token.refresh_token = credentials.refresh_token
            # Convert expiry to naive datetime if it has timezone info
            if credentials.expiry.tzinfo is not None:
                token.expires_at = credentials.expiry.replace(tzinfo=None)
            else:
                token.expires_at = credentials.expiry
            token.updated_at = datetime.now()
            
            # Store updated token
            await self._store_token(token)
            
            logger.info(f"Refreshed OAuth token for user {user_id}")
            return token
            
        except Exception as e:
            logger.error(f"Failed to refresh OAuth token for user {user_id}: {e}")
            return None
    
    async def get_valid_token(self, user_id: str) -> Optional[OAuthToken]:
        """Get valid token, refreshing if necessary"""
        try:
            token = await self.get_token(user_id)
            if not token:
                return None
            
            # Check if token needs refresh
            if token.is_expired():
                logger.info(f"Token expired for user {user_id}, refreshing...")
                token = await self.refresh_token(user_id)
            
            return token
            
        except Exception as e:
            logger.error(f"Failed to get valid token for user {user_id}: {e}")
            return None
    
    async def revoke_token(self, user_id: str) -> bool:
        """Revoke OAuth token for user"""
        try:
            token = await self.get_token(user_id)
            if not token:
                return False
            
            # Revoke token with Google
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://oauth2.googleapis.com/revoke",
                    data={"token": token.access_token}
                )
                
                if response.status_code != 200:
                    logger.warning(f"Failed to revoke token with Google: {response.status_code}")
            
            # Remove from database
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM oauth_tokens WHERE user_id = ?", (user_id,))
                conn.commit()
            
            logger.info(f"Revoked OAuth token for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to revoke OAuth token for user {user_id}: {e}")
            return False
    
    async def get_youtube_service(self, user_id: str, service_name: str = "youtube", version: str = "v3"):
        """Get authenticated YouTube service client"""
        try:
            token = await self.get_valid_token(user_id)
            if not token:
                logger.error(f"No valid token for user {user_id}")
                return None
            
            # Create credentials
            credentials = Credentials(
                token=token.access_token,
                refresh_token=token.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=token.scope.split()
            )
            
            # Build service
            service = build(service_name, version, credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Failed to create YouTube service for user {user_id}: {e}")
            return None
    
    def get_oauth_status(self, user_id: str) -> Dict[str, Any]:
        """Get OAuth status for user"""
        try:
            # This would typically be async, but keeping it sync for status checks
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT expires_at, scope FROM oauth_tokens WHERE user_id = ?
                """, (user_id,))
                
                row = cursor.fetchone()
                if not row:
                    return {
                        "authenticated": False,
                        "message": "No OAuth token found"
                    }
                
                expires_at = datetime.fromisoformat(row[0])
                scope = row[1]
                
                return {
                    "authenticated": True,
                    "expires_at": expires_at.isoformat(),
                    "expires_in_seconds": (expires_at - datetime.now()).total_seconds(),
                    "scopes": scope.split(),
                    "needs_refresh": expires_at <= datetime.now()
                }
                
        except Exception as e:
            logger.error(f"Failed to get OAuth status for user {user_id}: {e}")
            return {
                "authenticated": False,
                "error": str(e)
            }

# Global OAuth manager instance
_oauth_manager: Optional[OAuthManager] = None

def get_oauth_manager() -> OAuthManager:
    """Get or create global OAuth manager instance"""
    global _oauth_manager
    if _oauth_manager is None:
        _oauth_manager = OAuthManager()
    return _oauth_manager