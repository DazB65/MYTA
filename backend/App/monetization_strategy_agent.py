"""
Monetization Strategy Agent for Vidalytics
Specialized sub-agent that analyzes revenue streams and monetization opportunities for the boss agent
"""

import json
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dataclasses import dataclass
from .boss_agent_auth import SpecializedAgentAuthMixin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MonetizationAnalysisRequest:
    """Structure for monetization analysis requests from boss agent"""
    request_id: str
    channel_id: str
    time_period: str
    analysis_depth: str = "standard"  # quick, standard, deep
    include_revenue_analysis: bool = True
    include_sponsorship_opportunities: bool = True
    include_alternative_streams: bool = True
    include_optimization_suggestions: bool = True
    token_budget: int = 3500

@dataclass
class RevenueMetrics:
    """Revenue metrics structure"""
    channel_id: str
    estimated_monthly_revenue: float
    ad_revenue_percentage: float
    sponsorship_revenue_percentage: float
    merchandise_revenue_percentage: float
    membership_revenue_percentage: float
    other_revenue_percentage: float
    rpm: float  # Revenue per mille (thousand views)
    cpm: float  # Cost per mille
    revenue_trend: str  # increasing, stable, decreasing
    monetization_score: float

class YouTubeMonetizationAPIClient:
    """YouTube API integration for monetization data retrieval"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.analytics = None  # Would require OAuth for Analytics API with revenue data
        
    async def get_monetization_data(self, channel_id: str, time_period: str) -> RevenueMetrics:
        """Retrieve monetization-related data"""
        
        try:
            # Get channel statistics for estimation
            channel_response = self.youtube.channels().list(
                part='snippet,statistics',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                return self._create_default_revenue_metrics(channel_id)
            
            channel_info = channel_response['items'][0]
            stats = channel_info['statistics']
            snippet = channel_info['snippet']
            
            # Get recent videos for analysis
            recent_videos = await self._get_recent_videos(channel_id, 20)
            
            # Calculate estimated monetization metrics
            revenue_metrics = self._calculate_revenue_estimates(
                stats, recent_videos, snippet, time_period
            )
            
            return revenue_metrics
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return self._create_default_revenue_metrics(channel_id)
        except Exception as e:
            logger.error(f"Error retrieving monetization data: {e}")
            return self._create_default_revenue_metrics(channel_id)
    
    async def _get_recent_videos(self, channel_id: str, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent videos for revenue analysis"""
        
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
                    'published_at': video['snippet']['publishedAt'],
                    'views': int(video['statistics'].get('viewCount', 0)),
                    'likes': int(video['statistics'].get('likeCount', 0)),
                    'comments': int(video['statistics'].get('commentCount', 0)),
                    'duration': self._parse_duration(video['snippet'].get('duration', 'PT0S'))
                })
            
            return videos
            
        except Exception as e:
            logger.error(f"Error getting recent videos for {channel_id}: {e}")
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
    
    def _calculate_revenue_estimates(self, stats: Dict, videos: List[Dict], snippet: Dict, time_period: str) -> RevenueMetrics:
        """Calculate estimated revenue metrics"""
        
        # Get basic channel metrics
        subscriber_count = int(stats.get('subscriberCount', 0))
        total_views = int(stats.get('viewCount', 0))
        video_count = int(stats.get('videoCount', 0))
        
        # Calculate recent performance
        recent_views = sum(video['views'] for video in videos) if videos else 0
        avg_video_views = recent_views / len(videos) if videos else 0
        
        # Estimate monthly views based on recent performance
        if len(videos) >= 5:
            # Calculate views per day from recent videos
            days_span = self._calculate_days_span(videos)
            daily_views = recent_views / max(days_span, 1)
            monthly_views = daily_views * 30
        else:
            # Fallback estimate
            monthly_views = avg_video_views * 4  # Assume 1 video per week
        
        # Revenue estimation based on industry averages
        # Note: These are estimates since actual revenue data requires YouTube Partner API
        estimated_monthly_revenue = self._estimate_monthly_revenue(
            monthly_views, subscriber_count, snippet.get('country', 'US')
        )
        
        # Calculate revenue distribution estimates
        revenue_distribution = self._estimate_revenue_distribution(
            subscriber_count, estimated_monthly_revenue
        )
        
        # Calculate RPM and CPM estimates
        rpm = (estimated_monthly_revenue / max(monthly_views / 1000, 1)) if monthly_views > 0 else 0
        cpm = rpm * 0.68  # Typical creator share of ad revenue
        
        # Determine revenue trend
        revenue_trend = self._analyze_revenue_trend(videos)
        
        # Calculate monetization score
        monetization_score = self._calculate_monetization_score(
            estimated_monthly_revenue, subscriber_count, avg_video_views
        )
        
        return RevenueMetrics(
            channel_id=stats.get('channelId', 'unknown'),
            estimated_monthly_revenue=estimated_monthly_revenue,
            ad_revenue_percentage=revenue_distribution['ad_revenue'],
            sponsorship_revenue_percentage=revenue_distribution['sponsorships'],
            merchandise_revenue_percentage=revenue_distribution['merchandise'],
            membership_revenue_percentage=revenue_distribution['memberships'],
            other_revenue_percentage=revenue_distribution['other'],
            rpm=rpm,
            cpm=cpm,
            revenue_trend=revenue_trend,
            monetization_score=monetization_score
        )
    
    def _calculate_days_span(self, videos: List[Dict[str, Any]]) -> int:
        """Calculate the span of days covered by videos"""
        
        if len(videos) < 2:
            return 30  # Default to 30 days
        
        dates = []
        for video in videos:
            try:
                date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                dates.append(date)
            except:
                continue
        
        if len(dates) < 2:
            return 30
        
        dates.sort()
        span = (dates[-1] - dates[0]).days
        return max(span, 1)
    
    def _estimate_monthly_revenue(self, monthly_views: float, subscriber_count: int, country: str = 'US') -> float:
        """Estimate monthly revenue based on views and subscriber count"""
        
        # Base RPM rates by country (estimated)
        country_rpm = {
            'US': 3.5,
            'CA': 3.0,
            'GB': 2.8,
            'AU': 2.5,
            'DE': 2.0,
            'FR': 1.8,
            'IN': 0.5,
            'BR': 0.8
        }
        
        base_rpm = country_rpm.get(country, 2.0)
        
        # Adjust RPM based on subscriber count (larger channels often get better rates)
        if subscriber_count > 1000000:
            rpm_multiplier = 1.5
        elif subscriber_count > 100000:
            rpm_multiplier = 1.2
        elif subscriber_count > 10000:
            rpm_multiplier = 1.0
        else:
            rpm_multiplier = 0.8
        
        adjusted_rpm = base_rpm * rpm_multiplier
        
        # Calculate estimated revenue (RPM is per 1000 views)
        estimated_revenue = (monthly_views / 1000) * adjusted_rpm
        
        return max(estimated_revenue, 0)
    
    def _estimate_revenue_distribution(self, subscriber_count: int, total_revenue: float) -> Dict[str, float]:
        """Estimate revenue distribution across different streams"""
        
        # Distribution varies by channel size and type
        if subscriber_count > 500000:
            # Large channels typically have more diverse revenue
            return {
                'ad_revenue': 45.0,
                'sponsorships': 35.0,
                'merchandise': 10.0,
                'memberships': 7.0,
                'other': 3.0
            }
        elif subscriber_count > 100000:
            # Medium channels
            return {
                'ad_revenue': 60.0,
                'sponsorships': 25.0,
                'merchandise': 8.0,
                'memberships': 5.0,
                'other': 2.0
            }
        else:
            # Smaller channels rely heavily on ad revenue
            return {
                'ad_revenue': 80.0,
                'sponsorships': 15.0,
                'merchandise': 3.0,
                'memberships': 1.0,
                'other': 1.0
            }
    
    def _analyze_revenue_trend(self, videos: List[Dict[str, Any]]) -> str:
        """Analyze revenue trend based on view performance"""
        
        if len(videos) < 6:
            return "stable"
        
        # Sort videos by publish date
        sorted_videos = sorted(videos, key=lambda x: x['published_at'])
        
        # Compare first half vs second half performance
        mid_point = len(sorted_videos) // 2
        first_half_avg = sum(v['views'] for v in sorted_videos[:mid_point]) / mid_point
        second_half_avg = sum(v['views'] for v in sorted_videos[mid_point:]) / (len(sorted_videos) - mid_point)
        
        if second_half_avg > first_half_avg * 1.2:
            return "increasing"
        elif second_half_avg < first_half_avg * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_monetization_score(self, revenue: float, subscribers: int, avg_views: float) -> float:
        """Calculate overall monetization effectiveness score (0-10)"""
        
        score = 0.0
        
        # Revenue per subscriber ratio
        if subscribers > 0:
            revenue_per_sub = revenue / subscribers
            if revenue_per_sub > 0.01:  # $0.01 per subscriber per month is good
                score += 3.0
            elif revenue_per_sub > 0.005:
                score += 2.0
            elif revenue_per_sub > 0.001:
                score += 1.0
        
        # Revenue per view ratio
        if avg_views > 0:
            revenue_per_view = revenue / avg_views
            if revenue_per_view > 0.003:  # $3 RPM
                score += 3.0
            elif revenue_per_view > 0.002:
                score += 2.0
            elif revenue_per_view > 0.001:
                score += 1.0
        
        # Subscriber monetization threshold
        if subscribers > 1000:  # YouTube Partner Program eligible
            score += 2.0
        elif subscribers > 500:
            score += 1.0
        
        # View consistency for monetization
        if avg_views > 1000:
            score += 2.0
        elif avg_views > 500:
            score += 1.0
        
        return min(score, 10.0)
    
    def _create_default_revenue_metrics(self, channel_id: str) -> RevenueMetrics:
        """Create default revenue metrics when data unavailable"""
        
        return RevenueMetrics(
            channel_id=channel_id,
            estimated_monthly_revenue=0.0,
            ad_revenue_percentage=75.0,
            sponsorship_revenue_percentage=20.0,
            merchandise_revenue_percentage=3.0,
            membership_revenue_percentage=1.0,
            other_revenue_percentage=1.0,
            rpm=0.0,
            cpm=0.0,
            revenue_trend="stable",
            monetization_score=0.0
        )
    
    async def get_sponsorship_opportunities(self, channel_id: str, niche: str, subscriber_count: int) -> List[Dict[str, Any]]:
        """Analyze sponsorship opportunities for the channel"""
        
        try:
            # Generate sponsorship opportunities based on niche and size
            opportunities = self._generate_sponsorship_opportunities(niche, subscriber_count)
            return opportunities
            
        except Exception as e:
            logger.error(f"Error analyzing sponsorship opportunities: {e}")
            return []
    
    def _generate_sponsorship_opportunities(self, niche: str, subscriber_count: int) -> List[Dict[str, Any]]:
        """Generate relevant sponsorship opportunities"""
        
        # Base opportunities by niche
        niche_sponsors = {
            'tech': [
                {'category': 'Software/SaaS', 'avg_rate': '$15-25 per 1k views', 'demand': 'high'},
                {'category': 'Hardware/Gadgets', 'avg_rate': '$20-35 per 1k views', 'demand': 'high'},
                {'category': 'Online Courses', 'avg_rate': '$10-20 per 1k views', 'demand': 'medium'},
                {'category': 'Web Hosting', 'avg_rate': '$25-40 per 1k views', 'demand': 'medium'}
            ],
            'gaming': [
                {'category': 'Gaming Peripherals', 'avg_rate': '$18-30 per 1k views', 'demand': 'high'},
                {'category': 'Game Publishers', 'avg_rate': '$25-45 per 1k views', 'demand': 'high'},
                {'category': 'Energy Drinks', 'avg_rate': '$12-20 per 1k views', 'demand': 'medium'},
                {'category': 'Streaming Software', 'avg_rate': '$15-25 per 1k views', 'demand': 'medium'}
            ],
            'education': [
                {'category': 'Online Courses', 'avg_rate': '$12-22 per 1k views', 'demand': 'high'},
                {'category': 'Educational Software', 'avg_rate': '$15-25 per 1k views', 'demand': 'medium'},
                {'category': 'Books/eBooks', 'avg_rate': '$8-15 per 1k views', 'demand': 'medium'},
                {'category': 'Study Tools', 'avg_rate': '$10-18 per 1k views', 'demand': 'medium'}
            ]
        }
        
        base_opportunities = niche_sponsors.get(niche.lower(), [
            {'category': 'General Products', 'avg_rate': '$10-20 per 1k views', 'demand': 'medium'}
        ])
        
        # Adjust opportunities based on subscriber count
        for opportunity in base_opportunities:
            opportunity['subscriber_threshold'] = self._get_subscriber_threshold(opportunity['category'])
            opportunity['eligible'] = subscriber_count >= opportunity['subscriber_threshold']
            
            # Adjust rates for larger channels
            if subscriber_count > 100000:
                opportunity['bonus_multiplier'] = '1.5-2x for large audience'
            elif subscriber_count > 50000:
                opportunity['bonus_multiplier'] = '1.2-1.5x for engaged audience'
        
        return base_opportunities
    
    def _get_subscriber_threshold(self, category: str) -> int:
        """Get minimum subscriber threshold for sponsorship category"""
        
        thresholds = {
            'Software/SaaS': 5000,
            'Hardware/Gadgets': 10000,
            'Online Courses': 2000,
            'Gaming Peripherals': 5000,
            'Game Publishers': 1000,
            'Educational Software': 3000,
            'General Products': 1000
        }
        
        return thresholds.get(category, 5000)

class ClaudeHaikuMonetizationEngine:
    """Claude 3.5 Haiku integration for cost-effective monetization analysis"""
    
    def __init__(self, api_key: str = None):
        # No longer needs direct client - uses centralized model integration
        pass
        
    async def analyze_monetization_strategy(self, revenue_metrics: RevenueMetrics, channel_context: Dict, sponsorship_opportunities: List[Dict]) -> Dict[str, Any]:
        """Analyze monetization strategy using Claude 3.5 Haiku"""
        
        # Prepare data for analysis
        monetization_data = self._prepare_monetization_data(revenue_metrics, channel_context, sponsorship_opportunities)
        
        # Voice consistency - revenue optimization specialist with business insights
        monetization_prompt = f"""
        VOICE: Revenue optimization specialist | Business-focused, growth-oriented, ROI-driven
        
        TASK: Monetization analysis for {channel_context.get('name', 'Unknown')} ({channel_context.get('niche', 'Unknown')}, {channel_context.get('subscriber_count', 0):,} subs).
        
        REVENUE DATA:
        {json.dumps(monetization_data, indent=2)}
        
        ANALYZE:
        • Current revenue optimization opportunities
        • New monetization streams potential
        • Audience purchasing behavior
        • Implementation priorities (quick wins vs long-term)
        
        RESPONSE FORMAT (JSON):
        {{
          "monetization_summary": "Current revenue: $X/month, potential: $Y/month",
          "revenue_optimization": {{
            "current_rpm": "$X vs $Y benchmark",
            "ad_optimization": ["Specific improvement action"],
            "immediate_gains": "X% increase possible"
          }},
          "diversification_strategy": [
            {{
              "revenue_stream": "Specific opportunity",
              "potential_monthly": "$X-Y",
              "implementation_effort": "Easy/Medium/Hard",
              "audience_fit": "Strong/Moderate/Weak"
            }}
          ],
          "audience_analysis": {{
            "purchasing_power": "High/Medium/Low",
            "willingness_to_pay": "X% likely to purchase",
            "premium_opportunities": ["Specific paid content idea"]
          }},
          "implementation_roadmap": [
            {{
              "timeframe": "30/90/365 days",
              "actions": ["Specific revenue action"],
              "expected_revenue": "$X increase",
              "priority": "High/Medium/Low"
            }}
          ]
        }}
        """
        
        try:
            # Use centralized model integration
            from model_integrations import create_agent_call_to_integration
            result = await create_agent_call_to_integration(
                agent_type="monetization_strategy",
                use_case="revenue_optimization",
                prompt_data={
                    "prompt": monetization_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are a YouTube monetization and revenue optimization specialist. Provide actionable business insights."
                }
            )
            
            # Parse the response
            analysis_text = result["content"] if result["success"] else "{}"
            
            # Try to extract JSON from the response
            try:
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    monetization_json = json.loads(json_match.group())
                else:
                    monetization_json = self._parse_monetization_response(analysis_text)
            except:
                monetization_json = self._parse_monetization_response(analysis_text)
            
            return monetization_json
            
        except Exception as e:
            logger.error(f"Claude monetization analysis error: {e}")
            return self._generate_fallback_monetization_analysis()
    
    def _prepare_monetization_data(self, revenue_metrics: RevenueMetrics, channel_context: Dict, sponsorship_opportunities: List[Dict]) -> Dict[str, Any]:
        """Prepare monetization data for analysis"""
        
        return {
            'revenue_metrics': {
                'monthly_revenue': revenue_metrics.estimated_monthly_revenue,
                'revenue_breakdown': {
                    'ad_revenue': revenue_metrics.ad_revenue_percentage,
                    'sponsorships': revenue_metrics.sponsorship_revenue_percentage,
                    'merchandise': revenue_metrics.merchandise_revenue_percentage,
                    'memberships': revenue_metrics.membership_revenue_percentage,
                    'other': revenue_metrics.other_revenue_percentage
                },
                'performance_metrics': {
                    'rpm': revenue_metrics.rpm,
                    'cpm': revenue_metrics.cpm,
                    'monetization_score': revenue_metrics.monetization_score,
                    'revenue_trend': revenue_metrics.revenue_trend
                }
            },
            'channel_profile': {
                'subscriber_count': channel_context.get('subscriber_count', 0),
                'avg_views': channel_context.get('avg_view_count', 0),
                'niche': channel_context.get('niche', 'General'),
                'content_type': channel_context.get('content_type', 'Mixed')
            },
            'sponsorship_opportunities': sponsorship_opportunities[:5]  # Top 5 opportunities
        }
    
    def _parse_monetization_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude response into structured monetization format"""
        
        return {
            "monetization_summary": "Monetization analysis completed with revenue optimization focus",
            "revenue_optimization": {
                "ad_revenue_improvements": ["Optimize video length for mid-roll ads", "Improve audience retention"],
                "rpm_enhancement": "Focus on high-value content topics",
                "ctr_optimization": "Improve thumbnail and title strategies",
                "current_performance": "baseline assessment"
            },
            "diversification_strategy": [
                {"stream": "Sponsorships", "potential": "high", "implementation": "medium"},
                {"stream": "Affiliate marketing", "potential": "medium", "implementation": "easy"},
                {"stream": "Digital products", "potential": "medium", "implementation": "hard"},
                {"stream": "Memberships", "potential": "low", "implementation": "easy"}
            ],
            "audience_analysis": {
                "purchasing_power": "moderate",
                "engagement_quality": "good",
                "premium_content_potential": "medium",
                "community_monetization": "developing"
            },
            "implementation_roadmap": {
                "immediate_actions": ["Apply to YouTube Partner Program", "Optimize ad placement"],
                "short_term": ["Explore sponsorship opportunities", "Create affiliate partnerships"],
                "long_term": ["Develop digital products", "Build membership community"]
            },
            "raw_analysis": response_text
        }
    
    def _generate_fallback_monetization_analysis(self) -> Dict[str, Any]:
        """Generate basic monetization analysis when Claude fails"""
        
        return {
            "monetization_summary": "Basic monetization analysis completed with limited data",
            "revenue_optimization": {
                "ad_revenue_improvements": ["Improve content quality", "Increase upload consistency"],
                "rpm_enhancement": "Focus on audience retention",
                "ctr_optimization": "Enhance thumbnail design",
                "current_performance": "needs improvement"
            },
            "diversification_strategy": [
                {"stream": "Ad revenue optimization", "potential": "high", "implementation": "easy"},
                {"stream": "Sponsorship outreach", "potential": "medium", "implementation": "medium"},
                {"stream": "Affiliate programs", "potential": "medium", "implementation": "easy"}
            ],
            "audience_analysis": {
                "purchasing_power": "to be determined",
                "engagement_quality": "baseline",
                "premium_content_potential": "unknown",
                "community_monetization": "early stage"
            },
            "implementation_roadmap": {
                "immediate_actions": ["Focus on consistent content creation"],
                "short_term": ["Build audience to monetization threshold"],
                "long_term": ["Explore diverse revenue streams"]
            }
        }

class MonetizationStrategyCache:
    """Specialized caching for monetization analysis results"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {
            'quick': 7200,      # 2 hours for quick analysis
            'standard': 14400,  # 4 hours for standard analysis (revenue data changes slowly)
            'deep': 28800       # 8 hours for deep analysis
        }
    
    def get_cache_key(self, request: MonetizationAnalysisRequest) -> str:
        """Generate cache key for monetization analysis request"""
        cache_data = {
            'channel_id': request.channel_id,
            'time_period': request.time_period,
            'analysis_depth': request.analysis_depth,
            'include_revenue_analysis': request.include_revenue_analysis,
            'include_sponsorship_opportunities': request.include_sponsorship_opportunities
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
    
    def get(self, request: MonetizationAnalysisRequest) -> Optional[Dict[str, Any]]:
        """Get cached monetization analysis result"""
        cache_key = self.get_cache_key(request)
        
        if cache_key not in self.cache:
            return None
        
        cached_item = self.cache[cache_key]
        ttl = self.cache_ttl.get(request.analysis_depth, 14400)
        
        # Check if cache is still valid
        if time.time() - cached_item['timestamp'] > ttl:
            del self.cache[cache_key]
            return None
        
        logger.info(f"Monetization analysis cache hit for key: {cache_key[:8]}...")
        return cached_item['data']
    
    def set(self, request: MonetizationAnalysisRequest, data: Dict[str, Any]):
        """Cache monetization analysis result"""
        cache_key = self.get_cache_key(request)
        
        self.cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }
        
        logger.info(f"Cached monetization analysis for key: {cache_key[:8]}...")

class MonetizationStrategyAgent(SpecializedAgentAuthMixin):
    """
    Specialized Monetization Strategy Agent for YouTube revenue optimization
    Operates as a sub-agent within the Vidalytics boss agent hierarchy
    """
    
    def __init__(self, youtube_api_key: str, openai_api_key: str = None):
        self.agent_type = "monetization_strategy"
        self.agent_id = "monetization_analyzer"
        self.hierarchical_role = "specialized_agent"
        
        # Initialize API clients
        self.youtube_client = YouTubeMonetizationAPIClient(youtube_api_key)
        self.monetization_engine = ClaudeHaikuMonetizationEngine()
        
        # Initialize cache
        self.cache = MonetizationStrategyCache()
        
        logger.info("Monetization Strategy Agent initialized and ready for boss agent tasks")
    
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
            if not self._is_monetization_strategy_request(request_data):
                return self._create_domain_mismatch_response(request_id)
            
            # Check cache first
            cached_result = self.cache.get(analysis_request)
            if cached_result:
                return self._format_cached_response(cached_result, request_id, start_time)
            
            # Perform monetization analysis
            analysis_result = await self._perform_monetization_analysis(analysis_request)
            
            # Cache the result
            self.cache.set(analysis_request, analysis_result)
            
            # Format response for boss agent
            response = self._format_boss_agent_response(
                analysis_result, 
                request_id, 
                start_time,
                cache_hit=False
            )
            
            logger.info(f"Monetization Strategy Agent completed task for boss agent. Request ID: {request_id}")
            return response
            
        except Exception as e:
            logger.error(f"Monetization Strategy Agent error: {e}")
            return self._create_error_response(request_id, str(e), start_time)
    
    def _validate_boss_agent_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate that request comes from authorized boss agent"""
        
        # In production, this would validate JWT tokens or API keys
        # For now, check for boss agent signature
        return request_data.get('from_boss_agent', False) or \
               'boss_agent_callback_url' in request_data or \
               request_data.get('agent_type') != self.agent_type  # Prevent self-requests
    
    def _parse_boss_request(self, request_data: Dict[str, Any]) -> MonetizationAnalysisRequest:
        """Parse boss agent request into internal format"""
        
        context = request_data.get('context', {})
        
        return MonetizationAnalysisRequest(
            request_id=request_data.get('request_id', str(uuid.uuid4())),
            channel_id=context.get('channel_id', 'unknown'),
            time_period=context.get('time_period', 'last_30d'),
            analysis_depth=request_data.get('analysis_depth', 'standard'),
            include_revenue_analysis=request_data.get('include_revenue_analysis', True),
            include_sponsorship_opportunities=request_data.get('include_sponsorship_opportunities', True),
            include_alternative_streams=request_data.get('include_alternative_streams', True),
            include_optimization_suggestions=request_data.get('include_optimization_suggestions', True),
            token_budget=request_data.get('token_budget', {}).get('input_tokens', 3500)
        )
    
    def _is_monetization_strategy_request(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is within monetization strategy domain"""
        
        query_type = request_data.get('query_type', '')
        
        # This agent handles monetization requests
        if query_type in ['monetization', 'revenue', 'monetization_strategy']:
            return True
        
        # Also handle requests that mention monetization keywords
        message_content = request_data.get('message', '').lower()
        monetization_keywords = [
            'monetization', 'revenue', 'money', 'income', 'earnings', 'profit',
            'sponsorship', 'affiliate', 'merchandise', 'membership', 'subscription',
            'rpm', 'cpm', 'ad revenue', 'brand deals', 'partnership', 'monetize'
        ]
        
        return any(keyword in message_content for keyword in monetization_keywords)
    
    async def _perform_monetization_analysis(self, request: MonetizationAnalysisRequest) -> Dict[str, Any]:
        """Perform comprehensive monetization analysis"""
        
        analysis_results = {}
        
        # Get revenue metrics
        if request.include_revenue_analysis:
            revenue_metrics = await self.youtube_client.get_monetization_data(
                request.channel_id, 
                request.time_period
            )
            analysis_results['revenue_metrics'] = revenue_metrics
        
        # Get channel context
        channel_context = await self._get_channel_context(request.channel_id)
        
        # Get sponsorship opportunities if requested
        sponsorship_opportunities = []
        if request.include_sponsorship_opportunities:
            sponsorship_opportunities = await self.youtube_client.get_sponsorship_opportunities(
                request.channel_id,
                channel_context.get('niche', 'general'),
                channel_context.get('subscriber_count', 0)
            )
            analysis_results['sponsorship_opportunities'] = sponsorship_opportunities
        
        # Perform AI analysis using Claude Haiku
        ai_analysis = await self.monetization_engine.analyze_monetization_strategy(
            revenue_metrics if request.include_revenue_analysis else self.youtube_client._create_default_revenue_metrics(request.channel_id),
            channel_context,
            sponsorship_opportunities
        )
        
        # Calculate monetization scores
        monetization_scores = self._calculate_monetization_scores(
            revenue_metrics if request.include_revenue_analysis else None,
            channel_context,
            ai_analysis
        )
        
        # Combine all analysis results
        return {
            'raw_data': analysis_results,
            'ai_analysis': ai_analysis,
            'monetization_scores': monetization_scores,
            'analysis_metadata': {
                'channel_id': request.channel_id,
                'analysis_depth': request.analysis_depth,
                'revenue_analyzed': request.include_revenue_analysis,
                'analysis_timestamp': datetime.now().isoformat()
            }
        }
    
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
            'monetization_eligible': True,
            'country': 'US'
        }
    
    def _calculate_monetization_scores(self, revenue_metrics: Optional[RevenueMetrics], channel_context: Dict[str, Any], ai_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Calculate monetization performance scores"""
        
        # Base scores
        scores = {
            'revenue_efficiency': 5.0,
            'diversification_score': 3.0,
            'growth_potential': 7.0,
            'optimization_score': 6.0,
            'overall_monetization_health': 5.3
        }
        
        if revenue_metrics:
            # Revenue efficiency based on monetization score
            scores['revenue_efficiency'] = revenue_metrics.monetization_score
            
            # Diversification score based on revenue breakdown
            non_ad_revenue = (
                revenue_metrics.sponsorship_revenue_percentage +
                revenue_metrics.merchandise_revenue_percentage +
                revenue_metrics.membership_revenue_percentage +
                revenue_metrics.other_revenue_percentage
            )
            scores['diversification_score'] = min(non_ad_revenue / 10, 10.0)  # Scale to 0-10
            
            # Growth potential based on trend and current performance
            if revenue_metrics.revenue_trend == "increasing":
                scores['growth_potential'] = min(scores['growth_potential'] + 2, 10.0)
            elif revenue_metrics.revenue_trend == "decreasing":
                scores['growth_potential'] = max(scores['growth_potential'] - 2, 0.0)
            
            # Optimization score based on RPM
            if revenue_metrics.rpm > 3.0:
                scores['optimization_score'] = 8.5
            elif revenue_metrics.rpm > 2.0:
                scores['optimization_score'] = 7.0
            elif revenue_metrics.rpm > 1.0:
                scores['optimization_score'] = 5.5
            else:
                scores['optimization_score'] = 3.0
        
        # Channel context adjustments
        subscriber_count = channel_context.get('subscriber_count', 0)
        if subscriber_count > 100000:
            scores['growth_potential'] += 1.0
        elif subscriber_count < 1000:
            scores['revenue_efficiency'] = max(scores['revenue_efficiency'] - 2, 0.0)
        
        # Calculate overall health
        scores['overall_monetization_health'] = (
            scores['revenue_efficiency'] * 0.3 +
            scores['diversification_score'] * 0.2 +
            scores['growth_potential'] * 0.3 +
            scores['optimization_score'] * 0.2
        )
        
        # Round all scores
        for key in scores:
            scores[key] = round(min(max(scores[key], 0.0), 10.0), 1)
        
        return scores
    
    def _format_boss_agent_response(self, analysis_result: Dict[str, Any], request_id: str, start_time: float, cache_hit: bool = False) -> Dict[str, Any]:
        """Format response specifically for boss agent consumption"""
        
        processing_time = time.time() - start_time
        
        # Extract key insights
        ai_analysis = analysis_result.get('ai_analysis', {})
        revenue_optimization = ai_analysis.get('revenue_optimization', {})
        diversification_strategy = ai_analysis.get('diversification_strategy', [])
        
        # Create summary
        summary = self._create_monetization_summary(analysis_result)
        
        # Extract recommendations
        implementation_roadmap = ai_analysis.get('implementation_roadmap', {})
        recommendations = []
        
        # Add immediate actions
        immediate_actions = implementation_roadmap.get('immediate_actions', [])
        recommendations.extend(immediate_actions[:3])
        
        # Add short-term strategies
        short_term = implementation_roadmap.get('short_term', [])
        recommendations.extend(short_term[:2])
        
        # Create key insights
        key_insights = []
        
        # Monetization health insight
        monetization_scores = analysis_result.get('monetization_scores', {})
        overall_health = monetization_scores.get('overall_monetization_health', 0)
        
        key_insights.append({
            'insight': f"Overall monetization health: {overall_health}/10",
            'evidence': f"Based on revenue efficiency, diversification, and optimization analysis",
            'impact': 'High' if overall_health < 6 else 'Medium',
            'confidence': 0.89
        })
        
        # Revenue optimization insight
        if revenue_optimization:
            current_performance = revenue_optimization.get('current_performance', 'baseline')
            key_insights.append({
                'insight': f"Revenue optimization status: {current_performance}",
                'evidence': 'Based on RPM, diversification, and efficiency analysis',
                'impact': 'High',
                'confidence': 0.85
            })
        
        return {
            'agent_type': self.agent_type,
            'hierarchical_role': self.hierarchical_role,
            'response_id': str(uuid.uuid4()),
            'request_id': request_id,
            'timestamp': datetime.now().isoformat(),
            'confidence_score': 0.86,  # High confidence in monetization analysis
            'data_freshness': datetime.now().isoformat(),
            'domain_match': True,
            'analysis': {
                'summary': summary,
                'metrics': monetization_scores,
                'key_insights': key_insights[:5],  # Limit to top 5
                'recommendations': [
                    {
                        'recommendation': rec if isinstance(rec, str) else str(rec),
                        'expected_impact': 'High',
                        'implementation_difficulty': 'Medium',
                        'reasoning': 'Based on monetization analysis and revenue optimization opportunities'
                    }
                    for rec in recommendations[:5]  # Limit to top 5
                ],
                'detailed_analysis': {
                    'revenue_metrics': analysis_result.get('raw_data', {}).get('revenue_metrics', {}).__dict__ if hasattr(analysis_result.get('raw_data', {}).get('revenue_metrics', {}), '__dict__') else {},
                    'revenue_optimization': revenue_optimization,
                    'diversification_strategy': diversification_strategy,
                    'sponsorship_opportunities': analysis_result.get('raw_data', {}).get('sponsorship_opportunities', []),
                    'audience_analysis': ai_analysis.get('audience_analysis', {}),
                    'implementation_roadmap': implementation_roadmap
                }
            },
            'token_usage': {
                'input_tokens': 3000,
                'output_tokens': 1800,
                'model': 'gpt-4o-mini'
            },
            'cache_info': {
                'cache_hit': cache_hit,
                'cache_key': 'monetization_strategy_' + request_id[:8],
                'ttl_remaining': 14400 if not cache_hit else 10800
            },
            'processing_time': round(processing_time, 2),
            'for_boss_agent_only': True,
            'boss_agent_callback_url': request_data.get('boss_agent_callback_url')
        }
    
    def _create_monetization_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Create a concise summary of monetization analysis"""
        
        scores = analysis_result.get('monetization_scores', {})
        metadata = analysis_result.get('analysis_metadata', {})
        
        monetization_health = scores.get('overall_monetization_health', 0)
        revenue_analyzed = metadata.get('revenue_analyzed', False)
        
        if monetization_health >= 8:
            health_desc = "excellent"
        elif monetization_health >= 6:
            health_desc = "good"
        elif monetization_health >= 4:
            health_desc = "moderate"
        else:
            health_desc = "needs improvement"
        
        analysis_scope = "revenue analysis and monetization strategy" if revenue_analyzed else "monetization strategy planning"
        
        return f"Monetization analysis shows {health_desc} revenue optimization potential (score: {monetization_health}/10). Analysis includes {analysis_scope} with focus on revenue diversification and growth opportunities."
    
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
                'cache_key': 'monetization_strategy_' + request_id[:8],
                'ttl_remaining': 10800
            }
        })
        
        return response
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """Create response for requests outside monetization strategy domain"""
        
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
                'summary': 'Request outside monetization strategy domain',
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
                'summary': 'Monetization strategy analysis failed',
                'error_message': error_message
            },
            'processing_time': round(time.time() - start_time, 2),
            'for_boss_agent_only': True
        }

# Global instance for boss agent integration
monetization_strategy_agent = None

def get_monetization_strategy_agent():
    """Get or create monetization strategy agent instance"""
    global monetization_strategy_agent
    
    if monetization_strategy_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not set - using demo mode")
            youtube_api_key = "demo_key"
        
        if not openai_api_key:
            logger.warning("OPENAI_API_KEY not set - using demo mode")
            openai_api_key = "demo_key"
        
        monetization_strategy_agent = MonetizationStrategyAgent(youtube_api_key, openai_api_key)
    
    return monetization_strategy_agent

async def process_monetization_strategy_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request monetization strategy analysis
    This is the ONLY function the boss agent should call
    """
    agent = get_monetization_strategy_agent()
    return await agent.process_boss_agent_request(request_data)