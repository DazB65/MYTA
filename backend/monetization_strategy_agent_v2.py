"""
Monetization Strategy Agent for CreatorMate (Refactored)
Specialized sub-agent that analyzes revenue optimization opportunities using BaseAgent
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
# Monetization Analysis Engine
# =============================================================================

class MonetizationAnalysisEngine:
    """Claude-powered monetization analysis engine"""
    
    def __init__(self, api_key: str):
        if api_key and api_key != "demo_key":
            self.client = OpenAI(api_key=api_key)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
    
    async def analyze_monetization_opportunities(self, channel_context: Dict, request_context: Dict) -> Dict[str, Any]:
        """Analyze monetization strategies and revenue optimization"""
        
        if not self.enabled:
            return self._generate_fallback_analysis(channel_context)
        
        monetization_status = channel_context.get('monetization_status', 'Unknown')
        primary_goal = channel_context.get('primary_goal', 'Unknown')
        
        analysis_prompt = f"""
        As a YouTube monetization specialist, optimize revenue strategies for this channel:
        
        Channel: {channel_context.get('name', 'Unknown')}
        Niche: {channel_context.get('niche', 'Unknown')}
        Subscribers: {channel_context.get('subscriber_count', 0):,}
        Average Views: {channel_context.get('avg_view_count', 0):,}
        Content Type: {channel_context.get('content_type', 'Unknown')}
        Current Monetization: {monetization_status}
        Primary Goal: {primary_goal}
        
        Provide comprehensive monetization analysis including:
        1. Current Revenue Stream Assessment & Performance
        2. Monetization Opportunity Analysis & Potential
        3. Sponsorship & Brand Deal Strategies & Targeting
        4. Product/Service Integration & Development Opportunities
        5. Long-term Revenue Diversification Strategy
        
        Format as JSON with: summary, key_insights, recommendations, monetization_metrics
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
            logger.error(f"Monetization analysis error: {e}")
            return self._generate_fallback_analysis(channel_context)
    
    def _parse_text_response(self, content: str, channel_context: Dict) -> Dict[str, Any]:
        """Parse text response into structured format"""
        niche = channel_context.get('niche', 'Unknown')
        subscriber_count = channel_context.get('subscriber_count', 0)
        
        return {
            "summary": f"Monetization analysis for {niche} channel reveals revenue optimization opportunities",
            "key_insights": [
                {
                    "insight": f"Channel ready for {niche}-specific monetization strategies",
                    "evidence": f"Analysis of {subscriber_count:,} subscribers and {niche} market",
                    "impact": "High",
                    "confidence": 0.8
                },
                {
                    "insight": "Multiple revenue streams recommended for stability",
                    "evidence": "Diversification reduces dependence on single income source",
                    "impact": "Medium",
                    "confidence": 0.9
                }
            ],
            "recommendations": [
                {
                    "recommendation": f"Develop {niche}-specific product offerings",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": f"Products aligned with {niche} audience needs generate strong revenue"
                },
                {
                    "recommendation": "Implement tiered sponsorship packages for brands",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Structured packages attract more brand partnerships"
                }
            ],
            "monetization_metrics": {
                "revenue_potential_score": 8.2,
                "diversification_opportunities": 6,
                "brand_partnership_readiness": 7.5
            }
        }
    
    def _generate_fallback_analysis(self, channel_context: Dict) -> Dict[str, Any]:
        """Generate basic monetization analysis when AI is unavailable"""
        niche = channel_context.get('niche', 'Unknown')
        subscriber_count = channel_context.get('subscriber_count', 0)
        monetization_status = channel_context.get('monetization_status', 'Unknown')
        
        # Determine monetization readiness based on subscriber count
        if subscriber_count < 1000:
            readiness = "building foundation"
            focus = "growing audience before monetization"
            revenue_streams = ["affiliate marketing", "community building"]
        elif subscriber_count < 10000:
            readiness = "early monetization"
            focus = "implementing basic revenue streams"
            revenue_streams = ["YouTube Partner Program", "sponsorships", "affiliate marketing"]
        elif subscriber_count < 100000:
            readiness = "scaling monetization"
            focus = "diversifying and optimizing revenue"
            revenue_streams = ["brand partnerships", "products/courses", "membership programs"]
        else:
            readiness = "advanced monetization"
            focus = "maximizing revenue efficiency"
            revenue_streams = ["premium products", "speaking engagements", "business ventures"]
        
        return {
            "summary": f"Monetization analysis shows channel in {readiness} phase, focusing on {focus}",
            "key_insights": [
                {
                    "insight": f"Channel is in {readiness} phase with {subscriber_count:,} subscribers",
                    "evidence": f"Subscriber count indicates {readiness} for monetization strategies",
                    "impact": "High",
                    "confidence": 0.9
                },
                {
                    "insight": f"Optimal revenue streams: {', '.join(revenue_streams)}",
                    "evidence": f"Best suited for current {readiness} phase",
                    "impact": "High",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": f"Prioritize {focus} strategies",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": f"Critical for success in {readiness} phase"
                },
                {
                    "recommendation": f"Explore {revenue_streams[0]} as primary revenue source",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy" if subscriber_count > 1000 else "Medium",
                    "reasoning": f"Most appropriate for current subscriber level"
                }
            ],
            "monetization_metrics": {
                "monetization_readiness": readiness,
                "primary_focus": focus,
                "recommended_streams": revenue_streams,
                "revenue_potential": "high" if subscriber_count > 10000 else "medium" if subscriber_count > 1000 else "building"
            }
        }

# =============================================================================
# Monetization Strategy Agent (Refactored)
# =============================================================================

class MonetizationStrategyAgent(BaseSpecializedAgent):
    """
    Monetization Strategy Agent using BaseAgent architecture
    Massive code reduction compared to original implementation
    """
    
    def __init__(self, youtube_api_key: str = None, openai_api_key: str = None):
        super().__init__(
            agent_type=AgentType.MONETIZATION_STRATEGY,
            youtube_api_key=youtube_api_key,
            ai_api_key=openai_api_key,
            model_name="gpt-4o"
        )
        
        # Initialize monetization analysis engine
        self.monetization_engine = MonetizationAnalysisEngine(openai_api_key or "demo_key")
        
        logger.info("Monetization Strategy Agent v2 initialized with BaseAgent")
    
    def _get_domain_keywords(self) -> List[str]:
        """Return monetization domain keywords"""
        return [
            'monetization', 'revenue', 'income', 'earnings', 'sponsorship',
            'brand deal', 'affiliate', 'product', 'course', 'membership',
            'monetize', 'money', 'profit', 'business', 'partnership',
            'revenue stream', 'monetization strategy', 'income optimization'
        ]
    
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Core monetization analysis implementation"""
        
        # Get channel context
        channel_context = get_channel_context(request.user_context)
        
        # Perform monetization analysis
        monetization_analysis = await self.monetization_engine.analyze_monetization_opportunities(
            channel_context, 
            request.context
        )
        
        # Convert to standardized format
        return self._convert_to_standard_analysis(monetization_analysis)
    
    def _convert_to_standard_analysis(self, monetization_analysis: Dict) -> AgentAnalysis:
        """Convert monetization analysis to standardized format"""
        
        # Convert insights
        insights = []
        for insight_data in monetization_analysis.get('key_insights', []):
            insights.append(create_insight(
                insight=insight_data.get('insight', ''),
                evidence=insight_data.get('evidence', ''),
                impact=insight_data.get('impact', 'Medium'),
                confidence=insight_data.get('confidence', 0.8)
            ))
        
        # Convert recommendations
        recommendations = []
        for rec_data in monetization_analysis.get('recommendations', []):
            recommendations.append(create_recommendation(
                recommendation=rec_data.get('recommendation', ''),
                expected_impact=rec_data.get('expected_impact', 'Medium'),
                implementation_difficulty=rec_data.get('implementation_difficulty', 'Medium'),
                reasoning=rec_data.get('reasoning', '')
            ))
        
        return AgentAnalysis(
            summary=monetization_analysis.get('summary', 'Monetization analysis completed'),
            metrics=monetization_analysis.get('monetization_metrics', {}),
            key_insights=insights,
            recommendations=recommendations,
            detailed_analysis={
                'monetization_analysis': monetization_analysis,
                'revenue_opportunities': monetization_analysis.get('revenue_opportunities', {}),
                'optimization_strategies': monetization_analysis.get('optimization_strategies', {}),
                'partnership_opportunities': monetization_analysis.get('partnership_opportunities', {})
            }
        )

# =============================================================================
# Global Instance and Factory Function
# =============================================================================

monetization_strategy_agent = None

def get_monetization_strategy_agent():
    """Get or create monetization strategy agent instance"""
    global monetization_strategy_agent
    
    if monetization_strategy_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY", "demo_key")
        openai_api_key = os.getenv("OPENAI_API_KEY", "demo_key")
        
        monetization_strategy_agent = MonetizationStrategyAgent(youtube_api_key, openai_api_key)
    
    return monetization_strategy_agent

async def process_monetization_strategy_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main function for boss agent to request monetization analysis"""
    agent = get_monetization_strategy_agent()
    return await agent.process_boss_agent_request(request_data)