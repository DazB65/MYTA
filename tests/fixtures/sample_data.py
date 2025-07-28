"""
Sample data fixtures for testing
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any


class SampleDataFactory:
    """Factory for creating sample test data"""
    
    @staticmethod
    def create_user_data(user_id: str = "test-user-123") -> Dict[str, Any]:
        """Create sample user data"""
        return {
            "user_id": user_id,
            "channel_name": "Test Creator Channel",
            "channel_id": f"channel-{user_id}",
            "subscriber_count": 10000,
            "total_views": 500000,
            "video_count": 150,
            "niche": "Technology",
            "goals": ["Growth", "Monetization", "Engagement"],
            "content_type": "Educational",
            "upload_frequency": "3x per week",
            "primary_language": "English",
            "target_audience": "Tech enthusiasts",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_video_data(video_id: str = "test-video-123") -> Dict[str, Any]:
        """Create sample video data"""
        return {
            "video_id": video_id,
            "title": "How to Build Amazing Web Applications",
            "description": "Learn to build web applications from scratch using modern technologies.",
            "view_count": 15000,
            "like_count": 1200,
            "dislike_count": 45,
            "comment_count": 150,
            "published_at": (datetime.now() - timedelta(days=7)).isoformat(),
            "duration": "PT15M30S",  # ISO 8601 duration format
            "tags": ["web development", "programming", "tutorial", "javascript", "react"],
            "category": "Science & Technology",
            "thumbnail_url": "https://i.ytimg.com/vi/example/maxresdefault.jpg",
            "watch_time_minutes": 180000,  # Total watch time across all views
            "average_view_duration": "PT8M45S",
            "retention_data": [
                {"timestamp": 0, "retention": 100},
                {"timestamp": 30, "retention": 85},
                {"timestamp": 60, "retention": 75},
                {"timestamp": 120, "retention": 65},
                {"timestamp": 300, "retention": 45},
                {"timestamp": 600, "retention": 30},
                {"timestamp": 900, "retention": 20}
            ]
        }
    
    @staticmethod
    def create_channel_analytics() -> Dict[str, Any]:
        """Create sample channel analytics data"""
        return {
            "overview": {
                "total_subscribers": 12500,
                "total_views": 750000,
                "total_videos": 175,
                "average_views_per_video": 4285,
                "subscriber_growth_rate": 0.15,  # 15% monthly growth
                "view_growth_rate": 0.22,  # 22% monthly growth
            },
            "demographics": {
                "age_groups": {
                    "18-24": 25,
                    "25-34": 35,
                    "35-44": 20,
                    "45-54": 12,
                    "55-64": 6,
                    "65+": 2
                },
                "gender": {
                    "male": 68,
                    "female": 30,
                    "other": 2
                },
                "top_countries": [
                    {"country": "United States", "percentage": 45},
                    {"country": "United Kingdom", "percentage": 12},
                    {"country": "Canada", "percentage": 8},
                    {"country": "Australia", "percentage": 6},
                    {"country": "Germany", "percentage": 5}
                ]
            },
            "engagement": {
                "average_watch_time": "PT6M30S",
                "click_through_rate": 0.08,  # 8% CTR
                "like_rate": 0.12,  # 12% of viewers like
                "comment_rate": 0.03,  # 3% of viewers comment
                "subscriber_conversion_rate": 0.05  # 5% of viewers subscribe
            },
            "revenue": {
                "estimated_monthly_revenue": 2500,
                "rpm": 3.50,  # Revenue per mille
                "cpm": 4.20,  # Cost per mille
                "ad_revenue_percentage": 85,
                "membership_revenue": 250,
                "merchandise_revenue": 125
            }
        }
    
    @staticmethod
    def create_competitor_data() -> List[Dict[str, Any]]:
        """Create sample competitor data"""
        return [
            {
                "channel_id": "competitor-1",
                "channel_name": "Tech Guru Pro",
                "subscriber_count": 850000,
                "total_views": 45000000,
                "video_count": 320,
                "average_views": 140625,
                "upload_frequency": "Daily",
                "niche_overlap": 0.85,
                "strengths": ["High production quality", "Consistent uploads", "Strong SEO"],
                "weaknesses": ["Less personal connection", "Repetitive content"],
                "recent_performance": {
                    "last_30_days_views": 2500000,
                    "last_30_days_subscribers": 15000,
                    "trending_videos": 3
                }
            },
            {
                "channel_id": "competitor-2", 
                "channel_name": "Code Academy Live",
                "subscriber_count": 425000,
                "total_views": 18000000,
                "video_count": 180,
                "average_views": 100000,
                "upload_frequency": "3x per week",
                "niche_overlap": 0.75,
                "strengths": ["Interactive content", "Clear explanations", "Good thumbnails"],
                "weaknesses": ["Lower production value", "Inconsistent branding"],
                "recent_performance": {
                    "last_30_days_views": 1200000,
                    "last_30_days_subscribers": 8500,
                    "trending_videos": 1
                }
            }
        ]
    
    @staticmethod
    def create_content_analysis_response() -> Dict[str, Any]:
        """Create sample content analysis agent response"""
        return {
            "agent_type": "content_analysis",
            "response_id": "content-analysis-456",
            "request_id": "request-123",
            "timestamp": datetime.now().isoformat(),
            "confidence_score": 0.92,
            "domain_match": True,
            "analysis": {
                "summary": "Your content shows strong performance with room for optimization in hooks and retention.",
                "metrics": {
                    "average_view_duration": 6.5,
                    "retention_rate": 0.65,
                    "click_through_rate": 0.08,
                    "engagement_score": 8.2
                },
                "key_insights": [
                    {
                        "insight": "Your tutorial videos perform 40% better than vlogs",
                        "evidence": "Tutorial videos average 12K views vs 8.5K for vlogs",
                        "impact": "High",
                        "confidence": 0.95
                    },
                    {
                        "insight": "Videos with questions in titles get 25% more engagement",
                        "evidence": "Question-based titles show higher CTR and comments",
                        "impact": "Medium",
                        "confidence": 0.88
                    }
                ],
                "recommendations": [
                    {
                        "recommendation": "Focus more on tutorial-style content",
                        "expected_impact": "High",
                        "implementation_difficulty": "Easy",
                        "reasoning": "Tutorials consistently outperform other content types"
                    },
                    {
                        "recommendation": "Improve video hooks in first 15 seconds",
                        "expected_impact": "Medium",
                        "implementation_difficulty": "Medium",
                        "reasoning": "40% drop-off in first 15 seconds indicates weak hooks"
                    }
                ]
            },
            "token_usage": {
                "input_tokens": 3200,
                "output_tokens": 1800,
                "model": "gemini-2.5-pro"
            },
            "cache_info": {
                "cache_hit": False,
                "cache_key": "content_analysis_test_channel_30d",
                "ttl_remaining": 7200
            },
            "processing_time": 2.8,
            "for_boss_agent_only": True
        }
    
    @staticmethod
    def create_audience_insights_response() -> Dict[str, Any]:
        """Create sample audience insights agent response"""
        return {
            "agent_type": "audience_insights",
            "response_id": "audience-insights-789",
            "request_id": "request-123",
            "timestamp": datetime.now().isoformat(),
            "confidence_score": 0.89,
            "domain_match": True,
            "analysis": {
                "summary": "Your audience is primarily tech-savvy millennials with high engagement potential.",
                "demographics": {
                    "primary_age_group": "25-34",
                    "gender_split": {"male": 68, "female": 30, "other": 2},
                    "top_locations": ["US", "UK", "Canada", "Australia", "Germany"]
                },
                "behavior_patterns": {
                    "peak_activity_hours": ["19:00-21:00", "12:00-13:00"],
                    "preferred_content_length": "8-12 minutes",
                    "engagement_triggers": ["tutorials", "code examples", "problem-solving"]
                },
                "key_insights": [
                    {
                        "insight": "Your audience prefers hands-on learning content",
                        "evidence": "Code-along videos have 3x higher retention",
                        "impact": "High",
                        "confidence": 0.93
                    }
                ],
                "recommendations": [
                    {
                        "recommendation": "Create more interactive coding sessions",
                        "expected_impact": "High",
                        "implementation_difficulty": "Medium",
                        "reasoning": "Audience strongly responds to participatory content"
                    }
                ]
            },
            "token_usage": {
                "input_tokens": 2800,
                "output_tokens": 1500,
                "model": "claude-3-5-sonnet-20241022"
            },
            "for_boss_agent_only": True
        }
    
    @staticmethod
    def create_boss_agent_response() -> Dict[str, Any]:
        """Create sample boss agent synthesized response"""
        return {
            "response": "Based on my analysis of your channel, you're doing great with tutorial content! Your tech tutorials are significantly outperforming other content types, and your audience of tech-savvy millennials is highly engaged. I recommend focusing more on hands-on coding sessions and improving your video hooks in the first 15 seconds to reduce the 40% early drop-off rate.",
            "intent": "content_analysis",
            "confidence": 0.91,
            "agent_sources": ["content_analysis", "audience_insights"],
            "thinking_process": [
                "Classified user intent as content analysis request",
                "Delegated to content analysis agent for performance metrics",
                "Delegated to audience insights agent for demographic data",
                "Synthesized findings into actionable recommendations"
            ],
            "follow_up_suggestions": [
                "Would you like specific hook examples for your next video?",
                "Should I analyze your competitor strategies?",
                "Want me to help optimize your upload schedule?"
            ],
            "token_usage": {
                "total_tokens": 5800,
                "boss_agent_tokens": 2200,
                "specialist_tokens": 3600
            },
            "processing_time": 4.2,
            "success": True
        }
    
    @staticmethod
    def create_chat_history(user_id: str = "test-user-123") -> List[Dict[str, Any]]:
        """Create sample chat history"""
        return [
            {
                "message_id": "msg-001",
                "user_id": user_id,
                "message": "How are my videos performing?",
                "response": "Your videos are performing well overall! Your tutorial content is particularly strong...",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "intent": "content_analysis"
            },
            {
                "message_id": "msg-002", 
                "user_id": user_id,
                "message": "What should I focus on to grow my channel?",
                "response": "Based on your analytics, I recommend focusing on three key areas...",
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "intent": "growth_strategy"
            },
            {
                "message_id": "msg-003",
                "user_id": user_id,
                "message": "Can you help me improve my video titles?",
                "response": "Absolutely! Here are some title optimization strategies...",
                "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "intent": "seo_optimization"
            }
        ]
    
    @staticmethod
    def create_error_scenarios() -> Dict[str, Dict[str, Any]]:
        """Create various error scenarios for testing"""
        return {
            "api_rate_limit": {
                "error_type": "RateLimitError",
                "message": "API rate limit exceeded",
                "status_code": 429,
                "retry_after": 60
            },
            "invalid_api_key": {
                "error_type": "AuthenticationError", 
                "message": "Invalid API key provided",
                "status_code": 401
            },
            "service_unavailable": {
                "error_type": "ServiceUnavailableError",
                "message": "External service temporarily unavailable",
                "status_code": 503
            },
            "invalid_input": {
                "error_type": "ValidationError",
                "message": "Invalid input parameters",
                "status_code": 422,
                "details": {
                    "field": "user_id",
                    "error": "Field required"
                }
            },
            "database_error": {
                "error_type": "DatabaseError",
                "message": "Database connection failed",
                "status_code": 500
            }
        }


# Convenience instances for direct use
sample_data = SampleDataFactory()