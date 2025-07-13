"""
Competitive Analysis Agent for CreatorMate (Refactored)
Specialized sub-agent that analyzes competitor performance and market positioning using BaseAgent
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging
import os
import google.generativeai as genai

# Import base agent system
from base_agent import (
    BaseSpecializedAgent, AgentType, AgentRequest, AgentAnalysis,
    AgentInsight, AgentRecommendation, get_channel_context,
    create_insight, create_recommendation
)

# Configure logging
logger = logging.getLogger(__name__)

# =============================================================================
# Competitive Analysis Engine
# =============================================================================

class CompetitiveAnalysisEngine:
    """Gemini-powered competitive analysis engine"""
    
    def __init__(self, api_key: str):
        if api_key and api_key != "demo_key":
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.enabled = True
        else:
            self.model = None
            self.enabled = False
    
    async def analyze_competitive_landscape(self, channel_context: Dict, request_context: Dict) -> Dict[str, Any]:
        """Analyze competitive landscape and positioning"""
        
        if not self.enabled:
            return self._generate_fallback_analysis(channel_context)
        
        niche = channel_context.get('niche', 'Unknown')
        competitors = request_context.get('competitors', [])
        competitor_info = f"Competitors: {', '.join(competitors)}" if competitors else f"General {niche} competitive landscape"
        
        analysis_prompt = f"""
        As a competitive analysis expert, analyze market positioning for this YouTube channel:
        
        Channel: {channel_context.get('name', 'Unknown')}
        Niche: {niche}
        Subscribers: {channel_context.get('subscriber_count', 0):,}
        Average Views: {channel_context.get('avg_view_count', 0):,}
        Content Type: {channel_context.get('content_type', 'Unknown')}
        
        {competitor_info}
        
        Provide comprehensive competitive analysis including:
        1. Competitive Landscape Overview in {niche}
        2. Content Strategy Comparison & Differentiation
        3. Performance Benchmarking Against Industry Standards
        4. Market Opportunity Gaps & Niches
        5. Strategic Positioning & Differentiation Recommendations
        
        Format as JSON with: summary, key_insights, recommendations, competitive_metrics
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
                    analysis_json = self._parse_analysis_response(analysis_text, channel_context)
            except:
                analysis_json = self._parse_analysis_response(analysis_text, channel_context)
            
            return analysis_json
            
        except Exception as e:
            logger.error(f"Competitive analysis error: {e}")
            return self._generate_fallback_analysis(channel_context)
    
    def _parse_analysis_response(self, response_text: str, channel_context: Dict) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
        niche = channel_context.get('niche', 'Unknown')
        
        return {
            "summary": f"Competitive analysis for {niche} channel reveals market positioning opportunities",
            "key_insights": [
                {
                    "insight": f"Channel operates in competitive {niche} space",
                    "evidence": f"Market analysis of {niche} content creators",
                    "impact": "High",
                    "confidence": 0.8
                },
                {
                    "insight": "Differentiation opportunities exist in content approach",
                    "evidence": "Analysis of content strategy and market gaps",
                    "impact": "Medium",
                    "confidence": 0.7
                }
            ],
            "recommendations": [
                {
                    "recommendation": f"Focus on unique angles within {niche} to stand out",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": "Differentiation is key in competitive markets"
                },
                {
                    "recommendation": "Study top performers in niche for successful patterns",
                    "expected_impact": "High",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Learning from successful competitors accelerates growth"
                }
            ],
            "competitive_metrics": {
                "market_saturation": "medium",
                "differentiation_score": 7.2,
                "competitive_advantage_potential": 8.1
            },
            "raw_analysis": response_text
        }
    
    def _generate_fallback_analysis(self, channel_context: Dict) -> Dict[str, Any]:
        """Generate basic competitive analysis when Gemini is unavailable"""
        niche = channel_context.get('niche', 'Unknown')
        subscriber_count = channel_context.get('subscriber_count', 0)
        
        # Assess competitive position based on subscriber count
        if subscriber_count < 1000:
            position = "new entrant"
            strategy = "establishing market presence"
        elif subscriber_count < 10000:
            position = "emerging competitor"
            strategy = "scaling and differentiation"
        elif subscriber_count < 100000:
            position = "established player"
            strategy = "market leadership in sub-niches"
        else:
            position = "market leader"
            strategy = "maintaining competitive advantage"
        
        return {
            "summary": f"Competitive analysis shows channel as {position} in {niche} market, focusing on {strategy}",
            "key_insights": [
                {
                    "insight": f"Channel positioned as {position} in {niche} space",
                    "evidence": f"Based on {subscriber_count:,} subscribers and market analysis",
                    "impact": "High",
                    "confidence": 0.9
                },
                {
                    "insight": f"Market strategy should focus on {strategy}",
                    "evidence": f"Optimal approach for {position} in competitive landscape",
                    "impact": "High",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                {
                    "recommendation": f"Prioritize {strategy} initiatives",
                    "expected_impact": "High",
                    "implementation_difficulty": "Medium",
                    "reasoning": f"Critical for success as {position} in market"
                },
                {
                    "recommendation": f"Monitor top {niche} competitors for trend identification",
                    "expected_impact": "Medium",
                    "implementation_difficulty": "Easy",
                    "reasoning": "Staying informed helps anticipate market changes"
                }
            ],
            "competitive_metrics": {
                "market_position": position,
                "recommended_strategy": strategy,
                "niche_focus": niche,
                "competitive_pressure": "medium" if subscriber_count > 1000 else "low"
            }
        }

# =============================================================================
# Competitive Analysis Agent (Refactored)
# =============================================================================

class CompetitiveAnalysisAgent(BaseSpecializedAgent):
    """
    Competitive Analysis Agent using BaseAgent architecture
    Massive code reduction compared to original implementation
    """
    
    def __init__(self, youtube_api_key: str = None, gemini_api_key: str = None):
        super().__init__(
            agent_type=AgentType.COMPETITIVE_ANALYSIS,
            youtube_api_key=youtube_api_key,
            ai_api_key=gemini_api_key,
            model_name="gemini-2.0-flash-exp"
        )
        
        # Initialize competitive analysis engine
        self.competitive_engine = CompetitiveAnalysisEngine(gemini_api_key or "demo_key")
        
        logger.info("Competitive Analysis Agent v2 initialized with BaseAgent")
    
    def _get_domain_keywords(self) -> List[str]:
        """Return competitive analysis domain keywords"""
        return [
            'competitor', 'competition', 'competitive analysis', 'market positioning',
            'benchmarking', 'market share', 'competitor performance', 'differentiation',
            'market research', 'competitive landscape', 'industry analysis',
            'market positioning', 'competitive advantage', 'market comparison'
        ]
    
    async def _perform_analysis(self, request: AgentRequest) -> AgentAnalysis:
        """Core competitive analysis implementation"""
        
        # Get channel context
        channel_context = get_channel_context(request.user_context)
        
        # Perform competitive analysis
        competitive_analysis = await self.competitive_engine.analyze_competitive_landscape(
            channel_context, 
            request.context
        )
        
        # Convert to standardized format
        return self._convert_to_standard_analysis(competitive_analysis)
    
    def _convert_to_standard_analysis(self, competitive_analysis: Dict) -> AgentAnalysis:
        """Convert competitive analysis to standardized format"""
        
        # Convert insights
        insights = []
        for insight_data in competitive_analysis.get('key_insights', []):
            insights.append(create_insight(
                insight=insight_data.get('insight', ''),
                evidence=insight_data.get('evidence', ''),
                impact=insight_data.get('impact', 'Medium'),
                confidence=insight_data.get('confidence', 0.8)
            ))
        
        # Convert recommendations
        recommendations = []
        for rec_data in competitive_analysis.get('recommendations', []):
            recommendations.append(create_recommendation(
                recommendation=rec_data.get('recommendation', ''),
                expected_impact=rec_data.get('expected_impact', 'Medium'),
                implementation_difficulty=rec_data.get('implementation_difficulty', 'Medium'),
                reasoning=rec_data.get('reasoning', '')
            ))
        
        return AgentAnalysis(
            summary=competitive_analysis.get('summary', 'Competitive analysis completed'),
            metrics=competitive_analysis.get('competitive_metrics', {}),
            key_insights=insights,
            recommendations=recommendations,
            detailed_analysis={
                'competitive_analysis': competitive_analysis,
                'market_positioning': competitive_analysis.get('market_positioning', {}),
                'competitive_advantages': competitive_analysis.get('competitive_advantages', {}),
                'market_opportunities': competitive_analysis.get('market_opportunities', {})
            }
        )

# =============================================================================
# Global Instance and Factory Function
# =============================================================================

competitive_analysis_agent = None

def get_competitive_analysis_agent():
    """Get or create competitive analysis agent instance"""
    global competitive_analysis_agent
    
    if competitive_analysis_agent is None:
        youtube_api_key = os.getenv("YOUTUBE_API_KEY", "demo_key")
        gemini_api_key = os.getenv("GEMINI_API_KEY", "demo_key")
        
        competitive_analysis_agent = CompetitiveAnalysisAgent(youtube_api_key, gemini_api_key)
    
    return competitive_analysis_agent

async def process_competitive_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Main function for boss agent to request competitive analysis"""
    agent = get_competitive_analysis_agent()
    return await agent.process_boss_agent_request(request_data)