"""
Channel Analyzer for MYTA
Analyzes user's specific channel data to provide personalized AI responses
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from .supabase_client import get_supabase_service
from .redis_service import get_redis_service
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

@dataclass
class ChannelMetrics:
    """Channel performance metrics"""
    subscriber_count: int = 0
    total_views: int = 0
    video_count: int = 0
    avg_views_per_video: float = 0
    avg_ctr: float = 0
    avg_retention: float = 0
    engagement_rate: float = 0
    upload_frequency: float = 0
    top_performing_topics: List[str] = None
    audience_demographics: Dict[str, Any] = None
    revenue_metrics: Dict[str, Any] = None

@dataclass
class ChannelProfile:
    """Complete channel profile for personalized responses"""
    user_id: str
    channel_id: str
    channel_name: str
    niche: str
    channel_size_tier: str  # "micro", "small", "medium", "large", "mega"
    metrics: ChannelMetrics
    goals: List[Dict[str, Any]]
    recent_performance: Dict[str, Any]
    content_strategy: Dict[str, Any]
    challenges: List[str]
    opportunities: List[str]

class ChannelAnalyzer:
    """Analyzes user's channel data for personalized AI responses"""
    
    def __init__(self):
        self.supabase = get_supabase_service()
        self.redis_service = get_redis_service()
        
        # Channel size tiers based on subscriber count
        self.size_tiers = {
            "micro": (0, 1000),
            "small": (1000, 10000),
            "medium": (10000, 100000),
            "large": (100000, 1000000),
            "mega": (1000000, float('inf'))
        }
    
    async def get_channel_profile(self, user_id: str) -> ChannelProfile:
        """Get comprehensive channel profile for user"""
        try:
            # Check cache first
            cache_key = f"channel_profile:{user_id}"
            if self.redis_service.is_available():
                cached_profile = self.redis_service.get(cache_key)
                if cached_profile:
                    try:
                        # Reconstruct ChannelMetrics from cached data
                        metrics_data = cached_profile.get("metrics", {})
                        metrics = ChannelMetrics(**metrics_data)

                        # Create profile with reconstructed metrics
                        cached_profile["metrics"] = metrics
                        return ChannelProfile(**cached_profile)
                    except Exception as e:
                        logger.error(f"Error reconstructing cached profile: {e}")
                        # Continue to fetch fresh data
            
            # Get user's channel data
            channel_data = await self._get_channel_data(user_id)
            metrics = await self._calculate_metrics(user_id, channel_data)
            goals = await self._get_user_goals(user_id)
            recent_performance = await self._analyze_recent_performance(user_id)
            content_strategy = await self._analyze_content_strategy(user_id)
            challenges = await self._identify_challenges(metrics, recent_performance)
            opportunities = await self._identify_opportunities(metrics, recent_performance)
            
            # Determine channel size tier
            size_tier = self._get_size_tier(metrics.subscriber_count)
            
            # Create profile
            profile = ChannelProfile(
                user_id=user_id,
                channel_id=channel_data.get("channel_id", ""),
                channel_name=channel_data.get("channel_name", "Your Channel"),
                niche=channel_data.get("niche", "General"),
                channel_size_tier=size_tier,
                metrics=metrics,
                goals=goals,
                recent_performance=recent_performance,
                content_strategy=content_strategy,
                challenges=challenges,
                opportunities=opportunities
            )
            
            # Cache the profile
            if self.redis_service.is_available():
                try:
                    profile_dict = {
                        "user_id": profile.user_id,
                        "channel_id": profile.channel_id,
                        "channel_name": profile.channel_name,
                        "niche": profile.niche,
                        "channel_size_tier": profile.channel_size_tier,
                        "metrics": profile.metrics.__dict__,
                        "goals": profile.goals,
                        "recent_performance": profile.recent_performance,
                        "content_strategy": profile.content_strategy,
                        "challenges": profile.challenges,
                        "opportunities": profile.opportunities
                    }
                    self.redis_service.set(cache_key, profile_dict, 3600)  # Cache for 1 hour
                except Exception as e:
                    logger.error(f"Error caching profile: {e}")
            
            return profile
        
        except Exception as e:
            logger.error(f"Error getting channel profile: {e}")
            # Return default profile
            return self._get_default_profile(user_id)
    
    async def _get_channel_data(self, user_id: str) -> Dict[str, Any]:
        """Get basic channel data from database"""
        try:
            # Get user settings for channel info
            result = self.supabase.select("user_settings", "*", {"user_id": user_id})
            
            if result["success"] and result["data"]:
                settings = result["data"][0]
                return {
                    "channel_id": settings.get("youtube_channel_id", ""),
                    "channel_name": settings.get("channel_name", "Your Channel"),
                    "niche": settings.get("channel_niche", "General"),
                    "subscriber_count": settings.get("subscriber_count", 0),
                    "total_views": settings.get("total_views", 0),
                    "video_count": settings.get("video_count", 0)
                }
            
            return {}
        
        except Exception as e:
            logger.error(f"Error getting channel data: {e}")
            return {}
    
    async def _calculate_metrics(self, user_id: str, channel_data: Dict) -> ChannelMetrics:
        """Calculate channel performance metrics"""
        try:
            # In a real implementation, this would pull from YouTube Analytics API
            # For now, use stored data or reasonable defaults
            
            subscriber_count = channel_data.get("subscriber_count", 0)
            total_views = channel_data.get("total_views", 0)
            video_count = channel_data.get("video_count", 0)
            
            # Calculate derived metrics
            avg_views_per_video = total_views / video_count if video_count > 0 else 0
            
            # These would come from YouTube Analytics in production
            avg_ctr = 0.05  # 5% default CTR
            avg_retention = 0.45  # 45% default retention
            engagement_rate = 0.03  # 3% default engagement
            upload_frequency = 1.0  # 1 video per week default
            
            return ChannelMetrics(
                subscriber_count=subscriber_count,
                total_views=total_views,
                video_count=video_count,
                avg_views_per_video=avg_views_per_video,
                avg_ctr=avg_ctr,
                avg_retention=avg_retention,
                engagement_rate=engagement_rate,
                upload_frequency=upload_frequency,
                top_performing_topics=["tutorial", "review", "vlog"],  # Would be analyzed from actual data
                audience_demographics={"age_range": "25-34", "top_countries": ["US", "UK", "CA"]},
                revenue_metrics={"estimated_monthly": 0, "rpm": 0}
            )
        
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return ChannelMetrics()
    
    async def _get_user_goals(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's current goals"""
        try:
            result = self.supabase.select("goals", "*", {"user_id": user_id, "status": "active"})
            
            if result["success"]:
                return result["data"]
            
            return []
        
        except Exception as e:
            logger.error(f"Error getting user goals: {e}")
            return []
    
    async def _analyze_recent_performance(self, user_id: str) -> Dict[str, Any]:
        """Analyze recent channel performance trends"""
        try:
            # In production, this would analyze recent video performance
            # For now, return simulated data
            
            return {
                "trend": "stable",  # "growing", "declining", "stable"
                "recent_videos_performance": "average",
                "best_performing_video": {
                    "title": "Recent Tutorial",
                    "views": 5000,
                    "ctr": 0.08,
                    "retention": 0.52
                },
                "areas_for_improvement": ["thumbnail design", "video retention"],
                "recent_growth_rate": 0.02  # 2% monthly growth
            }
        
        except Exception as e:
            logger.error(f"Error analyzing recent performance: {e}")
            return {}
    
    async def _analyze_content_strategy(self, user_id: str) -> Dict[str, Any]:
        """Analyze user's content strategy"""
        try:
            # This would analyze upload patterns, content types, etc.
            return {
                "upload_schedule": "weekly",
                "content_types": ["tutorials", "reviews", "vlogs"],
                "average_video_length": "10-15 minutes",
                "consistency_score": 0.7,
                "content_gaps": ["trending topics", "seasonal content"]
            }
        
        except Exception as e:
            logger.error(f"Error analyzing content strategy: {e}")
            return {}
    
    async def _identify_challenges(self, metrics: ChannelMetrics, performance: Dict) -> List[str]:
        """Identify specific challenges based on channel data"""
        challenges = []
        
        try:
            # Low CTR challenge
            if metrics.avg_ctr < 0.04:
                challenges.append("Low click-through rate - thumbnails and titles need optimization")
            
            # Low retention challenge
            if metrics.avg_retention < 0.40:
                challenges.append("Low audience retention - content structure and pacing need improvement")
            
            # Low engagement challenge
            if metrics.engagement_rate < 0.02:
                challenges.append("Low engagement rate - need to encourage more comments and interactions")
            
            # Inconsistent uploads
            if performance.get("consistency_score", 1.0) < 0.5:
                challenges.append("Inconsistent upload schedule affecting algorithm performance")
            
            # Channel size specific challenges
            if metrics.subscriber_count < 1000:
                challenges.append("Building initial subscriber base and establishing channel authority")
            elif metrics.subscriber_count < 10000:
                challenges.append("Breaking through the small creator plateau and scaling content")
            
            return challenges
        
        except Exception as e:
            logger.error(f"Error identifying challenges: {e}")
            return ["General channel optimization needed"]
    
    async def _identify_opportunities(self, metrics: ChannelMetrics, performance: Dict) -> List[str]:
        """Identify specific opportunities based on channel data"""
        opportunities = []
        
        try:
            # High CTR opportunity
            if metrics.avg_ctr > 0.06:
                opportunities.append("Strong thumbnail/title performance - leverage this for more views")
            
            # Good retention opportunity
            if metrics.avg_retention > 0.50:
                opportunities.append("Good retention rate - focus on longer content and series")
            
            # Growing trend opportunity
            if performance.get("recent_growth_rate", 0) > 0.05:
                opportunities.append("Strong growth momentum - scale content production")
            
            # Niche opportunities based on performance
            top_topics = metrics.top_performing_topics or []
            if top_topics:
                opportunities.append(f"Double down on successful topics: {', '.join(top_topics[:3])}")
            
            return opportunities
        
        except Exception as e:
            logger.error(f"Error identifying opportunities: {e}")
            return ["Focus on consistent content creation and audience engagement"]
    
    def _get_size_tier(self, subscriber_count: int) -> str:
        """Determine channel size tier"""
        for tier, (min_subs, max_subs) in self.size_tiers.items():
            if min_subs <= subscriber_count < max_subs:
                return tier
        return "micro"
    
    def _get_default_profile(self, user_id: str) -> ChannelProfile:
        """Get default profile when data is unavailable"""
        return ChannelProfile(
            user_id=user_id,
            channel_id="",
            channel_name="Your Channel",
            niche="General",
            channel_size_tier="micro",
            metrics=ChannelMetrics(),
            goals=[],
            recent_performance={},
            content_strategy={},
            challenges=["Set up channel analytics and define content strategy"],
            opportunities=["Establish consistent content creation and audience engagement"]
        )
    
    async def invalidate_cache(self, user_id: str):
        """Invalidate cached channel profile"""
        if self.redis_service.is_available():
            cache_key = f"channel_profile:{user_id}"
            self.redis_service.delete(cache_key)

# Global analyzer instance
_channel_analyzer: Optional[ChannelAnalyzer] = None

def get_channel_analyzer() -> ChannelAnalyzer:
    """Get or create global channel analyzer instance"""
    global _channel_analyzer
    if _channel_analyzer is None:
        _channel_analyzer = ChannelAnalyzer()
    return _channel_analyzer
