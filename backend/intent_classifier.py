"""
Intent Classification System for Vidalytics Boss Agent
Analyzes user messages to determine appropriate specialized agent routing
"""

import json
import logging
from typing import Dict, Tuple
from agent_models import QueryType
from agent_model_adapter import migrate_openai_call_to_integration

logger = logging.getLogger(__name__)

class IntentClassifier:
    """Classifies user messages into query intents"""
    
    def __init__(self):
        # No longer needs OpenAI client - uses centralized model integration
        pass
        
    async def classify_intent(self, message: str, context: Dict) -> Tuple[QueryType, Dict]:
        """
        Classify user message intent and extract parameters
        
        Args:
            message: User's message
            context: Channel context and user data
            
        Returns:
            Tuple of (QueryType, extracted parameters)
        """
        
        channel_info = context.get('channel_info', {})
        classification_prompt = f"""
        You are Vidalytics's AI intent classifier. Analyze this YouTube creator's message with precision and extract actionable parameters.
        
        CREATOR MESSAGE: "{message}"
        
        CHANNEL CONTEXT:
        - Channel: {channel_info.get('name', 'Unknown')}
        - Niche: {channel_info.get('niche', 'Unknown')} 
        - Subscribers: {channel_info.get('subscriber_count', 0):,}
        - Total Views: {channel_info.get('total_view_count', 0):,}
        - Recent Performance: {channel_info.get('recent_views', 0):,} views (last 7d)
        
        INTENT CLASSIFICATION:
        Classify into the MOST SPECIFIC category:
        
        1. **content_analysis** - Video performance, analytics, metrics, rankings
           • Triggers: "best video", "top performing", "most views", "analytics", "performance", "total views", "video count", "CTR", "retention"
           • Examples: "what's my best video?", "total views?", "which content performs best?"
        
        2. **audience** - Demographics, behavior, engagement, subscriber insights  
           • Triggers: "audience", "subscribers", "demographics", "engagement", "comments", "who watches"
           • Examples: "who is my audience?", "how many subscribers?", "engagement rate?"
        
        3. **seo** - Search optimization, keywords, discoverability, algorithm
           • Triggers: "SEO", "keywords", "search", "ranking", "discoverability", "algorithm"
           • Examples: "optimize my titles", "keyword research", "search rankings"
        
        4. **competition** - Competitor analysis, benchmarking, market research
           • Triggers: "competitors", "compare", "benchmark", "similar channels", "market"
           • Examples: "analyze competitors", "how do I compare?", "market positioning"
        
        5. **monetization** - Revenue, sponsorships, monetization strategies
           • Triggers: "revenue", "money", "monetize", "sponsorship", "ads", "earnings"
           • Examples: "how to monetize?", "revenue optimization", "sponsorship rates"
        
        6. **general** - Greetings, unclear requests, or out-of-scope questions
           • Triggers: "hello", "help", unclear or non-YouTube related content
        
        PARAMETER EXTRACTION:
        Extract specific, actionable parameters:
        - time_period: "last_7d", "last_30d", "last_90d", or "all_time"
        - specific_videos: Exact video titles or IDs mentioned
        - competitors: Specific channel names mentioned
        - metrics: Specific metrics requested (views, CTR, retention, engagement, revenue)
        - focus_areas: Specific aspects to analyze
        
        RESPONSE FORMAT:
        {{
            "intent": "most_specific_category",
            "confidence": 0.85-1.0,
            "parameters": {{
                "time_period": "extracted_or_default_last_30d",
                "specific_videos": ["exact_titles_mentioned"],
                "competitors": ["exact_channel_names"],
                "metrics": ["specific_metrics_requested"],
                "focus_areas": ["specific_analysis_areas"]
            }},
            "reasoning": "Specific trigger words and context that led to this classification"
        }}
        """
        
        try:
            # Use model integration system for better model selection and fallbacks
            messages = [{"role": "user", "content": classification_prompt}]
            raw_content = await migrate_openai_call_to_integration(
                "boss_agent", messages, "quick"
            )
            logger.info(f"GPT-4o classification response: {raw_content}")
            
            # Try to extract JSON from the response
            if "```json" in raw_content:
                # Extract JSON from code block
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', raw_content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(1)
                else:
                    json_content = raw_content
            else:
                json_content = raw_content
            
            result = json.loads(json_content)
            intent = QueryType(result["intent"])
            
            return intent, result["parameters"]
            
        except json.JSONDecodeError as e:
            logger.error(f"Intent classification JSON parse failed: {e}")
            logger.error(f"Raw response: {raw_content}")
            # Fall back to manual parsing for content analysis
            if any(keyword in message.lower() for keyword in ["best video", "top video", "performing", "views", "analytics"]):
                return QueryType.CONTENT_ANALYSIS, {"time_period": "last_30d"}
            return QueryType.GENERAL, {}
        except Exception as e:
            logger.error(f"Intent classification failed: {e}")
            return QueryType.GENERAL, {}

def get_intent_classifier() -> IntentClassifier:
    """Get or create intent classifier instance"""
    return IntentClassifier()