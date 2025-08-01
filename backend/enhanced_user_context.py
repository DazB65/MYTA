"""
Enhanced User Context System for Vidalytics
Provides real-time, intelligence-enriched user context for agents
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json

from ai_services import get_user_context, update_user_context
from analytics_service import get_analytics_service
from realtime_data_pipeline import get_data_pipeline
from oauth_manager import get_oauth_manager

logger = logging.getLogger(__name__)

@dataclass
class EnhancedChannelContext:
    """Enhanced channel context with real-time data"""
    # Basic channel info
    name: str
    channel_id: str
    niche: str
    content_type: str
    
    # Static metrics (from onboarding)
    subscriber_count: int
    video_count: int
    total_view_count: int
    
    # Real-time performance data (last 7 days)
    recent_views: int
    recent_watch_time_hours: float
    recent_ctr: float
    recent_retention: float
    recent_subscriber_change: int
    recent_engagement_rate: float
    
    # Performance trends
    views_trend: str  # 'up', 'down', 'stable'
    ctr_trend: str
    retention_trend: str
    subscriber_trend: str
    
    # Traffic insights
    top_traffic_source: str
    traffic_source_breakdown: Dict[str, float]
    
    # Content pillars performance
    pillar_performance: List[Dict[str, Any]]
    top_performing_pillar: Optional[str]
    underperforming_pillars: List[str]
    
    # Audience insights
    top_countries: List[Dict[str, Any]]
    audience_age_gender: Dict[str, float]
    
    # Performance insights
    performance_alerts: List[str]
    key_insights: List[str]
    recommendations: List[str]
    
    # Data freshness
    last_updated: str
    data_quality: str  # 'real-time', 'recent', 'stale'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for agent use"""
        return asdict(self)

class EnhancedUserContextManager:
    """Manages enhanced user context with real-time data integration"""
    
    def __init__(self):
        self.analytics_service = get_analytics_service()
        self.data_pipeline = get_data_pipeline()
        self.oauth_manager = get_oauth_manager()
        self._context_cache: Dict[str, Any] = {}
        self._cache_ttl = 900  # 15 minutes
    
    async def get_enhanced_context(self, user_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get comprehensive, real-time enhanced context for user
        
        Args:
            user_id: User ID
            force_refresh: Force fresh data fetch
            
        Returns:
            Enhanced context dictionary with real-time data
        """
        try:
            # Register user activity for data pipeline
            await self.data_pipeline.register_user_activity(user_id, "context_request")
            
            # Check cache first
            cache_key = f"enhanced_context_{user_id}"
            if not force_refresh and self._is_cache_valid(cache_key):
                logger.info(f"Returning cached enhanced context for {user_id}")
                return self._context_cache[cache_key]['data']
            
            # Get base user context
            base_context = get_user_context(user_id)
            
            # Get real-time analytics context
            realtime_context = await self.data_pipeline.get_real_time_context(user_id)
            
            # Build enhanced channel context
            enhanced_channel = await self._build_enhanced_channel_context(
                user_id, base_context, realtime_context
            )
            
            # Build complete enhanced context
            enhanced_context = {
                'user_id': user_id,
                'channel_info': enhanced_channel.to_dict() if enhanced_channel else base_context.get('channel_info', {}),
                'realtime_data': realtime_context,
                'conversation_history': base_context.get('conversation_history', []),
                'preferences': base_context.get('preferences', {}),
                'last_updated': datetime.now().isoformat(),
                'context_type': 'enhanced_realtime'
            }
            
            # Add intelligence layer
            enhanced_context['intelligence'] = await self._add_intelligence_layer(
                user_id, enhanced_context
            )
            
            # Cache the result
            self._cache_context(cache_key, enhanced_context)
            
            logger.info(f"✅ Built enhanced context for {user_id} with real-time data")
            return enhanced_context
            
        except Exception as e:
            logger.error(f"Failed to get enhanced context for {user_id}: {e}")
            import traceback
            logger.error(f"Full enhanced context error traceback: {traceback.format_exc()}")
            
            # Enhanced error analysis and recovery
            error_context = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "user_id": user_id,
                "fallback_used": True,
                "timestamp": datetime.now().isoformat()
            }
            
            # Analyze specific failure types for better recovery
            if "oauth" in str(e).lower() or "token" in str(e).lower():
                error_context["likely_cause"] = "oauth_issue"
                error_context["recovery_suggestion"] = "refresh_oauth_token"
                logger.warning(f"🔐 OAuth-related error in enhanced context for {user_id}: {e}")
            elif "analytics" in str(e).lower() or "youtube" in str(e).lower():
                error_context["likely_cause"] = "analytics_api_issue"
                error_context["recovery_suggestion"] = "retry_analytics_later"
                logger.warning(f"📈 Analytics API error in enhanced context for {user_id}: {e}")
            elif "database" in str(e).lower() or "sqlite" in str(e).lower():
                error_context["likely_cause"] = "database_issue"
                error_context["recovery_suggestion"] = "check_database_schema"
                logger.warning(f"💾 Database error in enhanced context for {user_id}: {e}")
            elif "timeout" in str(e).lower() or "connection" in str(e).lower():
                error_context["likely_cause"] = "network_timeout"
                error_context["recovery_suggestion"] = "retry_with_timeout"
                logger.warning(f"🌐 Network/timeout error in enhanced context for {user_id}: {e}")
            else:
                error_context["likely_cause"] = "unknown"
                error_context["recovery_suggestion"] = "manual_investigation"
            
            # Try multiple fallback approaches
            fallback_context = await self._attempt_enhanced_fallback(user_id, error_context)
            
            if fallback_context:
                logger.info(f"✅ Enhanced fallback successful for {user_id}")
                return fallback_context
            else:
                # Final fallback to basic context
                logger.warning(f"🔄 Using basic context fallback for {user_id}")
                base_context = get_user_context(user_id)
                base_context['enhanced_context_error'] = error_context
                base_context['context_type'] = 'basic_fallback_after_error'
                base_context['oauth_status'] = self.oauth_manager.get_oauth_status(user_id)
                
                return base_context
    
    async def _attempt_enhanced_fallback(self, user_id: str, error_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Attempt enhanced fallback strategies based on error type"""
        try:
            logger.info(f"🔄 Attempting enhanced fallback for {user_id} due to {error_context.get('likely_cause')}")
            
            # Get base context first
            base_context = get_user_context(user_id)
            
            # Try to get OAuth status regardless of previous errors
            oauth_status = {}
            try:
                oauth_status = self.oauth_manager.get_oauth_status(user_id)
                logger.info(f"✅ Got OAuth status in fallback: {oauth_status.get('authenticated', False)}")
            except Exception as oauth_e:
                logger.warning(f"Could not get OAuth status in fallback: {oauth_e}")
                oauth_status = {"authenticated": False, "error": str(oauth_e)}
            
            # Create enhanced fallback context with available data
            fallback_context = {
                'user_id': user_id,
                'channel_info': base_context.get('channel_info', self._get_empty_channel_info()),
                'conversation_history': base_context.get('conversation_history', []),
                'preferences': base_context.get('preferences', {}),
                'oauth_status': oauth_status,
                'realtime_data': {},  # Empty but structured
                'intelligence': {},   # Empty but available for basic insights
                'last_updated': datetime.now().isoformat(),
                'context_type': 'enhanced_fallback',
                'fallback_reason': error_context.get('likely_cause', 'unknown'),
                'data_quality': 'fallback'
            }
            
            # Try to add some basic intelligence even without real-time data
            try:
                fallback_context['intelligence'] = await self._generate_basic_intelligence(
                    user_id, fallback_context
                )
                logger.info(f"✅ Added basic intelligence to fallback context")
            except Exception as intel_e:
                logger.warning(f"Could not add basic intelligence: {intel_e}")
                fallback_context['intelligence'] = {}
            
            # If OAuth is working, try to get minimal real-time data
            if oauth_status.get('authenticated', False) and error_context.get('likely_cause') != 'oauth_issue':
                try:
                    logger.info(f"🔄 Attempting minimal real-time data fetch in fallback")
                    minimal_data = await self._get_minimal_realtime_data(user_id)
                    if minimal_data:
                        fallback_context['realtime_data'] = minimal_data
                        fallback_context['data_quality'] = 'minimal_realtime'
                        logger.info(f"✅ Added minimal real-time data to fallback")
                except Exception as minimal_e:
                    logger.warning(f"Minimal real-time data fetch failed: {minimal_e}")
            
            logger.info(f"✅ Enhanced fallback context created for {user_id}")
            return fallback_context
            
        except Exception as fallback_e:
            logger.error(f"Enhanced fallback also failed for {user_id}: {fallback_e}")
            return None
    
    def _get_empty_channel_info(self) -> Dict[str, Any]:
        """Get empty channel info structure for fallbacks"""
        return {
            "name": "Unknown",
            "channel_id": "",
            "niche": "Unknown",
            "content_type": "Unknown",
            "subscriber_count": 0,
            "avg_view_count": 0,
            "total_view_count": 0,
            "video_count": 0,
            "ctr": 0,
            "retention": 0,
            "recent_views": 0,
            "recent_ctr": 0,
            "recent_retention": 0,
            "recent_engagement_rate": 0,
            "recent_subscriber_change": 0,
            "upload_frequency": "Unknown",
            "video_length": "Unknown",
            "monetization_status": "Unknown",
            "primary_goal": "Unknown",
            "notes": "",
            "last_message": ""
        }
    
    async def _generate_basic_intelligence(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic intelligence insights even without real-time data"""
        try:
            channel_info = context.get('channel_info', {})
            subscriber_count = channel_info.get('subscriber_count', 0)
            niche = channel_info.get('niche', 'Unknown')
            
            intelligence = {
                'performance_score': 0,  # Can't calculate without real-time data
                'growth_opportunities': [
                    f"Connect YouTube Analytics for personalized growth insights",
                    f"Consider content optimization for the {niche} niche",
                    "Regular content scheduling can improve channel performance"
                ],
                'optimization_priorities': [
                    "Enable YouTube Analytics integration",
                    "Establish consistent upload schedule",
                    "Focus on audience retention strategies"
                ],
                'competitive_position': f"Channel has {subscriber_count:,} subscribers in {niche} niche",
                'content_recommendations': [
                    f"Create content targeted at {niche} audience",
                    "Use analytics to identify top-performing content themes",
                    "Experiment with different video formats"
                ],
                'fallback_mode': True
            }
            
            return intelligence
            
        except Exception as e:
            logger.error(f"Failed to generate basic intelligence: {e}")
            return {'fallback_mode': True, 'error': str(e)}
    
    async def _get_minimal_realtime_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get minimal real-time data for fallback scenarios"""
        try:
            # Try to get just basic channel analytics with reduced scope
            channel_analytics = await self.analytics_service.get_channel_analytics(
                user_id, days=7, force_refresh=False  # Use cache if available
            )
            
            if channel_analytics:
                return {
                    'key_metrics': {
                        'current_week_views': channel_analytics.views,
                        'current_week_ctr': channel_analytics.ctr,
                        'current_week_retention': channel_analytics.average_view_percentage,
                        'subscriber_change': channel_analytics.net_subscriber_change
                    },
                    'performance_summary': {
                        'current_period': {
                            'views': channel_analytics.views,
                            'ctr': channel_analytics.ctr,
                            'average_view_percentage': channel_analytics.average_view_percentage,
                            'net_subscriber_change': channel_analytics.net_subscriber_change
                        }
                    },
                    'data_type': 'minimal_fallback'
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Minimal real-time data fetch failed: {e}")
            return None
    
    async def get_agent_context(self, user_id: str, agent_type: str) -> Dict[str, Any]:
        """
        Get context optimized for specific agent type with enhanced error handling
        
        Args:
            user_id: User ID
            agent_type: Type of agent requesting context
            
        Returns:
            Agent-optimized context
        """
        try:
            logger.info(f"🤖 Getting {agent_type} context for user {user_id}")
            
            # Get enhanced context with retries
            enhanced_context = None
            max_retries = 2
            
            for attempt in range(max_retries):
                try:
                    enhanced_context = await self.get_enhanced_context(user_id)
                    if enhanced_context:
                        logger.info(f"✅ Enhanced context retrieved on attempt {attempt + 1}")
                        break
                except Exception as context_e:
                    logger.warning(f"Enhanced context attempt {attempt + 1} failed: {context_e}")
                    if attempt == max_retries - 1:
                        # On final failure, create minimal context
                        logger.warning(f"Creating minimal context for {agent_type} agent")
                        enhanced_context = await self._create_minimal_agent_context(user_id, agent_type)
            
            if not enhanced_context:
                logger.error(f"Could not get any context for {agent_type} agent")
                return await self._create_minimal_agent_context(user_id, agent_type)
            
            # Optimize for specific agent type
            try:
                if agent_type == "content_analysis":
                    optimized = self._optimize_for_content_agent(enhanced_context)
                elif agent_type == "audience_insights":
                    optimized = self._optimize_for_audience_agent(enhanced_context)
                elif agent_type == "seo_discoverability":
                    optimized = self._optimize_for_seo_agent(enhanced_context)
                elif agent_type == "competitive_analysis":
                    optimized = self._optimize_for_competitive_agent(enhanced_context)
                elif agent_type == "monetization_strategy":
                    optimized = self._optimize_for_monetization_agent(enhanced_context)
                else:
                    optimized = enhanced_context
                
                logger.info(f"✅ Context optimized for {agent_type} agent")
                return optimized
                
            except Exception as opt_e:
                logger.error(f"Context optimization failed for {agent_type}: {opt_e}")
                # Return unoptimized context rather than failing
                return enhanced_context
            
        except Exception as e:
            logger.error(f"Critical error getting agent context for {agent_type}: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return await self._create_minimal_agent_context(user_id, agent_type)
    
    async def _create_minimal_agent_context(self, user_id: str, agent_type: str) -> Dict[str, Any]:
        """Create minimal context for agent when enhanced context fails"""
        try:
            # Get basic user context
            base_context = get_user_context(user_id)
            
            minimal_context = {
                'user_id': user_id,
                'channel_info': base_context.get('channel_info', self._get_empty_channel_info()),
                'conversation_history': base_context.get('conversation_history', []),
                'realtime_data': {},
                'intelligence': {},
                'context_type': f'minimal_{agent_type}',
                'data_quality': 'minimal_fallback',
                'last_updated': datetime.now().isoformat(),
                'agent_type': agent_type,
                'fallback_mode': True
            }
            
            # Add OAuth status if possible
            try:
                minimal_context['oauth_status'] = self.oauth_manager.get_oauth_status(user_id)
            except:
                minimal_context['oauth_status'] = {'authenticated': False, 'error': 'status_unavailable'}
            
            # Add agent-specific minimal data
            if agent_type == "content_analysis":
                minimal_context['focus_areas'] = ['basic_metrics', 'fallback_recommendations']
            elif agent_type == "audience_insights":
                minimal_context['focus_areas'] = ['subscriber_info', 'basic_demographics']
            elif agent_type in ["seo_discoverability", "competitive_analysis", "monetization_strategy"]:
                minimal_context['focus_areas'] = ['basic_guidance', 'general_recommendations']
            
            logger.info(f"✅ Created minimal {agent_type} context for {user_id}")
            return minimal_context
            
        except Exception as e:
            logger.error(f"Failed to create minimal context for {agent_type}: {e}")
            # Absolute fallback
            return {
                'user_id': user_id,
                'agent_type': agent_type,
                'context_type': 'absolute_fallback',
                'error': str(e),
                'fallback_mode': True,
                'channel_info': self._get_empty_channel_info()
            }
    
    async def _build_enhanced_channel_context(
        self, 
        user_id: str, 
        base_context: Dict[str, Any], 
        realtime_context: Dict[str, Any]
    ) -> Optional[EnhancedChannelContext]:
        """Build enhanced channel context with real-time data"""
        try:
            base_channel = base_context.get('channel_info', {})
            performance_summary = realtime_context.get('performance_summary', {})
            
            if not base_channel or not performance_summary:
                return None
            
            current_period = performance_summary.get('current_period', {})
            performance_changes = performance_summary.get('performance_changes', {})
            
            # Build enhanced context
            enhanced_channel = EnhancedChannelContext(
                # Basic info
                name=base_channel.get('name', 'Unknown'),
                channel_id=base_channel.get('channel_id', ''),
                niche=base_channel.get('niche', 'Unknown'),
                content_type=base_channel.get('content_type', 'Unknown'),
                
                # Static metrics
                subscriber_count=base_channel.get('subscriber_count', 0),
                video_count=base_channel.get('video_count', 0),
                total_view_count=base_channel.get('total_view_count', 0),
                
                # Real-time performance
                recent_views=current_period.get('views', 0),
                recent_watch_time_hours=current_period.get('watch_time_hours', 0.0),
                recent_ctr=current_period.get('ctr', 0.0),
                recent_retention=current_period.get('average_view_percentage', 0.0),
                recent_subscriber_change=current_period.get('net_subscriber_change', 0),
                recent_engagement_rate=self._calculate_engagement_rate(current_period),
                
                # Trends
                views_trend=self._classify_trend(performance_changes.get('views_change', 0)),
                ctr_trend=self._classify_trend(performance_changes.get('ctr_change', 0)),
                retention_trend=self._classify_trend(performance_changes.get('retention_change', 0)),
                subscriber_trend=self._classify_trend(performance_changes.get('subscribers_change', 0)),
                
                # Traffic insights
                top_traffic_source=realtime_context.get('key_metrics', {}).get('top_traffic_source', 'Unknown'),
                traffic_source_breakdown={
                    'YouTube Search': current_period.get('traffic_source_youtube_search', 0),
                    'Suggested Videos': current_period.get('traffic_source_suggested_videos', 0),
                    'External': current_period.get('traffic_source_external', 0),
                    'Direct/Other': current_period.get('traffic_source_direct', 0) + current_period.get('traffic_source_browse_features', 0)
                },
                
                # Content pillars performance (simple real data)
                pillar_performance=await self._get_pillar_performance(user_id),
                top_performing_pillar=await self._get_top_performing_pillar(user_id),
                underperforming_pillars=await self._get_underperforming_pillars(user_id),
                
                # Audience insights
                top_countries=current_period.get('top_countries', []),
                audience_age_gender=current_period.get('age_gender_breakdown', {}),
                
                # Performance insights
                performance_alerts=[alert['message'] for alert in realtime_context.get('recent_alerts', [])],
                key_insights=realtime_context.get('performance_insights', []),
                recommendations=await self._generate_smart_recommendations(user_id, current_period, performance_changes),
                
                # Data quality
                last_updated=datetime.now().isoformat(),
                data_quality='real-time' if realtime_context else 'stale'
            )
            
            return enhanced_channel
            
        except Exception as e:
            logger.error(f"Failed to build enhanced channel context: {e}")
            return None
    
    async def _add_intelligence_layer(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Add AI-powered intelligence insights to context"""
        try:
            intelligence = {
                'performance_score': await self._calculate_performance_score(context),
                'growth_opportunities': await self._identify_growth_opportunities(context),
                'optimization_priorities': await self._get_optimization_priorities(context),
                'competitive_position': await self._assess_competitive_position(context),
                'content_recommendations': await self._get_content_recommendations(context)
            }
            
            return intelligence
            
        except Exception as e:
            logger.error(f"Failed to add intelligence layer: {e}")
            return {}
    
    async def _generate_smart_recommendations(
        self, 
        user_id: str, 
        current_period: Dict[str, Any], 
        performance_changes: Dict[str, Any]
    ) -> List[str]:
        """Generate smart, actionable recommendations"""
        recommendations = []
        
        try:
            # CTR recommendations
            ctr = current_period.get('ctr', 0)
            ctr_change = performance_changes.get('ctr_change', 0)
            
            if ctr < 3:
                recommendations.append("🎯 Your CTR is below 3% - focus on more compelling thumbnails and titles")
            elif ctr > 8:
                recommendations.append("🎯 Excellent CTR! Your thumbnails and titles are performing well")
            
            if ctr_change < -15:
                recommendations.append("📉 CTR dropped significantly - review recent thumbnail/title strategy")
            
            # Retention recommendations
            retention = current_period.get('average_view_percentage', 0)
            retention_change = performance_changes.get('retention_change', 0)
            
            if retention < 30:
                recommendations.append("⏱️ Low retention suggests viewers drop off early - try shorter intros")
            elif retention > 60:
                recommendations.append("⏱️ Great retention! Your content keeps viewers engaged")
            
            if retention_change < -10:
                recommendations.append("⏱️ Retention declining - analyze where viewers drop off")
            
            # Subscriber recommendations
            subscriber_change = current_period.get('net_subscriber_change', 0)
            if subscriber_change < 0:
                recommendations.append("👥 Losing subscribers - review content quality and posting consistency")
            elif subscriber_change > 50:
                recommendations.append("👥 Strong subscriber growth! Maintain current content strategy")
            
            # Traffic source recommendations
            search_traffic = current_period.get('traffic_source_youtube_search', 0)
            if search_traffic > 40:
                recommendations.append("🔍 Strong search performance - continue optimizing SEO")
            elif search_traffic < 15:
                recommendations.append("🔍 Low search traffic - improve titles, descriptions, and tags")
            
            return recommendations[:5]  # Limit to top 5
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []
    
    def _calculate_engagement_rate(self, period_data: Dict[str, Any]) -> float:
        """Calculate engagement rate from period data"""
        try:
            views = period_data.get('views', 0)
            if views == 0:
                return 0.0
            
            likes = period_data.get('likes', 0)
            comments = period_data.get('comments', 0)
            shares = period_data.get('shares', 0)
            
            total_engagement = likes + comments + shares
            return (total_engagement / views) * 100
            
        except Exception:
            return 0.0
    
    def _classify_trend(self, change_percentage: float) -> str:
        """Classify trend based on percentage change"""
        if change_percentage > 10:
            return 'up'
        elif change_percentage < -10:
            return 'down'
        else:
            return 'stable'
    
    async def _calculate_performance_score(self, context: Dict[str, Any]) -> float:
        """Calculate overall performance score (0-100)"""
        try:
            channel_info = context.get('channel_info', {})
            
            # Score components (each 0-25 points)
            ctr_score = min(25, (channel_info.get('recent_ctr', 0) / 10) * 25)
            retention_score = min(25, (channel_info.get('recent_retention', 0) / 80) * 25)
            engagement_score = min(25, (channel_info.get('recent_engagement_rate', 0) / 5) * 25)
            growth_score = min(25, max(0, channel_info.get('recent_subscriber_change', 0) / 10) * 25)
            
            total_score = ctr_score + retention_score + engagement_score + growth_score
            return round(total_score, 1)
            
        except Exception:
            return 0.0
    
    async def _identify_growth_opportunities(self, context: Dict[str, Any]) -> List[str]:
        """Identify growth opportunities based on data"""
        opportunities = []
        
        try:
            channel_info = context.get('channel_info', {})
            traffic_sources = channel_info.get('traffic_source_breakdown', {})
            
            # Traffic diversification opportunities
            search_traffic = traffic_sources.get('YouTube Search', 0)
            suggested_traffic = traffic_sources.get('Suggested Videos', 0)
            external_traffic = traffic_sources.get('External', 0)
            
            if search_traffic < 30:
                opportunities.append("Improve SEO optimization for better search visibility")
            
            if suggested_traffic < 20:
                opportunities.append("Create content that triggers algorithm recommendations")
            
            if external_traffic < 10:
                opportunities.append("Expand social media presence to drive external traffic")
            
            # Performance opportunities
            if channel_info.get('recent_ctr', 0) < 5:
                opportunities.append("A/B test thumbnails and titles for higher CTR")
            
            if channel_info.get('recent_retention', 0) < 50:
                opportunities.append("Analyze retention graphs to improve content structure")
            
            return opportunities[:3]  # Top 3 opportunities
            
        except Exception as e:
            logger.error(f"Failed to identify growth opportunities: {e}")
            return []
    
    async def _get_optimization_priorities(self, context: Dict[str, Any]) -> List[str]:
        """Get optimization priorities based on current performance"""
        priorities = []
        
        try:
            channel_info = context.get('channel_info', {})
            
            # Prioritize based on current weaknesses
            ctr = channel_info.get('recent_ctr', 0)
            retention = channel_info.get('recent_retention', 0)
            engagement = channel_info.get('recent_engagement_rate', 0)
            
            if ctr < 3:
                priorities.append("HIGH: Thumbnail and title optimization")
            elif ctr < 5:
                priorities.append("MEDIUM: Thumbnail and title improvement")
            
            if retention < 30:
                priorities.append("HIGH: Content structure and pacing")
            elif retention < 50:
                priorities.append("MEDIUM: Audience retention optimization")
            
            if engagement < 1:
                priorities.append("HIGH: Audience engagement strategies")
            elif engagement < 2:
                priorities.append("MEDIUM: Community building")
            
            return priorities
            
        except Exception:
            return []
    
    async def _assess_competitive_position(self, context: Dict[str, Any]) -> str:
        """Assess competitive position (simplified)"""
        try:
            channel_info = context.get('channel_info', {})
            performance_score = await self._calculate_performance_score(context)
            
            if performance_score >= 80:
                return "Strong performer in niche"
            elif performance_score >= 60:
                return "Above average performance"
            elif performance_score >= 40:
                return "Average performance with room for improvement"
            else:
                return "Below average performance, needs optimization"
                
        except Exception:
            return "Position assessment unavailable"
    
    async def _get_content_recommendations(self, context: Dict[str, Any]) -> List[str]:
        """Get content strategy recommendations"""
        try:
            channel_info = context.get('channel_info', {})
            niche = channel_info.get('niche', '').lower()
            
            # Generic content recommendations based on performance
            recommendations = []
            
            if channel_info.get('recent_retention', 0) < 40:
                recommendations.append("Create shorter, more engaging introductions")
                recommendations.append("Use pattern interrupts every 30-60 seconds")
            
            if channel_info.get('recent_ctr', 0) < 4:
                recommendations.append("Test bold, contrasting thumbnail designs")
                recommendations.append("Use emotional triggers in titles")
            
            if channel_info.get('recent_engagement_rate', 0) < 1.5:
                recommendations.append("Ask more questions to encourage comments")
                recommendations.append("Create community posts to boost engagement")
            
            return recommendations[:3]
            
        except Exception:
            return []
    
    def _optimize_for_content_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize context for content analysis agent"""
        return {
            **context,
            'focus_areas': ['retention', 'ctr', 'engagement', 'video_performance'],
            'key_metrics': context.get('realtime_data', {}).get('key_metrics', {}),
            'performance_trends': {
                'views_trend': context.get('channel_info', {}).get('views_trend'),
                'ctr_trend': context.get('channel_info', {}).get('ctr_trend'),
                'retention_trend': context.get('channel_info', {}).get('retention_trend')
            }
        }
    
    def _optimize_for_audience_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize context for audience insights agent"""
        return {
            **context,
            'focus_areas': ['demographics', 'engagement', 'subscriber_growth', 'community'],
            'audience_data': {
                'top_countries': context.get('channel_info', {}).get('top_countries', []),
                'age_gender': context.get('channel_info', {}).get('audience_age_gender', {}),
                'engagement_rate': context.get('channel_info', {}).get('recent_engagement_rate', 0)
            }
        }
    
    def _optimize_for_seo_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize context for SEO agent"""
        return {
            **context,
            'focus_areas': ['search_traffic', 'discoverability', 'keywords', 'optimization'],
            'traffic_data': context.get('channel_info', {}).get('traffic_source_breakdown', {}),
            'search_performance': context.get('channel_info', {}).get('traffic_source_breakdown', {}).get('YouTube Search', 0)
        }
    
    def _optimize_for_competitive_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize context for competitive analysis agent"""
        return {
            **context,
            'focus_areas': ['benchmarking', 'market_position', 'opportunities', 'gaps'],
            'performance_score': context.get('intelligence', {}).get('performance_score', 0),
            'competitive_position': context.get('intelligence', {}).get('competitive_position', '')
        }
    
    def _optimize_for_monetization_agent(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize context for monetization agent"""
        return {
            **context,
            'focus_areas': ['revenue', 'optimization', 'opportunities', 'growth'],
            'revenue_data': context.get('realtime_data', {}).get('performance_summary', {}).get('current_period', {}).get('estimated_revenue'),
            'subscriber_growth': context.get('channel_info', {}).get('recent_subscriber_change', 0)
        }
    
    async def _get_pillar_performance(self, user_id: str) -> List[Dict[str, Any]]:
        """Get simple pillar performance data using real YouTube metrics"""
        try:
            from database import db_manager
            pillars = db_manager.get_content_pillars(user_id)
            
            pillar_data = []
            for pillar in pillars:
                videos = db_manager.get_videos_for_pillar(user_id, pillar['id'])
                if videos:
                    avg_views = sum(v.get('view_count', 0) for v in videos) / len(videos)
                    avg_ctr = sum(v.get('ctr', 0) for v in videos) / len(videos)
                    avg_retention = sum(v.get('average_view_percentage', 0) for v in videos) / len(videos)
                    
                    pillar_data.append({
                        'name': pillar['name'],
                        'video_count': len(videos),
                        'avg_views': round(avg_views),
                        'avg_ctr': round(avg_ctr, 2),
                        'avg_retention': round(avg_retention, 1)
                    })
            
            return pillar_data
        except Exception as e:
            logger.error(f"Error getting pillar performance: {e}")
            return []
    
    async def _get_top_performing_pillar(self, user_id: str) -> Optional[str]:
        """Get the best performing pillar based on views"""
        try:
            pillar_data = await self._get_pillar_performance(user_id)
            if pillar_data:
                top_pillar = max(pillar_data, key=lambda x: x['avg_views'])
                return top_pillar['name']
            return None
        except Exception as e:
            logger.error(f"Error getting top pillar: {e}")
            return None
    
    async def _get_underperforming_pillars(self, user_id: str) -> List[str]:
        """Get pillars with below-average performance"""
        try:
            pillar_data = await self._get_pillar_performance(user_id)
            if len(pillar_data) < 2:
                return []
            
            avg_views = sum(p['avg_views'] for p in pillar_data) / len(pillar_data)
            underperforming = [p['name'] for p in pillar_data if p['avg_views'] < avg_views * 0.7]
            return underperforming
        except Exception as e:
            logger.error(f"Error getting underperforming pillars: {e}")
            return []
    
    def _cache_context(self, key: str, context: Dict[str, Any]):
        """Cache context with timestamp"""
        self._context_cache[key] = {
            'data': context,
            'timestamp': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self._cache_ttl)
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached context is still valid"""
        if key not in self._context_cache:
            return False
        
        cache_entry = self._context_cache[key]
        return datetime.now() < cache_entry['expires_at']
    
    def clear_cache(self, user_id: Optional[str] = None):
        """Clear context cache"""
        if user_id:
            keys_to_remove = [k for k in self._context_cache.keys() if user_id in k]
            for key in keys_to_remove:
                del self._context_cache[key]
        else:
            self._context_cache.clear()

# Global instance
_enhanced_context_manager = None

def get_enhanced_context_manager() -> EnhancedUserContextManager:
    """Get global enhanced context manager"""
    global _enhanced_context_manager
    if _enhanced_context_manager is None:
        _enhanced_context_manager = EnhancedUserContextManager()
    return _enhanced_context_manager