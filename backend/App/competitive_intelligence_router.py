"""
Competitive Intelligence 2.0 API Router
Advanced market positioning and competitive strategy endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from backend.App.competitive_intelligence_2 import get_competitive_intelligence_engine

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/competitive-intelligence", tags=["competitive-intelligence"])

# Request/Response Models
class CompetitiveAnalysisRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth: quick, standard, comprehensive")
    include_blue_oceans: bool = Field(default=True, description="Include blue ocean opportunity analysis")
    competitor_limit: int = Field(default=10, description="Maximum number of competitors to analyze")

class CompetitorProfileResponse(BaseModel):
    competitor_id: str
    name: str
    channel_url: str
    tier: str
    subscriber_count: int
    avg_views: float
    growth_rate: float
    strengths: List[str]
    weaknesses: List[str]
    content_strategy: Dict[str, Any]

class ContentGapResponse(BaseModel):
    gap_id: str
    topic: str
    search_volume: int
    competition_level: str
    opportunity_score: float
    potential_views: int
    difficulty_rating: float
    suggested_approach: str
    keywords: List[str]
    estimated_effort: str

class MarketOpportunityResponse(BaseModel):
    opportunity_id: str
    type: str
    title: str
    description: str
    opportunity_score: float
    effort_required: str
    time_sensitivity: str
    potential_impact: str
    action_steps: List[str]
    competitors_missing: List[str]

class CompetitiveThreatResponse(BaseModel):
    threat_id: str
    competitor_name: str
    threat_level: str
    threat_type: str
    description: str
    impact_assessment: str
    timeline: str
    mitigation_strategies: List[str]

class BlueOceanOpportunityResponse(BaseModel):
    ocean_id: str
    market_name: str
    market_size: int
    competition_density: float
    entry_difficulty: str
    potential_roi: float
    unique_value_proposition: str
    success_probability: float
    investment_required: str

class CompetitiveLandscapeResponse(BaseModel):
    analysis_timestamp: str
    analysis_depth: str
    competitive_landscape: Dict[str, Any]
    competitor_profiles: List[CompetitorProfileResponse]
    content_gaps: List[ContentGapResponse]
    market_opportunities: List[MarketOpportunityResponse]
    competitive_threats: List[CompetitiveThreatResponse]
    blue_ocean_opportunities: List[BlueOceanOpportunityResponse]
    strategic_recommendations: Dict[str, Any]
    next_analysis_date: str

class QuickInsightsResponse(BaseModel):
    market_position: Dict[str, Any]
    top_opportunity: Optional[Dict[str, Any]]
    urgent_threat: Optional[Dict[str, Any]]
    recommended_action: str
    competitive_score: float

# Get competitive intelligence engine
def get_ci_engine():
    return get_competitive_intelligence_engine()

# API Endpoints

@router.post("/analyze", response_model=CompetitiveLandscapeResponse)
async def analyze_competitive_landscape(
    request: CompetitiveAnalysisRequest,
    ci_engine = Depends(get_ci_engine)
):
    """
    Perform comprehensive competitive landscape analysis
    
    Returns detailed competitive intelligence including:
    - Competitor profiles and analysis
    - Content gaps and opportunities
    - Market positioning insights
    - Strategic recommendations
    - Blue ocean opportunities
    """
    try:
        logger.info(f"🔍 Starting competitive analysis for user {request.user_id}")
        
        # Perform competitive analysis
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=request.user_id,
            analysis_depth=request.analysis_depth
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        logger.info(f"✅ Competitive analysis completed for user {request.user_id}")
        return CompetitiveLandscapeResponse(**analysis_result)
        
    except Exception as e:
        logger.error(f"Error in competitive analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/quick-insights/{user_id}", response_model=QuickInsightsResponse)
async def get_quick_competitive_insights(
    user_id: str,
    ci_engine = Depends(get_ci_engine)
):
    """
    Get quick competitive insights and recommendations
    
    Returns:
    - Current market position
    - Top opportunity
    - Most urgent threat
    - Recommended immediate action
    """
    try:
        logger.info(f"📊 Getting quick insights for user {user_id}")
        
        # Get full analysis (cached if recent)
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=user_id,
            analysis_depth="quick"
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        # Extract quick insights
        market_position = analysis_result.get('competitive_landscape', {}).get('market_position', {})
        
        # Get top opportunity
        opportunities = analysis_result.get('market_opportunities', [])
        top_opportunity = None
        if opportunities:
            top_opportunity = max(opportunities, key=lambda x: x.get('opportunity_score', 0))
        
        # Get most urgent threat
        threats = analysis_result.get('competitive_threats', [])
        urgent_threat = None
        if threats:
            urgent_threats = [t for t in threats if t.get('threat_level') in ['high', 'critical']]
            urgent_threat = urgent_threats[0] if urgent_threats else threats[0]
        
        # Generate recommended action
        recommended_action = "Continue current strategy"
        if top_opportunity:
            recommended_action = f"Focus on: {top_opportunity.get('title', 'Top opportunity')}"
        elif urgent_threat:
            recommended_action = f"Address threat: {urgent_threat.get('threat_type', 'Competitive threat')}"
        
        # Calculate competitive score
        competitive_score = market_position.get('overall_score', 50.0)
        
        quick_insights = QuickInsightsResponse(
            market_position=market_position,
            top_opportunity=top_opportunity,
            urgent_threat=urgent_threat,
            recommended_action=recommended_action,
            competitive_score=competitive_score
        )
        
        logger.info(f"✅ Quick insights generated for user {user_id}")
        return quick_insights
        
    except Exception as e:
        logger.error(f"Error getting quick insights: {e}")
        raise HTTPException(status_code=500, detail=f"Quick insights failed: {str(e)}")

@router.get("/content-gaps/{user_id}")
async def get_content_gaps(
    user_id: str,
    limit: int = Query(default=10, ge=1, le=50, description="Number of content gaps to return"),
    min_opportunity_score: float = Query(default=0.0, ge=0.0, le=100.0, description="Minimum opportunity score"),
    ci_engine = Depends(get_ci_engine)
):
    """
    Get content gap opportunities for strategic content planning
    
    Returns prioritized list of content gaps with:
    - Opportunity scores
    - Search volume data
    - Competition analysis
    - Implementation guidance
    """
    try:
        logger.info(f"🎯 Getting content gaps for user {user_id}")
        
        # Get analysis with focus on content gaps
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=user_id,
            analysis_depth="standard"
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        # Filter and limit content gaps
        content_gaps = analysis_result.get('content_gaps', [])
        
        # Filter by minimum opportunity score
        filtered_gaps = [
            gap for gap in content_gaps 
            if gap.get('opportunity_score', 0) >= min_opportunity_score
        ]
        
        # Limit results
        limited_gaps = filtered_gaps[:limit]
        
        logger.info(f"✅ Found {len(limited_gaps)} content gaps for user {user_id}")
        return {
            'content_gaps': limited_gaps,
            'total_found': len(filtered_gaps),
            'analysis_timestamp': analysis_result.get('analysis_timestamp'),
            'filters_applied': {
                'min_opportunity_score': min_opportunity_score,
                'limit': limit
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting content gaps: {e}")
        raise HTTPException(status_code=500, detail=f"Content gaps analysis failed: {str(e)}")

@router.get("/market-opportunities/{user_id}")
async def get_market_opportunities(
    user_id: str,
    opportunity_type: Optional[str] = Query(default=None, description="Filter by opportunity type"),
    min_score: float = Query(default=0.0, ge=0.0, le=100.0, description="Minimum opportunity score"),
    ci_engine = Depends(get_ci_engine)
):
    """
    Get strategic market opportunities
    
    Returns:
    - Timing advantages
    - Format innovations
    - Audience overlap opportunities
    - Blue ocean markets
    """
    try:
        logger.info(f"🚀 Getting market opportunities for user {user_id}")
        
        # Get analysis
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=user_id,
            analysis_depth="comprehensive"
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        # Get opportunities
        opportunities = analysis_result.get('market_opportunities', [])
        blue_oceans = analysis_result.get('blue_ocean_opportunities', [])
        
        # Filter opportunities
        if opportunity_type:
            opportunities = [opp for opp in opportunities if opp.get('type') == opportunity_type]
        
        opportunities = [opp for opp in opportunities if opp.get('opportunity_score', 0) >= min_score]
        
        logger.info(f"✅ Found {len(opportunities)} market opportunities and {len(blue_oceans)} blue oceans for user {user_id}")
        return {
            'market_opportunities': opportunities,
            'blue_ocean_opportunities': blue_oceans,
            'analysis_timestamp': analysis_result.get('analysis_timestamp'),
            'filters_applied': {
                'opportunity_type': opportunity_type,
                'min_score': min_score
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting market opportunities: {e}")
        raise HTTPException(status_code=500, detail=f"Market opportunities analysis failed: {str(e)}")

@router.get("/competitive-threats/{user_id}")
async def get_competitive_threats(
    user_id: str,
    threat_level: Optional[str] = Query(default=None, description="Filter by threat level: low, medium, high, critical"),
    ci_engine = Depends(get_ci_engine)
):
    """
    Get competitive threat assessment
    
    Returns:
    - Identified threats
    - Impact assessments
    - Mitigation strategies
    - Monitoring recommendations
    """
    try:
        logger.info(f"⚠️ Getting competitive threats for user {user_id}")
        
        # Get analysis
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=user_id,
            analysis_depth="standard"
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        # Get threats
        threats = analysis_result.get('competitive_threats', [])
        
        # Filter by threat level
        if threat_level:
            threats = [threat for threat in threats if threat.get('threat_level') == threat_level]
        
        # Sort by threat level priority
        threat_priority = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        threats.sort(key=lambda x: threat_priority.get(x.get('threat_level', 'low'), 1), reverse=True)
        
        logger.info(f"✅ Found {len(threats)} competitive threats for user {user_id}")
        return {
            'competitive_threats': threats,
            'threat_summary': {
                'total_threats': len(analysis_result.get('competitive_threats', [])),
                'critical_threats': len([t for t in analysis_result.get('competitive_threats', []) if t.get('threat_level') == 'critical']),
                'high_threats': len([t for t in analysis_result.get('competitive_threats', []) if t.get('threat_level') == 'high']),
                'requires_immediate_attention': len([t for t in analysis_result.get('competitive_threats', []) if t.get('threat_level') in ['critical', 'high']])
            },
            'analysis_timestamp': analysis_result.get('analysis_timestamp'),
            'filters_applied': {
                'threat_level': threat_level
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting competitive threats: {e}")
        raise HTTPException(status_code=500, detail=f"Competitive threats analysis failed: {str(e)}")

@router.get("/strategic-recommendations/{user_id}")
async def get_strategic_recommendations(
    user_id: str,
    timeframe: str = Query(default="all", description="Timeframe: immediate, short_term, long_term, all"),
    ci_engine = Depends(get_ci_engine)
):
    """
    Get strategic recommendations based on competitive analysis
    
    Returns:
    - Immediate actions (next 2 weeks)
    - Short-term strategy (1-3 months)
    - Long-term vision (6-12 months)
    - Competitive positioning advice
    """
    try:
        logger.info(f"💡 Getting strategic recommendations for user {user_id}")
        
        # Get analysis
        analysis_result = await ci_engine.analyze_competitive_landscape(
            user_id=user_id,
            analysis_depth="comprehensive"
        )
        
        if 'error' in analysis_result:
            raise HTTPException(status_code=500, detail=analysis_result['error'])
        
        # Get recommendations
        recommendations = analysis_result.get('strategic_recommendations', {})
        
        # Filter by timeframe
        if timeframe != "all":
            if timeframe == "immediate":
                filtered_recommendations = {'immediate_actions': recommendations.get('immediate_actions', [])}
            elif timeframe == "short_term":
                filtered_recommendations = {'short_term_strategy': recommendations.get('short_term_strategy', [])}
            elif timeframe == "long_term":
                filtered_recommendations = {'long_term_vision': recommendations.get('long_term_vision', [])}
            else:
                filtered_recommendations = recommendations
        else:
            filtered_recommendations = recommendations
        
        logger.info(f"✅ Generated strategic recommendations for user {user_id}")
        return {
            'strategic_recommendations': filtered_recommendations,
            'analysis_timestamp': analysis_result.get('analysis_timestamp'),
            'competitive_score': analysis_result.get('competitive_landscape', {}).get('market_position', {}).get('overall_score', 50.0),
            'filters_applied': {
                'timeframe': timeframe
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting strategic recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Strategic recommendations failed: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for competitive intelligence service"""
    return {
        "status": "healthy",
        "service": "Competitive Intelligence 2.0",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }
