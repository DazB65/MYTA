"""
Enhanced Caching Service for MYTA
Provides intelligent caching for AI responses, YouTube API data, and user sessions
"""

import json
import hashlib
import time
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import redis
    from redis.exceptions import RedisError, ConnectionError as RedisConnectionError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)

class CacheType(Enum):
    """Types of cached data"""
    AI_RESPONSE = "ai_response"
    YOUTUBE_API = "youtube_api"
    USER_SESSION = "user_session"
    ANALYTICS = "analytics"
    CHANNEL_INFO = "channel_info"
    CONTENT_INSIGHTS = "content_insights"

@dataclass
class CacheConfig:
    """Configuration for caching service"""
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    default_ttl: int = 3600  # 1 hour
    max_retries: int = 3
    retry_delay: float = 0.1
    key_prefix: str = "myta"
    
@dataclass
class CacheStats:
    """Cache performance statistics"""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    errors: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

class CacheKey:
    """Utility class for generating cache keys"""
    
    @staticmethod
    def generate(cache_type: CacheType, identifier: str, **kwargs) -> str:
        """Generate a cache key with optional parameters"""
        # Create a hash of the kwargs for consistent key generation
        if kwargs:
            params_str = json.dumps(kwargs, sort_keys=True)
            params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
            return f"myta:{cache_type.value}:{identifier}:{params_hash}"
        return f"myta:{cache_type.value}:{identifier}"
    
    @staticmethod
    def ai_response(user_id: str, query_hash: str, model: str = "default") -> str:
        """Generate cache key for AI responses"""
        return CacheKey.generate(CacheType.AI_RESPONSE, user_id, query=query_hash, model=model)
    
    @staticmethod
    def youtube_api(endpoint: str, params_hash: str) -> str:
        """Generate cache key for YouTube API responses"""
        return CacheKey.generate(CacheType.YOUTUBE_API, endpoint, params=params_hash)
    
    @staticmethod
    def user_session(user_id: str) -> str:
        """Generate cache key for user sessions"""
        return CacheKey.generate(CacheType.USER_SESSION, user_id)
    
    @staticmethod
    def analytics(user_id: str, time_period: str) -> str:
        """Generate cache key for analytics data"""
        return CacheKey.generate(CacheType.ANALYTICS, user_id, period=time_period)
    
    @staticmethod
    def channel_info(user_id: str) -> str:
        """Generate cache key for channel information"""
        return CacheKey.generate(CacheType.CHANNEL_INFO, user_id)

class EnhancedCachingService:
    """Enhanced caching service with Redis backend"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self.stats = CacheStats()
        self.client: Optional[redis.Redis] = None
        self._connected = False
        
    def connect(self) -> bool:
        """Connect to Redis server"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available, caching disabled")
            return False
            
        try:
            self.client = redis.Redis(
                host=self.config.redis_host,
                port=self.config.redis_port,
                db=self.config.redis_db,
                password=self.config.redis_password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            self.client.ping()
            self._connected = True
            logger.info(f"Connected to Redis at {self.config.redis_host}:{self.config.redis_port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._connected = False
            return False
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self._connected or not self.client:
            return False
            
        try:
            self.client.ping()
            return True
        except:
            self._connected = False
            return False
    
    def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute Redis operation with retry logic"""
        if not self.is_connected():
            if not self.connect():
                return None
                
        for attempt in range(self.config.max_retries):
            try:
                return operation(*args, **kwargs)
            except RedisConnectionError:
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                    self.connect()  # Try to reconnect
                else:
                    self.stats.errors += 1
                    logger.error(f"Redis operation failed after {self.config.max_retries} attempts")
                    return None
            except Exception as e:
                self.stats.errors += 1
                logger.error(f"Redis operation error: {e}")
                return None
        
        return None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            result = self._execute_with_retry(self.client.get, key)
            if result is not None:
                self.stats.hits += 1
                return json.loads(result)
            else:
                self.stats.misses += 1
                return None
        except json.JSONDecodeError:
            logger.error(f"Failed to decode cached value for key: {key}")
            self.stats.errors += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL"""
        try:
            ttl = ttl or self.config.default_ttl
            serialized_value = json.dumps(value, default=str)
            
            result = self._execute_with_retry(
                self.client.setex, 
                key, 
                ttl, 
                serialized_value
            )
            
            if result:
                self.stats.sets += 1
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to cache value for key {key}: {e}")
            self.stats.errors += 1
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            result = self._execute_with_retry(self.client.delete, key)
            if result:
                self.stats.deletes += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")
            self.stats.errors += 1
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            keys = self._execute_with_retry(self.client.keys, pattern)
            if keys:
                deleted = self._execute_with_retry(self.client.delete, *keys)
                self.stats.deletes += deleted or 0
                return deleted or 0
            return 0
        except Exception as e:
            logger.error(f"Failed to delete keys with pattern {pattern}: {e}")
            self.stats.errors += 1
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            result = self._execute_with_retry(self.client.exists, key)
            return bool(result)
        except Exception as e:
            logger.error(f"Failed to check existence of key {key}: {e}")
            return False
    
    def get_ttl(self, key: str) -> int:
        """Get TTL for a key"""
        try:
            return self._execute_with_retry(self.client.ttl, key) or -1
        except Exception as e:
            logger.error(f"Failed to get TTL for key {key}: {e}")
            return -1
    
    def extend_ttl(self, key: str, additional_seconds: int) -> bool:
        """Extend TTL for a key"""
        try:
            current_ttl = self.get_ttl(key)
            if current_ttl > 0:
                new_ttl = current_ttl + additional_seconds
                result = self._execute_with_retry(self.client.expire, key, new_ttl)
                return bool(result)
            return False
        except Exception as e:
            logger.error(f"Failed to extend TTL for key {key}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        redis_info = {}
        if self.is_connected():
            try:
                info = self._execute_with_retry(self.client.info)
                if info:
                    redis_info = {
                        "connected_clients": info.get("connected_clients", 0),
                        "used_memory": info.get("used_memory_human", "unknown"),
                        "keyspace_hits": info.get("keyspace_hits", 0),
                        "keyspace_misses": info.get("keyspace_misses", 0),
                        "total_commands_processed": info.get("total_commands_processed", 0)
                    }
            except Exception as e:
                logger.error(f"Failed to get Redis info: {e}")
        
        return {
            "cache_stats": asdict(self.stats),
            "redis_info": redis_info,
            "connected": self.is_connected()
        }
    
    def clear_user_cache(self, user_id: str) -> int:
        """Clear all cache entries for a specific user"""
        patterns = [
            f"myta:*:{user_id}:*",
            f"myta:*:{user_id}"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = self.delete_pattern(pattern)
            total_deleted += deleted
            
        logger.info(f"Cleared {total_deleted} cache entries for user {user_id}")
        return total_deleted
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on cache service"""
        health = {
            "status": "healthy",
            "connected": False,
            "latency_ms": None,
            "error": None
        }
        
        try:
            if not self.is_connected():
                health["status"] = "disconnected"
                health["error"] = "Not connected to Redis"
                return health
            
            # Test latency
            start_time = time.time()
            self.client.ping()
            latency = (time.time() - start_time) * 1000
            
            health["connected"] = True
            health["latency_ms"] = round(latency, 2)
            
            if latency > 100:  # High latency threshold
                health["status"] = "degraded"
                
        except Exception as e:
            health["status"] = "unhealthy"
            health["error"] = str(e)
            
        return health

# Global cache service instance
_cache_service: Optional[EnhancedCachingService] = None

def get_cache_service() -> EnhancedCachingService:
    """Get or create global cache service"""
    global _cache_service
    if _cache_service is None:
        config = CacheConfig()
        _cache_service = EnhancedCachingService(config)
        _cache_service.connect()
    return _cache_service

def cache_ai_response(user_id: str, query: str, response: Dict[str, Any], 
                     model: str = "default", ttl: int = 3600) -> bool:
    """Cache AI response with automatic key generation"""
    cache = get_cache_service()
    query_hash = hashlib.md5(query.encode()).hexdigest()
    key = CacheKey.ai_response(user_id, query_hash, model)
    
    cache_data = {
        "response": response,
        "cached_at": datetime.now().isoformat(),
        "query": query,
        "model": model
    }
    
    return cache.set(key, cache_data, ttl)

def get_cached_ai_response(user_id: str, query: str, model: str = "default") -> Optional[Dict[str, Any]]:
    """Get cached AI response"""
    cache = get_cache_service()
    query_hash = hashlib.md5(query.encode()).hexdigest()
    key = CacheKey.ai_response(user_id, query_hash, model)
    
    cached_data = cache.get(key)
    if cached_data:
        return cached_data.get("response")
    return None

def cache_youtube_data(endpoint: str, params: Dict[str, Any], data: Any, ttl: int = 1800) -> bool:
    """Cache YouTube API response"""
    cache = get_cache_service()
    params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
    key = CacheKey.youtube_api(endpoint, params_hash)
    
    cache_data = {
        "data": data,
        "cached_at": datetime.now().isoformat(),
        "endpoint": endpoint,
        "params": params
    }
    
    return cache.set(key, cache_data, ttl)

def get_cached_youtube_data(endpoint: str, params: Dict[str, Any]) -> Optional[Any]:
    """Get cached YouTube API data"""
    cache = get_cache_service()
    params_hash = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
    key = CacheKey.youtube_api(endpoint, params_hash)

    cached_data = cache.get(key)
    if cached_data:
        return cached_data.get("data")
    return None

# Cache decorators for easy integration
def cached(cache_type: CacheType, ttl: int = 3600, key_func=None):
    """Decorator for caching function results"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache_service()

            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                func_name = func.__name__
                args_str = str(args) + str(sorted(kwargs.items()))
                key_hash = hashlib.md5(args_str.encode()).hexdigest()[:8]
                cache_key = f"myta:{cache_type.value}:{func_name}:{key_hash}"

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return wrapper
    return decorator

def cache_user_data(ttl: int = 3600):
    """Decorator for caching user-specific data"""
    def key_func(*args, **kwargs):
        # Assume first argument is user_id
        user_id = args[0] if args else kwargs.get('user_id', 'unknown')
        func_name = args[0].__name__ if hasattr(args[0], '__name__') else 'unknown'
        return CacheKey.generate(CacheType.USER_SESSION, user_id, func=func_name)

    return cached(CacheType.USER_SESSION, ttl, key_func)

def invalidate_user_cache(user_id: str):
    """Invalidate all cache entries for a user"""
    cache = get_cache_service()
    return cache.clear_user_cache(user_id)
