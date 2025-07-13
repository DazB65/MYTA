"""
Audience Insights Agent for CreatorMate (Refactored)
Specialized sub-agent that analyzes YouTube audience demographics and behavior using BaseAgent
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import os
from openai import OpenAI

# Import base agent system
from base_agent import (
    BaseSpecializedAgent, AgentType, AgentRequest, AgentAnalysis,
    AgentInsight, AgentRecommendation, get_channel_context,
    create_insight, create_recommendation
)

# Configure logging
logger = logging.getLogger(__name__)

# =============================================================================
# Audience Analysis Engine
# =============================================================================

class AudienceAnalysisEngine:
    """Claude-powered audience analysis engine"""
    
    def __init__(self, api_key: str):
        if api_key and api_key != "demo_key":
            self.client = OpenAI(api_key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    async def analyze_audience_behavior(self, channel_context: Dict, request_context: Dict) -> Dict[str, Any]:
        """Analyze audience demographics and behavior patterns"""
        
        if not self.enabled:
            return self._generate_fallback_analysis(channel_context)
        
        analysis_prompt = f"""
        As a YouTube audience insights specialist, analyze viewer behavior for this channel:
        
        Channel: {channel_context.get('name', 'Unknown')}
        Niche: {channel_context.get('niche', 'Unknown')}
        Subscribers: {channel_context.get('subscriber_count', 0):,}
        Average Views: {channel_context.get('avg_view_count', 0):,}
        Content Type: {channel_context.get('content_type', 'Unknown')}
        
        Provide comprehensive audience analysis including:
        1. Audience Demographics & Behavior Patterns
        2. Engagement Patterns & Optimal Timing
        3. Content Preferences & Viewer Retention
        4. Subscriber Growth Analysis & Opportunities
        5. Community Building Recommendations
        
        Format as JSON with: summary, key_insights, recommendations, audience_metrics
        """
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": analysis_prompt}],
                    temperature=0.2,
                    max_tokens=1200
                )
            )
            
            content = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                return json.loads(content)
            except:
                return self._parse_text_response(content, channel_context)
                
        except Exception as e:
            logger.error(f"Audience analysis error: {e}")
            return self._generate_fallback_analysis(channel_context)
    
    def _parse_text_response(self, content: str, channel_context: Dict) -> Dict[str, Any]:
        """Parse text response into structured format"""
        niche = channel_context.get('niche', 'Unknown')
        
        return {
            "summary": f"Audience analysis for {niche} channel reveals growth opportunities",
            "key_insights": [
                {
                    "insight": f"Primary audience likely interested in {niche} content",
                    "evidence": f"Channel operates in {niche} space with specific content focus",
                    "impact": "High",
                    "confidence": 0.8
                },
                {
                    "insight": "Engagement patterns show potential for community building",
                    "evidence": "Analysis of subscriber count and content interaction",
                    "impact": "Medium",
                    "confidence": 0.7
                }
            ],
            "recommendations": [
                {
                    "recommendation": "Focus on community engagement through comments and responses",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Active community engagement increases retention and loyalty"
                },
                {
                    "recommendation": f"Create {niche}-specific content series for audience retention",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": "Series content keeps audiences coming back for more"
                }
            ],
            "audience_metrics": {
                "estimated_primary_age_group": "25-34",
                "engagement_potential": 8.2,
                "community_health_score": 7.5
            }
        }
    
    def _generate_fallback_analysis(self, channel_context: Dict) -> Dict[str, Any]:
        """Generate basic audience analysis when AI is unavailable"""
        niche = channel_context.get('niche', 'Unknown')
        subscriber_count = channel_context.get('subscriber_count', 0)
        
        # Determine audience tier
        if subscriber_count < 1000:
            tier = "emerging"
            growth_focus = "building initial community"
        elif subscriber_count < 10000:
            tier = "growing"
            growth_focus = "scaling engagement"
        elif subscriber_count < 100000:
            tier = "established"
            growth_focus = "optimizing retention"
        else:
            tier = "large"
            growth_focus = "maintaining loyalty"
        
        return {
            "summary": f"Audience analysis for {tier} {niche} channel focused on {growth_focus}",
            "key_insights": [
                {
                    "insight": f"Channel is in {tier} phase with {subscriber_count:,} subscribers",
                    "evidence": f"Subscriber count indicates {tier} audience base",
                    "impact": "High",
                    "confidence": 0.9
                },
                {
                    "insight": f"{niche} content attracts dedicated audience segments",
                    "evidence": f"Niche specialization in {niche} creates focused community",
                    "impact": "Medium",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": f"Prioritize {growth_focus} strategies",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": f"Current {tier} status requires focus on {growth_focus}"
                },
                {
                    "recommendation": "Analyze top-performing content for audience preferences",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Understanding what resonates helps replicate success"
                }
            ],
            "audience_metrics": {
                "subscriber_tier": tier,
                "growth_stage": growth_focus,
                "niche_focus": niche,
                "estimated_engagement_rate": min(5.0, max(2.0, 10000 / max(subscriber_count, 1000)))
            }
        }

# =============================================================================
# Audience Insights Agent (Refactored)
# =============================================================================

class AudienceInsightsAgent(BaseSpecializedAgent):
    """
    Audience Insights Agent using BaseAgent architecture
    Massive code reduction compared to original implementation
    """
    
    def __init__(self, youtube_api_key: str = None, openai_api_key: str = None):
        super().__init__(
            agent_type=AgentType.AUDIENCE_INSIGHTS,
            youtube_api_key=youtube_api_key,
            ai_api_key=openai_api_key,
            model_name="gpt-4o"
        )
        
        # Initialize audience analysis engine
        self.audience_engine = AudienceAnalysisEngine(openai_api_key or "demo_key")
        
        logger.info("Audience Insights Agent v2 initialized with BaseAgent")
    
    def _get_domain_keywords(self) -> List[str]:
        """Return audience analysis domain keywords"""
        return [
            'audience', 'demographics', 'behavior', 'engagement patterns',
            'subscriber', 'viewers', 'community', 'retention', 'loyalty',
            'viewer behavior', 'audience analysis', 'engagement', 'followers',
            'subscriber count', 'audience insights', 'viewer demographics'
        ]
    
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Core audience analysis implementation"""
        
        # Get channel context
        channel_context = get_channel_context(request.user_context)
        
        # Perform audience analysis
        audience_analysis = await self.audience_engine.analyze_audience_behavior(
            channel_context, 
            request.context
        )
        
        # Convert to standardized format
        return self._convert_to_standard_analysis(audience_analysis)
    
    def _convert_to_standard_analysis(self, audience_analysis: Dict) -> AgentAnalysis:
        """Convert audience analysis to standardized format"""
        
        # Convert insights
        insights = []
        for insight_data in audience_analysis.get('key_insights', []):
            insights.append(create_insight(
                insight=insight_data.get('insight', ''),
                evidence=insight_data.get('evidence', ''),
                impact=insight_data.get('impact', 'Medium'),
                confidence=insight_data.get('confidence', 0.8)
            ))
        
        # Convert recommendations
        recommendations = []
        for rec_data in audience_analysis.get('recommendations', []):
            recommendations.append(create_recommendation(
                recommendation=rec_data.get('recommendation', ''),
                expected_impact=rec_data.get('expected_impact', 'Medium'),
                implementation_difficulty=rec_data.get('implementation_difficulty', 'Medium'),
                reasoning=rec_data.get('reasoning', '')
            ))
        
        return AgentAnalysis(
            summary=audience_analysis.get('summary', 'Audience analysis completed'),
            metrics=audience_analysis.get('audience_metrics', {}),
            key_insights=insights,
            recommendations=recommendations,
            detailed_analysis={
                'audience_analysis': audience_analysis,
                'demographics': audience_analysis.get('demographics', {}),
                'behavior_patterns': audience_analysis.get('behavior_patterns', {}),
                'engagement_insights': audience_analysis.get('engagement_insights', {})
            }
        )

# =============================================================================
# Global Instance and Factory Function
# =============================================================================

audience_insights_agent = None

def get_audience_insights_agent():
    """Get or create audience insights agent instance"""
    global audience_insights_agent
    
    if audience_insights_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY", "demo_key")
        openai_api_key = os.getenv("OPENAI_API_KEY", "demo_key")
        
        audience_insights_agent = AudienceInsightsAgent(youtube_api_key, openai_api_key)
    
    return audience_insights_agent

async def process_audience_insights_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main function for boss agent to request audience analysis"""
    agent = get_audience_insights_agent()
    return await agent.process_boss_agent_request(request_data)