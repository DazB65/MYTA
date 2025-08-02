"""
Redis Session Manager for Vidalytics
Provides secure, scalable session management using Redis as the backend store
"""

import json
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import redis
from redis.exceptions import ConnectionError as RedisConnectionError

from backend.App.config import get_settings
from backend.App.logging_config import get_logger, LogCategory, log_performance_metrics


class SessionStatus(Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID = "invalid"


@dataclass
class SessionData:
    """Session data structure"""
    session_id: str
    user_id: str
    created_at: datetime
    last_accessed: datetime
    expires_at: datetime
    status: SessionStatus
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    permissions: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []
        if self.metadata is None:
            self.metadata = {}
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.now(timezone.utc) > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if session is valid and active"""
        return (
            self.status == SessionStatus.ACTIVE and
            not self.is_expired()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Redis storage"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        for key in ['created_at', 'last_accessed', 'expires_at']:
            if isinstance(data[key], datetime):
                data[key] = data[key].isoformat()
        # Convert enum to string
        data['status'] = data['status'].value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionData':
        """Create SessionData from dictionary"""
        # Convert ISO strings back to datetime objects
        for key in ['created_at', 'last_accessed', 'expires_at']:
            if isinstance(data[key], str):
                data[key] = datetime.fromisoformat(data[key])
        # Convert string back to enum
        data['status'] = SessionStatus(data['status'])
        return cls(**data)


class RedisSessionConfig:
    """Redis session configuration"""
    
    def __init__(self, settings=None):
        self.settings = settings or get_settings()
        
        # Session settings
        self.session_timeout = timedelta(hours=8)  # 8 hours default
        self.refresh_threshold = timedelta(hours=1)  # Refresh if < 1 hour left
        self.max_sessions_per_user = 10
        self.cleanup_interval = timedelta(hours=1)
        
        # Security settings
        self.secure_cookies = not self.settings.is_development()
        self.httponly_cookies = True
        self.samesite_policy = "strict"
        
        # Redis settings
        self.key_prefix = "Vidalytics:session:"
        self.user_sessions_prefix = "Vidalytics:user_sessions:"
        self.session_stats_key = "Vidalytics:session_stats"


class RedisSessionManager:
    """Redis-based session manager"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.settings = get_settings()
        self.config = RedisSessionConfig(self.settings)
        self.logger = get_logger(__name__, LogCategory.AUTHENTICATION)
        
        # Initialize Redis client
        if redis_client:
            self.redis = redis_client
        else:
            self.redis = self._create_redis_client()
        
        # Test Redis connection
        self._test_connection()
    
    def _create_redis_client(self) -> redis.Redis:
        """Create Redis client from configuration"""
        try:
            # Parse Redis URL if provided
            if hasattr(self.settings, 'redis_url') and self.settings.redis_url:
                redis_client = redis.from_url(
                    self.settings.redis_url,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
            else:
                # Fallback to individual settings
                redis_client = redis.Redis(
                    host=getattr(self.settings, 'redis_host', 'localhost'),
                    port=getattr(self.settings, 'redis_port', 6379),
                    db=getattr(self.settings, 'redis_db', 0),
                    password=getattr(self.settings, 'redis_password', None),
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
            
            return redis_client
            
        except Exception as e:
            self.logger.error(
                "Failed to create Redis client",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            raise
    
    def _test_connection(self) -> None:
        """Test Redis connection"""
        try:
            self.redis.ping()
            self.logger.info(
                "Redis connection established successfully",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {
                        'redis_host': self.redis.connection_pool.connection_kwargs.get('host', 'unknown'),
                        'redis_port': self.redis.connection_pool.connection_kwargs.get('port', 'unknown')
                    }
                }
            )
        except RedisConnectionError as e:
            self.logger.error(
                "Redis connection failed",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': 'RedisConnectionError',
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            raise
    
    def _generate_session_id(self) -> str:
        """Generate secure session ID"""
        # Combine random data for entropy
        random_data = secrets.token_bytes(32)
        timestamp = str(datetime.now(timezone.utc).timestamp())
        unique_data = f"{uuid.uuid4()}{timestamp}".encode('utf-8')
        
        # Create hash
        combined_data = random_data + unique_data
        session_id = hashlib.sha256(combined_data).hexdigest()
        
        return session_id
    
    def _get_session_key(self, session_id: str) -> str:
        """Get Redis key for session"""
        return f"{self.config.key_prefix}{session_id}"
    
    def _get_user_sessions_key(self, user_id: str) -> str:
        """Get Redis key for user sessions list"""
        return f"{self.config.user_sessions_prefix}{user_id}"
    
    async def create_session(
        self,
        user_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        permissions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        custom_expiry: Optional[timedelta] = None
    ) -> SessionData:
        """Create new session"""
        start_time = datetime.now()
        
        try:
            # Generate session ID
            session_id = self._generate_session_id()
            
            # Calculate expiry
            expires_at = datetime.now(timezone.utc) + (custom_expiry or self.config.session_timeout)
            
            # Create session data
            session_data = SessionData(
                session_id=session_id,
                user_id=user_id,
                created_at=datetime.now(timezone.utc),
                last_accessed=datetime.now(timezone.utc),
                expires_at=expires_at,
                status=SessionStatus.ACTIVE,
                ip_address=ip_address,
                user_agent=user_agent,
                permissions=permissions or [],
                metadata=metadata or {}
            )
            
            # Store session in Redis
            session_key = self._get_session_key(session_id)
            session_json = json.dumps(session_data.to_dict())
            
            # Calculate TTL in seconds
            ttl_seconds = int((expires_at - datetime.now(timezone.utc)).total_seconds())
            
            # Store with TTL
            self.redis.setex(session_key, ttl_seconds, session_json)
            
            # Add to user sessions list
            user_sessions_key = self._get_user_sessions_key(user_id)
            self.redis.sadd(user_sessions_key, session_id)
            self.redis.expire(user_sessions_key, ttl_seconds)
            
            # Cleanup old sessions for user
            await self._cleanup_user_sessions(user_id)
            
            # Update session statistics
            self._update_session_stats('created')
            
            # Log session creation
            self.logger.info(
                "Session created successfully",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'user_id': user_id,
                    'metadata': {
                        'session_id': session_id[:8] + '...',  # Partial ID for security
                        'expires_at': expires_at.isoformat(),
                        'ip_address': ip_address,
                        'permissions_count': len(permissions or [])
                    }
                }
            )
            
            # Log performance metrics
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_performance_metrics(
                'session_operation',
                operation='create_session',
                duration_ms=duration_ms,
                success=True,
                user_id=user_id
            )
            
            return session_data
            
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            self.logger.error(
                "Failed to create session",
                extra={
                    'category': LogCategory.ERROR.value,
                    'user_id': user_id,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e),
                        'ip_address': ip_address
                    }
                },
                exc_info=True
            )
            
            log_performance_metrics(
                'session_operation',
                operation='create_session',
                duration_ms=duration_ms,
                success=False,
                user_id=user_id
            )
            
            raise
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID"""
        start_time = datetime.now()
        
        try:
            session_key = self._get_session_key(session_id)
            session_json = self.redis.get(session_key)
            
            if not session_json:
                return None
            
            # Parse session data
            session_dict = json.loads(session_json)
            session_data = SessionData.from_dict(session_dict)
            
            # Check if session is valid
            if not session_data.is_valid():
                # Remove invalid session
                await self._remove_session(session_id, session_data.user_id)
                return None
            
            # Update last accessed time
            session_data.last_accessed = datetime.now(timezone.utc)
            
            # Check if session needs refresh
            time_until_expiry = session_data.expires_at - datetime.now(timezone.utc)
            if time_until_expiry < self.config.refresh_threshold:
                # Extend session
                session_data.expires_at = datetime.now(timezone.utc) + self.config.session_timeout
                
                # Update in Redis
                updated_json = json.dumps(session_data.to_dict())
                ttl_seconds = int((session_data.expires_at - datetime.now(timezone.utc)).total_seconds())
                self.redis.setex(session_key, ttl_seconds, updated_json)
                
                self.logger.info(
                    "Session automatically refreshed",
                    extra={
                        'category': LogCategory.AUTHENTICATION.value,
                        'user_id': session_data.user_id,
                        'metadata': {
                            'session_id': session_id[:8] + '...',
                            'new_expires_at': session_data.expires_at.isoformat()
                        }
                    }
                )
            else:
                # Just update last accessed time
                updated_json = json.dumps(session_data.to_dict())
                self.redis.set(session_key, updated_json, keepttl=True)
            
            # Log performance metrics
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            log_performance_metrics(
                'session_operation',
                operation='get_session',
                duration_ms=duration_ms,
                success=True,
                user_id=session_data.user_id
            )
            
            return session_data
            
        except Exception as e:
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            self.logger.error(
                "Failed to get session",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'session_id': session_id[:8] + '...' if session_id else 'unknown',
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            
            log_performance_metrics(
                'session_operation',
                operation='get_session',
                duration_ms=duration_ms,
                success=False
            )
            
            return None
    
    async def update_session(
        self,
        session_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        permissions: Optional[List[str]] = None
    ) -> bool:
        """Update session data"""
        try:
            session_data = await self.get_session(session_id)
            if not session_data:
                return False
            
            # Update fields
            if metadata is not None:
                session_data.metadata.update(metadata)
            
            if permissions is not None:
                session_data.permissions = permissions
            
            session_data.last_accessed = datetime.now(timezone.utc)
            
            # Save updated session
            session_key = self._get_session_key(session_id)
            session_json = json.dumps(session_data.to_dict())
            self.redis.set(session_key, session_json, keepttl=True)
            
            self.logger.info(
                "Session updated successfully",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'user_id': session_data.user_id,
                    'metadata': {
                        'session_id': session_id[:8] + '...',
                        'updated_metadata': bool(metadata),
                        'updated_permissions': bool(permissions)
                    }
                }
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to update session",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'session_id': session_id[:8] + '...' if session_id else 'unknown',
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return False
    
    async def revoke_session(self, session_id: str) -> bool:
        """Revoke a specific session"""
        try:
            session_data = await self.get_session(session_id)
            if not session_data:
                return False
            
            # Mark as revoked and remove from Redis
            await self._remove_session(session_id, session_data.user_id)
            
            self.logger.info(
                "Session revoked successfully",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'user_id': session_data.user_id,
                    'metadata': {
                        'session_id': session_id[:8] + '...',
                        'revoked_at': datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            self._update_session_stats('revoked')
            return True
            
        except Exception as e:
            self.logger.error(
                "Failed to revoke session",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'session_id': session_id[:8] + '...' if session_id else 'unknown',
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return False
    
    async def revoke_all_user_sessions(self, user_id: str, except_session_id: Optional[str] = None) -> int:
        """Revoke all sessions for a user"""
        try:
            user_sessions_key = self._get_user_sessions_key(user_id)
            session_ids = self.redis.smembers(user_sessions_key)
            
            revoked_count = 0
            for session_id in session_ids:
                if except_session_id and session_id == except_session_id:
                    continue
                
                if await self.revoke_session(session_id):
                    revoked_count += 1
            
            self.logger.info(
                f"Revoked {revoked_count} sessions for user",
                extra={
                    'category': LogCategory.AUTHENTICATION.value,
                    'user_id': user_id,
                    'metadata': {
                        'revoked_count': revoked_count,
                        'total_sessions': len(session_ids),
                        'kept_session': except_session_id[:8] + '...' if except_session_id else None
                    }
                }
            )
            
            return revoked_count
            
        except Exception as e:
            self.logger.error(
                "Failed to revoke user sessions",
                extra={
                    'category': LogCategory.ERROR.value,
                    'user_id': user_id,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return 0
    
    async def get_user_sessions(self, user_id: str) -> List[SessionData]:
        """Get all active sessions for a user"""
        try:
            user_sessions_key = self._get_user_sessions_key(user_id)
            session_ids = self.redis.smembers(user_sessions_key)
            
            sessions = []
            for session_id in session_ids:
                session_data = await self.get_session(session_id)
                if session_data:
                    sessions.append(session_data)
            
            return sessions
            
        except Exception as e:
            self.logger.error(
                "Failed to get user sessions",
                extra={
                    'category': LogCategory.ERROR.value,
                    'user_id': user_id,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return []
    
    async def _remove_session(self, session_id: str, user_id: str) -> None:
        """Remove session from Redis"""
        session_key = self._get_session_key(session_id)
        user_sessions_key = self._get_user_sessions_key(user_id)
        
        # Remove session data
        self.redis.delete(session_key)
        
        # Remove from user sessions list
        self.redis.srem(user_sessions_key, session_id)
    
    async def _cleanup_user_sessions(self, user_id: str) -> None:
        """Cleanup old sessions for a user if limit exceeded"""
        try:
            sessions = await self.get_user_sessions(user_id)
            
            if len(sessions) > self.config.max_sessions_per_user:
                # Sort by last accessed time (oldest first)
                sessions.sort(key=lambda s: s.last_accessed)
                
                # Remove oldest sessions
                sessions_to_remove = sessions[:-self.config.max_sessions_per_user]
                for session in sessions_to_remove:
                    await self._remove_session(session.session_id, user_id)
                
                self.logger.info(
                    f"Cleaned up {len(sessions_to_remove)} old sessions for user",
                    extra={
                        'category': LogCategory.AUTHENTICATION.value,
                        'user_id': user_id,
                        'metadata': {
                            'removed_count': len(sessions_to_remove),
                            'remaining_count': self.config.max_sessions_per_user
                        }
                    }
                )
                
        except Exception as e:
            self.logger.error(
                "Failed to cleanup user sessions",
                extra={
                    'category': LogCategory.ERROR.value,
                    'user_id': user_id,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
    
    def _update_session_stats(self, action: str) -> None:
        """Update session statistics"""
        try:
            stats_key = self.config.session_stats_key
            current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            
            # Increment daily counter
            self.redis.hincrby(stats_key, f"{current_date}:{action}", 1)
            
            # Set expiry for stats (keep for 30 days)
            self.redis.expire(stats_key, int(timedelta(days=30).total_seconds()))
            
        except Exception as e:
            # Don't fail the main operation if stats update fails
            self.logger.warning(
                "Failed to update session statistics",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {
                        'action': action,
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                }
            )
    
    async def get_session_stats(self) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            stats_key = self.config.session_stats_key
            stats_data = self.redis.hgetall(stats_key)
            
            # Organize stats by date and action
            organized_stats = {}
            for key, value in stats_data.items():
                date, action = key.split(':', 1)
                if date not in organized_stats:
                    organized_stats[date] = {}
                organized_stats[date][action] = int(value)
            
            return {
                'daily_stats': organized_stats,
                'total_active_sessions': len(self.redis.keys(f"{self.config.key_prefix}*")),
                'redis_info': {
                    'connected': True,
                    'memory_usage': self.redis.info('memory').get('used_memory_human', 'unknown')
                }
            }
            
        except Exception as e:
            self.logger.error(
                "Failed to get session statistics",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            return {'error': 'Failed to retrieve statistics'}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on Redis session store"""
        try:
            start_time = datetime.now()
            
            # Test basic operations
            test_key = "Vidalytics:health_check"
            test_value = str(uuid.uuid4())
            
            # Test write
            self.redis.set(test_key, test_value, ex=60)
            
            # Test read
            stored_value = self.redis.get(test_key)
            
            # Test delete
            self.redis.delete(test_key)
            
            # Calculate response time
            response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            # Get Redis info
            redis_info = self.redis.info()
            
            health_status = {
                'status': 'healthy' if stored_value == test_value else 'unhealthy',
                'response_time_ms': response_time_ms,
                'redis_version': redis_info.get('redis_version', 'unknown'),
                'connected_clients': redis_info.get('connected_clients', 0),
                'used_memory_human': redis_info.get('used_memory_human', 'unknown'),
                'total_active_sessions': len(self.redis.keys(f"{self.config.key_prefix}*")),
                'uptime_seconds': redis_info.get('uptime_in_seconds', 0)
            }
            
            return health_status
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'error_type': type(e).__name__
            }


# Global session manager instance
_session_manager: Optional[RedisSessionManager] = None


def get_session_manager() -> RedisSessionManager:
    """Get or create global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = RedisSessionManager()
    return _session_manager


async def cleanup_expired_sessions():
    """Cleanup expired sessions - can be run as a background task"""
    session_manager = get_session_manager()
    try:
        # This is handled automatically by Redis TTL, but we can add additional cleanup logic here
        stats = await session_manager.get_session_stats()
        session_manager.logger.info(
            "Session cleanup completed",
            extra={
                'category': LogCategory.SYSTEM.value,
                'metadata': {
                    'active_sessions': stats.get('total_active_sessions', 0)
                }
            }
        )
    except Exception as e:
        session_manager.logger.error(
            "Failed to cleanup expired sessions",
            extra={
                'category': LogCategory.ERROR.value,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )