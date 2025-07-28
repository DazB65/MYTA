"""
Distributed Cache System for CreatorMate
Redis-based caching with fallback to in-memory storage
"""

import json
import hashlib
import time
from typing import Any, Optional, Dict, Union, List
from datetime import datetime, timedelta
import asyncio
import pickle
import logging
from dataclasses import dataclass, asdict

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from exceptions import CacheError, CacheConnectionError
from circuit_breaker import circuit_breaker, CircuitBreakerConfig
from logging_config import get_logger, LogCategory


logger = get_logger(__name__, LogCategory.CACHE)


@dataclass
class CacheStats:
    """Cache statistics"""
    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    errors: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "hit_rate": self.hit_rate
        }


class CacheKeyBuilder:
    """Builds consistent cache keys"""
    
    @staticmethod
    def build_key(
        prefix: str,
        user_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """Build cache key with consistent format"""
        parts = [prefix]
        
        if user_id:
            parts.append(f"user:{user_id}")
        
        # Add sorted kwargs for consistency
        for key, value in sorted(kwargs.items()):
            if value is not None:
                parts.append(f"{key}:{value}")
        
        key = ":".join(parts)
        
        # Hash long keys to avoid Redis key length limits
        if len(key) > 250:
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            return f"{prefix}:hash:{key_hash[:16]}"
        
        return key
    
    @staticmethod
    def build_agent_key(
        agent_type: str,
        user_id: str,
        query_hash: str,
        context_hash: Optional[str] = None
    ) -> str:
        """Build cache key for agent responses"""
        return CacheKeyBuilder.build_key(
            "agent",
            user_id=user_id,
            type=agent_type,
            query=query_hash[:16],
            context=context_hash[:8] if context_hash else None
        )
    
    @staticmethod
    def build_api_key(
        service: str,
        endpoint: str,
        params_hash: str,
        user_id: Optional[str] = None
    ) -> str:
        """Build cache key for API responses"""
        return CacheKeyBuilder.build_key(
            "api",
            user_id=user_id,
            service=service,
            endpoint=endpoint,
            params=params_hash[:16]
        )


class InMemoryCache:
    """Fallback in-memory cache"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.stats = CacheStats()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if entry["expires_at"] > time.time():
                self.stats.hits += 1
                return entry["value"]
            else:
                # Expired entry
                del self.cache[key]
        
        self.stats.misses += 1
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """Set value in cache"""
        try:
            # Evict if at max size
            if len(self.cache) >= self.max_size:
                await self._evict_oldest()
            
            self.cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl,
                "created_at": time.time()
            }
            self.stats.sets += 1
            return True
        except Exception as e:
            logger.warning(f"In-memory cache set error: {e}")
            self.stats.errors += 1
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            self.stats.deletes += 1
            return True
        return False
    
    async def clear(self) -> bool:
        """Clear all cache entries"""
        self.cache.clear()
        return True
    
    async def _evict_oldest(self):
        """Evict oldest cache entry"""
        if not self.cache:
            return
        
        oldest_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k]["created_at"]
        )
        del self.cache[oldest_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "type": "in_memory",
            "size": len(self.cache),
            "max_size": self.max_size,
            **self.stats.to_dict()
        }


class RedisCache:
    """Redis-based distributed cache"""
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        max_connections: int = 10,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5
    ):
        self.redis_url = redis_url
        self.max_connections = max_connections
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self.pool: Optional[redis.ConnectionPool] = None
        self.redis_client: Optional[redis.Redis] = None
        self.stats = CacheStats()
        self._connected = False
    
    async def connect(self) -> bool:
        """Connect to Redis"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis package not available, using in-memory cache")
            return False
        
        try:
            self.pool = redis.ConnectionPool.from_url(
                self.redis_url,
                max_connections=self.max_connections,
                socket_timeout=self.socket_timeout,
                socket_connect_timeout=self.socket_connect_timeout,
                retry_on_timeout=True,
                decode_responses=False  # We'll handle encoding ourselves
            )
            
            self.redis_client = redis.Redis(connection_pool=self.pool)
            
            # Test connection
            await self.redis_client.ping()
            self._connected = True
            
            logger.info("Connected to Redis cache")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self._connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
        if self.pool:
            await self.pool.disconnect()
        self._connected = False
    
    @circuit_breaker(
        "redis",
        config=CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=15,
            success_threshold=3,
            timeout=5
        )
    )
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        if not self._connected:
            raise CacheConnectionError("Redis not connected")
        
        try:
            data = await self.redis_client.get(key)
            if data is not None:
                self.stats.hits += 1
                return pickle.loads(data)
            
            self.stats.misses += 1
            return None
            
        except Exception as e:
            self.stats.errors += 1
            raise CacheError(f"Redis get error: {e}", "get")
    
    @circuit_breaker("redis")
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """Set value in Redis cache"""
        if not self._connected:
            raise CacheConnectionError("Redis not connected")
        
        try:
            serialized_value = pickle.dumps(value)
            await self.redis_client.setex(key, ttl, serialized_value)
            self.stats.sets += 1
            return True
            
        except Exception as e:
            self.stats.errors += 1
            raise CacheError(f"Redis set error: {e}", "set")
    
    @circuit_breaker("redis")
    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache"""
        if not self._connected:
            raise CacheConnectionError("Redis not connected")
        
        try:
            result = await self.redis_client.delete(key)
            if result > 0:
                self.stats.deletes += 1
                return True
            return False
            
        except Exception as e:
            self.stats.errors += 1
            raise CacheError(f"Redis delete error: {e}", "delete")
    
    @circuit_breaker("redis")
    async def clear(self) -> bool:
        """Clear all cache entries (use with caution)"""
        if not self._connected:
            raise CacheConnectionError("Redis not connected")
        
        try:
            await self.redis_client.flushdb()
            return True
            
        except Exception as e:
            self.stats.errors += 1
            raise CacheError(f"Redis clear error: {e}", "clear")
    
    async def get_info(self) -> Dict[str, Any]:
        """Get Redis server info"""
        if not self._connected:
            return {"status": "disconnected"}
        
        try:
            info = await self.redis_client.info()
            return {
                "status": "connected",
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed")
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "type": "redis",
            "connected": self._connected,
            **self.stats.to_dict()
        }


class DistributedCache:
    """Distributed cache with Redis primary and in-memory fallback"""
    
    def __init__(
        self,
        redis_url: Optional[str] = None,
        enable_fallback: bool = True,
        fallback_max_size: int = 1000
    ):
        self.redis_cache = RedisCache(redis_url) if redis_url else None
        self.fallback_cache = InMemoryCache(fallback_max_size) if enable_fallback else None
        self.use_redis = False
        
        # Cache TTL defaults by category
        self.default_ttls = {
            "agent_response": 1800,      # 30 minutes
            "user_context": 3600,        # 1 hour
            "youtube_api": 900,          # 15 minutes
            "channel_data": 1800,        # 30 minutes
            "analytics": 600,            # 10 minutes
            "general": 3600              # 1 hour
        }
    
    async def initialize(self) -> bool:
        """Initialize cache system"""
        if self.redis_cache:
            self.use_redis = await self.redis_cache.connect()
            if self.use_redis:
                logger.info("Using Redis distributed cache")
                return True
        
        if self.fallback_cache:
            logger.info("Using in-memory fallback cache")
            return True
        
        logger.error("No cache system available")
        return False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.use_redis and self.redis_cache:
                return await self.redis_cache.get(key)
        except CacheError as e:
            logger.warning(f"Redis cache error, trying fallback: {e}")
        
        if self.fallback_cache:
            return await self.fallback_cache.get(key)
        
        return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        category: str = "general"
    ) -> bool:
        """Set value in cache"""
        if ttl is None:
            ttl = self.default_ttls.get(category, self.default_ttls["general"])
        
        success = False
        
        # Try Redis first
        if self.use_redis and self.redis_cache:
            try:
                success = await self.redis_cache.set(key, value, ttl)
            except CacheError as e:
                logger.warning(f"Redis cache error: {e}")
        
        # Always try fallback if available (for redundancy)
        if self.fallback_cache:
            fallback_success = await self.fallback_cache.set(key, value, ttl)
            success = success or fallback_success
        
        return success
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        success = False
        
        if self.use_redis and self.redis_cache:
            try:
                success = await self.redis_cache.delete(key)
            except CacheError as e:
                logger.warning(f"Redis cache error: {e}")
        
        if self.fallback_cache:
            fallback_success = await self.fallback_cache.delete(key)
            success = success or fallback_success
        
        return success
    
    async def clear(self, pattern: Optional[str] = None) -> bool:
        """Clear cache entries"""
        success = False
        
        if self.use_redis and self.redis_cache:
            try:
                success = await self.redis_cache.clear()
            except CacheError as e:
                logger.warning(f"Redis cache error: {e}")
        
        if self.fallback_cache:
            fallback_success = await self.fallback_cache.clear()
            success = success or fallback_success
        
        return success
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        stats = {
            "active_cache": "redis" if self.use_redis else "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if self.use_redis and self.redis_cache:
            stats["redis"] = self.redis_cache.get_stats()
            stats["redis"]["info"] = await self.redis_cache.get_info()
        
        if self.fallback_cache:
            stats["fallback"] = self.fallback_cache.get_stats()
        
        return stats
    
    async def cleanup(self):
        """Cleanup cache connections"""
        if self.redis_cache:
            await self.redis_cache.disconnect()


# Global cache instance
_distributed_cache: Optional[DistributedCache] = None


async def get_distributed_cache() -> DistributedCache:
    """Get global distributed cache instance"""
    global _distributed_cache
    
    if _distributed_cache is None:
        # Initialize with configuration from environment
        import os
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        _distributed_cache = DistributedCache(redis_url=redis_url)
        await _distributed_cache.initialize()
    
    return _distributed_cache


async def cache_get(key: str) -> Optional[Any]:
    """Convenience function to get from cache"""
    cache = await get_distributed_cache()
    return await cache.get(key)


async def cache_set(
    key: str,
    value: Any,
    ttl: Optional[int] = None,
    category: str = "general"
) -> bool:
    """Convenience function to set in cache"""
    cache = await get_distributed_cache()
    return await cache.set(key, value, ttl, category)


async def cache_delete(key: str) -> bool:
    """Convenience function to delete from cache"""
    cache = await get_distributed_cache()
    return await cache.delete(key)


async def cache_clear() -> bool:
    """Convenience function to clear cache"""
    cache = await get_distributed_cache()
    return await cache.clear()