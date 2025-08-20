"""
YouTube Knowledge Base for MYTA
Comprehensive YouTube expertise, best practices, and platform-specific guidance
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

class YouTubeKnowledge:
    """Comprehensive YouTube knowledge base for AI agents"""
    
    def __init__(self):
        self.algorithm_insights = self._load_algorithm_insights()
        self.best_practices = self._load_best_practices()
        self.optimization_strategies = self._load_optimization_strategies()
        self.content_strategies = self._load_content_strategies()
        self.monetization_guide = self._load_monetization_guide()
        self.analytics_benchmarks = self._load_analytics_benchmarks()
        self.troubleshooting_guide = self._load_troubleshooting_guide()
    
    def _load_algorithm_insights(self) -> Dict[str, Any]:
        """YouTube algorithm insights and ranking factors"""
        return {
            "ranking_factors": {
                "primary": [
                    "Watch time and session duration",
                    "Click-through rate (CTR)",
                    "Audience retention",
                    "Engagement (likes, comments, shares)",
                    "Video freshness and upload consistency",
                    "Viewer satisfaction signals"
                ],
                "secondary": [
                    "Video length optimization",
                    "Thumbnail and title performance",
                    "Description and tags relevance",
                    "End screen and card usage",
                    "Community engagement",
                    "Channel authority and subscriber count"
                ]
            },
            "algorithm_updates": {
                "2024": [
                    "Increased focus on Shorts integration",
                    "Enhanced AI-driven content recommendations",
                    "Improved creator-viewer matching",
                    "Better spam and misinformation detection"
                ],
                "key_changes": [
                    "Shorts now contribute to overall channel performance",
                    "Live streaming gets algorithm boost",
                    "Community posts affect recommendation",
                    "Playlist optimization impacts discovery"
                ]
            },
            "optimization_tips": {
                "upload_timing": "Consistent schedule more important than specific time",
                "video_length": "8-15 minutes optimal for most niches",
                "first_24_hours": "Critical for algorithm momentum",
                "engagement_window": "First 2 hours determine initial reach",
                "retention_targets": "50%+ retention for good performance"
            }
        }
    
    def _load_best_practices(self) -> Dict[str, Any]:
        """YouTube best practices by category"""
        return {
            "thumbnails": {
                "design_principles": [
                    "High contrast and bold colors",
                    "Clear, readable text (if any)",
                    "Faces with emotions perform well",
                    "Consistent branding elements",
                    "A/B testing different styles"
                ],
                "technical_specs": {
                    "resolution": "1280x720 pixels minimum",
                    "aspect_ratio": "16:9",
                    "file_size": "Under 2MB",
                    "formats": "JPG, GIF, PNG"
                },
                "common_mistakes": [
                    "Too much text",
                    "Low contrast",
                    "Misleading imagery",
                    "Poor mobile visibility"
                ]
            },
            "titles": {
                "best_practices": [
                    "Front-load important keywords",
                    "Keep under 60 characters",
                    "Use emotional triggers",
                    "Include numbers when relevant",
                    "Avoid clickbait that doesn't deliver"
                ],
                "power_words": [
                    "Ultimate", "Complete", "Secret", "Proven",
                    "Easy", "Quick", "Advanced", "Professional"
                ],
                "title_formulas": [
                    "How to [Achieve Goal] in [Time Frame]",
                    "[Number] [Things] That [Benefit]",
                    "The Ultimate Guide to [Topic]",
                    "Why [Common Belief] is Wrong"
                ]
            },
            "descriptions": {
                "structure": [
                    "Hook in first 125 characters",
                    "Detailed video summary",
                    "Timestamps for long videos",
                    "Links to related content",
                    "Call-to-action",
                    "Social media links"
                ],
                "seo_tips": [
                    "Include target keywords naturally",
                    "Use relevant hashtags (3-5 max)",
                    "Add video transcript",
                    "Include related search terms"
                ]
            }
        }
    
    def _load_optimization_strategies(self) -> Dict[str, Any]:
        """Channel and video optimization strategies"""
        return {
            "channel_optimization": {
                "channel_art": {
                    "dimensions": "2560x1440 pixels",
                    "safe_area": "1546x423 pixels",
                    "elements": ["Channel name", "Upload schedule", "Value proposition"]
                },
                "about_section": [
                    "Clear channel description",
                    "Upload schedule",
                    "Contact information",
                    "Channel keywords",
                    "Links to other platforms"
                ],
                "playlists": [
                    "Organize content by topic",
                    "Use keyword-rich titles",
                    "Add compelling descriptions",
                    "Set custom thumbnails",
                    "Optimize playlist order"
                ]
            },
            "video_optimization": {
                "pre_upload": [
                    "Keyword research",
                    "Competitor analysis",
                    "Content planning",
                    "Thumbnail creation",
                    "Title optimization"
                ],
                "during_upload": [
                    "Optimized filename",
                    "Complete metadata",
                    "Custom thumbnail",
                    "End screens and cards",
                    "Captions/subtitles"
                ],
                "post_upload": [
                    "Community engagement",
                    "Social media promotion",
                    "Performance monitoring",
                    "Optimization adjustments"
                ]
            },
            "seo_strategies": {
                "keyword_research": [
                    "Use YouTube search suggestions",
                    "Analyze competitor keywords",
                    "Check Google Trends",
                    "Use keyword tools",
                    "Monitor search volume"
                ],
                "tag_optimization": [
                    "Use specific long-tail keywords",
                    "Include broad category tags",
                    "Add misspelling variations",
                    "Use 10-15 relevant tags",
                    "Include branded terms"
                ]
            }
        }
    
    def _load_content_strategies(self) -> Dict[str, Any]:
        """Content creation and strategy guidance"""
        return {
            "content_types": {
                "educational": {
                    "formats": ["Tutorials", "How-to guides", "Explainers", "Reviews"],
                    "best_practices": [
                        "Clear learning objectives",
                        "Step-by-step structure",
                        "Visual demonstrations",
                        "Downloadable resources"
                    ]
                },
                "entertainment": {
                    "formats": ["Vlogs", "Challenges", "Reactions", "Comedy"],
                    "best_practices": [
                        "Strong personality",
                        "Consistent character",
                        "Engaging storytelling",
                        "Audience interaction"
                    ]
                },
                "informational": {
                    "formats": ["News", "Analysis", "Documentaries", "Interviews"],
                    "best_practices": [
                        "Credible sources",
                        "Balanced perspectives",
                        "Clear presentation",
                        "Timely content"
                    ]
                }
            },
            "content_planning": {
                "content_calendar": [
                    "Plan 4-6 weeks ahead",
                    "Mix content types",
                    "Consider seasonal trends",
                    "Plan series and collaborations",
                    "Leave room for trending topics"
                ],
                "series_development": [
                    "Choose compelling themes",
                    "Plan episode structure",
                    "Create consistent branding",
                    "Build anticipation",
                    "Cross-promote episodes"
                ]
            },
            "engagement_strategies": {
                "community_building": [
                    "Respond to comments quickly",
                    "Ask questions in videos",
                    "Create community posts",
                    "Host live streams",
                    "Collaborate with other creators"
                ],
                "retention_techniques": [
                    "Strong hooks in first 15 seconds",
                    "Pattern interrupts",
                    "Preview upcoming content",
                    "Use visual variety",
                    "Maintain good pacing"
                ]
            }
        }
    
    def _load_monetization_guide(self) -> Dict[str, Any]:
        """Monetization strategies and requirements"""
        return {
            "youtube_partner_program": {
                "requirements": {
                    "subscribers": 1000,
                    "watch_hours": 4000,
                    "community_guidelines": "Good standing",
                    "content_policy": "Advertiser-friendly"
                },
                "revenue_streams": [
                    "Ad revenue",
                    "Channel memberships",
                    "Super Chat/Super Thanks",
                    "YouTube Premium revenue"
                ]
            },
            "alternative_monetization": {
                "sponsorships": [
                    "Brand partnerships",
                    "Product placements",
                    "Affiliate marketing",
                    "Sponsored content"
                ],
                "direct_monetization": [
                    "Merchandise sales",
                    "Course creation",
                    "Consulting services",
                    "Patreon/membership sites"
                ]
            },
            "optimization_tips": {
                "ad_revenue": [
                    "Create advertiser-friendly content",
                    "Optimize video length (8+ minutes)",
                    "Use mid-roll ads strategically",
                    "Monitor demonetization risks"
                ],
                "sponsorship_rates": {
                    "micro": "$10-50 per 1K views",
                    "small": "$50-200 per 1K views",
                    "medium": "$200-500 per 1K views",
                    "large": "$500+ per 1K views"
                }
            }
        }
    
    def _load_analytics_benchmarks(self) -> Dict[str, Any]:
        """YouTube analytics benchmarks and KPIs"""
        return {
            "performance_benchmarks": {
                "click_through_rate": {
                    "excellent": ">10%",
                    "good": "6-10%",
                    "average": "4-6%",
                    "poor": "<4%"
                },
                "audience_retention": {
                    "excellent": ">60%",
                    "good": "50-60%",
                    "average": "40-50%",
                    "poor": "<40%"
                },
                "engagement_rate": {
                    "excellent": ">6%",
                    "good": "4-6%",
                    "average": "2-4%",
                    "poor": "<2%"
                }
            },
            "growth_metrics": {
                "subscriber_growth": {
                    "viral": ">1000/month",
                    "fast": "100-1000/month",
                    "steady": "10-100/month",
                    "slow": "<10/month"
                },
                "view_velocity": {
                    "first_hour": "Critical for algorithm",
                    "first_24_hours": "Determines reach",
                    "first_week": "Long-term performance indicator"
                }
            },
            "channel_health": {
                "upload_consistency": "Weekly minimum recommended",
                "content_variety": "80/20 rule (80% proven, 20% experimental)",
                "audience_retention": "Maintain 45%+ average",
                "subscriber_to_view_ratio": "1:10 to 1:20 healthy range"
            }
        }
    
    def _load_troubleshooting_guide(self) -> Dict[str, Any]:
        """Common YouTube problems and solutions"""
        return {
            "low_views": {
                "causes": [
                    "Poor thumbnail/title",
                    "Inconsistent uploads",
                    "Low audience retention",
                    "Poor SEO optimization",
                    "Algorithm not picking up content"
                ],
                "solutions": [
                    "A/B test thumbnails",
                    "Improve video hooks",
                    "Optimize upload schedule",
                    "Research better keywords",
                    "Engage with community more"
                ]
            },
            "low_retention": {
                "causes": [
                    "Weak opening",
                    "Poor pacing",
                    "Irrelevant content",
                    "Technical issues",
                    "Misleading title/thumbnail"
                ],
                "solutions": [
                    "Stronger hooks",
                    "Better editing",
                    "Content restructuring",
                    "Audio/video quality improvement",
                    "Honest marketing"
                ]
            },
            "algorithm_issues": {
                "symptoms": [
                    "Sudden view drops",
                    "Reduced impressions",
                    "Lower CTR",
                    "Decreased reach"
                ],
                "recovery_strategies": [
                    "Maintain upload consistency",
                    "Focus on audience retention",
                    "Engage with community",
                    "Try different content types",
                    "Optimize for search"
                ]
            }
        }
    
    def get_knowledge_for_agent(self, agent_id: str, topic: str = None) -> Dict[str, Any]:
        """Get relevant knowledge for specific agent"""
        
        agent_knowledge = {
            "1": {  # Alex - Analytics
                "focus_areas": ["analytics_benchmarks", "algorithm_insights", "troubleshooting_guide"],
                "specialties": ["Performance analysis", "KPI interpretation", "Growth metrics"]
            },
            "2": {  # Levi - Content
                "focus_areas": ["content_strategies", "best_practices", "optimization_strategies"],
                "specialties": ["Content creation", "Video production", "Creative optimization"]
            },
            "3": {  # Maya - Engagement
                "focus_areas": ["content_strategies", "best_practices"],
                "specialties": ["Community building", "Audience engagement", "Retention strategies"]
            },
            "4": {  # Zara - Growth
                "focus_areas": ["algorithm_insights", "optimization_strategies", "monetization_guide"],
                "specialties": ["Channel growth", "Algorithm optimization", "Scaling strategies"]
            },
            "5": {  # Kai - Technical
                "focus_areas": ["optimization_strategies", "best_practices", "troubleshooting_guide"],
                "specialties": ["SEO optimization", "Technical setup", "Platform mechanics"]
            }
        }
        
        agent_info = agent_knowledge.get(agent_id, agent_knowledge["1"])
        
        knowledge = {}
        for area in agent_info["focus_areas"]:
            if hasattr(self, area):
                knowledge[area] = getattr(self, area)
        
        knowledge["specialties"] = agent_info["specialties"]
        
        return knowledge
    
    def get_topic_guidance(self, topic: str, channel_size: str = "micro") -> Dict[str, Any]:
        """Get specific guidance for a topic based on channel size"""
        
        guidance = {
            "thumbnails": self.best_practices["thumbnails"],
            "titles": self.best_practices["titles"],
            "seo": self.optimization_strategies["seo_strategies"],
            "monetization": self.monetization_guide,
            "analytics": self.analytics_benchmarks,
            "algorithm": self.algorithm_insights,
            "content": self.content_strategies,
            "retention": self.troubleshooting_guide["low_retention"]
        }
        
        base_guidance = guidance.get(topic.lower(), {})
        
        # Add channel-size specific advice
        if channel_size == "micro":
            base_guidance["size_specific_tips"] = [
                "Focus on consistency over perfection",
                "Engage with every comment",
                "Collaborate with similar-sized creators",
                "Use trending hashtags strategically"
            ]
        elif channel_size == "small":
            base_guidance["size_specific_tips"] = [
                "Develop signature content style",
                "Build email list",
                "Consider live streaming",
                "Start building brand partnerships"
            ]
        
        return base_guidance

# Global knowledge base instance
_youtube_knowledge: Optional[YouTubeKnowledge] = None

def get_youtube_knowledge() -> YouTubeKnowledge:
    """Get or create global YouTube knowledge base instance"""
    global _youtube_knowledge
    if _youtube_knowledge is None:
        _youtube_knowledge = YouTubeKnowledge()
    return _youtube_knowledge
