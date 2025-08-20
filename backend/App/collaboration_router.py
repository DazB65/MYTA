"""
Agent Collaboration Router for MYTA
API endpoints for multi-agent collaboration and analysis
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict, List, Optional, Any

from backend.App.agent_collaboration import get_collaboration_engine, CollaborationRequest
from backend.App.channel_analyzer import get_channel_analyzer
from backend.App.auth_middleware import get_current_user
from backend.App.response_utils import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/collaboration", tags=["agent_collaboration"])

@router.post("/initiate")
async def initiate_collaboration(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Initiate collaboration between multiple agents"""
    try:
        body = await request.json()
        
        primary_agent_id = body.get("primary_agent_id", "1")
        user_message = body.get("message", "")
        collaboration_type = body.get("collaboration_type", "comprehensive_analysis")
        required_perspectives = body.get("required_perspectives", [])
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if primary_agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid primary agent ID")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Determine complexity level
        complexity_level = _determine_complexity_level(user_message, profile)
        
        # Create collaboration request
        collaboration_request = CollaborationRequest(
            primary_agent_id=primary_agent_id,
            user_message=user_message,
            user_id=user_id,
            channel_profile=profile,
            complexity_level=complexity_level,
            required_perspectives=required_perspectives,
            collaboration_type=collaboration_type,
            context=body.get("context", {})
        )
        
        # Initiate collaboration
        collaboration_engine = get_collaboration_engine()
        result = await collaboration_engine.initiate_collaboration(collaboration_request)
        
        # Format response
        response_data = {
            "collaboration_id": f"collab_{user_id}_{primary_agent_id}",
            "primary_agent": {
                "id": result.primary_agent_id,
                "name": _get_agent_name(result.primary_agent_id)
            },
            "participating_agents": [
                {"id": agent_id, "name": _get_agent_name(agent_id)} 
                for agent_id in result.participating_agents
            ],
            "collaboration_summary": result.collaboration_summary,
            "problem_analysis": result.problem_analysis,
            "unified_recommendations": result.unified_recommendations,
            "consensus_areas": result.consensus_areas,
            "debate_points": result.debate_points,
            "action_plan": result.action_plan,
            "confidence_score": result.confidence_score,
            "perspective_breakdown": [
                {
                    "agent_id": contrib.agent_id,
                    "agent_name": contrib.agent_name,
                    "perspective": contrib.perspective,
                    "key_recommendations": contrib.recommendations[:3],
                    "main_concerns": contrib.concerns,
                    "confidence": contrib.confidence_score
                }
                for contrib in result.perspective_breakdown
            ],
            "channel_context": {
                "name": profile.channel_name,
                "size_tier": profile.channel_size_tier,
                "niche": profile.niche,
                "subscriber_count": profile.metrics.subscriber_count
            }
        }
        
        return create_success_response("Agent collaboration completed", response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating collaboration: {e}")
        return create_error_response("Failed to initiate collaboration", str(e))

@router.get("/patterns")
async def get_collaboration_patterns(current_user: Dict = Depends(get_current_user)):
    """Get available collaboration patterns"""
    try:
        collaboration_engine = get_collaboration_engine()
        patterns = collaboration_engine.collaboration_patterns
        
        # Format patterns for frontend
        formatted_patterns = {}
        for pattern_name, pattern_config in patterns.items():
            formatted_patterns[pattern_name] = {
                "name": pattern_name.replace("_", " ").title(),
                "description": pattern_config["description"],
                "required_agents": [
                    {"id": agent_id, "name": _get_agent_name(agent_id)}
                    for agent_id in pattern_config["required_agents"]
                ],
                "coordination_style": pattern_config["coordination_style"],
                "debate_enabled": pattern_config["debate_enabled"],
                "use_cases": _get_pattern_use_cases(pattern_name)
            }
        
        return create_success_response("Collaboration patterns retrieved", formatted_patterns)
        
    except Exception as e:
        logger.error(f"Error getting collaboration patterns: {e}")
        return create_error_response("Failed to retrieve collaboration patterns", str(e))

@router.post("/suggest-collaboration")
async def suggest_collaboration(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Suggest optimal collaboration approach for a given problem"""
    try:
        body = await request.json()
        user_message = body.get("message", "")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Analyze message to suggest collaboration approach
        collaboration_engine = get_collaboration_engine()
        
        # Create mock request to determine pattern
        mock_request = CollaborationRequest(
            primary_agent_id="1",
            user_message=user_message,
            user_id=user_id,
            channel_profile=profile,
            complexity_level="medium",
            required_perspectives=[],
            collaboration_type="auto",
            context={}
        )
        
        # Determine best collaboration pattern
        suggested_pattern = collaboration_engine._determine_collaboration_pattern(mock_request)
        pattern_name = _find_pattern_name(suggested_pattern, collaboration_engine.collaboration_patterns)
        
        # Select participating agents
        participating_agents = collaboration_engine._select_participating_agents(
            mock_request, suggested_pattern
        )
        
        # Determine complexity and estimated time
        complexity_level = _determine_complexity_level(user_message, profile)
        estimated_time = _estimate_collaboration_time(complexity_level, len(participating_agents))
        
        suggestion = {
            "recommended_pattern": {
                "name": pattern_name.replace("_", " ").title(),
                "description": suggested_pattern["description"],
                "coordination_style": suggested_pattern["coordination_style"]
            },
            "participating_agents": [
                {"id": agent_id, "name": _get_agent_name(agent_id)}
                for agent_id in participating_agents
            ],
            "complexity_assessment": {
                "level": complexity_level,
                "factors": _get_complexity_factors(user_message, profile),
                "estimated_time": estimated_time
            },
            "expected_outcomes": {
                "unified_recommendations": f"Expected {len(participating_agents) * 2}-{len(participating_agents) * 3} recommendations",
                "perspective_coverage": f"{len(participating_agents)} expert perspectives",
                "debate_potential": suggested_pattern.get("debate_enabled", False),
                "confidence_level": "High" if len(participating_agents) >= 3 else "Medium"
            },
            "channel_considerations": {
                "size_tier": profile.channel_size_tier,
                "primary_challenges": profile.challenges[:2],
                "optimization_focus": _determine_optimization_focus(profile)
            }
        }
        
        return create_success_response("Collaboration suggestion generated", suggestion)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error suggesting collaboration: {e}")
        return create_error_response("Failed to suggest collaboration", str(e))

@router.get("/agent-relationships")
async def get_agent_relationships(current_user: Dict = Depends(get_current_user)):
    """Get information about agent relationships and collaboration dynamics"""
    try:
        collaboration_engine = get_collaboration_engine()
        relationships = collaboration_engine.agent_relationships
        
        # Format relationships for frontend
        formatted_relationships = {
            "collaboration_strengths": {},
            "expertise_overlaps": {},
            "debate_dynamics": {}
        }
        
        # Format collaboration strengths
        for agent_id, strengths in relationships["collaboration_strengths"].items():
            agent_name = _get_agent_name(agent_id)
            formatted_relationships["collaboration_strengths"][agent_id] = {
                "agent_name": agent_name,
                "leads_well_with": [
                    {"id": aid, "name": _get_agent_name(aid)} 
                    for aid in strengths.get("leads_well_with", [])
                ],
                "supports_well": [
                    {"id": aid, "name": _get_agent_name(aid)} 
                    for aid in strengths.get("supports_well", [])
                ],
                "challenges_constructively": [
                    {"id": aid, "name": _get_agent_name(aid)} 
                    for aid in strengths.get("challenges_constructively", [])
                ],
                "expertise_areas": strengths.get("expertise_areas", [])
            }
        
        # Format expertise overlaps
        for overlap_name, agent_ids in relationships["expertise_overlaps"].items():
            formatted_relationships["expertise_overlaps"][overlap_name] = {
                "name": overlap_name.replace("_", " ").title(),
                "agents": [
                    {"id": agent_id, "name": _get_agent_name(agent_id)}
                    for agent_id in agent_ids
                ],
                "collaboration_potential": "High"
            }
        
        # Format debate dynamics
        for dynamic_name, dynamic_info in relationships["debate_dynamics"].items():
            formatted_relationships["debate_dynamics"][dynamic_name] = {
                "name": dynamic_name.replace("_", " ").title(),
                "agents": [
                    {"id": agent_id, "name": _get_agent_name(agent_id)}
                    for agent_id in dynamic_info["agents"]
                ],
                "common_tensions": dynamic_info["common_tensions"],
                "resolution_approach": dynamic_info["resolution_approach"]
            }
        
        return create_success_response("Agent relationships retrieved", formatted_relationships)
        
    except Exception as e:
        logger.error(f"Error getting agent relationships: {e}")
        return create_error_response("Failed to retrieve agent relationships", str(e))

@router.post("/simulate-collaboration")
async def simulate_collaboration(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Simulate collaboration outcome without full execution"""
    try:
        body = await request.json()
        
        user_message = body.get("message", "")
        selected_agents = body.get("selected_agents", [])
        collaboration_type = body.get("collaboration_type", "comprehensive_analysis")
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        if not selected_agents:
            raise HTTPException(status_code=400, detail="At least one agent must be selected")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Simulate collaboration outcome
        simulation = {
            "simulation_id": f"sim_{user_id}_{len(selected_agents)}",
            "selected_agents": [
                {"id": agent_id, "name": _get_agent_name(agent_id)}
                for agent_id in selected_agents
            ],
            "predicted_outcomes": {
                "recommendation_count": len(selected_agents) * 2,
                "perspective_diversity": _calculate_perspective_diversity(selected_agents),
                "debate_likelihood": _calculate_debate_likelihood(selected_agents),
                "consensus_probability": _calculate_consensus_probability(selected_agents),
                "confidence_estimate": _estimate_collaboration_confidence(selected_agents, profile)
            },
            "expected_perspectives": [
                {
                    "agent_id": agent_id,
                    "agent_name": _get_agent_name(agent_id),
                    "focus_area": _get_agent_focus_area(agent_id),
                    "likely_recommendations": _predict_agent_recommendations(agent_id, user_message, profile)
                }
                for agent_id in selected_agents
            ],
            "potential_debates": _identify_potential_debates(selected_agents),
            "estimated_timeline": _estimate_collaboration_time("medium", len(selected_agents)),
            "channel_alignment": {
                "size_tier_appropriate": _is_collaboration_appropriate_for_size(selected_agents, profile),
                "challenge_alignment": _assess_challenge_alignment(selected_agents, profile),
                "goal_alignment": _assess_goal_alignment(selected_agents, profile)
            }
        }
        
        return create_success_response("Collaboration simulation completed", simulation)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simulating collaboration: {e}")
        return create_error_response("Failed to simulate collaboration", str(e))

# Helper functions

def _get_agent_name(agent_id: str) -> str:
    """Get agent name by ID"""
    from backend.App.agent_personalities import get_agent_personality
    try:
        agent = get_agent_personality(agent_id)
        return agent["name"]
    except:
        return f"Agent {agent_id}"

def _determine_complexity_level(message: str, profile) -> str:
    """Determine complexity level of the problem"""
    message_lower = message.lower()
    
    # High complexity indicators
    if any(word in message_lower for word in ["comprehensive", "everything", "full analysis", "complex"]):
        return "high"
    
    # Low complexity indicators
    if any(word in message_lower for word in ["simple", "quick", "basic", "just"]):
        return "low"
    
    # Medium complexity (default)
    return "medium"

def _get_pattern_use_cases(pattern_name: str) -> List[str]:
    """Get use cases for collaboration pattern"""
    use_cases = {
        "comprehensive_analysis": [
            "Channel performance review",
            "Strategic planning sessions",
            "Major optimization initiatives"
        ],
        "performance_optimization": [
            "Declining metrics analysis",
            "CTR and retention improvement",
            "Algorithm optimization"
        ],
        "content_strategy": [
            "Content planning and optimization",
            "Audience engagement improvement",
            "Creative strategy development"
        ],
        "growth_acceleration": [
            "Rapid scaling strategies",
            "Breakthrough growth planning",
            "Algorithm mastery"
        ],
        "crisis_response": [
            "Urgent performance issues",
            "Damage control situations",
            "Emergency optimization"
        ],
        "monetization_strategy": [
            "Revenue optimization",
            "Business model development",
            "Sponsorship strategies"
        ]
    }
    
    return use_cases.get(pattern_name, ["General optimization"])

def _find_pattern_name(pattern_config: Dict, all_patterns: Dict) -> str:
    """Find pattern name by configuration"""
    for name, config in all_patterns.items():
        if config == pattern_config:
            return name
    return "comprehensive_analysis"

def _estimate_collaboration_time(complexity: str, agent_count: int) -> str:
    """Estimate collaboration time"""
    base_time = {
        "low": 2,
        "medium": 5,
        "high": 10
    }
    
    minutes = base_time.get(complexity, 5) + (agent_count * 2)
    
    if minutes < 5:
        return "2-5 minutes"
    elif minutes < 10:
        return "5-10 minutes"
    else:
        return "10-15 minutes"

def _get_complexity_factors(message: str, profile) -> List[str]:
    """Get factors contributing to complexity"""
    factors = []
    
    if len(message) > 100:
        factors.append("Detailed problem description")
    
    if profile.channel_size_tier == "large":
        factors.append("Large channel complexity")
    
    if len(profile.challenges) > 3:
        factors.append("Multiple channel challenges")
    
    return factors

def _determine_optimization_focus(profile) -> str:
    """Determine primary optimization focus"""
    if profile.metrics.avg_ctr < 0.04:
        return "Click-through rate improvement"
    elif profile.metrics.avg_retention < 0.40:
        return "Audience retention optimization"
    elif profile.metrics.engagement_rate < 0.02:
        return "Engagement enhancement"
    else:
        return "General performance optimization"

def _calculate_perspective_diversity(agent_ids: List[str]) -> str:
    """Calculate perspective diversity score"""
    if len(agent_ids) >= 4:
        return "Very High"
    elif len(agent_ids) >= 3:
        return "High"
    elif len(agent_ids) >= 2:
        return "Medium"
    else:
        return "Low"

def _calculate_debate_likelihood(agent_ids: List[str]) -> str:
    """Calculate likelihood of debates"""
    # Check for known debate pairs
    debate_pairs = [("1", "2"), ("2", "4"), ("3", "5")]
    
    for pair in debate_pairs:
        if pair[0] in agent_ids and pair[1] in agent_ids:
            return "High"
    
    if len(agent_ids) >= 3:
        return "Medium"
    else:
        return "Low"

def _calculate_consensus_probability(agent_ids: List[str]) -> str:
    """Calculate probability of consensus"""
    if len(agent_ids) <= 2:
        return "High"
    elif len(agent_ids) <= 3:
        return "Medium"
    else:
        return "Low"

def _estimate_collaboration_confidence(agent_ids: List[str], profile) -> str:
    """Estimate collaboration confidence"""
    if len(agent_ids) >= 3:
        return "High"
    elif len(agent_ids) >= 2:
        return "Medium"
    else:
        return "Low"

def _get_agent_focus_area(agent_id: str) -> str:
    """Get agent's primary focus area"""
    focus_areas = {
        "1": "Analytics and Performance",
        "2": "Content and Creativity",
        "3": "Engagement and Community",
        "4": "Growth and Strategy",
        "5": "Technical and SEO"
    }
    return focus_areas.get(agent_id, "General Optimization")

def _predict_agent_recommendations(agent_id: str, message: str, profile) -> List[str]:
    """Predict likely recommendations from agent"""
    predictions = {
        "1": ["Analyze performance metrics", "Compare against benchmarks"],
        "2": ["Optimize content strategy", "Improve creative elements"],
        "3": ["Enhance audience engagement", "Build community"],
        "4": ["Implement growth strategies", "Optimize for algorithm"],
        "5": ["Improve SEO optimization", "Technical enhancements"]
    }
    return predictions.get(agent_id, ["General optimization"])

def _identify_potential_debates(agent_ids: List[str]) -> List[str]:
    """Identify potential debate topics"""
    debates = []
    
    if "1" in agent_ids and "2" in agent_ids:
        debates.append("Data-driven vs Creative approach")
    
    if "2" in agent_ids and "4" in agent_ids:
        debates.append("Quality vs Speed of growth")
    
    if "3" in agent_ids and "5" in agent_ids:
        debates.append("Engagement vs Technical optimization")
    
    return debates

def _is_collaboration_appropriate_for_size(agent_ids: List[str], profile) -> bool:
    """Check if collaboration is appropriate for channel size"""
    if profile.channel_size_tier == "micro" and len(agent_ids) > 3:
        return False
    return True

def _assess_challenge_alignment(agent_ids: List[str], profile) -> str:
    """Assess how well agents align with channel challenges"""
    # Simplified assessment
    if len(profile.challenges) >= len(agent_ids):
        return "Well aligned"
    else:
        return "Partially aligned"

def _assess_goal_alignment(agent_ids: List[str], profile) -> str:
    """Assess how well agents align with channel goals"""
    # Simplified assessment
    if len(profile.goals) >= len(agent_ids):
        return "Well aligned"
    else:
        return "Partially aligned"
