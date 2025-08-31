"""
Caching Middleware for MYTA
Provides response caching and performance optimization
"""

import json
import hashlib
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from backend.App.redis_service import get_redis_service
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.CACHE)

class CacheConfig:
    """Configuration for different endpoint caching"""
    
    # Cache durations in seconds
    CACHE_DURATIONS = {
        # Analytics endpoints - cache for 5 minutes
        "/api/analytics": 300,
        "/api/analytics/overview": 300,
        "/api/analytics/performance": 300,
        
        # User settings - cache for 1 hour
        "/api/settings": 3600,
        "/api/settings/agent": 3600,
        
        # Subscription plans - cache for 1 hour
        "/api/subscription/plans": 3600,
        
        # Tasks/Goals/Notes stats - cache for 2 minutes
        "/api/tasks/stats": 120,
        "/api/goals/stats": 120,
        "/api/notes/stats": 120,
        
        # Content cards - cache for 10 minutes
        "/api/content-cards": 600,
        
        # Default cache duration
        "default": 60
    }
    
    # Endpoints that should never be cached
    NO_CACHE_ENDPOINTS = {
        "/api/chat",
        "/api/subscription/checkout",
        "/api/subscription/cancel",
        "/api/auth",
        "/api/oauth"
    }
    
    # Methods that should never be cached
    NO_CACHE_METHODS = {"POST", "PUT", "DELETE", "PATCH"}

def should_cache_request(request: Request) -> bool:
    """Determine if a request should be cached"""
    
    # Don't cache non-GET requests
    if request.method in CacheConfig.NO_CACHE_METHODS:
        return False
    
    # Don't cache specific endpoints
    path = request.url.path
    for no_cache_endpoint in CacheConfig.NO_CACHE_ENDPOINTS:
        if path.startswith(no_cache_endpoint):
            return False
    
    # Don't cache if user is not authenticated (for security)
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return False
    
    return True

def get_cache_duration(path: str) -> int:
    """Get cache duration for a specific path"""
    
    # Check for exact matches first
    if path in CacheConfig.CACHE_DURATIONS:
        return CacheConfig.CACHE_DURATIONS[path]
    
    # Check for prefix matches
    for cached_path, duration in CacheConfig.CACHE_DURATIONS.items():
        if cached_path != "default" and path.startswith(cached_path):
            return duration
    
    # Return default duration
    return CacheConfig.CACHE_DURATIONS["default"]

def generate_cache_key(request: Request, user_id: str = None) -> str:
    """Generate a unique cache key for the request"""
    
    # Include path, query parameters, and user ID
    path = request.url.path
    query_params = dict(request.query_params)
    
    # Sort query params for consistent keys
    sorted_params = json.dumps(query_params, sort_keys=True)
    
    # Create cache key components
    key_components = [path, sorted_params]
    
    if user_id:
        key_components.append(user_id)
    
    # Generate hash using SHA-256 for better security
    key_string = ":".join(key_components)
    cache_key = hashlib.sha256(key_string.encode()).hexdigest()
    
    return f"api_cache:{cache_key}"

async def get_cached_response(request: Request, user_id: str = None) -> Optional[Dict]:
    """Get cached response for a request"""
    
    if not should_cache_request(request):
        return None
    
    try:
        redis_service = get_redis_service()
        if not redis_service.is_available():
            return None
        
        cache_key = generate_cache_key(request, user_id)
        cached_data = redis_service.get(cache_key)
        
        if cached_data and isinstance(cached_data, dict):
            # Check if cache is still valid
            cached_at = cached_data.get("cached_at")
            if cached_at:
                cached_time = datetime.fromisoformat(cached_at)
                cache_duration = get_cache_duration(request.url.path)
                
                if datetime.utcnow() - cached_time < timedelta(seconds=cache_duration):
                    logger.debug(f"Cache hit for {request.url.path}")
                    return cached_data
                else:
                    # Cache expired, delete it
                    redis_service.delete(cache_key)
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting cached response: {e}")
        return None

async def cache_response(request: Request, response_data: Dict, user_id: str = None) -> bool:
    """Cache a response"""
    
    if not should_cache_request(request):
        return False
    
    try:
        redis_service = get_redis_service()
        if not redis_service.is_available():
            return False
        
        cache_key = generate_cache_key(request, user_id)
        cache_duration = get_cache_duration(request.url.path)
        
        # Prepare cache data
        cache_data = {
            "response": response_data,
            "cached_at": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "user_id": user_id
        }
        
        success = redis_service.set(cache_key, cache_data, cache_duration)
        
        if success:
            logger.debug(f"Cached response for {request.url.path} (duration: {cache_duration}s)")
        
        return success
        
    except Exception as e:
        logger.error(f"Error caching response: {e}")
        return False

def invalidate_cache_pattern(pattern: str) -> int:
    """Invalidate cache entries matching a pattern"""
    
    try:
        redis_service = get_redis_service()
        if not redis_service.is_available():
            return 0
        
        return redis_service.clear_cache(pattern)
        
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        return 0

def invalidate_user_cache(user_id: str) -> int:
    """Invalidate all cache entries for a specific user"""
    
    try:
        redis_service = get_redis_service()
        if not redis_service.is_available():
            return 0
        
        # This is a simplified approach - in production you might want
        # to maintain a separate index of user cache keys
        pattern = f"*{user_id}*"
        return redis_service.clear_cache(pattern)
        
    except Exception as e:
        logger.error(f"Error invalidating user cache: {e}")
        return 0

# Decorator for caching function results
def cache_result(duration: int = 300, key_prefix: str = "func"):
    """Decorator to cache function results"""
    
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            try:
                redis_service = get_redis_service()
                if not redis_service.is_available():
                    return await func(*args, **kwargs)
                
                # Generate cache key from function name and arguments
                func_name = func.__name__
                args_str = json.dumps([str(arg) for arg in args], sort_keys=True)
                kwargs_str = json.dumps(kwargs, sort_keys=True)
                
                cache_key = f"{key_prefix}:{func_name}:{hashlib.sha256(f'{args_str}:{kwargs_str}'.encode()).hexdigest()}"
                
                # Try to get cached result
                cached_result = redis_service.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Function cache hit: {func_name}")
                    return cached_result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                redis_service.set(cache_key, result, duration)
                
                logger.debug(f"Function result cached: {func_name}")
                return result
                
            except Exception as e:
                logger.error(f"Error in cache decorator: {e}")
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Cache warming functions
async def warm_cache_for_user(user_id: str) -> Dict[str, bool]:
    """Pre-warm cache for a user's common requests"""
    
    results = {}
    
    try:
        # This would typically make requests to common endpoints
        # to pre-populate the cache. For now, it's a placeholder.
        
        common_endpoints = [
            "/api/settings",
            "/api/tasks/stats",
            "/api/goals/stats", 
            "/api/notes/stats"
        ]
        
        for endpoint in common_endpoints:
            # In a real implementation, you would make actual requests here
            results[endpoint] = True
        
        logger.info(f"Cache warmed for user {user_id}")
        return results
        
    except Exception as e:
        logger.error(f"Error warming cache for user {user_id}: {e}")
        return results

def get_cache_stats() -> Dict[str, Any]:
    """Get cache performance statistics"""
    
    try:
        redis_service = get_redis_service()
        if not redis_service.is_available():
            return {"status": "unavailable"}
        
        health = redis_service.health_check()
        
        # Get cache-specific stats
        cache_keys = redis_service.client.keys("myta:cache:*")
        api_cache_keys = redis_service.client.keys("api_cache:*")
        
        stats = {
            "redis_status": health.get("status"),
            "total_cache_keys": len(cache_keys),
            "api_cache_keys": len(api_cache_keys),
            "connected_clients": health.get("connected_clients", 0),
            "used_memory": health.get("used_memory", "unknown"),
            "cache_hit_rate": "Not implemented", # Would need hit/miss tracking
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {"status": "error", "error": str(e)}
