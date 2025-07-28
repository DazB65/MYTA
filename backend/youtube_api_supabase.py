"""
YouTube API Integration with Supabase Token Authentication
Handles YouTube Data API and Analytics API calls using tokens from Supabase OAuth
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class YouTubeTokens:
    """YouTube OAuth tokens from Supabase"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[str] = None
    scopes: List[str] = None

class YouTubeAPIClient:
    """YouTube API client that uses Supabase tokens"""
    
    def __init__(self, tokens: YouTubeTokens):
        self.tokens = tokens
        self._youtube_service = None
        self._analytics_service = None
        
    def _create_credentials(self) -> Credentials:
        """Create Google credentials from Supabase tokens"""
        return Credentials(
            token=self.tokens.access_token,
            refresh_token=self.tokens.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=self.tokens.scopes or []
        )
    
    def get_youtube_service(self):
        """Get or create YouTube Data API service"""
        if not self._youtube_service:
            credentials = self._create_credentials()
            self._youtube_service = build('youtube', 'v3', credentials=credentials)
        return self._youtube_service
    
    def get_analytics_service(self):
        """Get or create YouTube Analytics API service"""
        if not self._analytics_service:
            credentials = self._create_credentials()
            self._analytics_service = build('youtubeAnalytics', 'v2', credentials=credentials)
        return self._analytics_service
    
    async def get_channel_info(self, channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get basic channel information
        If channel_id is None, gets info for the authenticated user's channel
        """
        try:
            youtube = self.get_youtube_service()
            
            # Get channel info
            if channel_id:
                channels_response = youtube.channels().list(
                    part='snippet,statistics,contentDetails',
                    id=channel_id
                ).execute()
            else:
                # Get authenticated user's channel
                channels_response = youtube.channels().list(
                    part='snippet,statistics,contentDetails',
                    mine=True
                ).execute()
            
            if not channels_response.get('items'):
                raise ValueError("No channel found")
            
            channel = channels_response['items'][0]
            
            return {
                'channel_id': channel['id'],
                'title': channel['snippet']['title'],
                'description': channel['snippet']['description'],
                'published_at': channel['snippet']['publishedAt'],
                'subscriber_count': int(channel['statistics'].get('subscriberCount', 0)),
                'video_count': int(channel['statistics'].get('videoCount', 0)),
                'view_count': int(channel['statistics'].get('viewCount', 0)),
                'custom_url': channel['snippet'].get('customUrl'),
                'thumbnail_url': channel['snippet']['thumbnails']['default']['url']
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel info: {e}")
            raise
    
    async def get_channel_videos(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get recent videos for a channel"""
        try:
            youtube = self.get_youtube_service()
            
            # Get uploads playlist ID
            channels_response = youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            if not channels_response.get('items'):
                raise ValueError("Channel not found")
            
            uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_response = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            ).execute()
            
            video_ids = [item['contentDetails']['videoId'] for item in playlist_response['items']]
            
            if not video_ids:
                return []
            
            # Get detailed video information
            videos_response = youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            videos = []
            for video in videos_response['items']:
                videos.append({
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'published_at': video['snippet']['publishedAt'],
                    'thumbnail_url': video['snippet']['thumbnails']['default']['url'],
                    'duration': video['contentDetails']['duration'],
                    'view_count': int(video['statistics'].get('viewCount', 0)),
                    'like_count': int(video['statistics'].get('likeCount', 0)),
                    'comment_count': int(video['statistics'].get('commentCount', 0)),
                    'category_id': video['snippet'].get('categoryId'),
                    'tags': video['snippet'].get('tags', [])
                })
            
            return videos
            
        except Exception as e:
            logger.error(f"Failed to get channel videos: {e}")
            raise
    
    async def get_video_analytics(self, video_ids: List[str], start_date: str, end_date: str) -> Dict[str, Any]:
        """Get analytics data for specific videos"""
        try:
            analytics = self.get_analytics_service()
            
            # Get video analytics
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate=start_date,
                endDate=end_date,
                metrics='views,likes,comments,shares,estimatedMinutesWatched,averageViewDuration',
                dimensions='video',
                filters=f'video=={",".join(video_ids)}',
                sort='-views'
            ).execute()
            
            # Process the response
            analytics_data = {}
            if 'rows' in response:
                headers = [col['name'] for col in response['columnHeaders']]
                
                for row in response['rows']:
                    video_id = row[0]  # First column is video ID
                    analytics_data[video_id] = dict(zip(headers[1:], row[1:]))  # Skip video ID column
            
            return analytics_data
            
        except Exception as e:
            logger.error(f"Failed to get video analytics: {e}")
            raise
    
    async def get_channel_analytics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get channel-level analytics data"""
        try:
            analytics = self.get_analytics_service()
            
            # Get channel analytics
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate=start_date,
                endDate=end_date,
                metrics='views,likes,comments,shares,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost',
                dimensions='day'
            ).execute()
            
            # Process the response
            daily_data = []
            if 'rows' in response:
                headers = [col['name'] for col in response['columnHeaders']]
                
                for row in response['rows']:
                    daily_data.append(dict(zip(headers, row)))
            
            return {
                'daily_data': daily_data,
                'summary': {
                    'total_views': sum(int(day.get('views', 0)) for day in daily_data),
                    'total_watch_time': sum(int(day.get('estimatedMinutesWatched', 0)) for day in daily_data),
                    'total_subscribers_gained': sum(int(day.get('subscribersGained', 0)) for day in daily_data),
                    'total_subscribers_lost': sum(int(day.get('subscribersLost', 0)) for day in daily_data),
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel analytics: {e}")
            raise

# Helper functions for creating API clients
def create_youtube_client(tokens: YouTubeTokens) -> YouTubeAPIClient:
    """Create a YouTube API client with the given tokens"""
    return YouTubeAPIClient(tokens)

def create_youtube_client_from_dict(tokens_dict: Dict[str, Any]) -> YouTubeAPIClient:
    """Create a YouTube API client from a dictionary of tokens"""
    tokens = YouTubeTokens(
        access_token=tokens_dict['access_token'],
        refresh_token=tokens_dict.get('refresh_token'),
        expires_at=tokens_dict.get('expires_at'),
        scopes=tokens_dict.get('scopes', [])
    )
    return YouTubeAPIClient(tokens)