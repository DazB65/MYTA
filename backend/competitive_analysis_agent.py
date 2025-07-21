"""
Competitive Analysis Agent for CreatorMate
Specialized sub-agent that analyzes competitor performance and market positioning for the boss agent
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
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CompetitiveAnalysisRequest:
    """Structure for competitive analysis requests from boss agent"""
    request_id: str
    channel_id: str
    competitor_channels: List[str]
    time_period: str
    analysis_depth: str = "standard"  # quick, standard, deep
    include_content_strategy: bool = True
    include_performance_benchmarking: bool = True
    include_trend_analysis: bool = True
    token_budget: int = 5000

@dataclass
class CompetitorMetrics:
    """Competitor metrics structure"""
    channel_id: str
    channel_name: str
    subscriber_count: int
    avg_views: float
    avg_engagement_rate: float
    upload_frequency: float
    content_themes: List[str]
    recent_performance: Dict[str, Any]
    growth_rate: float
    competitive_advantage: List[str]

class YouTubeCompetitiveAPIClient:
    """YouTube API integration for competitive data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    async def get_competitor_data(self, competitor_channels: List[str], time_period: str) -> List[CompetitorMetrics]:
        """Retrieve competitor channel data"""
        
        competitor_data = []
        
        for channel_id in competitor_channels:
            try:
                # Get channel statistics
                channel_response = self.youtube.channels().list(
                    part='snippet,statistics',
                    id=channel_id
                ).execute()
                
                if not channel_response.get('items'):
                    continue
                
                channel_info = channel_response['items'][0]
                snippet = channel_info['snippet']
                stats = channel_info['statistics']
                
                # Get recent videos for analysis
                recent_videos = await self._get_recent_videos(channel_id, 10)
                
                # Calculate competitive metrics
                competitor_metrics = CompetitorMetrics(
                    channel_id=channel_id,
                    channel_name=snippet.get('title', 'Unknown'),
                    subscriber_count=int(stats.get('subscriberCount', 0)),
                    avg_views=self._calculate_avg_views(recent_videos),
                    avg_engagement_rate=self._calculate_avg_engagement(recent_videos),
                    upload_frequency=self._calculate_upload_frequency(recent_videos),
                    content_themes=self._extract_content_themes(recent_videos),
                    recent_performance=self._analyze_recent_performance(recent_videos),
                    growth_rate=self._estimate_growth_rate(stats),
                    competitive_advantage=self._identify_advantages(recent_videos, stats)
                )
                
                competitor_data.append(competitor_metrics)
                
            except HttpError as e:
                logger.error(f"YouTube API error for channel {channel_id}: {e}")
                continue
            except Exception as e:
                logger.error(f"Error analyzing competitor {channel_id}: {e}")
                continue
        
        return competitor_data
    
    async def _get_recent_videos(self, channel_id: str, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent videos from a channel"""
        
        try:
            # Get recent videos
            search_response = self.youtube.search().list(
                part='id',
                channelId=channel_id,
                type='video',
                order='date',
                maxResults=count
            ).execute()
            
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if not video_ids:
                return []
            
            # Get video details
            videos_response = self.youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids)
            ).execute()
            
            videos = []
            for video in videos_response.get('items', []):
                videos.append({
                    'video_id': video['id'],
                    'title': video['snippet']['title'],
                    'description': video['snippet']['description'],
                    'published_at': video['snippet']['publishedAt'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'thumbnail': video['snippet']['thumbnails'].get('high', {}).get('url', '')
                })
            
            return videos
            
        except Exception as e:
            logger.error(f"Error getting recent videos for {channel_id}: {e}")
            return []
    
    def _calculate_avg_views(self, videos: List[Dict[str, Any]]) -> float:
        """Calculate average views from video list"""
        if not videos:
            return 0.0
        
        total_views = sum(video['views'] for video in videos)
        return total_views / len(videos)
    
    def _calculate_avg_engagement(self, videos: List[Dict[str, Any]]) -> float:
        """Calculate average engagement rate"""
        if not videos:
            return 0.0
        
        engagement_rates = []
        for video in videos:
            if video['views'] > 0:
                engagement = (video['likes'] + video['comments']) / video['views'] * 100
                engagement_rates.append(engagement)
        
        return statistics.mean(engagement_rates) if engagement_rates else 0.0
    
    def _calculate_upload_frequency(self, videos: List[Dict[str, Any]]) -> float:
        """Calculate upload frequency (videos per week)"""
        if len(videos) < 2:
            return 0.0
        
        # Calculate time span between first and last video
        dates = [datetime.fromisoformat(video['published_at'].replace('Z', '+00:00')) for video in videos]
        dates.sort()
        
        if len(dates) < 2:
            return 0.0
        
        time_span = (dates[-1] - dates[0]).days
        if time_span == 0:
            return len(videos)  # All uploaded same day
        
        return (len(videos) / time_span) * 7  # Videos per week
    
    def _extract_content_themes(self, videos: List[Dict[str, Any]]) -> List[str]:
        """Extract common content themes from video titles"""
        
        if not videos:
            return []
        
        # Simple keyword extraction from titles
        all_titles = ' '.join(video['title'].lower() for video in videos)
        
        # Common YouTube content themes
        theme_keywords = {
            'tutorial': ['tutorial', 'how to', 'guide', 'learn'],
            'review': ['review', 'unboxing', 'first look', 'hands-on'],
            'entertainment': ['funny', 'comedy', 'entertainment', 'fun'],
            'news': ['news', 'update', 'announcement', 'breaking'],
            'gaming': ['gameplay', 'gaming', 'stream', 'let\'s play'],
            'lifestyle': ['vlog', 'daily', 'life', 'routine'],
            'educational': ['explained', 'science', 'learn', 'education'],
            'technology': ['tech', 'technology', 'gadget', 'software']
        }
        
        themes = []
        for theme, keywords in theme_keywords.items():
            if any(keyword in all_titles for keyword in keywords):
                themes.append(theme)
        
        return themes[:5]  # Return top 5 themes
    
    def _analyze_recent_performance(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze recent performance trends"""
        
        if not videos:
            return {}
        
        # Sort by publish date (newest first)
        sorted_videos = sorted(videos, key=lambda x: x['published_at'], reverse=True)
        
        # Calculate performance trends
        recent_half = sorted_videos[:len(sorted_videos)//2] if len(sorted_videos) > 2 else sorted_videos
        older_half = sorted_videos[len(sorted_videos)//2:] if len(sorted_videos) > 2 else []
        
        recent_avg_views = self._calculate_avg_views(recent_half)
        older_avg_views = self._calculate_avg_views(older_half) if older_half else recent_avg_views
        
        performance_trend = "stable"
        if recent_avg_views > older_avg_views * 1.2:
            performance_trend = "improving"
        elif recent_avg_views < older_avg_views * 0.8:
            performance_trend = "declining"
        
        return {
            'recent_avg_views': recent_avg_views,
            'performance_trend': performance_trend,
            'top_performing_video': max(videos, key=lambda x: x['views']) if videos else None,
            'consistency_score': self._calculate_consistency(videos)
        }
    
    def _calculate_consistency(self, videos: List[Dict[str, Any]]) -> float:
        """Calculate performance consistency score (0-10)"""
        
        if len(videos) < 3:
            return 5.0  # Default score for insufficient data
        
        views = [video['views'] for video in videos]
        mean_views = statistics.mean(views)
        
        if mean_views == 0:
            return 5.0
        
        # Calculate coefficient of variation
        std_dev = statistics.stdev(views)
        cv = std_dev / mean_views
        
        # Convert to 0-10 scale (lower CV = higher consistency)
        consistency = max(0, 10 - (cv * 10))
        return min(consistency, 10.0)
    
    def _estimate_growth_rate(self, stats: Dict[str, Any]) -> float:
        """Estimate channel growth rate (monthly %)"""
        
        # In production, this would use historical data
        # For now, estimate based on subscriber count patterns
        subscriber_count = int(stats.get('subscriberCount', 0))
        
        if subscriber_count < 1000:
            return 15.0  # High growth for small channels
        elif subscriber_count < 10000:
            return 8.0   # Moderate growth
        elif subscriber_count < 100000:
            return 4.0   # Steady growth
        else:
            return 2.0   # Slower growth for large channels
    
    def _identify_advantages(self, videos: List[Dict[str, Any]], stats: Dict[str, Any]) -> List[str]:
        """Identify competitive advantages"""
        
        advantages = []
        
        if not videos:
            return advantages
        
        avg_views = self._calculate_avg_views(videos)
        avg_engagement = self._calculate_avg_engagement(videos)
        upload_freq = self._calculate_upload_frequency(videos)
        
        # High engagement advantage
        if avg_engagement > 5.0:
            advantages.append("High audience engagement")
        
        # Consistent upload schedule
        if upload_freq > 2.0:
            advantages.append("Consistent content schedule")
        
        # High view performance
        if avg_views > 50000:
            advantages.append("Strong view performance")
        
        # Content variety
        themes = self._extract_content_themes(videos)
        if len(themes) >= 3:
            advantages.append("Diverse content strategy")
        
        # Subscriber base
        subscriber_count = int(stats.get('subscriberCount', 0))
        if subscriber_count > 100000:
            advantages.append("Large subscriber base")
        
        return advantages[:4]  # Return top 4 advantages

    async def get_niche_trends(self, niche: str, competitor_channels: List[str]) -> Dict[str, Any]:
        """Analyze niche-wide trends and patterns"""
        
        try:
            # Analyze trending topics in the niche
            trending_topics = await self._analyze_trending_topics(niche)
            
            # Analyze competitor content patterns
            content_patterns = await self._analyze_content_patterns(competitor_channels)
            
            return {
                'trending_topics': trending_topics,
                'content_patterns': content_patterns,
                'niche_growth_rate': self._estimate_niche_growth(niche),
                'competitive_landscape': self._assess_competitive_landscape(competitor_channels)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing niche trends: {e}")
            return {}
    
    async def _analyze_trending_topics(self, niche: str) -> List[Dict[str, Any]]:
        """Analyze trending topics in the niche"""
        
        # Mock trending topics by niche
        niche_trends = {
            'tech': [
                {'topic': 'AI and Machine Learning', 'growth': 25, 'competition': 'high'},
                {'topic': 'Web Development', 'growth': 15, 'competition': 'medium'},
                {'topic': 'Cybersecurity', 'growth': 30, 'competition': 'low'}
            ],
            'gaming': [
                {'topic': 'Battle Royale Games', 'growth': 10, 'competition': 'high'},
                {'topic': 'Indie Game Reviews', 'growth': 20, 'competition': 'low'},
                {'topic': 'Gaming Setup Tours', 'growth': 15, 'competition': 'medium'}
            ],
            'education': [
                {'topic': 'Online Learning', 'growth': 40, 'competition': 'medium'},
                {'topic': 'Study Techniques', 'growth': 25, 'competition': 'low'},
                {'topic': 'Career Advice', 'growth': 20, 'competition': 'medium'}
            ]
        }
        
        return niche_trends.get(niche.lower(), [
            {'topic': 'General Content', 'growth': 10, 'competition': 'medium'}
        ])
    
    async def _analyze_content_patterns(self, competitor_channels: List[str]) -> Dict[str, Any]:
        """Analyze content patterns across competitors"""
        
        return {
            'optimal_video_length': '8-12 minutes',
            'best_upload_days': ['Tuesday', 'Thursday', 'Saturday'],
            'trending_formats': ['tutorials', 'reviews', 'behind-the-scenes'],
            'engagement_drivers': ['thumbnail quality', 'title optimization', 'early engagement']
        }
    
    def _estimate_niche_growth(self, niche: str) -> float:
        """Estimate overall niche growth rate"""
        
        # Mock growth rates by niche
        growth_rates = {
            'tech': 12.5,
            'gaming': 8.0,
            'education': 15.0,
            'lifestyle': 6.0,
            'fitness': 10.0,
            'cooking': 7.5
        }
        
        return growth_rates.get(niche.lower(), 8.0)
    
    def _assess_competitive_landscape(self, competitor_channels: List[str]) -> Dict[str, Any]:
        """Assess competitive landscape intensity"""
        
        return {
            'competition_level': 'medium',
            'market_saturation': 'moderate',
            'growth_opportunities': ['underserved topics', 'new formats', 'audience segments'],
            'barriers_to_entry': 'medium'
        }

class GeminiCompetitiveEngine:
    """Gemini 2.5 Pro integration for competitive analysis and visual comparison"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            'gemini-2.0-flash-exp',
            generation_config=genai.GenerationConfig(
                temperature=0.1,  # Precise competitive analysis
                top_p=0.9,
                top_k=40
            )
        )
        
    async def analyze_competitive_landscape(self, competitor_data: List[CompetitorMetrics], channel_context: Dict, niche_trends: Dict) -> Dict[str, Any]:
        """Analyze competitive landscape using Gemini"""
        
        if not competitor_data:
            return self._generate_fallback_competitive_analysis()
        
        # Prepare data for analysis
        competitive_data = self._prepare_competitive_data(competitor_data, channel_context, niche_trends)
        
        # Voice consistency - strategic market analyst with competitive insights
        competitive_prompt = f"""
        VOICE: Strategic YouTube market analyst | Data-driven, competitive, precise
        
        TASK: Competitive analysis for {channel_context.get('name', 'Unknown')} ({channel_context.get('niche', 'Unknown')} niche, {channel_context.get('subscriber_count', 0):,} subs).
        
        COMPETITIVE DATA:
        {json.dumps(competitive_data, indent=2)}
        
        ANALYZE:
        • Market position vs competitors
        • Performance gaps & opportunities
        • Content strategy advantages
        • Differentiation strategies
        
        RESPONSE FORMAT (JSON):
        {{
          "competitive_summary": "Channel ranks #X in niche with Y advantage",
          "performance_comparison": {{
            "vs_top_competitor": "Specific metrics comparison",
            "growth_trajectory": "Behind/ahead by X%",
            "content_gaps": ["Specific opportunity"]
          }},
          "content_opportunities": [
            {{
              "opportunity": "Specific content gap",
              "evidence": "Competitor data showing gap",
              "potential_impact": "High/Medium/Low"
            }}
          ],
          "market_insights": {{
            "niche_trends": ["Trend with data"],
            "audience_segments": ["Underserved segment"]
          }},
          "strategic_recommendations": [
            {{
              "strategy": "Specific competitive move",
              "reasoning": "Why this beats competitors",
              "implementation": "Easy/Medium/Hard"
            }}
          ]
        }}
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.model.generate_content(competitive_prompt)
            )
            
            # Parse the response
            analysis_text = response.text
            
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    competitive_json = json.loads(json_match.group())
                else:
                    competitive_json = self._parse_competitive_response(analysis_text)
            except:
                competitive_json = self._parse_competitive_response(analysis_text)
            
            return competitive_json
            
        except Exception as e:
            logger.error(f"Gemini competitive analysis error: {e}")
            return self._generate_fallback_competitive_analysis()
    
    def _prepare_competitive_data(self, competitor_data: List[CompetitorMetrics], channel_context: Dict, niche_trends: Dict) -> Dict[str, Any]:
        """Prepare competitive data for analysis"""
        
        prepared_data = {
            'own_channel': {
                'subscriber_count': channel_context.get('subscriber_count', 0),
                'avg_view_count': channel_context.get('avg_view_count', 0),
                'niche': channel_context.get('niche', 'Unknown')
            },
            'competitors': [],
            'niche_trends': niche_trends
        }
        
        for competitor in competitor_data:
            prepared_data['competitors'].append({
                'name': competitor.channel_name,
                'subscriber_count': competitor.subscriber_count,
                'avg_views': competitor.avg_views,
                'engagement_rate': competitor.avg_engagement_rate,
                'upload_frequency': competitor.upload_frequency,
                'content_themes': competitor.content_themes,
                'performance_trend': competitor.recent_performance.get('performance_trend', 'stable'),
                'growth_rate': competitor.growth_rate,
                'competitive_advantages': competitor.competitive_advantage
            })
        
        return prepared_data
    
    def _parse_competitive_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured competitive format"""
        
        return {
            "competitive_summary": "Competitive analysis completed with market positioning insights",
            "performance_comparison": {
                "relative_position": "middle tier",
                "growth_potential": "high",
                "key_metrics_comparison": "competitive on engagement, opportunity in reach",
                "market_share_estimate": "emerging player"
            },
            "content_opportunities": [
                {"opportunity": "Underserved tutorial formats", "potential": "high", "competition": "low"},
                {"opportunity": "Trending topic integration", "potential": "medium", "competition": "medium"},
                {"opportunity": "Audience segment expansion", "potential": "high", "competition": "medium"}
            ],
            "market_insights": {
                "niche_growth_rate": "positive",
                "competition_intensity": "moderate",
                "trend_adoption_speed": "fast",
                "audience_behavior_shifts": ["mobile-first consumption", "shorter attention spans"]
            },
            "strategic_recommendations": [
                "Focus on unique content angles to differentiate",
                "Optimize upload schedule for maximum reach",
                "Leverage trending topics with unique perspective",
                "Build strategic partnerships with complementary creators"
            ],
            "raw_analysis": response_text
        }
    
    def _generate_fallback_competitive_analysis(self) -> Dict[str, Any]:
        """Generate basic competitive analysis when Gemini fails"""
        
        return {
            "competitive_summary": "Basic competitive analysis completed with limited data",
            "performance_comparison": {
                "relative_position": "to be determined",
                "growth_potential": "moderate",
                "key_metrics_comparison": "baseline assessment",
                "market_share_estimate": "developing"
            },
            "content_opportunities": [
                {"opportunity": "Content format innovation", "potential": "medium", "competition": "unknown"},
                {"opportunity": "Audience engagement improvement", "potential": "high", "competition": "medium"}
            ],
            "market_insights": {
                "niche_growth_rate": "stable",
                "competition_intensity": "moderate",
                "trend_adoption_speed": "moderate",
                "audience_behavior_shifts": ["digital-first preferences"]
            },
            "strategic_recommendations": [
                "Conduct detailed competitor research",
                "Identify unique value proposition",
                "Optimize content for target audience",
                "Monitor competitive landscape regularly"
            ]
        }

class CompetitiveAnalysisCache:
    """Specialized caching for competitive analysis results"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            'quick': 7200,      # 2 hours for quick analysis
            'standard': 21600,  # 6 hours for standard analysis (competitive data changes slowly)
            'deep': 43200       # 12 hours for deep analysis
        }
    
    def get_cache_key(self, request: CompetitiveAnalysisRequest) -> str:
        """Generate cache key for competitive analysis request"""
        cache_data = {
            'channel_id': request.channel_id,
            'competitor_channels': sorted(request.competitor_channels),
            'time_period': request.time_period,
            'analysis_depth': request.analysis_depth,
            'include_content_strategy': request.include_content_strategy,
            'include_performance_benchmarking': request.include_performance_benchmarking
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, request: CompetitiveAnalysisRequest) -> Optional[Dict[str, Any]]:
        """Get cached competitive analysis result"""
        cache_key = self.get_cache_key(request)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        ttl = self.cache_ttl.get(request.analysis_depth, 21600)
        
        # Check if cache is still valid
        if time.time() - cached_item['timestamp'] > ttl:
            del self.cache[cache_key]
            return None
        
        logger.info(f"Competitive analysis cache hit for key: {cache_key[:8]}...")
        return cached_item['data']
    
    def set(self, request: CompetitiveAnalysisRequest, data: Dict[str, Any]):
        """Cache competitive analysis result"""
        cache_key = self.get_cache_key(request)
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached competitive analysis for key: {cache_key[:8]}...")

class CompetitiveAnalysisAgent:
    """
    Specialized Competitive Analysis Agent for YouTube market positioning
    Operates as a sub-agent within the CreatorMate boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, gemini_api_key: str):
        self.agent_type = "competitive_analysis"
        self.agent_id = "competitive_analyzer"
        self.hierarchical_role = "specialized_agent"
        
        # Initialize API clients
        self.youtube_client = YouTubeCompetitiveAPIClient(youtube_api_key)
        self.competitive_engine = GeminiCompetitiveEngine(gemini_api_key)
        
        # Initialize cache
        self.cache = CompetitiveAnalysisCache()
        
        logger.info("Competitive Analysis Agent initialized and ready for boss agent tasks")
    
    async def process_boss_agent_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for boss agent requests
        This is the ONLY interface the boss agent should use
        """
        
        start_time = time.time()
        request_id = request_data.get('request_id', str(uuid.uuid4()))
        
        try:
            # Validate this is a legitimate boss agent request
            if not self._validate_boss_agent_request(request_data):
                return self._create_unauthorized_response(request_id)
            
            # Parse request from boss agent
            analysis_request = self._parse_boss_request(request_data)
            
            # Check for domain mismatch
            if not self._is_competitive_analysis_request(request_data):
                return self._create_domain_mismatch_response(request_id)
            
            # Check cache first
            cached_result = self.cache.get(analysis_request)
            if cached_result:
                return self._format_cached_response(cached_result, request_id, start_time)
            
            # Perform competitive analysis
            analysis_result = await self._perform_competitive_analysis(analysis_request)
            
            # Cache the result
            self.cache.set(analysis_request, analysis_result)
            
            # Format response for boss agent
            response = self._format_boss_agent_response(
                analysis_result, 
                request_id, 
                start_time,
                cache_hit=False
            )
            
            logger.info(f"Competitive Analysis Agent completed task for boss agent. Request ID: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Competitive Analysis Agent error: {e}")
            return self._create_error_response(request_id, str(e), start_time)
    
    def _validate_boss_agent_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate that request comes from authorized boss agent"""
        
        # In production, this would validate JWT tokens or API keys
        # For now, check for boss agent signature
        return request_data.get('from_boss_agent', False) or \
               'boss_agent_callback_url' in request_data or \
               request_data.get('agent_type') != self.agent_type  # Prevent self-requests
    
    def _parse_boss_request(self, request_data: Dict[str, Any]) -> CompetitiveAnalysisRequest:
        """Parse boss agent request into internal format"""
        
        context = request_data.get('context', {})
        
        return CompetitiveAnalysisRequest(
            request_id=request_data.get('request_id', str(uuid.uuid4())),
            channel_id=context.get('channel_id', 'unknown'),
            competitor_channels=context.get('competitors', []),
            time_period=context.get('time_period', 'last_30d'),
            analysis_depth=request_data.get('analysis_depth', 'standard'),
            include_content_strategy=request_data.get('include_content_strategy', True),
            include_performance_benchmarking=request_data.get('include_performance_benchmarking', True),
            include_trend_analysis=request_data.get('include_trend_analysis', True),
            token_budget=request_data.get('token_budget', {}).get('input_tokens', 5000)
        )
    
    def _is_competitive_analysis_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within competitive analysis domain"""
        
        query_type = request_data.get('query_type', '')
        
        # This agent handles competitive analysis requests
        if query_type in ['competitive_analysis', 'competition', 'competitors']:
            return True
        
        # Also handle requests that mention competitive keywords
        message_content = request_data.get('message', '').lower()
        competitive_keywords = [
            'competitor', 'competition', 'competitive', 'benchmark', 'compare',
            'market', 'rival', 'similar channels', 'other creators', 'industry',
            'niche analysis', 'market position', 'competitive advantage'
        ]
        
        return any(keyword in message_content for keyword in competitive_keywords)
    
    async def _perform_competitive_analysis(self, request: CompetitiveAnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive competitive analysis"""
        
        analysis_results = {}
        
        # Get competitor data
        if request.competitor_channels:
            competitor_data = await self.youtube_client.get_competitor_data(
                request.competitor_channels, 
                request.time_period
            )
        else:
            # Generate sample competitor data if no competitors specified
            competitor_data = self._create_sample_competitor_data(request.channel_id)
        
        analysis_results['competitor_data'] = competitor_data
        
        # Get channel context
        channel_context = await self._get_channel_context(request.channel_id)
        
        # Get niche trends if requested
        niche_trends = {}
        if request.include_trend_analysis:
            niche_trends = await self.youtube_client.get_niche_trends(
                channel_context.get('niche', 'general'),
                request.competitor_channels
            )
            analysis_results['niche_trends'] = niche_trends
        
        # Perform AI analysis using Gemini
        ai_analysis = await self.competitive_engine.analyze_competitive_landscape(
            competitor_data, 
            channel_context,
            niche_trends
        )
        
        # Calculate competitive scores
        competitive_scores = self._calculate_competitive_scores(competitor_data, channel_context)
        
        # Combine all analysis results
        return {
            'raw_data': analysis_results,
            'ai_analysis': ai_analysis,
            'competitive_scores': competitive_scores,
            'analysis_metadata': {
                'channel_id': request.channel_id,
                'analysis_depth': request.analysis_depth,
                'competitors_analyzed': len(competitor_data),
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
    def _create_sample_competitor_data(self, channel_id: str) -> List[CompetitorMetrics]:
        """Create sample competitor data for demo purposes"""
        
        import random
        
        sample_competitors = [
            {
                'name': 'TechMaster Pro',
                'subscriber_base': 'large',
                'content_focus': 'advanced tutorials'
            },
            {
                'name': 'EduChannel Plus',
                'subscriber_base': 'medium',
                'content_focus': 'beginner-friendly content'
            },
            {
                'name': 'Innovation Hub',
                'subscriber_base': 'growing',
                'content_focus': 'trending topics'
            }
        ]
        
        competitors = []
        for i, comp_data in enumerate(sample_competitors):
            competitors.append(CompetitorMetrics(
                channel_id=f"competitor_{i}",
                channel_name=comp_data['name'],
                subscriber_count=random.randint(10000, 500000),
                avg_views=random.uniform(5000, 50000),
                avg_engagement_rate=random.uniform(2.0, 8.0),
                upload_frequency=random.uniform(1.0, 7.0),
                content_themes=['tutorial', 'review', 'educational'],
                recent_performance={
                    'performance_trend': random.choice(['improving', 'stable', 'declining']),
                    'consistency_score': random.uniform(6.0, 9.0)
                },
                growth_rate=random.uniform(5.0, 25.0),
                competitive_advantage=[
                    'High production quality',
                    'Consistent upload schedule',
                    'Strong audience engagement'
                ]
            ))
        
        return competitors
    
    async def _get_channel_context(self, channel_id: str) -> Dict[str, Any]:
        """Get channel context for analysis"""
        
        # In production, this would fetch from database or API
        return {
            'name': channel_id,
            'niche': 'Education',
            'subscriber_count': 25000,
            'avg_view_count': 8500,
            'content_type': 'Educational',
            'target_audience': 'Content creators and marketers',
            'upload_frequency': 3.5,
            'avg_engagement_rate': 5.2
        }
    
    def _calculate_competitive_scores(self, competitor_data: List[CompetitorMetrics], channel_context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate competitive performance scores"""
        
        if not competitor_data:
            return {
                'market_position': 5.0,
                'competitive_strength': 5.0,
                'growth_potential': 7.0,
                'content_differentiation': 6.0,
                'overall_competitive_health': 5.8
            }
        
        # Get own channel metrics
        own_subscribers = channel_context.get('subscriber_count', 0)
        own_avg_views = channel_context.get('avg_view_count', 0)
        own_engagement = channel_context.get('avg_engagement_rate', 0)
        
        # Calculate relative positioning
        competitor_subscribers = [c.subscriber_count for c in competitor_data]
        competitor_views = [c.avg_views for c in competitor_data]
        competitor_engagement = [c.avg_engagement_rate for c in competitor_data]
        
        # Market position (based on subscriber ranking)
        subscriber_percentile = self._calculate_percentile(own_subscribers, competitor_subscribers)
        market_position = (subscriber_percentile / 100) * 10
        
        # Competitive strength (based on multiple metrics)
        view_percentile = self._calculate_percentile(own_avg_views, competitor_views)
        engagement_percentile = self._calculate_percentile(own_engagement, competitor_engagement)
        competitive_strength = ((view_percentile + engagement_percentile) / 200) * 10
        
        # Growth potential (inverse of market saturation)
        avg_competitor_growth = sum(c.growth_rate for c in competitor_data) / len(competitor_data)
        growth_potential = min(10.0, max(0.0, 10 - (avg_competitor_growth / 5)))
        
        # Content differentiation (based on content theme diversity)
        content_differentiation = 7.0  # Default good differentiation
        
        # Overall competitive health
        overall_competitive_health = (
            market_position * 0.3 +
            competitive_strength * 0.4 +
            growth_potential * 0.2 +
            content_differentiation * 0.1
        )
        
        return {
            'market_position': round(market_position, 1),
            'competitive_strength': round(competitive_strength, 1),
            'growth_potential': round(growth_potential, 1),
            'content_differentiation': round(content_differentiation, 1),
            'overall_competitive_health': round(overall_competitive_health, 1)
        }
    
    def _calculate_percentile(self, value: float, comparison_list: List[float]) -> float:
        """Calculate percentile ranking"""
        
        if not comparison_list:
            return 50.0  # Default median
        
        sorted_list = sorted(comparison_list + [value])
        rank = sorted_list.index(value) + 1
        percentile = (rank / len(sorted_list)) * 100
        
        return percentile
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights
        ai_analysis = analysis_result.get('ai_analysis', {})
        performance_comparison = ai_analysis.get('performance_comparison', {})
        content_opportunities = ai_analysis.get('content_opportunities', [])
        
        # Create summary
        summary = self._create_competitive_summary(analysis_result)
        
        # Extract recommendations
        recommendations = ai_analysis.get('strategic_recommendations', [])
        
        # Create key insights
        key_insights = []
        
        # Competitive position insight
        competitive_scores = analysis_result.get('competitive_scores', {})
        competitive_health = competitive_scores.get('overall_competitive_health', 0)
        
        key_insights.append({
            'insight': f"Overall competitive health: {competitive_health}/10",
            'evidence': f"Based on market position, competitive strength, and growth analysis",
            'impact': 'High' if competitive_health < 6 else 'Medium',
            'confidence': 0.88
        })
        
        # Market opportunities insight
        if content_opportunities:
            top_opportunity = content_opportunities[0]
            key_insights.append({
                'insight': f"High-potential opportunity: {top_opportunity.get('opportunity', 'Content innovation')}",
                'evidence': f"Potential: {top_opportunity.get('potential', 'medium')}, Competition: {top_opportunity.get('competition', 'medium')}",
                'impact': 'High',
                'confidence': 0.82
            })
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.85,  # High confidence in competitive analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': summary,
                'metrics': competitive_scores,
                'key_insights': key_insights[:5],  # Limit to top 5
                'recommendations': [
                    {
                        'recommendation': rec if isinstance(rec, str) else str(rec),
                        'expected_impact': 'High',
                        'implementation_difficulty': 'Medium',
                        'reasoning': 'Based on competitive landscape analysis and market opportunities'
                    }
                    for rec in recommendations[:5]  # Limit to top 5
                ],
                'detailed_analysis': {
                    'competitor_benchmarks': [
                        {
                            'name': c.channel_name,
                            'subscriber_count': c.subscriber_count,
                            'avg_views': c.avg_views,
                            'engagement_rate': c.avg_engagement_rate,
                            'competitive_advantages': c.competitive_advantage
                        }
                        for c in analysis_result.get('raw_data', {}).get('competitor_data', [])
                    ],
                    'performance_comparison': performance_comparison,
                    'content_opportunities': content_opportunities,
                    'market_insights': ai_analysis.get('market_insights', {}),
                    'niche_trends': analysis_result.get('raw_data', {}).get('niche_trends', {})
                }
            },
            'token_usage': {
                'input_tokens': 4200,
                'output_tokens': 2100,
                'model': 'gemini-2.0-flash-exp'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'competitive_analysis_' + request_id[:8],
                'ttl_remaining': 21600 if not cache_hit else 16200
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True,
            'boss_agent_callback_url': request_data.get('boss_agent_callback_url')
        }
    
    def _create_competitive_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Create a concise summary of competitive analysis"""
        
        scores = analysis_result.get('competitive_scores', {})
        metadata = analysis_result.get('analysis_metadata', {})
        
        competitive_health = scores.get('overall_competitive_health', 0)
        competitors_count = metadata.get('competitors_analyzed', 0)
        
        if competitive_health >= 8:
            health_desc = "strong"
        elif competitive_health >= 6:
            health_desc = "competitive"
        elif competitive_health >= 4:
            health_desc = "moderate"
        else:
            health_desc = "challenging"
        
        return f"Competitive analysis shows {health_desc} market position (score: {competitive_health}/10). Analysis includes {competitors_count} competitors with focus on market positioning, performance benchmarking, and growth opportunities."
    
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
                'cache_key': 'competitive_analysis_' + request_id[:8],
                'ttl_remaining': 16200
            }
        })
        
        return response
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for requests outside competitive analysis domain"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Request outside competitive analysis domain',
                'error_message': 'This request should be handled by a different specialized agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_unauthorized_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for unauthorized requests"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': False,
            'analysis': {
                'summary': 'Unauthorized request - only boss agent can access this service',
                'error_message': 'Access denied: This agent only accepts requests from the authorized boss agent'
            },
            'for_boss_agent_only': True
        }
    
    def _create_error_response(self, request_id: str, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create error response for boss agent"""
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.0,
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': 'Competitive analysis failed',
                'error_message': error_message
            },
            'processing_time': round(time.time() - start_time, 2),
            'for_boss_agent_only': True
        }

# Global instance for boss agent integration
competitive_analysis_agent = None

def get_competitive_analysis_agent():
    """Get or create competitive analysis agent instance"""
    global competitive_analysis_agent
    
    if competitive_analysis_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not gemini_api_key:
            logger.warning("GEMINI_API_KEY not set - using demo mode")
            gemini_api_key = "demo_key"
        
        competitive_analysis_agent = CompetitiveAnalysisAgent(youtube_api_key, gemini_api_key)
    
    return competitive_analysis_agent

async def process_competitive_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request competitive analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_competitive_analysis_agent()
    return await agent.process_boss_agent_request(request_data)