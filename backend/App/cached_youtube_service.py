"""
Cached YouTube API Service
Provides caching layer for YouTube API calls to reduce quota usage and improve performance
"""

import json
import hashlib
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from .enhanced_caching_service import (
    get_cache_service, cache_youtube_data, get_cached_youtube_data,
    CacheType, cached
)

logger = logging.getLogger(__name__)

class CachedYouTubeService:
    """YouTube API service with intelligent caching"""
    
    def __init__(self, youtube_service):
        """Initialize with existing YouTube service"""
        self.youtube_service = youtube_service
        self.cache = get_cache_service()
        
        # Cache TTL settings (in seconds)
        self.cache_ttls = {
            'channel_info': 3600,      # 1 hour
            'video_details': 1800,     # 30 minutes
            'video_statistics': 900,   # 15 minutes
            'search_results': 1800,    # 30 minutes
            'playlist_items': 3600,    # 1 hour
            'comments': 7200,          # 2 hours
            'analytics': 3600,         # 1 hour
        }
    
    def _generate_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate cache key for YouTube API request"""
        # Remove sensitive data and normalize parameters
        clean_params = {k: v for k, v in params.items() if k not in ['key', 'access_token']}
        params_str = json.dumps(clean_params, sort_keys=True)
        params_hash = hashlib.md5(params_str.encode()).hexdigest()
        return f"youtube:{endpoint}:{params_hash}"
    
    def _get_cache_ttl(self, endpoint: str) -> int:
        """Get appropriate cache TTL for endpoint"""
        for key, ttl in self.cache_ttls.items():
            if key in endpoint.lower():
                return ttl
        return 1800  # Default 30 minutes
    
    async def get_channel_info(self, channel_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get channel information with caching"""
        params = {'id': channel_id, **kwargs}
        cache_key = self._generate_cache_key('channels', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel info: {channel_id}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.get_channel_info(channel_id, **kwargs)
            if data:
                # Cache the result
                ttl = self._get_cache_ttl('channel_info')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached channel info for {channel_id} (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch channel info for {channel_id}: {e}")
            return None
    
    async def get_video_details(self, video_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get video details with caching"""
        params = {'id': video_id, **kwargs}
        cache_key = self._generate_cache_key('videos', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for video details: {video_id}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.get_video_details(video_id, **kwargs)
            if data:
                # Cache the result
                ttl = self._get_cache_ttl('video_details')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached video details for {video_id} (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch video details for {video_id}: {e}")
            return None
    
    async def get_video_statistics(self, video_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get video statistics with shorter cache TTL (more frequently updated)"""
        params = {'id': video_id, **kwargs}
        cache_key = self._generate_cache_key('video_statistics', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for video statistics: {video_id}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.get_video_statistics(video_id, **kwargs)
            if data:
                # Cache with shorter TTL for statistics
                ttl = self._get_cache_ttl('video_statistics')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached video statistics for {video_id} (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch video statistics for {video_id}: {e}")
            return None
    
    async def search_videos(self, query: str, max_results: int = 25, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """Search videos with caching"""
        params = {'q': query, 'maxResults': max_results, **kwargs}
        cache_key = self._generate_cache_key('search', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for search: {query}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.search_videos(query, max_results, **kwargs)
            if data:
                # Cache the result
                ttl = self._get_cache_ttl('search_results')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached search results for '{query}' (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to search videos for '{query}': {e}")
            return None
    
    async def get_channel_videos(self, channel_id: str, max_results: int = 50, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """Get channel videos with caching"""
        params = {'channelId': channel_id, 'maxResults': max_results, **kwargs}
        cache_key = self._generate_cache_key('channel_videos', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel videos: {channel_id}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.get_channel_videos(channel_id, max_results, **kwargs)
            if data:
                # Cache the result
                ttl = self._get_cache_ttl('playlist_items')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached channel videos for {channel_id} (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch channel videos for {channel_id}: {e}")
            return None
    
    async def get_video_comments(self, video_id: str, max_results: int = 100, **kwargs) -> Optional[List[Dict[str, Any]]]:
        """Get video comments with caching"""
        params = {'videoId': video_id, 'maxResults': max_results, **kwargs}
        cache_key = self._generate_cache_key('comments', params)
        
        # Try cache first
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for video comments: {video_id}")
            return cached_data
        
        # Fetch from API
        try:
            data = await self.youtube_service.get_video_comments(video_id, max_results, **kwargs)
            if data:
                # Cache the result
                ttl = self._get_cache_ttl('comments')
                self.cache.set(cache_key, data, ttl)
                logger.info(f"Cached video comments for {video_id} (TTL: {ttl}s)")
            return data
        except Exception as e:
            logger.error(f"Failed to fetch video comments for {video_id}: {e}")
            return None
    
    def invalidate_video_cache(self, video_id: str):
        """Invalidate all cache entries for a specific video"""
        patterns = [
            f"youtube:videos:*{video_id}*",
            f"youtube:video_statistics:*{video_id}*",
            f"youtube:comments:*{video_id}*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = self.cache.delete_pattern(pattern)
            total_deleted += deleted
            
        logger.info(f"Invalidated {total_deleted} cache entries for video {video_id}")
        return total_deleted
    
    def invalidate_channel_cache(self, channel_id: str):
        """Invalidate all cache entries for a specific channel"""
        patterns = [
            f"youtube:channels:*{channel_id}*",
            f"youtube:channel_videos:*{channel_id}*",
            f"youtube:playlist_items:*{channel_id}*"
        ]
        
        total_deleted = 0
        for pattern in patterns:
            deleted = self.cache.delete_pattern(pattern)
            total_deleted += deleted
            
        logger.info(f"Invalidated {total_deleted} cache entries for channel {channel_id}")
        return total_deleted
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()
    
    def warm_cache_for_channel(self, channel_id: str):
        """Pre-warm cache with essential channel data"""
        logger.info(f"Warming cache for channel {channel_id}")
        
        # This could be run as a background task
        # to pre-fetch commonly needed data
        pass

# Decorator for caching YouTube API calls
def cache_youtube_api(endpoint: str, ttl: int = 1800):
    """Decorator for caching YouTube API calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            params = {'args': str(args), 'kwargs': str(sorted(kwargs.items()))}
            cache_key = f"youtube:{endpoint}:{hashlib.md5(str(params).encode()).hexdigest()}"
            
            cache = get_cache_service()
            
            # Try cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {endpoint}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            if result is not None:
                cache.set(cache_key, result, ttl)
                logger.info(f"Cached result for {endpoint} (TTL: {ttl}s)")
            
            return result
        return wrapper
    return decorator

# Global cached YouTube service instance
_cached_youtube_service: Optional[CachedYouTubeService] = None

def get_cached_youtube_service(youtube_service=None) -> CachedYouTubeService:
    """Get or create global cached YouTube service"""
    global _cached_youtube_service
    if _cached_youtube_service is None and youtube_service:
        _cached_youtube_service = CachedYouTubeService(youtube_service)
    return _cached_youtube_service
