"""
Analytics Caching Service
Provides Redis-based caching with fallback to in-memory storage
"""
# Optional dependency: redis
try:
    import redis  # type: ignore
    REDIS_AVAILABLE = True
except Exception:
    redis = None  # type: ignore
    REDIS_AVAILABLE = False

import json
import pickle
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

class CacheService:
    """High-performance caching service with Redis backend and memory fallback"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379", use_redis: bool = True):
        self.use_redis = use_redis
        self.memory_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "errors": 0
        }
        
        if use_redis:
            try:
                self.redis_client = redis.from_url(redis_url, decode_responses=False)
                # Test connection
                self.redis_client.ping()
                logger.info("Redis connection established successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}. Falling back to memory cache.")
                self.use_redis = False
                self.redis_client = None
        else:
            self.redis_client = None
            logger.info("Using in-memory cache only")
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate consistent cache key from parameters"""
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            kwargs_str = ':'.join(f"{k}={v}" for k, v in sorted_kwargs)
            key_data += f":{kwargs_str}"
        
        # Hash long keys to keep them manageable using SHA-256
        if len(key_data) > 200:
            key_hash = hashlib.sha256(key_data.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash}"
        
        return key_data
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for storage"""
        try:
            # Try JSON first for simple types (faster)
            json_str = json.dumps(value, default=str)
            return f"json:{json_str}".encode()
        except (TypeError, ValueError):
            # Fall back to pickle for complex objects
            pickled = pickle.dumps(value)
            return b"pickle:" + pickled
    
    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from storage"""
        try:
            data_str = data.decode()
            if data_str.startswith("json:"):
                return json.loads(data_str[5:])
            elif data.startswith(b"pickle:"):
                return pickle.loads(data[7:])
            else:
                # Legacy support
                return json.loads(data_str)
        except Exception as e:
            logger.error(f"Failed to deserialize cache data: {e}")
            return None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.use_redis and self.redis_client:
                data = self.redis_client.get(key)
                if data is not None:
                    self.cache_stats["hits"] += 1
                    return self._deserialize_value(data)
            else:
                # Memory cache
                cache_entry = self.memory_cache.get(key)
                if cache_entry and cache_entry["expires"] > datetime.now():
                    self.cache_stats["hits"] += 1
                    return cache_entry["value"]
                elif cache_entry:
                    # Expired entry
                    del self.memory_cache[key]
            
            self.cache_stats["misses"] += 1
            return None
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            self.cache_stats["errors"] += 1
            return None
    
    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Set value in cache with TTL"""
        try:
            if self.use_redis and self.redis_client:
                serialized = self._serialize_value(value)
                success = self.redis_client.setex(key, ttl_seconds, serialized)
                if success:
                    self.cache_stats["sets"] += 1
                    return True
            else:
                # Memory cache
                expires = datetime.now() + timedelta(seconds=ttl_seconds)
                self.memory_cache[key] = {
                    "value": value,
                    "expires": expires
                }
                self.cache_stats["sets"] += 1
                return True
                
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            self.cache_stats["errors"] += 1
            
        return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.use_redis and self.redis_client:
                deleted = self.redis_client.delete(key)
                if deleted:
                    self.cache_stats["deletes"] += 1
                    return True
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    self.cache_stats["deletes"] += 1
                    return True
                    
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            self.cache_stats["errors"] += 1
            
        return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        deleted = 0
        try:
            if self.use_redis and self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    deleted = self.redis_client.delete(*keys)
                    self.cache_stats["deletes"] += deleted
            else:
                # Memory cache pattern matching
                keys_to_delete = []
                for key in self.memory_cache.keys():
                    if pattern.replace("*", "") in key:
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self.memory_cache[key]
                    deleted += 1
                
                self.cache_stats["deletes"] += deleted
                
        except Exception as e:
            logger.error(f"Cache clear pattern error for {pattern}: {e}")
            self.cache_stats["errors"] += 1
            
        return deleted
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            **self.cache_stats,
            "hit_rate_percent": round(hit_rate, 2),
            "total_requests": total_requests,
            "backend": "redis" if self.use_redis else "memory"
        }
        
        if not self.use_redis:
            stats["memory_entries"] = len(self.memory_cache)
        
        return stats
    
    async def cleanup_expired(self):
        """Clean up expired entries (memory cache only)"""
        if not self.use_redis:
            now = datetime.now()
            expired_keys = [
                key for key, entry in self.memory_cache.items()
                if entry["expires"] <= now
            ]
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            return len(expired_keys)
        return 0

# Cache decorators
def cached(ttl_seconds: int = 3600, key_prefix: str = "default"):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = get_cache_service()
            
            # Generate cache key
            cache_key = cache._generate_cache_key(key_prefix, func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                await cache.set(cache_key, result, ttl_seconds)
            
            return result
        return wrapper
    return decorator

# Analytics-specific cache configurations
ANALYTICS_CACHE_CONFIGS = {
    "channel_health": {"ttl": 300, "prefix": "analytics:health"},      # 5 minutes
    "revenue": {"ttl": 900, "prefix": "analytics:revenue"},            # 15 minutes
    "subscribers": {"ttl": 600, "prefix": "analytics:subscribers"},    # 10 minutes
    "content_performance": {"ttl": 1800, "prefix": "analytics:content"}, # 30 minutes
    "overview": {"ttl": 300, "prefix": "analytics:overview"},          # 5 minutes
    "charts_data": {"ttl": 600, "prefix": "charts:data"},             # 10 minutes
}

def analytics_cached(analytics_type: str):
    """Specialized decorator for analytics data caching"""
    config = ANALYTICS_CACHE_CONFIGS.get(analytics_type, {"ttl": 3600, "prefix": "analytics"})
    return cached(ttl_seconds=config["ttl"], key_prefix=config["prefix"])

# Global cache instance
_cache_service: Optional[CacheService] = None

def get_cache_service() -> CacheService:
    """Get global cache service instance"""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service

def init_cache_service(redis_url: str = "redis://localhost:6379", use_redis: bool = True) -> CacheService:
    """Initialize global cache service"""
    global _cache_service
    _cache_service = CacheService(redis_url, use_redis)
    return _cache_service

# Background cache maintenance
async def cache_maintenance_task():
    """Background task for cache maintenance"""
    cache = get_cache_service()
    
    while True:
        try:
            # Clean up expired entries
            cleaned = await cache.cleanup_expired()
            if cleaned > 0:
                logger.info(f"Cleaned up {cleaned} expired cache entries")
            
            # Log cache statistics
            stats = cache.get_stats()
            logger.info(f"Cache stats: {stats}")
            
            # Wait 5 minutes before next cleanup
            await asyncio.sleep(300)
            
        except Exception as e:
            logger.error(f"Cache maintenance error: {e}")
            await asyncio.sleep(60)  # Wait 1 minute on error