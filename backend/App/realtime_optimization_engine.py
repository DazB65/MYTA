"""
Real-Time Optimization Intelligence Engine
Provides live performance monitoring with instant optimization recommendations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np

from .enhanced_user_context import EnhancedUserContextManager
from .youtube_analytics_service import YouTubeAnalyticsService
from .advanced_prediction_engine import get_prediction_engine

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class OptimizationType(Enum):
    TITLE = "title"
    THUMBNAIL = "thumbnail"
    DESCRIPTION = "description"
    TAGS = "tags"
    TIMING = "timing"
    PROMOTION = "promotion"

@dataclass
class RealTimeAlert:
    """Real-time performance alert"""
    alert_id: str
    user_id: str
    video_id: str
    alert_type: str
    severity: AlertSeverity
    title: str
    message: str
    current_value: float
    expected_value: float
    deviation_percentage: float
    recommendations: List[str]
    created_at: datetime
    expires_at: datetime

@dataclass
class OptimizationRecommendation:
    """Real-time optimization recommendation"""
    recommendation_id: str
    user_id: str
    video_id: str
    optimization_type: OptimizationType
    title: str
    description: str
    specific_action: str
    expected_impact: str
    urgency_score: float
    confidence: float
    time_sensitive: bool
    expires_at: Optional[datetime]

@dataclass
class PerformanceSnapshot:
    """Real-time performance snapshot"""
    video_id: str
    timestamp: datetime
    views: int
    ctr: float
    engagement_rate: float
    retention: float
    velocity: float  # Views per hour
    trend: str  # 'up', 'down', 'stable'
    performance_score: float

class RealTimeOptimizationEngine:
    """Real-time optimization and monitoring system"""
    
    def __init__(self):
        self.context_service = EnhancedUserContextManager()
        self.analytics_service = None
        self.prediction_engine = get_prediction_engine()
        
        # Performance thresholds
        self.performance_thresholds = {
            'ctr_low': 0.02,  # 2% CTR threshold
            'engagement_low': 0.01,  # 1% engagement threshold
            'retention_low': 0.30,  # 30% retention threshold
            'velocity_low': 10,  # 10 views per hour threshold
        }
        
        # Alert cooldown periods (minutes)
        self.alert_cooldowns = {
            'ctr_alert': 60,
            'engagement_alert': 30,
            'retention_alert': 120,
            'velocity_alert': 15
        }
        
        # Active alerts tracking
        self.active_alerts = {}
        
        logger.info("Real-Time Optimization Engine initialized")
    
    async def monitor_video_performance(
        self, 
        user_id: str, 
        video_id: str, 
        hours_since_publish: float = None
    ) -> Dict[str, Any]:
        """
        Monitor video performance in real-time and generate optimization recommendations
        
        Args:
            user_id: User identifier
            video_id: Video to monitor
            hours_since_publish: Hours since video was published
        
        Returns:
            Real-time monitoring results with alerts and recommendations
        """
        try:
            logger.info(f"📊 Monitoring real-time performance for video {video_id}")
            
            # Get current performance snapshot
            performance_snapshot = await self._get_performance_snapshot(user_id, video_id)
            
            # Get expected performance baseline
            expected_performance = await self._get_expected_performance(
                user_id, video_id, hours_since_publish
            )
            
            # Generate performance alerts
            alerts = await self._generate_performance_alerts(
                user_id, video_id, performance_snapshot, expected_performance
            )
            
            # Generate optimization recommendations
            recommendations = await self._generate_optimization_recommendations(
                user_id, video_id, performance_snapshot, expected_performance
            )
            
            # Calculate overall health score
            health_score = self._calculate_performance_health_score(
                performance_snapshot, expected_performance
            )
            
            # Generate action plan
            action_plan = await self._generate_action_plan(
                alerts, recommendations, health_score
            )
            
            monitoring_result = {
                'video_id': video_id,
                'timestamp': datetime.now().isoformat(),
                'performance_snapshot': asdict(performance_snapshot),
                'expected_performance': expected_performance,
                'health_score': health_score,
                'alerts': [asdict(alert) for alert in alerts],
                'recommendations': [asdict(rec) for rec in recommendations],
                'action_plan': action_plan,
                'monitoring_status': 'active'
            }
            
            logger.info(f"✅ Real-time monitoring completed: Health Score {health_score:.1f}/100")
            return monitoring_result
            
        except Exception as e:
            logger.error(f"Error monitoring video performance: {e}")
            return {
                'video_id': video_id,
                'error': str(e),
                'monitoring_status': 'error'
            }
    
    async def _get_performance_snapshot(self, user_id: str, video_id: str) -> PerformanceSnapshot:
        """Get current performance snapshot for a video"""
        
        try:
            # Get enhanced context with real-time data
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            
            # Find video in recent content
            recent_videos = enhanced_context.get('recent_content', [])
            video_data = None
            
            for video in recent_videos:
                if video.get('video_id') == video_id:
                    video_data = video
                    break
            
            if not video_data:
                # Fallback to basic data
                video_data = {
                    'video_id': video_id,
                    'metrics': {
                        'views': 100,
                        'ctr': 3.0,
                        'engagement_rate': 2.0,
                        'retention': 40.0
                    },
                    'published_at': datetime.now().isoformat()
                }
            
            metrics = video_data.get('metrics', {})
            published_at = video_data.get('published_at')
            
            # Calculate velocity (views per hour)
            if published_at:
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                hours_since_publish = (datetime.now() - pub_date).total_seconds() / 3600
                velocity = metrics.get('views', 0) / max(hours_since_publish, 1)
            else:
                velocity = 0
            
            # Determine trend
            trend = self._calculate_performance_trend(metrics, enhanced_context)
            
            # Calculate performance score
            performance_score = self._calculate_current_performance_score(metrics, enhanced_context)
            
            return PerformanceSnapshot(
                video_id=video_id,
                timestamp=datetime.now(),
                views=metrics.get('views', 0),
                ctr=metrics.get('ctr', 0.0),
                engagement_rate=metrics.get('engagement_rate', 0.0),
                retention=metrics.get('retention', 0.0),
                velocity=velocity,
                trend=trend,
                performance_score=performance_score
            )
            
        except Exception as e:
            logger.error(f"Error getting performance snapshot: {e}")
            return PerformanceSnapshot(
                video_id=video_id,
                timestamp=datetime.now(),
                views=0,
                ctr=0.0,
                engagement_rate=0.0,
                retention=0.0,
                velocity=0.0,
                trend='unknown',
                performance_score=0.0
            )
    
    async def _get_expected_performance(
        self, 
        user_id: str, 
        video_id: str, 
        hours_since_publish: float = None
    ) -> Dict[str, Any]:
        """Get expected performance baseline for comparison"""
        
        try:
            # Get user's historical averages
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            performance_data = enhanced_context.get('performance_data', {})
            
            # Base expectations on user's averages
            expected = {
                'views_24h': performance_data.get('avg_views_24h', 500),
                'ctr': performance_data.get('avg_ctr_30d', 4.0),
                'engagement_rate': performance_data.get('avg_engagement_30d', 3.0),
                'retention': performance_data.get('avg_retention_30d', 45.0),
                'velocity_1h': performance_data.get('avg_views_24h', 500) / 24
            }
            
            # Adjust expectations based on time since publish
            if hours_since_publish:
                # Early hours typically have higher velocity
                if hours_since_publish <= 2:
                    expected['velocity_1h'] *= 2.0  # Higher initial velocity
                elif hours_since_publish <= 6:
                    expected['velocity_1h'] *= 1.5
                elif hours_since_publish >= 24:
                    expected['velocity_1h'] *= 0.3  # Lower long-term velocity
            
            return expected
            
        except Exception as e:
            logger.error(f"Error getting expected performance: {e}")
            return {
                'views_24h': 500,
                'ctr': 4.0,
                'engagement_rate': 3.0,
                'retention': 45.0,
                'velocity_1h': 20
            }
    
    def _calculate_performance_trend(self, metrics: Dict[str, Any], enhanced_context: Dict[str, Any]) -> str:
        """Calculate performance trend direction"""
        
        try:
            current_views = metrics.get('views', 0)
            avg_views = enhanced_context.get('performance_data', {}).get('avg_views_30d', 1000)
            
            if current_views > avg_views * 1.2:
                return 'up'
            elif current_views < avg_views * 0.8:
                return 'down'
            else:
                return 'stable'
                
        except Exception:
            return 'unknown'
    
    def _calculate_current_performance_score(self, metrics: Dict[str, Any], enhanced_context: Dict[str, Any]) -> float:
        """Calculate current performance score (0-100)"""
        
        try:
            performance_data = enhanced_context.get('performance_data', {})
            
            # Compare current metrics to user averages
            ctr_ratio = metrics.get('ctr', 0) / max(performance_data.get('avg_ctr_30d', 4.0), 1)
            engagement_ratio = metrics.get('engagement_rate', 0) / max(performance_data.get('avg_engagement_30d', 3.0), 1)
            retention_ratio = metrics.get('retention', 0) / max(performance_data.get('avg_retention_30d', 45.0), 1)
            
            # Weighted score
            score = (
                ctr_ratio * 40 +
                engagement_ratio * 35 +
                retention_ratio * 25
            )
            
            return max(0, min(100, score * 50))  # Scale to 0-100
            
        except Exception:
            return 50.0  # Default average score

    async def _generate_performance_alerts(
        self,
        user_id: str,
        video_id: str,
        performance: PerformanceSnapshot,
        expected: Dict[str, Any]
    ) -> List[RealTimeAlert]:
        """Generate performance alerts based on current vs expected performance"""

        alerts = []

        try:
            # CTR Alert
            if performance.ctr < expected['ctr'] * 0.7:  # 30% below expected
                deviation = ((expected['ctr'] - performance.ctr) / expected['ctr']) * 100
                severity = AlertSeverity.HIGH if deviation > 50 else AlertSeverity.MEDIUM

                alert = RealTimeAlert(
                    alert_id=f"{video_id}_ctr_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    alert_type="low_ctr",
                    severity=severity,
                    title="Low Click-Through Rate",
                    message=f"CTR is {performance.ctr:.1f}% (expected {expected['ctr']:.1f}%)",
                    current_value=performance.ctr,
                    expected_value=expected['ctr'],
                    deviation_percentage=deviation,
                    recommendations=[
                        "Consider updating thumbnail for better visual appeal",
                        "Optimize title for more compelling hook",
                        "A/B test different thumbnail styles"
                    ],
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=6)
                )
                alerts.append(alert)

            # Engagement Alert
            if performance.engagement_rate < expected['engagement_rate'] * 0.6:
                deviation = ((expected['engagement_rate'] - performance.engagement_rate) / expected['engagement_rate']) * 100
                severity = AlertSeverity.HIGH if deviation > 60 else AlertSeverity.MEDIUM

                alert = RealTimeAlert(
                    alert_id=f"{video_id}_engagement_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    alert_type="low_engagement",
                    severity=severity,
                    title="Low Engagement Rate",
                    message=f"Engagement is {performance.engagement_rate:.1f}% (expected {expected['engagement_rate']:.1f}%)",
                    current_value=performance.engagement_rate,
                    expected_value=expected['engagement_rate'],
                    deviation_percentage=deviation,
                    recommendations=[
                        "Add engaging call-to-action in video",
                        "Respond to early comments to boost engagement",
                        "Share on social media to drive initial engagement"
                    ],
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=4)
                )
                alerts.append(alert)

            # Velocity Alert (for recent videos)
            if performance.velocity < expected['velocity_1h'] * 0.5:
                deviation = ((expected['velocity_1h'] - performance.velocity) / expected['velocity_1h']) * 100
                severity = AlertSeverity.CRITICAL if deviation > 70 else AlertSeverity.HIGH

                alert = RealTimeAlert(
                    alert_id=f"{video_id}_velocity_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    alert_type="low_velocity",
                    severity=severity,
                    title="Low View Velocity",
                    message=f"Getting {performance.velocity:.1f} views/hour (expected {expected['velocity_1h']:.1f})",
                    current_value=performance.velocity,
                    expected_value=expected['velocity_1h'],
                    deviation_percentage=deviation,
                    recommendations=[
                        "Promote video on social media immediately",
                        "Notify subscribers about new upload",
                        "Consider updating title/thumbnail for better appeal"
                    ],
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=2)
                )
                alerts.append(alert)

            # Retention Alert
            if performance.retention < expected['retention'] * 0.7:
                deviation = ((expected['retention'] - performance.retention) / expected['retention']) * 100
                severity = AlertSeverity.MEDIUM

                alert = RealTimeAlert(
                    alert_id=f"{video_id}_retention_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    alert_type="low_retention",
                    severity=severity,
                    title="Low Audience Retention",
                    message=f"Retention is {performance.retention:.1f}% (expected {expected['retention']:.1f}%)",
                    current_value=performance.retention,
                    expected_value=expected['retention'],
                    deviation_percentage=deviation,
                    recommendations=[
                        "Analyze retention graph for drop-off points",
                        "Improve video pacing and content structure",
                        "Add more engaging elements throughout video"
                    ],
                    created_at=datetime.now(),
                    expires_at=datetime.now() + timedelta(hours=12)
                )
                alerts.append(alert)

            return alerts

        except Exception as e:
            logger.error(f"Error generating performance alerts: {e}")
            return []

    async def _generate_optimization_recommendations(
        self,
        user_id: str,
        video_id: str,
        performance: PerformanceSnapshot,
        expected: Dict[str, Any]
    ) -> List[OptimizationRecommendation]:
        """Generate specific optimization recommendations"""

        recommendations = []

        try:
            # Title Optimization
            if performance.ctr < expected['ctr'] * 0.8:
                rec = OptimizationRecommendation(
                    recommendation_id=f"{video_id}_title_opt_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    optimization_type=OptimizationType.TITLE,
                    title="Optimize Video Title",
                    description="Low CTR suggests title may not be compelling enough",
                    specific_action="Update title with more emotional hooks or clearer value proposition",
                    expected_impact="15-30% CTR improvement",
                    urgency_score=0.8,
                    confidence=0.7,
                    time_sensitive=True,
                    expires_at=datetime.now() + timedelta(hours=6)
                )
                recommendations.append(rec)

            # Thumbnail Optimization
            if performance.ctr < expected['ctr'] * 0.75:
                rec = OptimizationRecommendation(
                    recommendation_id=f"{video_id}_thumb_opt_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    optimization_type=OptimizationType.THUMBNAIL,
                    title="Update Video Thumbnail",
                    description="CTR below expectations - thumbnail may need improvement",
                    specific_action="Create more eye-catching thumbnail with better contrast and clear focal point",
                    expected_impact="20-40% CTR improvement",
                    urgency_score=0.9,
                    confidence=0.8,
                    time_sensitive=True,
                    expires_at=datetime.now() + timedelta(hours=4)
                )
                recommendations.append(rec)

            # Promotion Recommendation
            if performance.velocity < expected['velocity_1h'] * 0.6:
                rec = OptimizationRecommendation(
                    recommendation_id=f"{video_id}_promo_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    optimization_type=OptimizationType.PROMOTION,
                    title="Boost Video Promotion",
                    description="Low view velocity indicates need for additional promotion",
                    specific_action="Share on all social platforms and engage with early viewers",
                    expected_impact="50-100% velocity increase",
                    urgency_score=1.0,
                    confidence=0.9,
                    time_sensitive=True,
                    expires_at=datetime.now() + timedelta(hours=2)
                )
                recommendations.append(rec)

            # Description Optimization
            if performance.engagement_rate < expected['engagement_rate'] * 0.7:
                rec = OptimizationRecommendation(
                    recommendation_id=f"{video_id}_desc_opt_{datetime.now().strftime('%Y%m%d%H%M')}",
                    user_id=user_id,
                    video_id=video_id,
                    optimization_type=OptimizationType.DESCRIPTION,
                    title="Enhance Video Description",
                    description="Low engagement suggests description could be more compelling",
                    specific_action="Add clear call-to-action and engaging questions in description",
                    expected_impact="10-25% engagement increase",
                    urgency_score=0.6,
                    confidence=0.6,
                    time_sensitive=False,
                    expires_at=datetime.now() + timedelta(hours=12)
                )
                recommendations.append(rec)

            return recommendations

        except Exception as e:
            logger.error(f"Error generating optimization recommendations: {e}")
            return []

    def _calculate_performance_health_score(
        self,
        performance: PerformanceSnapshot,
        expected: Dict[str, Any]
    ) -> float:
        """Calculate overall performance health score (0-100)"""

        try:
            # Calculate individual metric scores
            ctr_score = min(100, (performance.ctr / expected['ctr']) * 100)
            engagement_score = min(100, (performance.engagement_rate / expected['engagement_rate']) * 100)
            retention_score = min(100, (performance.retention / expected['retention']) * 100)
            velocity_score = min(100, (performance.velocity / expected['velocity_1h']) * 100)

            # Weighted health score
            health_score = (
                ctr_score * 0.3 +
                engagement_score * 0.25 +
                retention_score * 0.25 +
                velocity_score * 0.2
            )

            return max(0, min(100, health_score))

        except Exception:
            return 50.0  # Default score

    async def _generate_action_plan(
        self,
        alerts: List[RealTimeAlert],
        recommendations: List[OptimizationRecommendation],
        health_score: float
    ) -> Dict[str, Any]:
        """Generate prioritized action plan"""

        try:
            action_plan = {
                'overall_status': self._get_status_from_health_score(health_score),
                'priority_actions': [],
                'immediate_actions': [],
                'monitoring_actions': [],
                'next_review': self._calculate_next_review_time(health_score)
            }

            # Sort recommendations by urgency and impact
            urgent_recommendations = [
                rec for rec in recommendations
                if rec.urgency_score >= 0.8 and rec.time_sensitive
            ]

            # Priority actions (from critical alerts and urgent recommendations)
            critical_alerts = [alert for alert in alerts if alert.severity == AlertSeverity.CRITICAL]
            high_alerts = [alert for alert in alerts if alert.severity == AlertSeverity.HIGH]

            for alert in critical_alerts:
                action_plan['priority_actions'].append({
                    'action': f"Address {alert.title}",
                    'description': alert.message,
                    'recommendations': alert.recommendations[:2],
                    'urgency': 'critical'
                })

            for rec in urgent_recommendations[:3]:  # Top 3 urgent recommendations
                action_plan['immediate_actions'].append({
                    'action': rec.title,
                    'description': rec.description,
                    'specific_action': rec.specific_action,
                    'expected_impact': rec.expected_impact,
                    'urgency': 'high'
                })

            # Monitoring actions
            if health_score < 70:
                action_plan['monitoring_actions'].append({
                    'action': 'Increase monitoring frequency',
                    'description': 'Check performance every 30 minutes',
                    'duration': '4 hours'
                })

            action_plan['monitoring_actions'].append({
                'action': 'Track key metrics',
                'description': 'Monitor CTR, engagement, and velocity trends',
                'metrics': ['ctr', 'engagement_rate', 'velocity']
            })

            return action_plan

        except Exception as e:
            logger.error(f"Error generating action plan: {e}")
            return {
                'overall_status': 'unknown',
                'priority_actions': [],
                'immediate_actions': [],
                'monitoring_actions': [],
                'next_review': datetime.now() + timedelta(hours=1)
            }

    def _get_status_from_health_score(self, health_score: float) -> str:
        """Get status description from health score"""
        if health_score >= 80:
            return 'excellent'
        elif health_score >= 60:
            return 'good'
        elif health_score >= 40:
            return 'needs_attention'
        elif health_score >= 20:
            return 'poor'
        else:
            return 'critical'

    def _calculate_next_review_time(self, health_score: float) -> datetime:
        """Calculate when to next review performance"""
        if health_score < 30:
            return datetime.now() + timedelta(minutes=30)  # Critical - check every 30 min
        elif health_score < 50:
            return datetime.now() + timedelta(hours=1)     # Poor - check hourly
        elif health_score < 70:
            return datetime.now() + timedelta(hours=2)     # Needs attention - check every 2 hours
        else:
            return datetime.now() + timedelta(hours=4)     # Good - check every 4 hours

    async def get_optimization_dashboard(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive optimization dashboard for user"""
        try:
            logger.info(f"📊 Generating optimization dashboard for user {user_id}")

            # Get enhanced context
            enhanced_context = await self.context_service.get_enhanced_context(user_id)
            recent_videos = enhanced_context.get('recent_content', [])

            # Monitor recent videos
            video_monitoring = []
            for video in recent_videos[:5]:  # Monitor last 5 videos
                video_id = video.get('video_id')
                if video_id:
                    monitoring_result = await self.monitor_video_performance(user_id, video_id)
                    video_monitoring.append(monitoring_result)

            # Aggregate insights
            total_alerts = sum(len(vm.get('alerts', [])) for vm in video_monitoring)
            total_recommendations = sum(len(vm.get('recommendations', [])) for vm in video_monitoring)
            avg_health_score = np.mean([vm.get('health_score', 50) for vm in video_monitoring]) if video_monitoring else 50

            # Generate overall recommendations
            overall_recommendations = await self._generate_overall_recommendations(
                user_id, video_monitoring, enhanced_context
            )

            dashboard = {
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'overview': {
                    'total_videos_monitored': len(video_monitoring),
                    'total_alerts': total_alerts,
                    'total_recommendations': total_recommendations,
                    'average_health_score': round(avg_health_score, 1),
                    'overall_status': self._get_status_from_health_score(avg_health_score)
                },
                'video_monitoring': video_monitoring,
                'overall_recommendations': overall_recommendations,
                'next_actions': await self._generate_next_actions(video_monitoring),
                'monitoring_schedule': self._generate_monitoring_schedule(avg_health_score)
            }

            logger.info(f"✅ Optimization dashboard generated: {total_alerts} alerts, {total_recommendations} recommendations")
            return dashboard

        except Exception as e:
            logger.error(f"Error generating optimization dashboard: {e}")
            return {
                'user_id': user_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _generate_overall_recommendations(
        self,
        user_id: str,
        video_monitoring: List[Dict],
        enhanced_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate overall optimization recommendations across all videos"""

        recommendations = []

        try:
            # Analyze patterns across videos
            low_ctr_count = sum(1 for vm in video_monitoring if vm.get('health_score', 50) < 50)

            if low_ctr_count >= 2:
                recommendations.append({
                    'type': 'pattern_analysis',
                    'title': 'Consistent CTR Issues Detected',
                    'description': f'{low_ctr_count} recent videos have low CTR performance',
                    'action': 'Review thumbnail and title strategy across all content',
                    'priority': 'high'
                })

            # Channel-level recommendations
            performance_data = enhanced_context.get('performance_data', {})
            if performance_data.get('avg_ctr_30d', 4.0) < 3.0:
                recommendations.append({
                    'type': 'channel_optimization',
                    'title': 'Channel-Wide CTR Optimization Needed',
                    'description': 'Overall channel CTR is below optimal levels',
                    'action': 'Implement systematic thumbnail and title testing',
                    'priority': 'medium'
                })

            return recommendations

        except Exception as e:
            logger.error(f"Error generating overall recommendations: {e}")
            return []

    async def _generate_next_actions(self, video_monitoring: List[Dict]) -> List[Dict[str, Any]]:
        """Generate prioritized next actions"""

        actions = []

        try:
            # Collect all urgent recommendations
            for vm in video_monitoring:
                for rec in vm.get('recommendations', []):
                    if rec.get('urgency_score', 0) >= 0.8:
                        actions.append({
                            'video_id': vm.get('video_id'),
                            'action': rec.get('title'),
                            'urgency': 'high',
                            'expected_impact': rec.get('expected_impact')
                        })

            # Sort by urgency and impact
            actions.sort(key=lambda x: x.get('urgency') == 'high', reverse=True)

            return actions[:5]  # Top 5 actions

        except Exception as e:
            logger.error(f"Error generating next actions: {e}")
            return []

    def _generate_monitoring_schedule(self, avg_health_score: float) -> Dict[str, Any]:
        """Generate monitoring schedule based on performance"""

        if avg_health_score < 40:
            return {
                'frequency': 'every_30_minutes',
                'duration': '6_hours',
                'focus': 'critical_metrics'
            }
        elif avg_health_score < 60:
            return {
                'frequency': 'hourly',
                'duration': '12_hours',
                'focus': 'key_metrics'
            }
        else:
            return {
                'frequency': 'every_4_hours',
                'duration': '24_hours',
                'focus': 'standard_monitoring'
            }

# Global instance
_optimization_engine = None

def get_optimization_engine() -> RealTimeOptimizationEngine:
    """Get global optimization engine instance"""
    global _optimization_engine
    if _optimization_engine is None:
        _optimization_engine = RealTimeOptimizationEngine()
    return _optimization_engine
