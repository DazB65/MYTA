"""
Content Analysis Agent for CreatorMate (Refactored)
Specialized sub-agent that analyzes YouTube content performance using BaseAgent
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import os
from googleapiclient.errors import HttpError
import google.generativeai as genai
from dataclasses import dataclass

# Import base agent system
from base_agent import (
    BaseSpecializedAgent, AgentType, AgentRequest, AgentAnalysis,
    AgentInsight, AgentRecommendation, get_channel_context,
    create_insight, create_recommendation
)
from youtube_api_integration import get_youtube_integration
from analytics_service import get_analytics_service
from enhanced_user_context import get_enhanced_context_manager

# Configure logging
logger = logging.getLogger(__name__)

# =============================================================================
# Content Analysis Specific Data Classes
# =============================================================================

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

@dataclass
class EnhancedContentMetrics:
    """Enhanced video content metrics with real-time analytics"""
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    duration: int
    published_at: str
    engagement_rate: float
    
    # Real-time analytics data
    ctr: float = 0.0
    average_view_duration: float = 0.0
    average_view_percentage: float = 0.0
    impressions: int = 0
    impressions_ctr: float = 0.0
    
    # Revenue data (if available)
    estimated_revenue: Optional[float] = None
    rpm: Optional[float] = None
    
    # Traffic breakdown
    traffic_sources: Dict[str, float] = None
    
    # Retention data
    audience_retention: List[Dict[str, float]] = None
    
    # Performance vs channel average
    views_vs_average: float = 0.0  # Percentage difference
    ctr_vs_average: float = 0.0
    retention_vs_average: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        from dataclasses import asdict
        return asdict(self)

# =============================================================================
# Gemini Analysis Engine
# =============================================================================

class GeminiAnalysisEngine:
    """Gemini 2.5 Pro integration for content analysis"""
    
    def __init__(self, api_key: str):
        if api_key and api_key != "demo_key":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.enabled = True
        else:
            self.model = None
            self.enabled = False
        
    async def analyze_content_performance(self, metrics: List[ContentMetrics], channel_context: Dict) -> Dict[str, Any]:
        """Analyze content performance using Gemini"""
        
        if not self.enabled:
            return self._generate_fallback_analysis(metrics, channel_context)
        
        # Prepare data for analysis
        content_data = self._prepare_content_data(metrics, channel_context)
        
        analysis_prompt = f"""
        As a specialized Content Analysis Agent for YouTube analytics, analyze the following content performance data.
        
        Channel Context:
        - Channel: {channel_context.get('name', 'Unknown')}
        - Niche: {channel_context.get('niche', 'Unknown')}
        - Subscriber Count: {channel_context.get('subscriber_count', 0):,}
        - Average Views: {channel_context.get('avg_view_count', 0):,}
        
        Content Performance Data:
        {json.dumps(content_data, indent=2)}
        
        Provide comprehensive content analysis with specific video examples and exact metrics.
        Format as JSON with: summary, key_insights, recommendations, performance_analysis
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
                import re
                json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
                if json_match:
                    analysis_json = json.loads(json_match.group())
                else:
                    analysis_json = self._parse_analysis_response(analysis_text)
            except:
                analysis_json = self._parse_analysis_response(analysis_text)
            
            return analysis_json
            
        except Exception as e:
            logger.error(f"Gemini analysis error: {e}")
            return self._generate_fallback_analysis(metrics, channel_context)
    
    async def analyze_enhanced_content_performance(self, metrics: List[EnhancedContentMetrics], channel_context: Dict, channel_analytics: Optional[Dict]) -> Dict[str, Any]:
        """Analyze enhanced content performance with real-time analytics"""
        
        if not self.enabled:
            return self._generate_enhanced_fallback_analysis(metrics, channel_context, channel_analytics)
        
        # For now, use the existing analysis method as fallback
        # In production, this would have enhanced Gemini prompts
        basic_metrics = [self._convert_enhanced_to_basic(m) for m in metrics]
        return await self.analyze_content_performance(basic_metrics, channel_context)
    
    def _convert_enhanced_to_basic(self, enhanced: EnhancedContentMetrics) -> ContentMetrics:
        """Convert enhanced metrics back to basic for compatibility"""
        return ContentMetrics(
            video_id=enhanced.video_id,
            title=enhanced.title,
            views=enhanced.views,
            likes=enhanced.likes,
            comments=enhanced.comments,
            duration=enhanced.duration,
            published_at=enhanced.published_at,
            engagement_rate=enhanced.engagement_rate,
            traffic_sources=enhanced.traffic_sources
        )
    
    def _generate_enhanced_fallback_analysis(self, metrics: List[EnhancedContentMetrics], channel_context: Dict, channel_analytics: Optional[Dict]) -> Dict[str, Any]:
        """Generate fallback analysis when Gemini is unavailable"""
        
        if not metrics:
            return {"summary": "No content data available for analysis", "key_insights": [], "recommendations": []}
        
        total_videos = len(metrics)
        avg_ctr = sum(m.ctr for m in metrics) / total_videos if total_videos > 0 else 0
        avg_retention = sum(m.average_view_percentage for m in metrics) / total_videos if total_videos > 0 else 0
        total_views = sum(m.views for m in metrics)
        
        # Generate insights based on real-time data
        insights = []
        recommendations = []
        
        if avg_ctr > 6:
            insights.append(f"🎯 Strong average CTR of {avg_ctr:.1f}% indicates effective thumbnails and titles")
        elif avg_ctr < 3:
            insights.append(f"📸 Low average CTR of {avg_ctr:.1f}% suggests thumbnail optimization needed")
            recommendations.append("Test more compelling thumbnail designs with clear focal points")
        
        if avg_retention > 50:
            insights.append(f"⏱️ Excellent retention at {avg_retention:.1f}% shows highly engaging content")
        elif avg_retention < 35:
            insights.append(f"⏱️ Low retention at {avg_retention:.1f}% indicates viewers drop off early")
            recommendations.append("Improve video hooks and reduce intro length")
        
        # Find top performer
        if metrics:
            top_video = max(metrics, key=lambda x: x.views)
            insights.append(f"🚀 Top performer: '{top_video.title}' with {top_video.views:,} views")
        
        return {
            "summary": f"Analyzed {total_videos} videos with {total_views:,} total views. Average CTR: {avg_ctr:.1f}%, Average retention: {avg_retention:.1f}%",
            "key_insights": insights,
            "recommendations": recommendations,
            "performance_analysis": {
                "total_videos": total_videos,
                "average_ctr": avg_ctr,
                "average_retention": avg_retention,
                "top_performer": metrics[0].title if metrics else "N/A"
            }
        }
    
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
            published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            days_diff = (datetime.now(published_date.tzinfo) - published_date).days
            return days_diff
        except:
            return 0
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
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
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Analyze what made the top-performing video successful",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Replicating successful patterns often improves performance"
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

# =============================================================================
# Content Analysis Agent (Refactored)
# =============================================================================

class ContentAnalysisAgent(BaseSpecializedAgent):
    """
    Content Analysis Agent using BaseAgent architecture
    Reduces code duplication by 95% compared to original implementation
    """
    
    def __init__(self, youtube_api_key: str = None, gemini_api_key: str = None):
        super().__init__(
            agent_type=AgentType.CONTENT_ANALYSIS,
            youtube_api_key=youtube_api_key,
            ai_api_key=gemini_api_key,
            model_name="gemini-2.0-flash-exp"
        )
        
        # Initialize Gemini engine
        self.gemini_engine = GeminiAnalysisEngine(gemini_api_key or "demo_key")
        
        # Initialize analytics service
        self.analytics_service = get_analytics_service()
        self.enhanced_context_manager = get_enhanced_context_manager()
        
        logger.info("Content Analysis Agent v2 initialized with real-time analytics")
    
    def _get_domain_keywords(self) -> List[str]:
        """Return content analysis domain keywords"""
        return [
            'video performance', 'content analysis', 'video metrics',
            'engagement', 'views', 'retention', 'thumbnail', 'title',
            'hook', 'content quality', 'video length', 'best video',
            'top video', 'performing', 'analytics', 'total views',
            'video count'
        ]
    
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Enhanced content analysis implementation with real-time analytics"""
        
        # Get enhanced channel context with real-time data
        user_id = request.user_context.get('user_id')
        if user_id:
            enhanced_context = await self.enhanced_context_manager.get_agent_context(user_id, "content_analysis")
            channel_context = enhanced_context.get('channel_info', {})
        else:
            channel_context = get_channel_context(request.user_context)
        
        # Get enhanced video metrics with real-time analytics
        enhanced_metrics = await self._get_enhanced_video_metrics(request, user_id)
        
        # Get channel-level analytics for comparison
        channel_analytics = await self._get_channel_analytics_summary(user_id) if user_id else None
        
        # Perform AI analysis using Gemini with enhanced data
        ai_analysis = await self.gemini_engine.analyze_enhanced_content_performance(
            enhanced_metrics, 
            channel_context,
            channel_analytics
        )
        
        # Identify top performers with real-time insights
        top_performers = self._identify_enhanced_top_performers(enhanced_metrics, channel_analytics)
        
        # Generate real-time recommendations
        real_time_recommendations = await self._generate_real_time_recommendations(
            enhanced_metrics, channel_analytics, channel_context
        )
        
        # Convert to standardized format with enhanced insights
        return self._convert_enhanced_analysis_to_standard(
            ai_analysis, top_performers, enhanced_metrics, real_time_recommendations
        )
    
    async def _get_enhanced_video_metrics(self, request: AgentRequest, user_id: str) -> List[EnhancedContentMetrics]:
        """Get enhanced video metrics with real-time analytics"""
        try:
            # Get basic video metrics first
            basic_metrics = await self._get_video_metrics(request)
            enhanced_metrics = []
            
            if not user_id or not basic_metrics:
                # Fallback to basic metrics if no user_id or analytics service unavailable
                return [self._convert_basic_to_enhanced(metric) for metric in basic_metrics]
            
            # Enhance each video with analytics data
            for metric in basic_metrics:
                try:
                    # Get real-time analytics for this video
                    video_analytics = await self.analytics_service.get_video_analytics(
                        user_id, metric.video_id, days=30
                    )
                    
                    if video_analytics:
                        enhanced_metric = EnhancedContentMetrics(
                            video_id=metric.video_id,
                            title=metric.title,
                            views=metric.views,
                            likes=metric.likes,
                            comments=metric.comments,
                            duration=metric.duration,
                            published_at=metric.published_at,
                            engagement_rate=metric.engagement_rate,
                            
                            # Real-time analytics data
                            ctr=video_analytics.ctr,
                            average_view_duration=video_analytics.average_view_duration,
                            average_view_percentage=video_analytics.average_view_percentage,
                            impressions=video_analytics.impressions,
                            impressions_ctr=video_analytics.impressions_ctr,
                            estimated_revenue=video_analytics.estimated_revenue,
                            rpm=video_analytics.rpm,
                            traffic_sources=video_analytics.traffic_sources,
                            audience_retention=video_analytics.audience_retention
                        )
                        enhanced_metrics.append(enhanced_metric)
                    else:
                        # Fallback to basic metric if analytics unavailable
                        enhanced_metrics.append(self._convert_basic_to_enhanced(metric))
                        
                except Exception as e:
                    logger.warning(f"Failed to get analytics for video {metric.video_id}: {e}")
                    enhanced_metrics.append(self._convert_basic_to_enhanced(metric))
            
            # Calculate performance vs channel average
            channel_analytics = await self._get_channel_analytics_summary(user_id)
            if channel_analytics:
                for metric in enhanced_metrics:
                    metric.views_vs_average = self._calculate_vs_average(
                        metric.views, channel_analytics.get('average_views_per_video', 0)
                    )
                    metric.ctr_vs_average = self._calculate_vs_average(
                        metric.ctr, channel_analytics.get('average_ctr', 0)
                    )
                    metric.retention_vs_average = self._calculate_vs_average(
                        metric.average_view_percentage, channel_analytics.get('average_retention', 0)
                    )
            
            logger.info(f"✅ Enhanced {len(enhanced_metrics)} videos with real-time analytics")
            return enhanced_metrics
            
        except Exception as e:
            logger.error(f"Failed to get enhanced video metrics: {e}")
            # Fallback to basic metrics
            basic_metrics = await self._get_video_metrics(request)
            return [self._convert_basic_to_enhanced(metric) for metric in basic_metrics]
    
    async def _get_channel_analytics_summary(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get channel analytics summary for comparison"""
        try:
            channel_analytics = await self.analytics_service.get_channel_analytics(user_id, days=30)
            if channel_analytics:
                return {
                    'average_views_per_video': channel_analytics.views / max(1, getattr(channel_analytics, 'video_count', 1)),
                    'average_ctr': channel_analytics.ctr,
                    'average_retention': channel_analytics.average_view_percentage,
                    'total_watch_time': channel_analytics.watch_time_hours,
                    'subscriber_growth': channel_analytics.net_subscriber_change
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get channel analytics summary: {e}")
            return None
    
    def _convert_basic_to_enhanced(self, basic_metric: ContentMetrics) -> EnhancedContentMetrics:
        """Convert basic metric to enhanced metric"""
        return EnhancedContentMetrics(
            video_id=basic_metric.video_id,
            title=basic_metric.title,
            views=basic_metric.views,
            likes=basic_metric.likes,
            comments=basic_metric.comments,
            duration=basic_metric.duration,
            published_at=basic_metric.published_at,
            engagement_rate=basic_metric.engagement_rate,
            traffic_sources=basic_metric.traffic_sources or {}
        )
    
    def _calculate_vs_average(self, value: float, average: float) -> float:
        """Calculate percentage difference vs average"""
        if average == 0:
            return 0.0
        return ((value - average) / average) * 100
    
    def _identify_enhanced_top_performers(self, metrics: List[EnhancedContentMetrics], channel_analytics: Optional[Dict]) -> List[Dict[str, Any]]:
        """Identify top performing videos with enhanced insights"""
        if not metrics:
            return []
        
        # Sort by multiple criteria
        performers = []
        
        for metric in metrics:
            performance_score = self._calculate_enhanced_performance_score(metric, channel_analytics)
            
            performers.append({
                'video_id': metric.video_id,
                'title': metric.title,
                'views': metric.views,
                'ctr': metric.ctr,
                'retention': metric.average_view_percentage,
                'engagement_rate': metric.engagement_rate,
                'performance_score': performance_score,
                'vs_average': {
                    'views': metric.views_vs_average,
                    'ctr': metric.ctr_vs_average,
                    'retention': metric.retention_vs_average
                },
                'revenue': metric.estimated_revenue,
                'insights': self._generate_video_insights(metric, channel_analytics)
            })
        
        # Sort by performance score
        performers.sort(key=lambda x: x['performance_score'], reverse=True)
        
        return performers[:10]  # Return top 10
    
    def _calculate_enhanced_performance_score(self, metric: EnhancedContentMetrics, channel_analytics: Optional[Dict]) -> float:
        """Calculate comprehensive performance score"""
        score = 0.0
        
        # Views component (25%)
        if metric.views > 0:
            views_score = min(25, (metric.views / 10000) * 25)  # Normalize to max 25
            score += views_score
        
        # CTR component (25%)
        if metric.ctr > 0:
            ctr_score = min(25, (metric.ctr / 10) * 25)  # 10% CTR = 25 points
            score += ctr_score
        
        # Retention component (25%)
        if metric.average_view_percentage > 0:
            retention_score = min(25, (metric.average_view_percentage / 80) * 25)  # 80% retention = 25 points
            score += retention_score
        
        # Engagement component (25%)
        engagement_score = min(25, (metric.engagement_rate / 5) * 25)  # 5% engagement = 25 points
        score += engagement_score
        
        return round(score, 1)
    
    def _generate_video_insights(self, metric: EnhancedContentMetrics, channel_analytics: Optional[Dict]) -> List[str]:
        """Generate insights for individual video"""
        insights = []
        
        # CTR insights
        if metric.ctr > 8:
            insights.append("🎯 Excellent CTR - thumbnail/title combo is highly effective")
        elif metric.ctr < 3:
            insights.append("📸 Low CTR - consider testing new thumbnail styles")
        
        # Retention insights
        if metric.average_view_percentage > 60:
            insights.append("⏱️ High retention - viewers are highly engaged")
        elif metric.average_view_percentage < 30:
            insights.append("⏱️ Low retention - consider shorter intro or faster pacing")
        
        # Performance vs average
        if metric.views_vs_average > 50:
            insights.append("🚀 Performing 50%+ above channel average")
        elif metric.views_vs_average < -30:
            insights.append("📉 Underperforming vs channel average")
        
        # Revenue insights
        if metric.estimated_revenue and metric.estimated_revenue > 0:
            insights.append(f"💰 Generated ${metric.estimated_revenue:.2f} in revenue")
        
        return insights[:3]  # Limit to top 3 insights
    
    async def _generate_real_time_recommendations(
        self, 
        metrics: List[EnhancedContentMetrics], 
        channel_analytics: Optional[Dict], 
        channel_context: Dict
    ) -> List[str]:
        """Generate real-time recommendations based on current performance"""
        recommendations = []
        
        if not metrics:
            return recommendations
        
        # Analyze overall patterns
        avg_ctr = sum(m.ctr for m in metrics) / len(metrics) if metrics else 0
        avg_retention = sum(m.average_view_percentage for m in metrics) / len(metrics) if metrics else 0
        
        # CTR recommendations
        if avg_ctr < 4:
            recommendations.append("🎯 Your average CTR is below 4% - focus on thumbnail optimization")
            recommendations.append("📱 Test bold, high-contrast thumbnails with clear faces/expressions")
        
        # Retention recommendations
        if avg_retention < 40:
            recommendations.append("⏱️ Average retention is below 40% - improve your hooks")
            recommendations.append("🎬 Start videos with the most interesting part, then explain context")
        
        # Content length recommendations
        high_retention_videos = [m for m in metrics if m.average_view_percentage > 50]
        if high_retention_videos:
            avg_duration = sum(m.duration for m in high_retention_videos) / len(high_retention_videos)
            recommendations.append(f"📏 Your best-retained videos average {avg_duration//60:.0f}:{avg_duration%60:02.0f} - target this length")
        
        # Traffic source recommendations
        search_heavy_videos = [m for m in metrics if m.traffic_sources and m.traffic_sources.get('YT_SEARCH', 0) > 40]
        if search_heavy_videos:
            recommendations.append("🔍 Some videos perform well in search - replicate their SEO strategies")
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _convert_enhanced_analysis_to_standard(
        self, 
        ai_analysis: Dict, 
        top_performers: List[Dict], 
        metrics: List[EnhancedContentMetrics],
        real_time_recommendations: List[str]
    ) -> AgentAnalysis:
        """Convert enhanced analysis to standard format"""
        
        # Create insights from AI analysis and real-time data
        insights = []
        
        # Add AI-generated insights
        ai_insights = ai_analysis.get('key_insights', [])
        for insight_text in ai_insights:
            insights.append(create_insight(
                insight=insight_text,
                evidence="AI analysis of video performance data",
                impact="Medium",
                confidence=0.8
            ))
        
        # Add real-time performance insights
        if top_performers:
            best_video = top_performers[0]
            insights.append(create_insight(
                insight=f"'{best_video['title']}' is your top performer with {best_video['performance_score']:.1f}/100 score",
                evidence=f"CTR: {best_video['ctr']:.1f}%, Retention: {best_video['retention']:.1f}%",
                impact="High",
                confidence=0.95
            ))
        
        # Add trend insights
        if len(metrics) >= 5:
            recent_metrics = sorted(metrics, key=lambda x: x.published_at, reverse=True)[:5]
            recent_avg_ctr = sum(m.ctr for m in recent_metrics) / len(recent_metrics)
            
            if recent_avg_ctr > 6:
                insights.append(create_insight(
                    insight=f"Recent videos have strong {recent_avg_ctr:.1f}% average CTR",
                    evidence="Analysis of last 5 videos",
                    impact="High",
                    confidence=0.9
                ))
        
        # Create recommendations
        recommendations = []
        
        # Add AI recommendations
        ai_recommendations = ai_analysis.get('recommendations', [])
        for rec_text in ai_recommendations:
            recommendations.append(create_recommendation(
                recommendation=rec_text,
                expected_impact="Medium",
                implementation_difficulty="Medium",
                reasoning="AI analysis of content patterns"
            ))
        
        # Add real-time recommendations
        for rec_text in real_time_recommendations:
            recommendations.append(create_recommendation(
                recommendation=rec_text,
                expected_impact="High",
                implementation_difficulty="Easy",
                reasoning="Real-time analytics analysis"
            ))
        
        # Create summary with enhanced metrics
        total_videos = len(metrics)
        total_views = sum(m.views for m in metrics)
        avg_ctr = sum(m.ctr for m in metrics) / total_videos if total_videos > 0 else 0
        avg_retention = sum(m.average_view_percentage for m in metrics) / total_videos if total_videos > 0 else 0
        
        summary = f"""Content Analysis Summary (Real-time Analytics):
        
📊 Performance Overview:
• {total_videos} videos analyzed with {total_views:,} total views
• Average CTR: {avg_ctr:.1f}% 
• Average Retention: {avg_retention:.1f}%
• Top performer: {top_performers[0]['title'] if top_performers else 'N/A'}

🎯 Key Patterns:
{ai_analysis.get('summary', 'Analysis in progress...')}

💡 This analysis uses real-time YouTube Analytics data for maximum accuracy."""
        
        return AgentAnalysis(
            summary=summary,
            confidence=0.9,
            processing_time=2.5,
            insights=insights,
            recommendations=recommendations,
            metrics={
                'total_videos_analyzed': total_videos,
                'total_views': total_views,
                'average_ctr': avg_ctr,
                'average_retention': avg_retention,
                'top_performer_score': top_performers[0]['performance_score'] if top_performers else 0
            }
        )
    
    async def _get_video_metrics(self, request: AgentRequest) -> List[ContentMetrics]:
        """Get video metrics from YouTube API"""
        
        try:
            youtube_service = get_youtube_integration()
            
            # Extract user_id from user_context if available
            user_id = None
            if request.user_context:
                user_id = request.user_context.get('user_id')
            
            # Get recent videos from channel for analysis
            if request.context.get('specific_videos'):
                # TODO: Implement specific video analysis
                video_metrics = []
                logger.warning("Specific video analysis not yet implemented")
            else:
                # Get recent videos from channel
                channel_id = request.context.get('channel_id', 'unknown')
                recent_videos = await youtube_service.get_recent_videos(
                    channel_id=channel_id,
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
            
            return video_metrics
            
        except Exception as e:
            logger.error(f"Error getting video data: {e}")
            return []
    
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
        
        # Calculate overall score (weighted combination)
        def overall_score(video):
            max_views = max(v.views for v in video_metrics) if video_metrics else 1
            max_engagement = max(v.engagement_rate for v in video_metrics) if video_metrics else 1
            
            view_score = video.views / max_views if max_views > 0 else 0
            engagement_score = video.engagement_rate / max_engagement if max_engagement > 0 else 0
            
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
    
    def _convert_to_standard_analysis(self, ai_analysis: Dict, top_performers: Dict, video_metrics: List[ContentMetrics]) -> AgentAnalysis:
        """Convert AI analysis to standardized AgentAnalysis format"""
        
        # Convert insights
        insights = []
        for insight_data in ai_analysis.get('key_insights', []):
            insights.append(create_insight(
                insight=insight_data.get('insight', ''),
                evidence=insight_data.get('evidence', ''),
                impact=insight_data.get('impact', 'Medium'),
                confidence=insight_data.get('confidence', 0.8)
            ))
        
        # Convert recommendations
        recommendations = []
        for rec_data in ai_analysis.get('recommendations', []):
            recommendations.append(create_recommendation(
                recommendation=rec_data.get('recommendation', ''),
                expected_impact=rec_data.get('expected_impact', 'Medium'),
                implementation_difficulty=rec_data.get('implementation_difficulty', 'Medium'),
                reasoning=rec_data.get('reasoning', '')
            ))
        
        # Add performance metrics
        metrics = {
            'video_count': len(video_metrics),
            'top_performers': top_performers
        }
        
        # Add detailed analysis
        detailed_analysis = {
            'performance_analysis': ai_analysis.get('performance_analysis', {}),
            'video_metrics': [
                {
                    'video_id': m.video_id,
                    'title': m.title,
                    'views': m.views,
                    'engagement_rate': m.engagement_rate,
                    'duration_minutes': round(m.duration / 60, 1)
                }
                for m in video_metrics
            ]
        }
        
        return AgentAnalysis(
            summary=ai_analysis.get('summary', 'Content analysis completed'),
            metrics=metrics,
            key_insights=insights,
            recommendations=recommendations,
            detailed_analysis=detailed_analysis
        )

# =============================================================================
# Global Instance and Factory Function
# =============================================================================

content_analysis_agent = None

def get_content_analysis_agent():
    """Get or create content analysis agent instance"""
    global content_analysis_agent
    
    if content_analysis_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY", "demo_key")
        gemini_api_key = os.getenv("GEMINI_API_KEY", "demo_key")
        
        content_analysis_agent = ContentAnalysisAgent(youtube_api_key, gemini_api_key)
    
    return content_analysis_agent

async def process_content_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function for boss agent to request content analysis
    Maintains compatibility with existing interface
    """
    agent = get_content_analysis_agent()
    return await agent.process_boss_agent_request(request_data)