"""
Caching system for Vidalytics Boss Agent
Implements intelligent caching with TTL and context-aware invalidation
"""

import json
import time
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AgentCache:
    """Intelligent cache for agent responses with context-aware TTL"""
    
    def __init__(self):
        self.cache = {}
        self.access_times = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "invalidations": 0,
            "size": 0
        }
        
        # TTL settings (in seconds)
        self.ttl_settings = {
            "content_analysis": 1800,     # 30 minutes - content changes frequently
            "audience": 3600,             # 1 hour - audience data is more stable
            "seo": 7200,                  # 2 hours - SEO data changes slowly
            "competition": 10800,         # 3 hours - competitor data is relatively stable
            "monetization": 7200,         # 2 hours - monetization opportunities change moderately
            "general": 3600,              # 1 hour - general queries
            "default": 3600               # 1 hour default
        }
    
    def _generate_cache_key(self, message: str, user_context: Dict, intent: str = None) -> str:
        """Generate a unique cache key based on message content and context"""
        
        # Extract relevant context for cache key
        cache_context = {
            "channel_id": user_context.get("channel_info", {}).get("name", "unknown"),
            "niche": user_context.get("channel_info", {}).get("niche", "unknown"),
            "subscriber_count": user_context.get("channel_info", {}).get("subscriber_count", 0),
            "intent": intent or "unknown"
        }
        
        # Normalize message for caching (remove timestamps, specific numbers that might change)
        normalized_message = self._normalize_message(message)
        
        # Create cache key
        cache_data = {
            "message": normalized_message,
            "context": cache_context
        }
        
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    def _normalize_message(self, message: str) -> str:
        """Normalize message for caching by removing time-specific elements"""
        
        # Convert to lowercase
        normalized = message.lower().strip()
        
        # Remove common time-specific words that shouldn't affect caching
        time_words = ["today", "yesterday", "now", "currently", "recent", "latest"]
        for word in time_words:
            normalized = normalized.replace(word, "")
        
        # Remove extra whitespace
        normalized = " ".join(normalized.split())
        
        return normalized
    
    def get(self, message: str, user_context: Dict, intent: str = None) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if valid"""
        
        cache_key = self._generate_cache_key(message, user_context, intent)
        
        if cache_key not in self.cache:
            self.cache_stats["misses"] += 1
            return None
        
        cached_item = self.cache[cache_key]
        cached_time = cached_item["timestamp"]
        ttl = self.ttl_settings.get(intent, self.ttl_settings["default"])
        
        # Check if cache is still valid
        if time.time() - cached_time > ttl:
            # Cache expired, remove it
            del self.cache[cache_key]
            if cache_key in self.access_times:
                del self.access_times[cache_key]
            self.cache_stats["invalidations"] += 1
            self.cache_stats["misses"] += 1
            return None
        
        # Update access time
        self.access_times[cache_key] = time.time()
        self.cache_stats["hits"] += 1
        
        logger.info(f"Cache hit for intent: {intent}, key: {cache_key[:8]}...")
        return cached_item["data"]
    
    def set(self, message: str, user_context: Dict, response_data: Dict[str, Any], intent: str = None):
        """Cache a response with appropriate TTL"""
        
        cache_key = self._generate_cache_key(message, user_context, intent)
        
        self.cache[cache_key] = {
            "data": response_data,
            "timestamp": time.time(),
            "intent": intent,
            "access_count": 1
        }
        
        self.access_times[cache_key] = time.time()
        self.cache_stats["size"] = len(self.cache)
        
        logger.info(f"Cached response for intent: {intent}, key: {cache_key[:8]}...")
        
        # Clean up old entries if cache gets too large
        self._cleanup_cache()
    
    def _cleanup_cache(self, max_size: int = 1000):
        """Clean up old cache entries when cache gets too large"""
        
        if len(self.cache) <= max_size:
            return
        
        # Remove oldest accessed items
        sorted_keys = sorted(self.access_times.keys(), key=lambda k: self.access_times[k])
        keys_to_remove = sorted_keys[:len(self.cache) - max_size + 100]  # Remove extra for buffer
        
        for key in keys_to_remove:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
        
        self.cache_stats["size"] = len(self.cache)
        logger.info(f"Cache cleanup: removed {len(keys_to_remove)} entries")
    
    def invalidate_user_cache(self, user_id: str):
        """Invalidate all cache entries for a specific user"""
        
        keys_to_remove = []
        for key, item in self.cache.items():
            # This is a simple approach - in a more sophisticated system,
            # you'd store user_id in the cache metadata
            if user_id in str(item.get("data", {})):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
        
        self.cache_stats["invalidations"] += len(keys_to_remove)
        self.cache_stats["size"] = len(self.cache)
        
        logger.info(f"Invalidated {len(keys_to_remove)} cache entries for user: {user_id}")
    
    def invalidate_by_intent(self, intent: str):
        """Invalidate all cache entries for a specific intent"""
        
        keys_to_remove = []
        for key, item in self.cache.items():
            if item.get("intent") == intent:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
        
        self.cache_stats["invalidations"] += len(keys_to_remove)
        self.cache_stats["size"] = len(self.cache)
        
        logger.info(f"Invalidated {len(keys_to_remove)} cache entries for intent: {intent}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_size": len(self.cache),
            "hit_rate": round(hit_rate, 2),
            "total_hits": self.cache_stats["hits"],
            "total_misses": self.cache_stats["misses"],
            "total_invalidations": self.cache_stats["invalidations"],
            "total_requests": total_requests
        }
    
    def clear_expired(self):
        """Manually clear all expired cache entries"""
        
        current_time = time.time()
        keys_to_remove = []
        
        for key, item in self.cache.items():
            intent = item.get("intent", "default")
            ttl = self.ttl_settings.get(intent, self.ttl_settings["default"])
            
            if current_time - item["timestamp"] > ttl:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            if key in self.cache:
                del self.cache[key]
            if key in self.access_times:
                del self.access_times[key]
        
        self.cache_stats["invalidations"] += len(keys_to_remove)
        self.cache_stats["size"] = len(self.cache)
        
        logger.info(f"Cleared {len(keys_to_remove)} expired cache entries")
        return len(keys_to_remove)

# Global cache instance
agent_cache = AgentCache()

def get_agent_cache() -> AgentCache:
    """Get the global agent cache instance"""
    return agent_cache