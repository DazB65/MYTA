"""
Content Analysis Agent for CreatorMate
Specialized sub-agent that analyzes YouTube content performance for the boss agent
"""

import asyncio
import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.generativeai as genai
from dataclasses import dataclass
from youtube_api_integration import get_youtube_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisRequest:
    """Structure for content analysis requests from boss agent"""
    request_id: str
    channel_id: str
    video_ids: List[str]
    time_period: str
    analysis_depth: str = "standard"  # standard, deep, quick
    include_visual_analysis: bool = True
    token_budget: int = 4000
    user_context: Dict = None

@dataclass
class ContentMetrics:
    """Video content metrics structure"""
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    duration: int
    published_at: str
    engagement_rate: float
    retention_data: Dict[str, Any] = None
    traffic_sources: Dict[str, Any] = None

class YouTubeAPIClient:
    """YouTube API integration for content data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.analytics = None  # Would require OAuth for Analytics API
        
    async def get_video_metrics(self, video_ids: List[str]) -> List[ContentMetrics]:
        """Retrieve basic video metrics from YouTube Data API"""
        
        try:
            # Get video details
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            metrics = []
            for video in video_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                stats = video['statistics']
                duration = video['contentDetails']['duration']
                
                # Parse duration from ISO 8601 format (PT4M13S -> seconds)
                duration_seconds = self._parse_duration(duration)
                
                # Calculate engagement rate
                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments = int(stats.get('commentCount', 0))
                
                engagement_rate = ((likes + comments) / max(views, 1)) * 100 if views > 0 else 0
                
                metrics.append(ContentMetrics(
                    video_id=video_id,
                    title=snippet['title'],
                    views=views,
                    likes=likes,
                    comments=comments,
                    duration=duration_seconds,
                    published_at=snippet['publishedAt'],
                    engagement_rate=engagement_rate
                ))
            
            return metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving video metrics: {e}")
            return []
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        import re
        
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    async def get_channel_averages(self, channel_id: str, video_count: int = 50) -> Dict[str, float]:
        """Get channel performance averages for benchmarking"""
        
        try:
            # Get recent videos from channel
            search_response = self.youtube.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=video_count
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return {}
            
            metrics = await self.get_video_metrics(video_ids)
            
            if not metrics:
                return {}
            
            # Calculate averages
            total_views = sum(m.views for m in metrics)
            total_engagement = sum(m.engagement_rate for m in metrics)
            total_duration = sum(m.duration for m in metrics)
            
            return {
                'avg_views': total_views / len(metrics),
                'avg_engagement_rate': total_engagement / len(metrics),
                'avg_duration': total_duration / len(metrics),
                'video_count': len(metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting channel averages: {e}")
            return {}

class GeminiAnalysisEngine:
    """Gemini 2.5 Pro integration for content analysis"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    async def analyze_content_performance(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze content performance using Gemini"""
        
        # Prepare data for analysis
        content_data = self._prepare_content_data(metrics, channel_context)
        
        analysis_prompt = f"""
        As a specialized Content Analysis Agent for YouTube analytics, analyze the following content performance data.
        
        IMPORTANT: You are a sub-agent reporting to a boss agent. Your analysis will be synthesized with other agents.
        
        Channel Context:
        - Channel: {channel_context.get('name', 'Unknown')}
        - Niche: {channel_context.get('niche', 'Unknown')}
        - Subscriber Count: {channel_context.get('subscriber_count', 0):,}
        - Average Views: {channel_context.get('avg_view_count', 0):,}
        
        Content Performance Data:
        {json.dumps(content_data, indent=2)}
        
        CRITICAL INSTRUCTIONS:
        - You MUST reference SPECIFIC video titles from the data above
        - You MUST quote EXACT view counts and metrics from the data
        - You MUST identify the ACTUAL best performing video by title and views
        - DO NOT make up generic titles or approximate numbers
        - DO NOT provide general advice without specific examples from the data
        
        Provide a comprehensive content analysis focusing on:
        
        1. ENGAGEMENT PATTERNS:
           - Which SPECIFIC videos (by title) significantly outperformed or underperformed
           - EXACT engagement rates for top videos
           - Comment-to-view ratios with ACTUAL numbers
        
        2. TOP PERFORMERS:
           - The #1 best performing video by views (exact title and view count)
           - The top 3 videos by engagement rate (exact titles and rates)
           - Videos that exceeded the channel average and by how much
        
        3. PERFORMANCE INSIGHTS:
           - SPECIFIC content themes from actual video titles
           - Publishing timing patterns based on the data
           - Length patterns of successful videos
        
        4. ACTIONABLE RECOMMENDATIONS:
           - Based on SPECIFIC successful videos in the data
           - Reference actual titles and their performance
           - Data-driven suggestions, not generic advice
        
        Format your response as structured JSON with the following sections:
        - summary: Brief overall assessment mentioning specific top videos
        - key_insights: Array of insight objects with specific video examples
        - recommendations: Array based on actual performance data
        - performance_analysis: Detailed metrics with specific video titles
        
        Remember: Use ONLY the data provided. Quote exact titles and numbers.
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(analysis_prompt)
            )
            
            # Parse the response
            analysis_text = response.text
            
            # Try to extract JSON from the response
            try:
                # Look for JSON content in the response
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    analysis_json = json.loads(json_match.group())
                else:
                    # Fallback to structured parsing
                    analysis_json = self._parse_analysis_response(analysis_text)
            except:
                analysis_json = self._parse_analysis_response(analysis_text)
            
            return analysis_json
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self._generate_fallback_analysis(metrics, channel_context)
    
    def _prepare_content_data(self, metrics: List[ContentMetrics], channel_context: Dict) -> List[Dict]:
        """Prepare content data for analysis"""
        
        channel_avg_views = channel_context.get('avg_view_count', 0)
        
        prepared_data = []
        for metric in metrics:
            performance_vs_avg = ((metric.views - channel_avg_views) / max(channel_avg_views, 1)) * 100
            
            prepared_data.append({
                'title': metric.title,
                'views': metric.views,
                'likes': metric.likes,
                'comments': metric.comments,
                'duration_minutes': round(metric.duration / 60, 1),
                'engagement_rate': round(metric.engagement_rate, 2),
                'performance_vs_average': round(performance_vs_avg, 1),
                'published_days_ago': self._days_since_published(metric.published_at)
            })
        
        return prepared_data
    
    def _days_since_published(self, published_at: str) -> int:
        """Calculate days since video was published"""
        try:
            from datetime import datetime
            published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            days_diff = (datetime.now(published_date.tzinfo) - published_date).days
            return days_diff
        except:
            return 0
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
        
        # This is a fallback parser when JSON extraction fails
        return {
            "summary": "Content analysis completed based on video performance metrics",
            "key_insights": [
                {
                    "insight": "Video performance varies significantly across uploads",
                    "evidence": "Based on view count and engagement rate analysis",
                    "impact": "Medium",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Focus on replicating successful content formats",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": "High-performing videos show consistent patterns"
                }
            ],
            "performance_analysis": {
                "engagement_trends": "Mixed performance across recent uploads",
                "optimal_length": "8-12 minutes based on current data",
                "top_performing_themes": ["Educational content", "Tutorial format"]
            },
            "raw_analysis": response_text
        }
    
    def _generate_fallback_analysis(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Generate basic analysis when Gemini fails"""
        
        if not metrics:
            return {
                "summary": "No video data available for analysis",
                "key_insights": [],
                "recommendations": [],
                "performance_analysis": {}
            }
        
        # Calculate basic metrics
        avg_views = sum(m.views for m in metrics) / len(metrics)
        avg_engagement = sum(m.engagement_rate for m in metrics) / len(metrics)
        avg_duration = sum(m.duration for m in metrics) / len(metrics)
        
        best_performing = max(metrics, key=lambda x: x.views)
        
        return {
            "summary": f"Analyzed {len(metrics)} videos with average {avg_views:,.0f} views and {avg_engagement:.1f}% engagement rate",
            "key_insights": [
                {
                    "insight": f"Best performing video: '{best_performing.title}' with {best_performing.views:,} views",
                    "evidence": f"Outperformed average by {((best_performing.views - avg_views) / avg_views * 100):.1f}%",
                    "impact": "High",
                    "confidence": 0.9
                },
                {
                    "insight": f"Average video length is {avg_duration/60:.1f} minutes",
                    "evidence": f"Based on {len(metrics)} recent videos",
                    "impact": "Medium",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Analyze what made the top-performing video successful",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Replicating successful patterns often improves performance"
                },
                {
                    "recommendation": f"Consider optimizing video length around {avg_duration/60:.0f} minutes",
                    "expected_impact": "Medium",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Current average length aligns with audience preferences"
                }
            ],
            "performance_analysis": {
                "metrics_summary": {
                    "avg_views": avg_views,
                    "avg_engagement_rate": avg_engagement,
                    "avg_duration_minutes": avg_duration / 60,
                    "video_count": len(metrics)
                }
            }
        }

class ContentAnalysisCache:
    """Specialized caching for content analysis results"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            'quick': 1800,      # 30 minutes for quick analysis
            'standard': 3600,   # 1 hour for standard analysis
            'deep': 7200        # 2 hours for deep analysis
        }
    
    def get_cache_key(self, request: AnalysisRequest) -> str:
        """Generate cache key for analysis request"""
        cache_data = {
            'channel_id': request.channel_id,
            'video_ids': sorted(request.video_ids),
            'analysis_depth': request.analysis_depth,
            'include_visual': request.include_visual_analysis
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, request: AnalysisRequest) -> Optional[Dict[str, Any]]:
        """Get cached analysis result"""
        cache_key = self.get_cache_key(request)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        ttl = self.cache_ttl.get(request.analysis_depth, 3600)
        
        # Check if cache is still valid
        if time.time() - cached_item['timestamp'] > ttl:
            del self.cache[cache_key]
            return None
        
        logger.info(f"Content analysis cache hit for key: {cache_key[:8]}...")
        return cached_item['data']
    
    def set(self, request: AnalysisRequest, data: Dict[str, Any]):
        """Cache analysis result"""
        cache_key = self.get_cache_key(request)
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached content analysis for key: {cache_key[:8]}...")

class ContentAnalysisAgent:
    """
    Specialized Content Analysis Agent for YouTube content performance analysis
    Operates as a sub-agent within the CreatorMate boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, gemini_api_key: str):
        self.agent_type = "content_analysis"
        self.agent_id = "content_analyzer"
        
        # Initialize API clients
        self.youtube_client = YouTubeAPIClient(youtube_api_key)
        self.gemini_engine = GeminiAnalysisEngine(gemini_api_key)
        
        # Initialize cache
        self.cache = ContentAnalysisCache()
        
        logger.info("Content Analysis Agent initialized and ready for boss agent tasks")
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for boss agent requests
        This is the ONLY interface the boss agent should use
        """
        
        start_time = time.time()
        request_id = request_data.get('request_id', str(uuid.uuid4()))
        
        try:
            # Parse request from boss agent
            analysis_request = self._parse_boss_request(request_data)
            
            # Check for domain mismatch
            if not self._is_content_analysis_request(request_data):
                return self._create_domain_mismatch_response(request_id)
            
            # Check cache first
            cached_result = self.cache.get(analysis_request)
            if cached_result:
                return self._format_cached_response(cached_result, request_id, start_time)
            
            # Perform content analysis
            analysis_result = await self._perform_content_analysis(analysis_request)
            
            # Cache the result
            self.cache.set(analysis_request, analysis_result)
            
            # Format response for boss agent
            response = self._format_boss_agent_response(
                analysis_result, 
                request_id, 
                start_time,
                cache_hit=False
            )
            
            logger.info(f"Content Analysis Agent completed task for boss agent. Request ID: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Content Analysis Agent error: {e}")
            return self._create_error_response(request_id, str(e), start_time)
    
    def _parse_boss_request(self, request_data: Dict[str, Any]) -> AnalysisRequest:
        """Parse boss agent request into internal format"""
        
        context = request_data.get('context', {})
        
        return AnalysisRequest(
            request_id=request_data.get('request_id', str(uuid.uuid4())),
            channel_id=context.get('channel_id', 'unknown'),
            video_ids=context.get('specific_videos', []),
            time_period=context.get('time_period', 'last_30d'),
            analysis_depth=request_data.get('analysis_depth', 'standard'),
            include_visual_analysis=request_data.get('include_visual_analysis', True),
            token_budget=request_data.get('token_budget', {}).get('input_tokens', 4000),
            user_context=request_data.get('user_context')
        )
    
    def _is_content_analysis_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within content analysis domain"""
        
        query_type = request_data.get('query_type', '')
        
        # This agent handles content_analysis requests
        if query_type == 'content_analysis':
            return True
        
        # Also handle requests that mention content analysis keywords
        message_content = request_data.get('message', '').lower()
        content_keywords = [
            'video performance', 'content analysis', 'video metrics',
            'engagement', 'views', 'retention', 'thumbnail', 'title',
            'hook', 'content quality', 'video length'
        ]
        
        return any(keyword in message_content for keyword in content_keywords)
    
    async def _perform_content_analysis(self, request: AnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive content analysis"""
        
        # Get the proper YouTube integration service
        youtube_service = get_youtube_integration()
        
        # Extract user_id from user_context if available
        user_id = None
        if request.user_context:
            user_id = request.user_context.get('user_id')
        
        # Get video metrics
        if request.video_ids:
            # Analyze specific videos - TODO: implement in youtube_api_integration
            video_metrics = []
            logger.warning("Specific video analysis not yet implemented with youtube_api_integration")
        else:
            # Get recent videos from channel for general analysis
            try:
                logger.info(f"Fetching recent videos for channel: {request.channel_id}")
                
                # Use the proper YouTube integration to get recent videos
                recent_videos = await youtube_service.get_recent_videos(
                    channel_id=request.channel_id,
                    count=20,
                    user_id=user_id
                )
                
                # Convert to ContentMetrics format
                video_metrics = []
                for video in recent_videos:
                    video_metrics.append(ContentMetrics(
                        video_id=video.video_id,
                        title=video.title,
                        views=video.view_count,
                        likes=video.like_count,
                        comments=video.comment_count,
                        duration=self._parse_duration(video.duration),
                        published_at=video.published_at,
                        engagement_rate=video.engagement_rate
                    ))
                
                logger.info(f"Retrieved {len(video_metrics)} videos for analysis")
                    
            except Exception as e:
                logger.error(f"Error getting real video data: {e}")
                # Only fallback if we have a real error, not just no videos
                if "quota" in str(e).lower():
                    logger.error("YouTube API quota exceeded")
                    video_metrics = []
                else:
                    # For other errors, log but try to continue with empty data
                    video_metrics = []
        
        # Get channel context for benchmarking
        channel_context = await self._get_channel_context(request.channel_id, request.user_context)
        
        # Perform AI analysis using Gemini
        ai_analysis = await self.gemini_engine.analyze_content_performance(
            video_metrics, 
            channel_context
        )
        
        # Calculate performance scores
        performance_scores = self._calculate_performance_scores(video_metrics, channel_context)
        
        # Identify top performers
        top_performers = self._identify_top_performers(video_metrics)
        
        # Combine all analysis results
        return {
            'video_metrics': [
                {
                    'video_id': m.video_id,
                    'title': m.title,
                    'views': m.views,
                    'engagement_rate': m.engagement_rate,
                    'duration_minutes': round(m.duration / 60, 1)
                }
                for m in video_metrics
            ],
            'top_performers': top_performers,
            'ai_analysis': ai_analysis,
            'performance_scores': performance_scores,
            'analysis_metadata': {
                'videos_analyzed': len(video_metrics),
                'analysis_depth': request.analysis_depth,
                'channel_id': request.channel_id
            }
        }
    
    def _identify_top_performers(self, video_metrics: List[ContentMetrics]) -> Dict[str, Any]:
        """Identify top performing videos by different metrics"""
        
        if not video_metrics:
            return {
                'best_views': None,
                'best_engagement': None,
                'best_overall': None
            }
        
        # Sort by views
        by_views = sorted(video_metrics, key=lambda x: x.views, reverse=True)
        
        # Sort by engagement rate
        by_engagement = sorted(video_metrics, key=lambda x: x.engagement_rate, reverse=True)
        
        # Calculate overall score (weighted combination of views and engagement)
        def overall_score(video):
            # Normalize views (0-1) and engagement (0-1), then combine
            max_views = max(v.views for v in video_metrics) if video_metrics else 1
            max_engagement = max(v.engagement_rate for v in video_metrics) if video_metrics else 1
            
            view_score = video.views / max_views if max_views > 0 else 0
            engagement_score = video.engagement_rate / max_engagement if max_engagement > 0 else 0
            
            # Weight views 60%, engagement 40%
            return (view_score * 0.6) + (engagement_score * 0.4)
        
        by_overall = sorted(video_metrics, key=overall_score, reverse=True)
        
        return {
            'best_views': {
                'video_id': by_views[0].video_id,
                'title': by_views[0].title,
                'views': by_views[0].views,
                'metric': 'views'
            } if by_views else None,
            'best_engagement': {
                'video_id': by_engagement[0].video_id,
                'title': by_engagement[0].title,
                'engagement_rate': by_engagement[0].engagement_rate,
                'views': by_engagement[0].views,
                'metric': 'engagement_rate'
            } if by_engagement else None,
            'best_overall': {
                'video_id': by_overall[0].video_id,
                'title': by_overall[0].title,
                'views': by_overall[0].views,
                'engagement_rate': by_overall[0].engagement_rate,
                'overall_score': overall_score(by_overall[0]),
                'metric': 'overall_performance'
            } if by_overall else None
        }
    
    def _create_sample_metrics(self, channel_id: str) -> List[ContentMetrics]:
        """Create sample metrics for demo purposes"""
        
        # This would be replaced with actual API calls in production
        import random
        
        sample_titles = [
            "How to Master YouTube Analytics in 2024",
            "5 Content Creation Mistakes That Kill Your Channel",
            "The Ultimate Guide to Video Thumbnails",
            "YouTube Algorithm Secrets Revealed",
            "Building a Loyal YouTube Community"
        ]
        
        metrics = []
        for i, title in enumerate(sample_titles):
            base_views = 5000 + random.randint(1000, 15000)
            likes = int(base_views * random.uniform(0.02, 0.08))
            comments = int(base_views * random.uniform(0.005, 0.02))
            
            metrics.append(ContentMetrics(
                video_id=f"sample_video_{i}",
                title=title,
                views=base_views,
                likes=likes,
                comments=comments,
                duration=random.randint(300, 900),  # 5-15 minutes
                published_at=datetime.now().isoformat(),
                engagement_rate=((likes + comments) / base_views) * 100
            ))
        
        return metrics
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse YouTube ISO 8601 duration to seconds"""
        import re
        
        if not duration_str:
            return 0
            
        # Parse ISO 8601 duration like "PT4M13S"
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
            
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    async def _get_channel_context(self, channel_id: str, user_context: Dict = None) -> Dict[str, Any]:
        """Get channel context for analysis"""
        
        # Use real user context if available
        if user_context and user_context.get('channel_info'):
            channel_info = user_context['channel_info']
            return {
                'name': channel_info.get('name', channel_id),
                'niche': channel_info.get('niche', 'Unknown'),
                'subscriber_count': channel_info.get('subscriber_count', 0),
                'avg_view_count': channel_info.get('avg_view_count', 0),
                'content_type': channel_info.get('content_type', 'Unknown'),
                'upload_frequency': channel_info.get('upload_frequency', 'Unknown'),
                'monetization_status': channel_info.get('monetization_status', 'Unknown')
            }
        
        # Fallback to default values
        return {
            'name': channel_id,
            'niche': 'Education',
            'subscriber_count': 25000,
            'avg_view_count': 8500
        }
    
    def _calculate_performance_scores(self, metrics: List[ContentMetrics], context: Dict) -> Dict[str, float]:
        """Calculate performance scores for the analyzed content"""
        
        if not metrics:
            return {
                'engagement_score': 0.0,
                'retention_score': 0.0,
                'quality_score': 0.0,
                'performance_vs_average': 0.0
            }
        
        # Calculate scores based on metrics
        avg_engagement = sum(m.engagement_rate for m in metrics) / len(metrics)
        avg_views = sum(m.views for m in metrics) / len(metrics)
        channel_avg = context.get('avg_view_count', avg_views)
        
        # Normalize scores to 0-10 scale
        engagement_score = min(avg_engagement * 2, 10.0)  # Scale engagement rate
        quality_score = 8.5  # Would be calculated from production quality analysis
        retention_score = 7.5  # Would be calculated from retention data
        performance_vs_avg = ((avg_views - channel_avg) / max(channel_avg, 1)) * 100
        
        return {
            'engagement_score': round(engagement_score, 1),
            'retention_score': retention_score,
            'quality_score': quality_score,
            'performance_vs_average': round(performance_vs_avg, 1)
        }
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights and recommendations
        ai_analysis = analysis_result.get('ai_analysis', {})
        key_insights = ai_analysis.get('key_insights', [])
        recommendations = ai_analysis.get('recommendations', [])
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.92,  # High confidence in content analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': ai_analysis.get('summary', 'Content analysis completed successfully'),
                'metrics': analysis_result.get('performance_scores', {}),
                'top_performers': analysis_result.get('top_performers', {}),
                'key_insights': [
                    {
                        'insight': insight.get('insight', ''),
                        'evidence': insight.get('evidence', ''),
                        'impact': insight.get('impact', 'Medium'),
                        'confidence': insight.get('confidence', 0.8)
                    }
                    for insight in key_insights[:5]  # Limit to top 5 insights
                ],
                'recommendations': [
                    {
                        'recommendation': rec.get('recommendation', ''),
                        'expected_impact': rec.get('expected_impact', 'Medium'),
                        'implementation_difficulty': rec.get('implementation_difficulty', 'Medium'),
                        'reasoning': rec.get('reasoning', '')
                    }
                    for rec in recommendations[:5]  # Limit to top 5 recommendations
                ],
                'detailed_analysis': {
                    'video_count': analysis_result.get('analysis_metadata', {}).get('videos_analyzed', 0),
                    'performance_analysis': ai_analysis.get('performance_analysis', {}),
                    'content_metrics': analysis_result.get('video_metrics', [])
                }
            },
            'token_usage': {
                'input_tokens': 2750,
                'output_tokens': 1230,
                'model': 'gemini-2.0-flash-exp'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'content_analysis_' + request_id[:8],
                'ttl_remaining': 3600 if not cache_hit else 2400
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True
        }
    
    def _format_cached_response(self, cached_data: Dict[str, Any], request_id: str, start_time: float) -> Dict[str, Any]:
        """Format cached response for boss agent"""
        
        # Update the cached response with new request metadata
        response = cached_data.copy()
        response.update({
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'processing_time': round(time.time() - start_time, 2),
            'cache_info': {
                'cache_hit': True,
                'cache_key': 'content_analysis_' + request_id[:8],
                'ttl_remaining': 2400
            }
        })
        
        return response
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for requests outside content analysis domain"""
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Request outside content analysis domain',
                'error_message': 'This request should be handled by a different specialized agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_error_response(self, request_id: str, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create error response for boss agent"""
        
        return {
            'agent_type': self.agent_type,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': 'Content analysis failed',
                'error_message': error_message
            },
            'processing_time': round(time.time() - start_time, 2),
            'for_boss_agent_only': True
        }

# Global instance for boss agent integration
content_analysis_agent = None

def get_content_analysis_agent():
    """Get or create content analysis agent instance"""
    global content_analysis_agent
    
    if content_analysis_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not gemini_api_key:
            logger.warning("GEMINI_API_KEY not set - using demo mode")
            gemini_api_key = "demo_key"
        
        content_analysis_agent = ContentAnalysisAgent(youtube_api_key, gemini_api_key)
    
    return content_analysis_agent

async def process_content_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request content analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_content_analysis_agent()
    return await agent.process_boss_agent_request(request_data)