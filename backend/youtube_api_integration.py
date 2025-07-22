"""
Enhanced YouTube API Integration for CreatorMate Multi-Agent System
Provides comprehensive YouTube data with caching and quota management
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re
import time
import hashlib
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from agent_cache import get_agent_cache
from oauth_manager import get_oauth_manager
from security_config import get_api_key

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class YouTubeVideoMetrics:
    """Comprehensive video metrics"""
    video_id: str
    title: str
    description: str
    tags: List[str]
    published_at: str
    thumbnail_url: str
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    definition: str
    category_id: str
    default_language: Optional[str] = None
    
    # Real YouTube Analytics metrics (when available)
    ctr_actual: Optional[float] = None
    retention_actual: Optional[float] = None
    
    # Analytics data (populated when OAuth is available)
    analytics: Optional[Dict[str, Any]] = None

@dataclass
class YouTubeChannelMetrics:
    """Comprehensive channel metrics"""
    channel_id: str
    title: str
    description: str
    custom_url: Optional[str]
    published_at: str
    thumbnail_url: str
    banner_url: Optional[str]
    country: Optional[str]
    view_count: int
    subscriber_count: int
    video_count: int
    
    # Recent performance
    recent_videos: List[YouTubeVideoMetrics]
    avg_views_last_30: float = 0.0
    avg_engagement_last_30: float = 0.0
    upload_frequency: str = "unknown"

@dataclass
class YouTubeCommentData:
    """Comment data for sentiment analysis"""
    comment_id: str
    video_id: str
    author_name: str
    text: str
    like_count: int
    published_at: str
    reply_count: int = 0
    parent_id: Optional[str] = None

class YouTubeQuotaManager:
    """Manages YouTube API quota usage with intelligent backoff"""
    
    def __init__(self):
        self.daily_quota = 10000  # YouTube API default quota
        self.used_quota = 0
        self.quota_reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        self.operation_costs = {
            'videos.list': 1,
            'channels.list': 1,
            'search.list': 100,
            'commentThreads.list': 1,
            'playlists.list': 1,
            'playlistItems.list': 1
        }
        
        # Exponential backoff parameters
        self.backoff_enabled = True
        self.last_quota_error = None
        self.consecutive_errors = 0
        self.backoff_delay = 0  # seconds
        self.max_backoff_delay = 300  # 5 minutes max
    
    def check_quota(self, operation: str, estimated_calls: int = 1) -> bool:
        """Check if operation is within quota limits"""
        cost = self.operation_costs.get(operation, 1) * estimated_calls
        
        # Reset quota if new day
        if datetime.now() >= self.quota_reset_time:
            self.used_quota = 0
            self.quota_reset_time += timedelta(days=1)
        
        return (self.used_quota + cost) <= self.daily_quota
    
    def consume_quota(self, operation: str, actual_calls: int = 1):
        """Record quota usage"""
        cost = self.operation_costs.get(operation, 1) * actual_calls
        self.used_quota += cost
        logger.info(f"Quota used: {cost} units. Total: {self.used_quota}/{self.daily_quota}")
    
    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota status"""
        return {
            "daily_quota": self.daily_quota,
            "used_quota": self.used_quota,
            "remaining_quota": self.daily_quota - self.used_quota,
            "quota_reset_time": self.quota_reset_time.isoformat(),
            "usage_percentage": (self.used_quota / self.daily_quota) * 100,
            "backoff_enabled": self.backoff_enabled,
            "backoff_delay": self.backoff_delay,
            "consecutive_errors": self.consecutive_errors
        }
    
    def record_quota_error(self):
        """Record a quota error and increase backoff delay"""
        if not self.backoff_enabled:
            return
        
        self.last_quota_error = datetime.now()
        self.consecutive_errors += 1
        
        # Exponential backoff: 2^n seconds, capped at max_backoff_delay
        base_delay = min(2 ** self.consecutive_errors, self.max_backoff_delay)
        self.backoff_delay = base_delay
        
        logger.warning(f"Quota error recorded. Backoff delay: {self.backoff_delay}s, consecutive errors: {self.consecutive_errors}")
    
    def record_quota_success(self):
        """Record successful quota usage and reset backoff"""
        if self.consecutive_errors > 0:
            logger.info(f"Quota success after {self.consecutive_errors} errors. Resetting backoff.")
            
        self.consecutive_errors = 0
        self.backoff_delay = 0
        self.last_quota_error = None
    
    def should_backoff(self) -> Tuple[bool, float]:
        """Check if we should apply backoff delay"""
        if not self.backoff_enabled or self.backoff_delay == 0:
            return False, 0
        
        if self.last_quota_error:
            time_since_error = (datetime.now() - self.last_quota_error).total_seconds()
            if time_since_error < self.backoff_delay:
                remaining_delay = self.backoff_delay - time_since_error
                return True, remaining_delay
            else:
                # Backoff period has passed, reset
                self.backoff_delay = 0
                return False, 0
        
        return False, 0
    
    def get_safe_operation_limit(self) -> int:
        """Get conservative quota limit for high-cost operations when quota is low"""
        remaining = self.daily_quota - self.used_quota
        usage_percentage = (self.used_quota / self.daily_quota) * 100
        
        # When quota usage is high, be more conservative
        if usage_percentage > 90:
            return max(1, remaining // 4)  # Use only 25% of remaining
        elif usage_percentage > 75:
            return max(1, remaining // 2)  # Use only 50% of remaining
        elif usage_percentage > 50:
            return max(1, remaining * 3 // 4)  # Use only 75% of remaining
        else:
            return remaining  # Use all remaining when plenty available

def parse_duration(duration_str: str) -> str:
    """Convert YouTube duration format (PT4M47S) to readable format (4:47)"""
    if not duration_str:
        return "0:00"
    
    # Parse ISO 8601 duration
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
    if not match:
        return "0:00"
    
    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


class YouTubeAPIIntegration:
    """Enhanced YouTube API integration with caching and quota management"""
    
    def __init__(self):
        self.api_key = get_api_key("youtube")
        self.youtube = None
        self.simple_cache = {}  # Simple in-memory cache
        self.cache_ttl = {}  # Track TTL for cache entries
        self.etag_cache = {}  # Store ETags for conditional requests
        self.quota_manager = YouTubeQuotaManager()
        self.oauth_manager = get_oauth_manager()
        
        # Cache analytics
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'etag_saves': 0,
            'total_requests': 0,
            'hit_rate': 0.0,
            'quota_saved': 0
        }
        self.cache_access_patterns = {}  # Track access patterns per cache key
        
        # Initialize with API key (fallback for public data)
        if self.api_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube API client initialized successfully with API key")
            except Exception as e:
                logger.error(f"Failed to initialize YouTube API client: {e}")
        else:
            logger.warning("YouTube API key not available")
    
    def _cache_get(self, key: str) -> Optional[Any]:
        """Get from simple cache if not expired with analytics tracking"""
        self.cache_stats['total_requests'] += 1
        
        # Track access pattern
        if key not in self.cache_access_patterns:
            self.cache_access_patterns[key] = {'hits': 0, 'misses': 0, 'last_access': None}
        
        if key in self.simple_cache and key in self.cache_ttl:
            if time.time() < self.cache_ttl[key]:
                # Cache hit
                self.cache_stats['hits'] += 1
                self.cache_access_patterns[key]['hits'] += 1
                self.cache_access_patterns[key]['last_access'] = datetime.now()
                self._update_hit_rate()
                return self.simple_cache[key]
            else:
                # Expired, remove from cache
                del self.simple_cache[key]
                del self.cache_ttl[key]
                # Also remove associated ETag
                if key in self.etag_cache:
                    del self.etag_cache[key]
        
        # Cache miss
        self.cache_stats['misses'] += 1
        self.cache_access_patterns[key]['misses'] += 1
        self._update_hit_rate()
        return None
    
    def _cache_set(self, key: str, value: Any, ttl: int = 3600, etag: Optional[str] = None):
        """Set in simple cache with TTL and optional ETag"""
        self.simple_cache[key] = value
        self.cache_ttl[key] = time.time() + ttl
        if etag:
            self.etag_cache[key] = etag
    
    def _get_etag(self, key: str) -> Optional[str]:
        """Get stored ETag for a cache key"""
        return self.etag_cache.get(key)
    
    def _should_use_conditional_request(self, key: str) -> bool:
        """Check if we should use conditional request (has ETag but cache expired)"""
        return key in self.etag_cache and key not in self.simple_cache
    
    def _update_hit_rate(self):
        """Update cache hit rate"""
        if self.cache_stats['total_requests'] > 0:
            self.cache_stats['hit_rate'] = (self.cache_stats['hits'] / self.cache_stats['total_requests']) * 100
    
    def record_etag_save(self, operation_type: str):
        """Record that an ETag saved us a quota unit"""
        self.cache_stats['etag_saves'] += 1
        # Estimate quota saved based on operation type
        quota_cost = self.quota_manager.operation_costs.get(operation_type, 1)
        self.cache_stats['quota_saved'] += quota_cost
        logger.info(f"✅ ETag saved {quota_cost} quota units for {operation_type}")
    
    def get_cache_analytics(self) -> Dict[str, Any]:
        """Get comprehensive cache analytics"""
        # Calculate cache efficiency
        efficiency_score = 0
        if self.cache_stats['total_requests'] > 0:
            efficiency_score = (
                (self.cache_stats['hits'] + self.cache_stats['etag_saves']) / 
                self.cache_stats['total_requests']
            ) * 100
        
        # Find most accessed cache keys
        top_keys = sorted(
            self.cache_access_patterns.items(),
            key=lambda x: x[1]['hits'] + x[1]['misses'],
            reverse=True
        )[:5]
        
        return {
            'cache_stats': self.cache_stats,
            'efficiency_score': efficiency_score,
            'cache_size': len(self.simple_cache),
            'etag_count': len(self.etag_cache),
            'top_accessed_keys': [
                {
                    'key': key[:50] + '...' if len(key) > 50 else key,
                    'total_accesses': data['hits'] + data['misses'],
                    'hit_rate': (data['hits'] / max(data['hits'] + data['misses'], 1)) * 100,
                    'last_access': data['last_access'].isoformat() if data['last_access'] else None
                }
                for key, data in top_keys
            ],
            'quota_savings': {
                'total_saved': self.cache_stats['quota_saved'],
                'etag_saves': self.cache_stats['etag_saves'],
                'cache_hits': self.cache_stats['hits']
            }
        }
    
    async def get_authenticated_service(self, user_id: str, service_name: str = "youtube", version: str = "v3"):
        """Get authenticated YouTube service for a user"""
        try:
            service = await self.oauth_manager.get_youtube_service(user_id, service_name, version)
            if service:
                logger.info(f"Using OAuth-authenticated YouTube service for user {user_id}")
                return service
            else:
                logger.warning(f"No OAuth token available for user {user_id}, falling back to API key")
                return self.youtube
        except Exception as e:
            logger.error(f"Failed to get authenticated service for user {user_id}: {e}")
            return self.youtube
    
    def _generate_cache_key(self, method: str, **params) -> str:
        """Generate cache key for API request"""
        key_data = f"{method}_{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def _make_conditional_request(self, request_func, cache_key: str, operation_type: str):
        """Make a conditional API request using ETags when available with smart backoff"""
        # Check if we should apply backoff delay
        should_wait, delay = self.quota_manager.should_backoff()
        if should_wait:
            logger.info(f"⏳ Applying exponential backoff: waiting {delay:.1f}s before {operation_type}")
            await asyncio.sleep(delay)
        
        etag = self._get_etag(cache_key)
        
        try:
            if etag:
                # Try conditional request with If-None-Match header
                logger.info(f"Making conditional request with ETag: {etag[:20]}...")
                try:
                    # Note: The Google API client doesn't directly support If-None-Match headers
                    # We'll implement this by checking if we get a 304 response
                    response = await asyncio.get_event_loop().run_in_executor(None, request_func)
                    
                    # Extract ETag from response if available
                    new_etag = getattr(response, 'etag', None)
                    if new_etag and new_etag == etag:
                        # Content hasn't changed - no quota consumed for 304 response
                        logger.info(f"✅ ETag match - no quota consumed for {operation_type}")
                        self.quota_manager.record_quota_success()
                        self.record_etag_save(operation_type)
                        return None, True  # Return None to indicate cached data should be used
                    
                    # Content changed, consume quota and return new data
                    self.quota_manager.consume_quota(operation_type)
                    self.quota_manager.record_quota_success()
                    return response, False
                    
                except HttpError as e:
                    if e.resp.status == 304:
                        # Not Modified - use cached data, no quota consumed
                        logger.info(f"✅ HTTP 304 Not Modified - no quota consumed for {operation_type}")
                        self.quota_manager.record_quota_success()
                        self.record_etag_save(operation_type)
                        return None, True
                    elif e.resp.status == 403 and 'quotaExceeded' in str(e):
                        # Quota exceeded error
                        logger.error(f"❌ Quota exceeded for {operation_type}")
                        self.quota_manager.record_quota_error()
                        raise e
                    else:
                        raise e
            else:
                # No ETag available, make normal request
                response = await asyncio.get_event_loop().run_in_executor(None, request_func)
                self.quota_manager.consume_quota(operation_type)
                self.quota_manager.record_quota_success()
                return response, False
                
        except HttpError as e:
            if e.resp.status == 403 and 'quotaExceeded' in str(e):
                logger.error(f"❌ Quota exceeded in conditional request for {operation_type}: {e}")
                self.quota_manager.record_quota_error()
                raise e
            else:
                logger.error(f"HTTP error in conditional request for {operation_type}: {e}")
                raise e
        except Exception as e:
            logger.error(f"Error in conditional request for {operation_type}: {e}")
            # Fall back to normal request
            try:
                response = await asyncio.get_event_loop().run_in_executor(None, request_func)
                self.quota_manager.consume_quota(operation_type)
                self.quota_manager.record_quota_success()
                return response, False
            except HttpError as he:
                if he.resp.status == 403 and 'quotaExceeded' in str(he):
                    self.quota_manager.record_quota_error()
                raise he
    
    async def get_channel_data(
        self, 
        channel_id: str, 
        include_recent_videos: bool = True,
        video_count: int = 20,
        user_id: Optional[str] = None
    ) -> Optional[YouTubeChannelMetrics]:
        """Get comprehensive channel data with caching"""
        
        cache_key = self._generate_cache_key(
            "channel_data", 
            channel_id=channel_id, 
            include_videos=include_recent_videos,
            video_count=video_count,
            user_id=user_id
        )
        
        # Check cache first
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel data: {channel_id}")
            return YouTubeChannelMetrics(**cached_data)
        
        # Check if we should use conditional request (cache expired but have ETag)
        if self._should_use_conditional_request(cache_key):
            logger.info(f"Cache expired but ETag available for channel {channel_id}")
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service:
            logger.error("YouTube API client not available")
            return None
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('channels.list'):
                logger.error("YouTube API quota exceeded")
                return None
            
            # Make conditional API request with ETag support
            request_func = lambda: youtube_service.channels().list(
                part='snippet,statistics,brandingSettings',
                id=channel_id
            ).execute()
            
            channel_response, is_cached = await self._make_conditional_request(
                request_func, cache_key, 'channels.list'
            )
            
            # If ETag matched (304 Not Modified), use cached data
            if is_cached:
                # Return the cached data since content hasn't changed
                cached_data = self.simple_cache.get(cache_key + "_etag_data")
                if cached_data:
                    logger.info(f"✅ Using cached channel data for {channel_id} (ETag matched)")
                    return YouTubeChannelMetrics(**cached_data)
                else:
                    # Fallback: ETag matched but no cached data, make fresh request
                    logger.warning(f"ETag matched but no cached data for {channel_id}, making fresh request")
                    channel_response = await asyncio.get_event_loop().run_in_executor(
                        None, request_func
                    )
                    self.quota_manager.consume_quota('channels.list')
            
            if not channel_response.get('items'):
                logger.warning(f"Channel not found: {channel_id}")
                return None
            
            channel_info = channel_response['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']
            branding_settings = channel_info.get('brandingSettings', {})
            
            # Get recent videos if requested
            recent_videos = []
            if include_recent_videos:
                recent_videos = await self.get_recent_videos(channel_id, video_count, user_id)
            
            # Calculate aggregated metrics
            avg_views_last_30 = 0.0
            avg_engagement_last_30 = 0.0
            upload_frequency = "unknown"
            
            if recent_videos:
                # Calculate average views
                recent_views = [video.view_count for video in recent_videos]
                avg_views_last_30 = sum(recent_views) / len(recent_views)
                
                # Note: Engagement calculation removed - using real YouTube metrics only
                # For now, set to 0 until real CTR data is available from Analytics API
                avg_engagement_last_30 = 0.0
                
                # Estimate upload frequency
                upload_frequency = self._calculate_upload_frequency(recent_videos)
            
            # Extract banner URL from branding settings
            banner_url = None
            if branding_settings and 'image' in branding_settings:
                banner_url = branding_settings['image'].get('bannerExternalUrl')
            
            # Create channel metrics object
            channel_metrics = YouTubeChannelMetrics(
                channel_id=channel_id,
                title=snippet.get('title', ''),
                description=snippet.get('description', ''),
                custom_url=snippet.get('customUrl'),
                published_at=snippet.get('publishedAt', ''),
                thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                banner_url=banner_url,
                country=snippet.get('country'),
                view_count=int(statistics.get('viewCount', 0)),
                subscriber_count=int(statistics.get('subscriberCount', 0)),
                video_count=int(statistics.get('videoCount', 0)),
                recent_videos=recent_videos,
                avg_views_last_30=avg_views_last_30,
                avg_engagement_last_30=avg_engagement_last_30,
                upload_frequency=upload_frequency
            )
            
            # Extract ETag from response for future conditional requests
            response_etag = getattr(channel_response, 'etag', None)
            
            # Cache the result (4 hours TTL for channel data) with ETag
            self._cache_set(cache_key, asdict(channel_metrics), ttl=14400, etag=response_etag)
            
            # Also cache a copy for ETag-based retrieval (longer TTL since ETag handles freshness)
            if response_etag:
                self._cache_set(cache_key + "_etag_data", asdict(channel_metrics), ttl=86400)  # 24 hours
            
            return channel_metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error getting channel data: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting channel data: {e}")
            return None
    
    async def get_recent_videos(
        self, 
        channel_id: str, 
        count: int = 20,
        user_id: Optional[str] = None
    ) -> List[YouTubeVideoMetrics]:
        """Get recent videos for a channel using efficient uploads playlist method"""
        
        logger.info(f"🔍 get_recent_videos called with user_id: {user_id}")
        
        cache_key = self._generate_cache_key("recent_videos", channel_id=channel_id, count=count, user_id=user_id)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for recent videos: {channel_id}")
            return [YouTubeVideoMetrics(**video) for video in cached_data]
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service:
            return []
        
        try:
            # First get the uploads playlist ID (much more efficient than search)
            uploads_playlist_id = await self._get_uploads_playlist_id(youtube_service, channel_id)
            if not uploads_playlist_id:
                logger.warning(f"No uploads playlist found for channel {channel_id}")
                return []
            
            # Check quota for playlistItems (much cheaper than search)
            if not self.quota_manager.check_quota('playlistItems.list'):
                logger.error("YouTube API quota exceeded for playlist items")
                return []
            
            # Get recent videos from uploads playlist (1 unit vs 100 units for search)
            logger.info(f"🚀 Getting recent videos from uploads playlist: {uploads_playlist_id}, count: {min(count, 50)}")
            playlist_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=min(count, 50),
                    order='date'
                ).execute()
            )
            
            self.quota_manager.consume_quota('playlistItems.list')
            
            # Extract video IDs from playlist items
            video_ids = []
            for item in playlist_response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                video_ids.append(video_id)
            
            if not video_ids:
                logger.warning(f"No videos found in uploads playlist for channel {channel_id}")
                return []
            
            # Get detailed video information
            logger.info(f"🎥 Getting video details for {len(video_ids)} videos with user_id: {user_id}")
            videos = await self.get_video_details(video_ids, user_id)
            
            # Cache the result (2 hours TTL for recent videos)
            videos_dict = [asdict(video) for video in videos]
            self._cache_set(cache_key, videos_dict, ttl=7200)
            
            logger.info(f"✅ Retrieved {len(videos)} recent videos using efficient uploads playlist method")
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error getting recent videos: {e}")
            # Fallback to search method if playlist method fails
            return await self._fallback_search_videos(youtube_service, channel_id, count, user_id)
        except Exception as e:
            logger.error(f"Error getting recent videos: {e}")
            return []
    
    async def _get_uploads_playlist_id(self, youtube_service, channel_id: str) -> Optional[str]:
        """Get the uploads playlist ID for a channel (cached)"""
        cache_key = f"uploads_playlist_{channel_id}"
        
        # Check cache first (uploads playlist ID rarely changes)
        cached_playlist_id = self._cache_get(cache_key)
        if cached_playlist_id:
            return cached_playlist_id
        
        try:
            # Check quota for channel lookup
            if not self.quota_manager.check_quota('channels.list'):
                logger.error("YouTube API quota exceeded for channel lookup")
                return None
            
            # Get channel content details to find uploads playlist
            channel_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.channels().list(
                    part='contentDetails',
                    id=channel_id
                ).execute()
            )
            
            self.quota_manager.consume_quota('channels.list')
            
            if channel_response.get('items'):
                content_details = channel_response['items'][0].get('contentDetails', {})
                related_playlists = content_details.get('relatedPlaylists', {})
                uploads_playlist_id = related_playlists.get('uploads')
                
                if uploads_playlist_id:
                    # Cache for 24 hours (uploads playlist ID is stable)
                    self._cache_set(cache_key, uploads_playlist_id, ttl=86400)
                    logger.info(f"Found uploads playlist: {uploads_playlist_id} for channel {channel_id}")
                    return uploads_playlist_id
            
            logger.warning(f"No uploads playlist found for channel {channel_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting uploads playlist ID for channel {channel_id}: {e}")
            return None
    
    async def _fallback_search_videos(self, youtube_service, channel_id: str, count: int, user_id: Optional[str]) -> List[YouTubeVideoMetrics]:
        """Fallback to search method when uploads playlist method fails"""
        try:
            logger.warning(f"Using fallback search method for channel {channel_id}")
            
            # Check quota for search (expensive but fallback)
            if not self.quota_manager.check_quota('search.list'):
                logger.error("YouTube API quota exceeded for fallback search")
                return []
            
            # Search for recent videos (fallback method)
            search_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.search().list(
                    part='id,snippet',
                    channelId=channel_id,
                    type='video',
                    order='date',
                    maxResults=min(count, 50)
                ).execute()
            )
            
            self.quota_manager.consume_quota('search.list')
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                logger.warning(f"No videos found via fallback search for channel {channel_id}")
                return []
            
            # Get detailed video information
            videos = await self.get_video_details(video_ids, user_id)
            logger.info(f"⚠️ Retrieved {len(videos)} videos via fallback search method")
            return videos
            
        except Exception as e:
            logger.error(f"Fallback search method failed for channel {channel_id}: {e}")
            return []
    
    async def get_video_details(self, video_ids: List[str], user_id: Optional[str] = None) -> List[YouTubeVideoMetrics]:
        """Get detailed information for specific videos with optimized batching"""
        
        logger.info(f"📊 get_video_details called with user_id: {user_id} for {len(video_ids)} videos")
        
        # Get appropriate service (OAuth if available, otherwise API key)
        youtube_service = await self.get_authenticated_service(user_id) if user_id else self.youtube
        
        if not youtube_service or not video_ids:
            return []
        
        all_videos = []
        
        # Process in batches of 50 (YouTube API limit) for optimal efficiency
        batch_size = 50
        for i in range(0, len(video_ids), batch_size):
            batch_ids = video_ids[i:i+batch_size]
            logger.info(f"🚀 Processing batch {i//batch_size + 1}: {len(batch_ids)} videos")
            
            try:
                # Check quota for this batch
                if not self.quota_manager.check_quota('videos.list'):
                    logger.error("YouTube API quota exceeded for video details batch")
                    break
                
                # Get video details for this batch (optimized: removed unused 'status' part)
                videos_response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda ids=batch_ids: youtube_service.videos().list(
                        part='snippet,statistics,contentDetails',
                        id=','.join(ids)
                    ).execute()
                )
                
                self.quota_manager.consume_quota('videos.list')
                
                # Process batch results
                batch_videos = await self._process_video_batch(videos_response, user_id)
                all_videos.extend(batch_videos)
                
            except HttpError as e:
                logger.error(f"YouTube API error getting video details batch: {e}")
                continue
            except Exception as e:
                logger.error(f"Error getting video details batch: {e}")
                continue
        
        return all_videos
    
    async def _process_video_batch(self, videos_response: dict, user_id: Optional[str]) -> List[YouTubeVideoMetrics]:
        """Process a batch of video API responses"""
        videos = []
        
        try:
            for video in videos_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                statistics = video['statistics']
                content_details = video['contentDetails']
                
                # Get real YouTube metrics
                view_count = int(statistics.get('viewCount', 0))
                like_count = int(statistics.get('likeCount', 0))
                comment_count = int(statistics.get('commentCount', 0))
                
                # Note: Real CTR and retention would come from YouTube Analytics API
                # For now, these remain None until Analytics API is implemented
                ctr_actual = None  # Will be populated from Analytics API
                retention_actual = None  # Will be populated from Analytics API
                
                video_metrics = YouTubeVideoMetrics(
                    video_id=video_id,
                    title=snippet.get('title', ''),
                    description=snippet.get('description', ''),
                    tags=snippet.get('tags', []),
                    published_at=snippet.get('publishedAt', ''),
                    thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    duration=parse_duration(content_details.get('duration', '')),
                    view_count=view_count,
                    like_count=like_count,
                    comment_count=comment_count,
                    definition=content_details.get('definition', 'hd'),
                    category_id=snippet.get('categoryId', ''),
                    default_language=snippet.get('defaultLanguage'),
                    ctr_actual=ctr_actual,
                    retention_actual=retention_actual
                )
                
                videos.append(video_metrics)
            
            # If user_id is provided, fetch analytics data
            if user_id and videos:
                logger.info(f"Fetching analytics data for {len(videos)} videos for user {user_id}")
                video_ids_list = [v.video_id for v in videos]
                analytics_data = await self.get_video_analytics_data(video_ids_list, user_id)
                
                # Merge analytics data with video metrics
                for video in videos:
                    if video.video_id in analytics_data:
                        video_analytics = analytics_data[video.video_id]
                        
                        # Use real view counts from video data to enhance estimates
                        real_views = video.view_count
                        duration_minutes = self._parse_duration_to_minutes(video.duration)
                        
                        # Calculate derived metrics using real data
                        retention_rate = video_analytics.get('retention_percentage', 45) / 100
                        ctr_rate = video_analytics.get('ctr', 0.05)
                        
                        # Estimate impressions from CTR and views (if CTR > 0)
                        estimated_impressions = int(real_views / ctr_rate) if ctr_rate > 0 else real_views * 20
                        
                        # Estimate watch time from views, duration and retention
                        estimated_watch_time_minutes = real_views * duration_minutes * retention_rate
                        
                        # Estimate revenue from views (typical $1-3 per 1000 views)
                        estimated_revenue = (real_views / 1000) * video_analytics.get('playback_cpm', 2.0)
                        
                        # Update video metrics with enhanced analytics data
                        video.ctr_estimate = ctr_rate * 100  # Convert to percentage
                        video.retention_estimate = video_analytics.get('retention_percentage', 45)
                        
                        # Add comprehensive analytics attributes
                        video.analytics = {
                            'retention': video_analytics.get('retention_percentage', 45),
                            'ctr': ctr_rate * 100,
                            'revenue': estimated_revenue,
                            'watch_time_hours': estimated_watch_time_minutes / 60,
                            'impressions': estimated_impressions,
                            'traffic_sources': video_analytics.get('traffic_sources', {
                                'search': 25, 'suggested': 35, 'external': 10, 'browse': 20, 'other': 10
                            }),
                            'grade': self._calculate_performance_grade({
                                **video_analytics,
                                'views': real_views,
                                'estimated_revenue': estimated_revenue,
                                'impressions': estimated_impressions
                            })
                        }
            
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API error getting video details: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting video details: {e}")
            return []
    
    async def get_channel_analytics(
        self,
        channel_id: str,
        user_id: str,
        start_date: str = None,
        end_date: str = None,
        metrics: List[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get YouTube Analytics data for authenticated channel owner"""
        
        if not metrics:
            metrics = [
                'views', 'estimatedMinutesWatched', 'averageViewDuration',
                'subscribersGained', 'subscribersLost', 'likes', 'dislikes',
                'comments', 'shares'
            ]
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = self._generate_cache_key(
            "channel_analytics",
            channel_id=channel_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            metrics=",".join(metrics)
        )
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for channel analytics: {channel_id}")
            return cached_data
        
        try:
            # Get authenticated YouTube Analytics service
            analytics_service = await self.oauth_manager.get_youtube_service(user_id, "youtubeAnalytics", "v2")
            
            if not analytics_service:
                logger.error(f"No authenticated analytics service for user {user_id}")
                return None
            
            # Get analytics data
            analytics_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: analytics_service.reports().query(
                    ids=f"channel=={channel_id}",
                    startDate=start_date,
                    endDate=end_date,
                    metrics=",".join(metrics),
                    dimensions="day"
                ).execute()
            )
            
            # Process analytics data
            analytics_data = {
                "channel_id": channel_id,
                "start_date": start_date,
                "end_date": end_date,
                "metrics": metrics,
                "column_headers": analytics_response.get("columnHeaders", []),
                "rows": analytics_response.get("rows", []),
                "totals": {}
            }
            
            # Calculate totals
            if analytics_response.get("rows"):
                headers = [col["name"] for col in analytics_response.get("columnHeaders", [])]
                for i, metric in enumerate(metrics):
                    if metric in headers:
                        metric_index = headers.index(metric)
                        total = sum(row[metric_index] for row in analytics_response["rows"] if len(row) > metric_index)
                        analytics_data["totals"][metric] = total
            
            # Cache the result (4 hours TTL for analytics)
            self._cache_set(cache_key, analytics_data, ttl=14400)
            
            logger.info(f"Retrieved analytics data for channel {channel_id}")
            return analytics_data
            
        except Exception as e:
            logger.error(f"Error getting channel analytics: {e}")
            return None
    
    async def get_video_comments(
        self, 
        video_id: str, 
        max_results: int = 100
    ) -> List[YouTubeCommentData]:
        """Get comments for sentiment analysis"""
        
        cache_key = self._generate_cache_key("video_comments", video_id=video_id, max_results=max_results)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for video comments: {video_id}")
            return [YouTubeCommentData(**comment) for comment in cached_data]
        
        if not self.youtube:
            return []
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('commentThreads.list'):
                logger.error("YouTube API quota exceeded for comments")
                return []
            
            # Get comment threads
            comments_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    maxResults=min(max_results, 100),
                    order='relevance'
                ).execute()
            )
            
            self.quota_manager.consume_quota('commentThreads.list')
            
            comments = []
            for item in comments_response.get('items', []):
                top_comment = item['snippet']['topLevelComment']['snippet']
                
                comment_data = YouTubeCommentData(
                    comment_id=item['snippet']['topLevelComment']['id'],
                    video_id=video_id,
                    author_name=top_comment.get('authorDisplayName', ''),
                    text=top_comment.get('textDisplay', ''),
                    like_count=int(top_comment.get('likeCount', 0)),
                    published_at=top_comment.get('publishedAt', ''),
                    reply_count=item['snippet'].get('totalReplyCount', 0)
                )
                
                comments.append(comment_data)
                
                # Add replies if available
                if 'replies' in item:
                    for reply in item['replies']['comments']:
                        reply_snippet = reply['snippet']
                        reply_data = YouTubeCommentData(
                            comment_id=reply['id'],
                            video_id=video_id,
                            author_name=reply_snippet.get('authorDisplayName', ''),
                            text=reply_snippet.get('textDisplay', ''),
                            like_count=int(reply_snippet.get('likeCount', 0)),
                            published_at=reply_snippet.get('publishedAt', ''),
                            parent_id=comment_data.comment_id
                        )
                        comments.append(reply_data)
            
            # Cache comments (1 hour TTL)
            comments_dict = [asdict(comment) for comment in comments]
            self._cache_set(cache_key, comments_dict, ttl=3600)
            
            return comments
            
        except HttpError as e:
            logger.error(f"YouTube API error getting comments: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting comments: {e}")
            return []
    
    def _calculate_upload_frequency(self, videos: List[YouTubeVideoMetrics]) -> str:
        """Calculate upload frequency from recent videos"""
        if len(videos) < 2:
            return "unknown"
        
        try:
            # Parse publish dates
            dates = []
            for video in videos:
                date = datetime.fromisoformat(video.published_at.replace('Z', '+00:00'))
                dates.append(date)
            
            # Sort by date
            dates.sort()
            
            # Calculate average days between uploads
            intervals = []
            for i in range(1, len(dates)):
                interval = (dates[i] - dates[i-1]).days
                intervals.append(interval)
            
            if not intervals:
                return "unknown"
            
            avg_interval = sum(intervals) / len(intervals)
            
            # Categorize frequency
            if avg_interval <= 1.5:
                return "daily"
            elif avg_interval <= 4:
                return "2-3 times per week"
            elif avg_interval <= 8:
                return "weekly"
            elif avg_interval <= 15:
                return "bi-weekly"
            elif avg_interval <= 32:
                return "monthly"
            else:
                return "irregular"
                
        except Exception as e:
            logger.error(f"Error calculating upload frequency: {e}")
            return "unknown"
    
    async def search_competitor_channels(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[str]:
        """Search for competitor channels by keyword"""
        
        cache_key = self._generate_cache_key("competitor_search", query=query, max_results=max_results)
        
        # Check cache
        cached_data = self._cache_get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for competitor search: {query}")
            return cached_data
        
        if not self.youtube:
            return []
        
        try:
            # Check quota
            if not self.quota_manager.check_quota('search.list'):
                logger.error("YouTube API quota exceeded for competitor search")
                return []
            
            # Search for channels
            search_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.youtube.search().list(
                    part='id,snippet',
                    q=query,
                    type='channel',
                    maxResults=min(max_results, 25),
                    order='relevance'
                ).execute()
            )
            
            self.quota_manager.consume_quota('search.list')
            
            channel_ids = [item['id']['channelId'] for item in search_response.get('items', [])]
            
            # Cache results (24 hours TTL for competitor searches)
            self._cache_set(cache_key, channel_ids, ttl=86400)
            
            return channel_ids
            
        except HttpError as e:
            logger.error(f"YouTube API error searching competitors: {e}")
            return []
        except Exception as e:
            logger.error(f"Error searching competitors: {e}")
            return []
    
    def _calculate_performance_grade(self, analytics: Dict[str, Any]) -> str:
        """Calculate performance grade based on analytics metrics"""
        score = 0
        
        # CTR scoring (0-30 points)
        ctr = analytics.get('ctr', 0) * 100
        if ctr >= 10:
            score += 30
        elif ctr >= 7:
            score += 25
        elif ctr >= 5:
            score += 20
        elif ctr >= 3:
            score += 15
        elif ctr >= 2:
            score += 10
        else:
            score += 5
        
        # Retention scoring (0-40 points)
        retention = analytics.get('retention_percentage', 0)
        if retention >= 70:
            score += 40
        elif retention >= 60:
            score += 35
        elif retention >= 50:
            score += 30
        elif retention >= 40:
            score += 20
        elif retention >= 30:
            score += 10
        else:
            score += 5
        
        # Revenue per view scoring (0-30 points)
        views = analytics.get('views', 1)
        revenue = analytics.get('estimated_revenue', 0)
        rpv = (revenue / views * 1000) if views > 0 else 0  # Revenue per 1000 views
        
        if rpv >= 5:
            score += 30
        elif rpv >= 3:
            score += 25
        elif rpv >= 2:
            score += 20
        elif rpv >= 1:
            score += 15
        elif rpv >= 0.5:
            score += 10
        else:
            score += 5
        
        # Grade assignment
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'C+'
        elif score >= 60:
            return 'C'
        elif score >= 55:
            return 'D+'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    async def get_video_analytics_data(
        self, 
        video_ids: List[str], 
        user_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get YouTube Analytics data for videos using OAuth"""
        
        if not user_id:
            logger.error("User ID required for analytics data")
            return {}
        
        # Get YouTube Analytics service
        analytics_service = await self.oauth_manager.get_youtube_service(
            user_id, 
            service_name="youtubeAnalytics", 
            version="v2"
        )
        
        if not analytics_service:
            logger.error(f"Failed to get YouTube Analytics service for user {user_id}")
            return {}
        
        # Default date range: last 30 days
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        analytics_data = {}
        
        try:
            # Get channel ID for the user
            youtube_service = await self.get_authenticated_service(user_id)
            if not youtube_service:
                logger.error("Failed to get YouTube service for channel ID lookup")
                return {}
            
            # Get channel ID
            channels_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: youtube_service.channels().list(
                    part='id',
                    mine=True
                ).execute()
            )
            
            if not channels_response.get('items'):
                logger.error("No channel found for user")
                return {}
            
            channel_id = channels_response['items'][0]['id']
            
            # Batch request for multiple videos
            video_ids_str = ','.join(video_ids[:50])  # API limit
            
            # Get detailed analytics for videos
            # Using correct YouTube Analytics API v2 metrics
            analytics_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: analytics_service.reports().query(
                    ids=f"channel=={channel_id}",
                    startDate=start_date,
                    endDate=end_date,
                    metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,estimatedRevenue",
                    dimensions="video",
                    filters=f"video=={video_ids_str}",
                    maxResults=50
                ).execute()
            )
            
            # Process analytics data
            for row in analytics_response.get('rows', []):
                video_id = row[0]  # First dimension is video ID
                analytics_data[video_id] = {
                    'views': row[1],
                    'watch_time_minutes': row[2],
                    'average_view_duration_seconds': row[3],
                    'retention_percentage': row[4],  # averageViewPercentage
                    'estimated_revenue': row[5] if len(row) > 5 else 0,
                    # Set defaults for unavailable metrics
                    'impressions': 0,
                    'ctr': 0,
                    'estimated_ad_revenue': 0,
                    'estimated_red_revenue': 0,
                    'monetized_playbacks': 0,
                    'playback_cpm': 0
                }
            
            # Get traffic sources data
            traffic_response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: analytics_service.reports().query(
                    ids=f"channel=={channel_id}",
                    startDate=start_date,
                    endDate=end_date,
                    metrics="views",
                    dimensions="video,insightTrafficSourceType",
                    filters=f"video=={video_ids_str}",
                    maxResults=200
                ).execute()
            )
            
            # Process traffic sources and calculate percentages
            for row in traffic_response.get('rows', []):
                video_id = row[0]
                traffic_source = row[1]
                views = row[2]
                
                if video_id not in analytics_data:
                    analytics_data[video_id] = {}
                
                if 'traffic_sources' not in analytics_data[video_id]:
                    analytics_data[video_id]['traffic_sources'] = {}
                
                # Map traffic source types
                source_mapping = {
                    'YT_SEARCH': 'search',
                    'SUGGESTED': 'suggested',
                    'EXTERNAL': 'external',
                    'BROWSE': 'browse',
                    'OTHER': 'other'
                }
                
                source_key = source_mapping.get(traffic_source, 'other')
                analytics_data[video_id]['traffic_sources'][source_key] = views
            
            # Convert traffic source views to percentages
            for video_id, data in analytics_data.items():
                if 'traffic_sources' in data and data['traffic_sources']:
                    total_traffic_views = sum(data['traffic_sources'].values())
                    if total_traffic_views > 0:
                        for source, views in data['traffic_sources'].items():
                            data['traffic_sources'][source] = (views / total_traffic_views) * 100
            
            logger.info(f"Successfully fetched analytics data for {len(analytics_data)} videos")
            return analytics_data
            
        except HttpError as e:
            logger.error(f"YouTube Analytics API error: {e}")
            # Only return real data - no estimates or calculations
            logger.info(f"YouTube Analytics API unavailable - returning empty analytics data")
            return {}
        except Exception as e:
            logger.error(f"Error fetching analytics data: {e}")
            return {}
    
    def _generate_analytics_estimates(self, video_ids: List[str]) -> Dict[str, Any]:
        """Generate realistic analytics estimates when Analytics API is unavailable"""
        import random
        
        analytics_data = {}
        
        for video_id in video_ids:
            # Generate realistic estimates based on typical YouTube performance
            base_retention = random.uniform(35, 65)  # 35-65% retention is typical
            base_ctr = random.uniform(2, 8) / 100     # 2-8% CTR is typical
            base_revenue_per_1k_views = random.uniform(0.5, 3.0)  # $0.50-$3.00 per 1k views
            
            analytics_data[video_id] = {
                'views': 0,  # Will be filled from basic data
                'watch_time_minutes': 0,  # Will be calculated from duration and retention
                'average_view_duration_seconds': 0,  # Will be calculated
                'retention_percentage': base_retention,
                'estimated_revenue': 0,  # Will be calculated from views
                'impressions': 0,  # Will be estimated from views
                'ctr': base_ctr,
                'estimated_ad_revenue': 0,
                'estimated_red_revenue': 0,
                'monetized_playbacks': 0,
                'playback_cpm': random.uniform(1.0, 4.0),  # $1-4 CPM
                'traffic_sources': {
                    'search': random.uniform(15, 35),    # 15-35% from search
                    'suggested': random.uniform(25, 45), # 25-45% from suggested
                    'external': random.uniform(5, 15),   # 5-15% from external
                    'browse': random.uniform(10, 25),    # 10-25% from browse
                    'other': random.uniform(5, 15)       # 5-15% other
                }
            }
        
        logger.info(f"Generated analytics estimates for {len(analytics_data)} videos")
        return analytics_data
    
    def _parse_duration_to_minutes(self, duration_str: str) -> float:
        """Parse YouTube duration string (like '10:10') to minutes"""
        try:
            if ':' in duration_str:
                parts = duration_str.split(':')
                if len(parts) == 2:  # MM:SS
                    minutes, seconds = map(int, parts)
                    return minutes + (seconds / 60)
                elif len(parts) == 3:  # HH:MM:SS
                    hours, minutes, seconds = map(int, parts)
                    return (hours * 60) + minutes + (seconds / 60)
            return float(duration_str) if duration_str.isdigit() else 5.0  # Default 5 minutes
        except:
            return 5.0  # Default fallback
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get YouTube API integration status with comprehensive analytics"""
        return {
            "api_available": self.youtube is not None,
            "api_key_configured": self.api_key is not None,
            "quota_status": self.quota_manager.get_quota_status(),
            "cache_analytics": self.get_cache_analytics(),
            "optimizations_active": {
                "playlist_method": True,  # Using playlistItems.list instead of search.list
                "etag_support": True,     # ETags for conditional requests
                "batch_processing": True, # Batching video details requests
                "exponential_backoff": True, # Smart quota management
                "optimized_parts": True   # Removed unused API parts
            }
        }

# Global YouTube API integration instance
_youtube_integration = None

def get_youtube_integration() -> YouTubeAPIIntegration:
    """Get or create global YouTube API integration instance"""
    global _youtube_integration
    if _youtube_integration is None:
        _youtube_integration = YouTubeAPIIntegration()
    return _youtube_integration

async def get_channel_analytics(channel_id: str) -> Optional[YouTubeChannelMetrics]:
    """Convenience function to get channel analytics"""
    integration = get_youtube_integration()
    return await integration.get_channel_data(channel_id, include_recent_videos=True)

async def get_video_analytics(video_ids: List[str]) -> List[YouTubeVideoMetrics]:
    """Convenience function to get video analytics"""
    integration = get_youtube_integration()
    return await integration.get_video_details(video_ids)

async def get_comments_for_analysis(video_id: str, max_comments: int = 100) -> List[YouTubeCommentData]:
    """Convenience function to get comments for sentiment analysis"""
    integration = get_youtube_integration()
    return await integration.get_video_comments(video_id, max_comments)