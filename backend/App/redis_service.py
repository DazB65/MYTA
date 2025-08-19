"""
Redis Service for MYTA
Handles caching, session management, and background task queuing
"""

import os
import json
import redis
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import pickle
import hashlib

from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.CACHE)

class RedisService:
    """Service for handling Redis operations"""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.redis_password = os.getenv('REDIS_PASSWORD', '')
        self.redis_db = int(os.getenv('REDIS_DB', '0'))
        self.max_connections = int(os.getenv('REDIS_MAX_CONNECTIONS', '10'))
        
        try:
            # Create Redis connection pool
            self.pool = redis.ConnectionPool.from_url(
                self.redis_url,
                password=self.redis_password if self.redis_password else None,
                db=self.redis_db,
                max_connections=self.max_connections,
                decode_responses=True
            )
            
            self.client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            self.client.ping()
            logger.info("Redis client initialized successfully")
            
        except redis.ConnectionError:
            logger.warning("Redis connection failed - using fallback mode")
            self.client = None
        except Exception as e:
            logger.error(f"Redis initialization error: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Redis is available"""
        return self.client is not None
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate a standardized cache key"""
        return f"myta:{prefix}:{identifier}"
    
    # Basic Cache Operations
    def set(self, key: str, value: Any, expire_seconds: int = 3600) -> bool:
        """Set a value in cache with expiration"""
        if not self.is_available():
            return False
        
        try:
            cache_key = self._generate_key("cache", key)
            
            # Serialize complex objects
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            elif not isinstance(value, (str, int, float, bool)):
                value = pickle.dumps(value)
            
            result = self.client.setex(cache_key, expire_seconds, value)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        if not self.is_available():
            return None
        
        try:
            cache_key = self._generate_key("cache", key)
            value = self.client.get(cache_key)
            
            if value is None:
                return None
            
            # Try to deserialize JSON
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
            
            # Try to deserialize pickle
            try:
                return pickle.loads(value.encode() if isinstance(value, str) else value)
            except:
                pass
            
            # Return as string
            return value
            
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        if not self.is_available():
            return False
        
        try:
            cache_key = self._generate_key("cache", key)
            result = self.client.delete(cache_key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in cache"""
        if not self.is_available():
            return False
        
        try:
            cache_key = self._generate_key("cache", key)
            return bool(self.client.exists(cache_key))
            
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False
    
    # Session Management
    def set_session(self, session_id: str, session_data: Dict, expire_seconds: int = 86400) -> bool:
        """Store session data (24 hour default expiration)"""
        if not self.is_available():
            return False
        
        try:
            session_key = self._generate_key("session", session_id)
            session_json = json.dumps(session_data)
            result = self.client.setex(session_key, expire_seconds, session_json)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Redis set session error: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        if not self.is_available():
            return None
        
        try:
            session_key = self._generate_key("session", session_id)
            session_data = self.client.get(session_key)
            
            if session_data:
                return json.loads(session_data)
            return None
            
        except Exception as e:
            logger.error(f"Redis get session error: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session data"""
        if not self.is_available():
            return False
        
        try:
            session_key = self._generate_key("session", session_id)
            result = self.client.delete(session_key)
            return bool(result)
            
        except Exception as e:
            logger.error(f"Redis delete session error: {e}")
            return False
    
    # API Response Caching
    def cache_api_response(self, endpoint: str, params: Dict, response_data: Any, expire_seconds: int = 300) -> bool:
        """Cache API response (5 minute default)"""
        if not self.is_available():
            return False
        
        try:
            # Create cache key from endpoint and params
            params_str = json.dumps(params, sort_keys=True)
            cache_key = hashlib.md5(f"{endpoint}:{params_str}".encode()).hexdigest()
            
            cache_data = {
                "endpoint": endpoint,
                "params": params,
                "response": response_data,
                "cached_at": datetime.utcnow().isoformat()
            }
            
            return self.set(f"api_response:{cache_key}", cache_data, expire_seconds)
            
        except Exception as e:
            logger.error(f"Redis cache API response error: {e}")
            return False
    
    def get_cached_api_response(self, endpoint: str, params: Dict) -> Optional[Any]:
        """Get cached API response"""
        if not self.is_available():
            return None
        
        try:
            params_str = json.dumps(params, sort_keys=True)
            cache_key = hashlib.md5(f"{endpoint}:{params_str}".encode()).hexdigest()
            
            cached_data = self.get(f"api_response:{cache_key}")
            
            if cached_data and isinstance(cached_data, dict):
                return cached_data.get("response")
            
            return None
            
        except Exception as e:
            logger.error(f"Redis get cached API response error: {e}")
            return None
    
    # Rate Limiting
    def check_rate_limit(self, identifier: str, limit: int, window_seconds: int) -> Dict[str, Any]:
        """Check and update rate limit for an identifier"""
        if not self.is_available():
            return {"allowed": True, "remaining": limit, "reset_time": None}
        
        try:
            rate_key = self._generate_key("rate_limit", identifier)
            current_time = datetime.utcnow()
            
            # Get current count
            current_count = self.client.get(rate_key)
            current_count = int(current_count) if current_count else 0
            
            if current_count >= limit:
                # Rate limit exceeded
                ttl = self.client.ttl(rate_key)
                reset_time = current_time + timedelta(seconds=ttl) if ttl > 0 else None
                
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_time": reset_time.isoformat() if reset_time else None,
                    "current_count": current_count
                }
            
            # Increment counter
            pipe = self.client.pipeline()
            pipe.incr(rate_key)
            pipe.expire(rate_key, window_seconds)
            pipe.execute()
            
            return {
                "allowed": True,
                "remaining": limit - (current_count + 1),
                "reset_time": (current_time + timedelta(seconds=window_seconds)).isoformat(),
                "current_count": current_count + 1
            }
            
        except Exception as e:
            logger.error(f"Redis rate limit error: {e}")
            return {"allowed": True, "remaining": limit, "reset_time": None}
    
    # Background Tasks Queue
    def enqueue_task(self, task_type: str, task_data: Dict, priority: int = 0) -> bool:
        """Enqueue a background task"""
        if not self.is_available():
            return False
        
        try:
            task = {
                "id": f"task_{datetime.utcnow().timestamp()}",
                "type": task_type,
                "data": task_data,
                "priority": priority,
                "created_at": datetime.utcnow().isoformat(),
                "status": "pending"
            }
            
            queue_key = self._generate_key("task_queue", task_type)
            task_json = json.dumps(task)
            
            # Use priority queue (higher priority = lower score)
            result = self.client.zadd(queue_key, {task_json: -priority})
            return bool(result)
            
        except Exception as e:
            logger.error(f"Redis enqueue task error: {e}")
            return False
    
    def dequeue_task(self, task_type: str) -> Optional[Dict]:
        """Dequeue a background task"""
        if not self.is_available():
            return None
        
        try:
            queue_key = self._generate_key("task_queue", task_type)
            
            # Get highest priority task
            result = self.client.zpopmax(queue_key)
            
            if result:
                task_json, priority = result[0]
                return json.loads(task_json)
            
            return None
            
        except Exception as e:
            logger.error(f"Redis dequeue task error: {e}")
            return None
    
    # Health Check
    def health_check(self) -> Dict[str, Any]:
        """Get Redis health status"""
        if not self.is_available():
            return {
                "status": "unavailable",
                "error": "Redis client not initialized"
            }
        
        try:
            # Test basic operations
            test_key = "health_check_test"
            self.client.set(test_key, "test_value", ex=10)
            test_value = self.client.get(test_key)
            self.client.delete(test_key)
            
            # Get Redis info
            info = self.client.info()
            
            return {
                "status": "healthy",
                "test_passed": test_value == "test_value",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory_human", "unknown"),
                "uptime": info.get("uptime_in_seconds", 0)
            }
            
        except Exception as e:
            logger.error(f"Redis health check error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def clear_cache(self, pattern: str = None) -> int:
        """Clear cache entries matching pattern"""
        if not self.is_available():
            return 0
        
        try:
            if pattern:
                search_pattern = self._generate_key("cache", pattern)
            else:
                search_pattern = self._generate_key("cache", "*")
            
            keys = self.client.keys(search_pattern)
            
            if keys:
                deleted = self.client.delete(*keys)
                logger.info(f"Cleared {deleted} cache entries")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"Redis clear cache error: {e}")
            return 0

# Global service instance
_redis_service: Optional[RedisService] = None

def get_redis_service() -> RedisService:
    """Get or create global Redis service instance"""
    global _redis_service
    if _redis_service is None:
        _redis_service = RedisService()
    return _redis_service
