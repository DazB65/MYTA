"""
Insights Engine for Vidalytics
Generates dynamic insights based on user context and channel data
"""

from typing import List, Dict
import random
from .database import db_manager
import logging

logger = logging.getLogger(__name__)

class InsightsEngine:
    def __init__(self):
        self.insight_templates = {
            "performance": [
                {
                    "title": "CTR Optimization Opportunity",
                    "template": "Your CTR of {ctr}% is {comparison} average for {niche} channels. {recommendation}",
                    "type": "performance",
                    "priority": 3
                },
                {
                    "title": "Retention Analysis",
                    "template": "Your retention rate of {retention}% indicates {analysis}. {suggestion}",
                    "type": "performance", 
                    "priority": 2
                },
                {
                    "title": "Subscriber Growth Pattern",
                    "template": "With {subscribers} subscribers, you're in the {growth_stage} stage. {growth_advice}",
                    "type": "growth",
                    "priority": 2
                }
            ],
            "content": [
                {
                    "title": "Trending Topic Alert",
                    "template": "{trending_topic} is trending in {niche}. Create content now for maximum reach!",
                    "type": "trending",
                    "priority": 3
                },
                {
                    "title": "Content Strategy Insight",
                    "template": "Your {content_type} content performs well. Consider {content_suggestion}",
                    "type": "strategy",
                    "priority": 2
                },
                {
                    "title": "Upload Timing Optimization",
                    "template": "Based on your {upload_frequency} schedule, {timing_advice}",
                    "type": "timing",
                    "priority": 1
                }
            ],
            "monetization": [
                {
                    "title": "Revenue Opportunity",
                    "template": "Your channel is ready for {monetization_opportunity}. {revenue_advice}",
                    "type": "revenue",
                    "priority": 2
                },
                {
                    "title": "Monetization Status Update",
                    "template": "Your monetization status: {monetization_status}. {next_steps}",
                    "type": "monetization",
                    "priority": 1
                }
            ]
        }
        
        # Trending topics by niche (simulated - in production, this would come from APIs)
        self.trending_topics = {
            "gaming": ["AI Gaming Tools", "Game Review Formats", "Speedrun Strategies", "Gaming Setup Tours"],
            "tech": ["AI Development", "VR/AR Updates", "Cybersecurity Tips", "Tech Reviews"],
            "beauty": ["Skincare Routines", "Makeup Tutorials", "Product Reviews", "Beauty Trends"],
            "fitness": ["Home Workouts", "Nutrition Plans", "Mental Health", "Workout Gear"],
            "education": ["Study Techniques", "Online Learning", "Skill Development", "Educational Tech"],
            "finance": ["Investment Strategies", "Budgeting Tips", "Cryptocurrency", "Financial Planning"],
            "cooking": ["Quick Recipes", "Meal Prep", "Cooking Techniques", "Food Reviews"],
            "travel": ["Budget Travel", "Travel Vlogs", "Destination Reviews", "Travel Tips"],
            "vlog": ["Daily Routines", "Life Updates", "Behind the Scenes", "Personal Growth"],
            "review": ["Product Reviews", "Service Reviews", "Comparison Videos", "Unboxing"],
            "tutorial": ["How-To Guides", "Step-by-Step", "Tips & Tricks", "Educational Content"]
        }
    
    def generate_insights_for_user(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Generate personalized insights for a user"""
        try:
            # Get user context
            context = db_manager.get_user_context(user_id)
            channel_info = context["channel_info"]
            
            insights = []
            
            # Generate performance insights
            insights.extend(self._generate_performance_insights(channel_info))
            
            # Generate content insights
            insights.extend(self._generate_content_insights(channel_info))
            
            # Generate monetization insights
            insights.extend(self._generate_monetization_insights(channel_info))
            
            # Sort by priority and limit
            insights.sort(key=lambda x: x["priority"], reverse=True)
            
            # Save new insights to database
            for insight in insights[:limit]:
                db_manager.create_insight(
                    user_id=user_id,
                    title=insight["title"],
                    content=insight["content"],
                    insight_type=insight["type"],
                    priority=insight["priority"]
                )
            
            return insights[:limit]
            
        except Exception as e:
            logger.error(f"Error generating insights for user {user_id}: {e}")
            return []
    
    def _generate_performance_insights(self, channel_info: Dict) -> List[Dict]:
        """Generate performance-related insights"""
        insights = []
        
        # CTR Analysis
        ctr = channel_info.get("ctr", 0)
        if ctr > 0:
            if ctr < 2:
                comparison = "below"
                recommendation = "Focus on creating more compelling thumbnails and titles."
            elif ctr < 5:
                comparison = "around"
                recommendation = "You're doing well! Try A/B testing different thumbnail styles."
            else:
                comparison = "above"
                recommendation = "Excellent CTR! Share your thumbnail strategy in a tutorial."
            
            insights.append({
                "title": "CTR Optimization Opportunity",
                "content": f"Your CTR of {ctr}% is {comparison} average for {channel_info.get('niche', 'your')} channels. {recommendation}",
                "type": "performance",
                "priority": 3
            })
        
        # Retention Analysis
        retention = channel_info.get("retention", 0)
        if retention > 0:
            if retention < 30:
                analysis = "room for improvement in audience engagement"
                suggestion = "Focus on stronger hooks and better pacing."
            elif retention < 50:
                analysis = "decent audience engagement"
                suggestion = "Work on mid-video retention tactics like pattern interrupts."
            else:
                analysis = "excellent audience engagement"
                suggestion = "You're crushing it! Consider longer-form content."
            
            insights.append({
                "title": "Retention Analysis",
                "content": f"Your retention rate of {retention}% indicates {analysis}. {suggestion}",
                "type": "performance",
                "priority": 2
            })
        
        # Subscriber Growth Analysis
        subscribers = channel_info.get("subscriber_count", 0)
        if subscribers < 1000:
            growth_stage = "early growth"
            growth_advice = "Focus on consistency and finding your unique voice."
        elif subscribers < 10000:
            growth_stage = "momentum building"
            growth_advice = "Double down on what's working and experiment with new formats."
        elif subscribers < 100000:
            growth_stage = "scaling"
            growth_advice = "Consider collaborations and trending topics to accelerate growth."
        else:
            growth_stage = "established creator"
            growth_advice = "Focus on diversifying content and building a community."
        
        insights.append({
            "title": "Growth Stage Analysis",
            "content": f"With {subscribers:,} subscribers, you're in the {growth_stage} stage. {growth_advice}",
            "type": "growth",
            "priority": 2
        })
        
        return insights
    
    def _generate_content_insights(self, channel_info: Dict) -> List[Dict]:
        """Generate content-related insights"""
        insights = []
        
        # Trending topics
        niche = channel_info.get("niche", "general")
        if niche in self.trending_topics:
            trending_topic = random.choice(self.trending_topics[niche])
            insights.append({
                "title": "Trending Topic Alert",
                "content": f"{trending_topic} is trending in {niche}. Create content now for maximum reach!",
                "type": "trending",
                "priority": 3
            })
        
        # Content strategy
        content_type = channel_info.get("content_type", "general")
        if content_type != "Unknown":
            content_suggestions = {
                "tutorial": "creating a series or advanced tutorials",
                "vlog": "themed vlogs or day-in-the-life content",
                "review": "comparison videos or first impressions",
                "gameplay": "live streaming or commentary videos",
                "educational": "interactive content or case studies"
            }
            
            suggestion = content_suggestions.get(content_type, "experimenting with new formats")
            insights.append({
                "title": "Content Strategy Insight",
                "content": f"Your {content_type} content performs well. Consider {suggestion}",
                "type": "strategy",
                "priority": 2
            })
        
        # Upload timing
        upload_frequency = channel_info.get("upload_frequency", "unknown")
        timing_advice_map = {
            "daily": "maintain consistency but ensure quality doesn't suffer",
            "weekly": "this is optimal for most creators - stick with it!",
            "monthly": "consider increasing frequency for better algorithm performance",
            "sporadic": "consistency is key - aim for a regular schedule"
        }
        
        timing_advice = timing_advice_map.get(upload_frequency, "establish a consistent upload schedule")
        insights.append({
            "title": "Upload Strategy",
            "content": f"Based on your {upload_frequency} schedule, {timing_advice}",
            "type": "timing",
            "priority": 1
        })
        
        return insights
    
    def _generate_monetization_insights(self, channel_info: Dict) -> List[Dict]:
        """Generate monetization-related insights"""
        insights = []
        
        subscribers = channel_info.get("subscriber_count", 0)
        monetization_status = channel_info.get("monetization_status", "unknown")
        
        # Revenue opportunities
        if subscribers >= 1000 and monetization_status == "monetized":
            opportunities = ["brand partnerships", "merchandise", "channel memberships", "super chat"]
            opportunity = random.choice(opportunities)
            advice = f"Your subscriber count and engagement make you eligible for {opportunity}."
        elif subscribers >= 1000:
            opportunity = "YouTube Partner Program"
            advice = "Apply for monetization to start earning ad revenue."
        else:
            opportunity = "building your audience"
            advice = f"Focus on reaching 1,000 subscribers (currently at {subscribers})."
        
        insights.append({
            "title": "Revenue Opportunity",
            "content": f"Your channel is ready for {opportunity}. {advice}",
            "type": "revenue",
            "priority": 2
        })
        
        # Monetization status
        status_advice = {
            "monetized": "Optimize your CPM by creating longer videos and targeting higher-value keywords.",
            "partial": "Work on getting fully monetized to maximize revenue potential.",
            "pending": "Be patient during the review process and continue creating quality content.",
            "not-eligible": f"You need {1000 - subscribers} more subscribers and 4,000 watch hours.",
            "demonetized": "Focus on following community guidelines and appeal if necessary."
        }
        
        next_steps = status_advice.get(monetization_status, "Review YouTube's monetization policies.")
        insights.append({
            "title": "Monetization Status",
            "content": f"Your monetization status: {monetization_status}. {next_steps}",
            "type": "monetization",
            "priority": 1
        })
        
        return insights
    
    def get_user_insights(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get existing insights for a user"""
        return db_manager.get_user_insights(user_id, limit)

# Global insights engine instance
insights_engine = InsightsEngine()