"""
Smart Notification Engine for MYTA
Intelligent notifications for performance changes, optimization opportunities, and agent recommendations
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import asyncio
from collections import defaultdict

from backend.App.youtube_analytics_service import get_youtube_analytics_service
from backend.App.agent_collaboration import get_collaboration_engine
from backend.App.channel_analyzer import get_channel_analyzer
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.NOTIFICATIONS)

class NotificationPriority(Enum):
    """Notification priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class NotificationType(Enum):
    """Types of notifications"""
    PERFORMANCE_ALERT = "performance_alert"
    OPTIMIZATION_OPPORTUNITY = "optimization_opportunity"
    AGENT_RECOMMENDATION = "agent_recommendation"
    MILESTONE_ACHIEVEMENT = "milestone_achievement"
    TRENDING_OPPORTUNITY = "trending_opportunity"
    COMPETITIVE_INSIGHT = "competitive_insight"
    GOAL_UPDATE = "goal_update"
    SYSTEM_UPDATE = "system_update"

class NotificationChannel(Enum):
    """Notification delivery channels"""
    IN_APP = "in_app"
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    WEBHOOK = "webhook"

@dataclass
class NotificationRule:
    """Rule for triggering notifications"""
    rule_id: str
    name: str
    description: str
    condition: Dict[str, Any]
    notification_type: NotificationType
    priority: NotificationPriority
    channels: List[NotificationChannel]
    frequency_limit: str  # "once", "daily", "weekly", "immediate"
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Notification:
    """Individual notification"""
    notification_id: str
    user_id: str
    channel_id: Optional[str]
    notification_type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    data: Dict[str, Any]
    channels: List[NotificationChannel]
    created_at: datetime
    scheduled_for: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    action_taken: Optional[str] = None
    expires_at: Optional[datetime] = None

@dataclass
class NotificationPreferences:
    """User notification preferences"""
    user_id: str
    enabled_channels: List[NotificationChannel]
    priority_threshold: NotificationPriority
    quiet_hours: Dict[str, Any]  # {"start": "22:00", "end": "08:00", "timezone": "UTC"}
    frequency_limits: Dict[NotificationType, str]
    custom_rules: List[NotificationRule]
    agent_notifications: Dict[str, bool]  # Per-agent notification settings

class SmartNotificationEngine:
    """Intelligent notification engine for MYTA"""
    
    def __init__(self):
        self.analytics_service = get_youtube_analytics_service()
        self.collaboration_engine = get_collaboration_engine()
        self.channel_analyzer = get_channel_analyzer()
        self.notification_history = defaultdict(list)
        self.active_rules = {}
        self.user_preferences = {}
        
        # Load default notification rules
        self.default_rules = self._load_default_rules()
    
    def _load_default_rules(self) -> List[NotificationRule]:
        """Load default notification rules"""
        
        return [
            NotificationRule(
                rule_id="critical_ctr_drop",
                name="Critical CTR Drop",
                description="Alert when CTR drops below 2%",
                condition={
                    "metric": "ctr",
                    "operator": "less_than",
                    "value": 0.02,
                    "timeframe": "24_hours"
                },
                notification_type=NotificationType.PERFORMANCE_ALERT,
                priority=NotificationPriority.CRITICAL,
                channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL],
                frequency_limit="immediate"
            ),
            NotificationRule(
                rule_id="low_retention_warning",
                name="Low Retention Warning",
                description="Alert when retention drops below 35%",
                condition={
                    "metric": "retention",
                    "operator": "less_than",
                    "value": 0.35,
                    "timeframe": "7_days"
                },
                notification_type=NotificationType.PERFORMANCE_ALERT,
                priority=NotificationPriority.HIGH,
                channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL],
                frequency_limit="daily"
            ),
            NotificationRule(
                rule_id="subscriber_milestone",
                name="Subscriber Milestone",
                description="Celebrate subscriber milestones",
                condition={
                    "metric": "subscribers",
                    "operator": "milestone_reached",
                    "values": [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
                },
                notification_type=NotificationType.MILESTONE_ACHIEVEMENT,
                priority=NotificationPriority.MEDIUM,
                channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL],
                frequency_limit="once"
            ),
            NotificationRule(
                rule_id="optimization_opportunity",
                name="Optimization Opportunity",
                description="Suggest optimizations when performance could improve",
                condition={
                    "metric": "optimization_score",
                    "operator": "less_than",
                    "value": 70,
                    "timeframe": "7_days"
                },
                notification_type=NotificationType.OPTIMIZATION_OPPORTUNITY,
                priority=NotificationPriority.MEDIUM,
                channels=[NotificationChannel.IN_APP],
                frequency_limit="weekly"
            ),
            NotificationRule(
                rule_id="trending_opportunity",
                name="Trending Content Opportunity",
                description="Alert about trending topics in user's niche",
                condition={
                    "metric": "trending_score",
                    "operator": "greater_than",
                    "value": 80,
                    "timeframe": "24_hours"
                },
                notification_type=NotificationType.TRENDING_OPPORTUNITY,
                priority=NotificationPriority.HIGH,
                channels=[NotificationChannel.IN_APP, NotificationChannel.PUSH],
                frequency_limit="immediate"
            ),
            NotificationRule(
                rule_id="agent_recommendation",
                name="Agent Recommendation",
                description="Proactive recommendations from AI agents",
                condition={
                    "metric": "recommendation_confidence",
                    "operator": "greater_than",
                    "value": 0.8,
                    "context": "performance_analysis"
                },
                notification_type=NotificationType.AGENT_RECOMMENDATION,
                priority=NotificationPriority.MEDIUM,
                channels=[NotificationChannel.IN_APP],
                frequency_limit="daily"
            )
        ]
    
    async def monitor_and_notify(self, user_id: str, channel_id: str) -> List[Notification]:
        """Monitor channel performance and generate notifications"""
        
        try:
            notifications = []
            
            # Get user preferences
            preferences = await self._get_user_preferences(user_id)
            
            # Skip if notifications disabled
            if not preferences.enabled_channels:
                return notifications
            
            # Get current channel data
            channel_profile = await self.channel_analyzer.get_channel_profile(user_id)
            analytics_data = await self.analytics_service.get_real_time_insights(channel_id, "mock_token")
            
            # Check each notification rule
            active_rules = await self._get_active_rules(user_id)
            
            for rule in active_rules:
                if await self._should_trigger_notification(rule, channel_profile, analytics_data, user_id):
                    notification = await self._create_notification(rule, user_id, channel_id, channel_profile, analytics_data)
                    if notification:
                        notifications.append(notification)
            
            # Store notifications
            for notification in notifications:
                await self._store_notification(notification)
            
            return notifications
        
        except Exception as e:
            logger.error(f"Error monitoring and notifying for user {user_id}: {e}")
            return []
    
    async def _should_trigger_notification(
        self, 
        rule: NotificationRule, 
        channel_profile, 
        analytics_data, 
        user_id: str
    ) -> bool:
        """Check if notification rule should trigger"""
        
        try:
            # Check frequency limits
            if not await self._check_frequency_limit(rule, user_id):
                return False
            
            # Evaluate rule condition
            condition = rule.condition
            metric = condition.get("metric")
            operator = condition.get("operator")
            value = condition.get("value")
            
            if metric == "ctr":
                current_value = channel_profile.metrics.avg_ctr
            elif metric == "retention":
                current_value = channel_profile.metrics.avg_retention
            elif metric == "subscribers":
                current_value = channel_profile.metrics.subscriber_count
            elif metric == "optimization_score":
                current_value = await self._calculate_optimization_score(channel_profile)
            elif metric == "trending_score":
                current_value = await self._calculate_trending_score(channel_profile)
            elif metric == "recommendation_confidence":
                current_value = await self._calculate_recommendation_confidence(analytics_data)
            else:
                return False
            
            # Apply operator
            if operator == "less_than":
                return current_value < value
            elif operator == "greater_than":
                return current_value > value
            elif operator == "equals":
                return current_value == value
            elif operator == "milestone_reached":
                return await self._check_milestone_reached(current_value, condition.get("values", []), user_id)
            
            return False
        
        except Exception as e:
            logger.error(f"Error checking notification trigger: {e}")
            return False
    
    async def _create_notification(
        self, 
        rule: NotificationRule, 
        user_id: str, 
        channel_id: str, 
        channel_profile, 
        analytics_data
    ) -> Optional[Notification]:
        """Create notification based on rule and data"""
        
        try:
            notification_id = f"notif_{user_id}_{rule.rule_id}_{int(datetime.now().timestamp())}"
            
            # Generate notification content based on type
            if rule.notification_type == NotificationType.PERFORMANCE_ALERT:
                title, message, data = await self._generate_performance_alert(rule, channel_profile)
            elif rule.notification_type == NotificationType.OPTIMIZATION_OPPORTUNITY:
                title, message, data = await self._generate_optimization_opportunity(rule, channel_profile, analytics_data)
            elif rule.notification_type == NotificationType.AGENT_RECOMMENDATION:
                title, message, data = await self._generate_agent_recommendation(rule, channel_profile, analytics_data)
            elif rule.notification_type == NotificationType.MILESTONE_ACHIEVEMENT:
                title, message, data = await self._generate_milestone_achievement(rule, channel_profile)
            elif rule.notification_type == NotificationType.TRENDING_OPPORTUNITY:
                title, message, data = await self._generate_trending_opportunity(rule, channel_profile, analytics_data)
            else:
                title, message, data = "Update", "New notification available", {}
            
            # Set expiration
            expires_at = datetime.now() + timedelta(days=7)  # Default 7 days
            if rule.priority == NotificationPriority.CRITICAL:
                expires_at = datetime.now() + timedelta(days=1)
            
            return Notification(
                notification_id=notification_id,
                user_id=user_id,
                channel_id=channel_id,
                notification_type=rule.notification_type,
                priority=rule.priority,
                title=title,
                message=message,
                data=data,
                channels=rule.channels,
                created_at=datetime.now(),
                expires_at=expires_at
            )
        
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    async def _generate_performance_alert(self, rule: NotificationRule, channel_profile) -> Tuple[str, str, Dict]:
        """Generate performance alert notification"""
        
        metric = rule.condition.get("metric")
        value = rule.condition.get("value")
        
        if metric == "ctr":
            current_ctr = channel_profile.metrics.avg_ctr
            title = "🚨 Critical: Low Click-Through Rate"
            message = f"Your CTR has dropped to {current_ctr:.1%}, below the {value:.1%} threshold. This significantly impacts video discovery."
            data = {
                "current_value": current_ctr,
                "threshold": value,
                "recommended_actions": [
                    "Optimize thumbnail design with high contrast",
                    "A/B test different thumbnail styles",
                    "Improve title emotional appeal"
                ],
                "urgency": "high",
                "estimated_impact": "15-25% CTR improvement possible"
            }
        elif metric == "retention":
            current_retention = channel_profile.metrics.avg_retention
            title = "⚠️ Warning: Low Audience Retention"
            message = f"Your retention has dropped to {current_retention:.1%}, below the {value:.1%} threshold. This affects algorithm performance."
            data = {
                "current_value": current_retention,
                "threshold": value,
                "recommended_actions": [
                    "Strengthen video hooks in first 15 seconds",
                    "Add pattern interrupts every 60-90 seconds",
                    "Improve pacing and remove dead time"
                ],
                "urgency": "medium",
                "estimated_impact": "10-20% retention improvement possible"
            }
        else:
            title = "Performance Alert"
            message = f"Performance metric {metric} needs attention"
            data = {"metric": metric, "threshold": value}
        
        return title, message, data
    
    async def _generate_optimization_opportunity(self, rule: NotificationRule, channel_profile, analytics_data) -> Tuple[str, str, Dict]:
        """Generate optimization opportunity notification"""
        
        title = "🎯 Optimization Opportunity Detected"
        message = "Our AI analysis has identified several ways to improve your channel performance."
        
        # Get optimization recommendations
        recommendations = analytics_data.optimization_recommendations or []
        
        data = {
            "optimization_score": await self._calculate_optimization_score(channel_profile),
            "recommendations": recommendations[:3],  # Top 3
            "potential_impact": "20-40% performance improvement",
            "implementation_time": "1-2 weeks",
            "priority_areas": ["thumbnails", "content_structure", "seo"]
        }
        
        return title, message, data
    
    async def _generate_agent_recommendation(self, rule: NotificationRule, channel_profile, analytics_data) -> Tuple[str, str, Dict]:
        """Generate agent recommendation notification"""
        
        # Get best agent for current situation
        best_agent = await self._determine_best_agent(channel_profile, analytics_data)
        
        title = f"💡 {best_agent['name']} Has a Recommendation"
        message = f"{best_agent['name']} suggests specific actions to improve your channel performance."
        
        data = {
            "agent_id": best_agent["id"],
            "agent_name": best_agent["name"],
            "recommendation": best_agent["recommendation"],
            "confidence": best_agent["confidence"],
            "category": best_agent["category"],
            "expected_impact": best_agent["expected_impact"]
        }
        
        return title, message, data
    
    async def _generate_milestone_achievement(self, rule: NotificationRule, channel_profile) -> Tuple[str, str, Dict]:
        """Generate milestone achievement notification"""
        
        current_subs = channel_profile.metrics.subscriber_count
        milestone = self._find_reached_milestone(current_subs, rule.condition.get("values", []))
        
        title = f"🎉 Congratulations! {milestone:,} Subscribers!"
        message = f"You've reached {milestone:,} subscribers! This is a significant milestone in your YouTube journey."
        
        data = {
            "milestone": milestone,
            "current_subscribers": current_subs,
            "next_milestone": self._get_next_milestone(current_subs),
            "celebration_suggestions": [
                "Share this achievement with your community",
                "Create a milestone celebration video",
                "Thank your subscribers for their support"
            ]
        }
        
        return title, message, data
    
    async def _generate_trending_opportunity(self, rule: NotificationRule, channel_profile, analytics_data) -> Tuple[str, str, Dict]:
        """Generate trending opportunity notification"""
        
        title = "🔥 Trending Content Opportunity"
        message = "Hot topics in your niche are trending right now. Act fast to capitalize!"
        
        trending_topics = analytics_data.trending_opportunities or []
        
        data = {
            "trending_topics": [opp.get("trending_topics", []) for opp in trending_topics][:3],
            "urgency": "high",
            "time_sensitive": True,
            "action_deadline": "next 24-48 hours",
            "potential_impact": "30-50% view increase",
            "recommended_actions": [
                "Create content around trending topics",
                "Use trending keywords in titles",
                "Optimize upload timing for maximum reach"
            ]
        }
        
        return title, message, data
    
    async def get_user_notifications(
        self, 
        user_id: str, 
        limit: int = 20, 
        unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user"""
        
        try:
            # In real implementation, query database
            notifications = self.notification_history.get(user_id, [])
            
            if unread_only:
                notifications = [n for n in notifications if n.read_at is None]
            
            # Sort by priority and creation time
            priority_order = {
                NotificationPriority.CRITICAL: 5,
                NotificationPriority.HIGH: 4,
                NotificationPriority.MEDIUM: 3,
                NotificationPriority.LOW: 2,
                NotificationPriority.INFO: 1
            }
            
            notifications.sort(
                key=lambda n: (priority_order.get(n.priority, 0), n.created_at),
                reverse=True
            )
            
            return notifications[:limit]
        
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []
    
    async def mark_notification_read(self, notification_id: str, user_id: str) -> bool:
        """Mark notification as read"""
        
        try:
            notifications = self.notification_history.get(user_id, [])
            for notification in notifications:
                if notification.notification_id == notification_id:
                    notification.read_at = datetime.now()
                    return True
            return False
        
        except Exception as e:
            logger.error(f"Error marking notification read: {e}")
            return False
    
    async def update_notification_preferences(
        self, 
        user_id: str, 
        preferences: NotificationPreferences
    ) -> bool:
        """Update user notification preferences"""
        
        try:
            self.user_preferences[user_id] = preferences
            # In real implementation, save to database
            return True
        
        except Exception as e:
            logger.error(f"Error updating notification preferences: {e}")
            return False
    
    # Helper methods
    
    async def _get_user_preferences(self, user_id: str) -> NotificationPreferences:
        """Get user notification preferences"""
        
        if user_id in self.user_preferences:
            return self.user_preferences[user_id]
        
        # Default preferences
        return NotificationPreferences(
            user_id=user_id,
            enabled_channels=[NotificationChannel.IN_APP, NotificationChannel.EMAIL],
            priority_threshold=NotificationPriority.MEDIUM,
            quiet_hours={"start": "22:00", "end": "08:00", "timezone": "UTC"},
            frequency_limits={},
            custom_rules=[],
            agent_notifications={"1": True, "2": True, "3": True, "4": True, "5": True}
        )
    
    async def _get_active_rules(self, user_id: str) -> List[NotificationRule]:
        """Get active notification rules for user"""
        
        preferences = await self._get_user_preferences(user_id)
        active_rules = self.default_rules.copy()
        active_rules.extend(preferences.custom_rules)
        
        return [rule for rule in active_rules if rule.enabled]
    
    async def _check_frequency_limit(self, rule: NotificationRule, user_id: str) -> bool:
        """Check if notification frequency limit allows sending"""
        
        if rule.frequency_limit == "immediate":
            return True
        
        # Check recent notifications of same type
        recent_notifications = [
            n for n in self.notification_history.get(user_id, [])
            if n.notification_type == rule.notification_type
        ]
        
        if rule.frequency_limit == "once":
            return len(recent_notifications) == 0
        elif rule.frequency_limit == "daily":
            today = datetime.now().date()
            return not any(n.created_at.date() == today for n in recent_notifications)
        elif rule.frequency_limit == "weekly":
            week_ago = datetime.now() - timedelta(days=7)
            return not any(n.created_at > week_ago for n in recent_notifications)
        
        return True
    
    async def _store_notification(self, notification: Notification) -> None:
        """Store notification in history"""
        
        self.notification_history[notification.user_id].append(notification)
        
        # Keep only last 100 notifications per user
        if len(self.notification_history[notification.user_id]) > 100:
            self.notification_history[notification.user_id] = \
                self.notification_history[notification.user_id][-100:]
    
    async def _calculate_optimization_score(self, channel_profile) -> float:
        """Calculate optimization score for channel"""
        
        # Simple scoring based on key metrics
        ctr_score = min(channel_profile.metrics.avg_ctr / 0.06, 1.0) * 30
        retention_score = min(channel_profile.metrics.avg_retention / 0.50, 1.0) * 40
        growth_score = min(channel_profile.metrics.subscriber_count / 10000, 1.0) * 30
        
        return (ctr_score + retention_score + growth_score)
    
    async def _calculate_trending_score(self, channel_profile) -> float:
        """Calculate trending score for channel's niche"""
        
        # Mock implementation - in real app, analyze trending content
        return 75.0
    
    async def _calculate_recommendation_confidence(self, analytics_data) -> float:
        """Calculate confidence in recommendations"""
        
        if analytics_data.optimization_recommendations:
            return 0.85  # High confidence
        return 0.5
    
    async def _check_milestone_reached(self, current_value: int, milestones: List[int], user_id: str) -> bool:
        """Check if a milestone was recently reached"""
        
        # Check if current value matches any milestone
        for milestone in milestones:
            if current_value >= milestone:
                # Check if we already notified about this milestone
                recent_milestone_notifications = [
                    n for n in self.notification_history.get(user_id, [])
                    if n.notification_type == NotificationType.MILESTONE_ACHIEVEMENT
                    and n.data.get("milestone") == milestone
                ]
                if not recent_milestone_notifications:
                    return True
        
        return False
    
    def _find_reached_milestone(self, current_value: int, milestones: List[int]) -> int:
        """Find the milestone that was reached"""
        
        reached_milestones = [m for m in milestones if current_value >= m]
        return max(reached_milestones) if reached_milestones else 0
    
    def _get_next_milestone(self, current_value: int) -> int:
        """Get the next milestone to reach"""
        
        milestones = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
        next_milestones = [m for m in milestones if current_value < m]
        return min(next_milestones) if next_milestones else current_value * 2
    
    async def _determine_best_agent(self, channel_profile, analytics_data) -> Dict[str, Any]:
        """Determine which agent should provide recommendation"""
        
        # Simple logic - in real implementation, use more sophisticated analysis
        if channel_profile.metrics.avg_ctr < 0.04:
            return {
                "id": "1",
                "name": "Alex",
                "recommendation": "Focus on thumbnail optimization to improve CTR",
                "confidence": 0.9,
                "category": "analytics",
                "expected_impact": "15-25% CTR improvement"
            }
        elif channel_profile.metrics.avg_retention < 0.45:
            return {
                "id": "2",
                "name": "Levi",
                "recommendation": "Improve content hooks and pacing for better retention",
                "confidence": 0.85,
                "category": "content",
                "expected_impact": "10-20% retention improvement"
            }
        else:
            return {
                "id": "4",
                "name": "Zara",
                "recommendation": "Implement growth strategies to accelerate channel expansion",
                "confidence": 0.8,
                "category": "growth",
                "expected_impact": "25-40% growth acceleration"
            }

# Global notification engine instance
_notification_engine: Optional[SmartNotificationEngine] = None

def get_notification_engine() -> SmartNotificationEngine:
    """Get or create global notification engine instance"""
    global _notification_engine
    if _notification_engine is None:
        _notification_engine = SmartNotificationEngine()
    return _notification_engine
