"""
Agent Tools Router for MYTA
API endpoints for agent-specific tools and capabilities
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from typing import Dict, List, Optional, Any

from .agent_tools import get_agent_tools, AnalysisResult
from .channel_analyzer import get_channel_analyzer
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/agent-tools", tags=["agent_tools"])

@router.get("/available/{agent_id}")
async def get_available_tools(
    agent_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get available tools for a specific agent"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        agent_tools = get_agent_tools()
        available_tools = agent_tools.get_available_tools(agent_id)
        
        # Get agent info
        from .agent_personalities import get_agent_personality
        agent = get_agent_personality(agent_id)
        
        # Tool descriptions
        tool_descriptions = {
            "1": {  # Alex - Analytics
                "performance_analyzer": "Analyze channel performance metrics and benchmarks",
                "benchmark_comparator": "Compare metrics against industry standards",
                "growth_forecaster": "Forecast channel growth and milestone timelines",
                "revenue_optimizer": "Optimize revenue streams and monetization",
                "audience_insights": "Analyze audience demographics and behavior"
            },
            "2": {  # Levi - Content
                "content_analyzer": "Analyze content performance and optimization opportunities",
                "title_optimizer": "Optimize video titles for better performance",
                "thumbnail_evaluator": "Evaluate and optimize thumbnail design",
                "trend_spotter": "Identify trending content opportunities",
                "series_planner": "Plan content series and scheduling"
            },
            "3": {  # Maya - Engagement
                "engagement_analyzer": "Analyze audience engagement patterns",
                "community_health": "Assess community health and growth",
                "retention_optimizer": "Optimize audience retention strategies",
                "comment_strategy": "Develop comment interaction strategies",
                "live_stream_planner": "Plan live streaming content and schedule"
            },
            "4": {  # Zara - Growth
                "growth_strategy": "Develop comprehensive growth strategies",
                "algorithm_optimizer": "Optimize for YouTube algorithm performance",
                "scaling_planner": "Plan content scaling and production",
                "monetization_strategy": "Develop monetization and revenue strategies",
                "competitor_analyzer": "Analyze competitor strategies and opportunities"
            },
            "5": {  # Kai - Technical
                "seo_optimizer": "Optimize SEO and search discoverability",
                "metadata_analyzer": "Analyze and optimize video metadata",
                "technical_audit": "Perform technical channel audit",
                "workflow_optimizer": "Optimize content creation workflows",
                "platform_optimizer": "Optimize platform settings and features"
            }
        }
        
        agent_descriptions = tool_descriptions.get(agent_id, {})
        
        tools_with_descriptions = [
            {
                "name": tool,
                "description": agent_descriptions.get(tool, f"{tool.replace('_', ' ').title()} tool")
            }
            for tool in available_tools
        ]
        
        result = {
            "agent": {
                "id": agent_id,
                "name": agent["name"],
                "role": agent["role"],
                "color": agent["color"]
            },
            "available_tools": tools_with_descriptions,
            "total_tools": len(available_tools)
        }
        
        return create_success_response("Available tools retrieved successfully", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting available tools: {e}")
        return create_error_response("Failed to retrieve available tools", str(e))

@router.post("/execute/{agent_id}/{tool_name}")
async def execute_agent_tool(
    agent_id: str,
    tool_name: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Execute a specific tool for an agent"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get request context
        try:
            body = await request.json()
            context = body.get("context", {})
        except:
            context = {}
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Execute the tool
        agent_tools = get_agent_tools()
        result = agent_tools.execute_tool(agent_id, tool_name, profile, context)
        
        # Convert result to dict for JSON response
        result_data = {
            "agent_id": result.agent_id,
            "tool_name": result.tool_name,
            "analysis": result.analysis,
            "recommendations": result.recommendations,
            "action_items": result.action_items,
            "confidence_score": result.confidence_score,
            "timestamp": result.timestamp.isoformat(),
            "channel_context": {
                "name": profile.channel_name,
                "size_tier": profile.channel_size_tier,
                "niche": profile.niche
            }
        }
        
        return create_success_response(f"Tool '{tool_name}' executed successfully", result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing tool {tool_name} for agent {agent_id}: {e}")
        return create_error_response("Failed to execute tool", str(e))

@router.get("/suggest/{agent_id}")
async def suggest_best_tool(
    agent_id: str,
    message: str,
    current_user: Dict = Depends(get_current_user)
):
    """Suggest the best tool for an agent based on user message"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Get tool suggestion
        agent_tools = get_agent_tools()
        suggested_tool = agent_tools.suggest_best_tool(agent_id, message, profile)
        
        # Get tool description
        tool_descriptions = {
            "performance_analyzer": "Analyze your channel's performance metrics",
            "benchmark_comparator": "Compare your metrics against industry standards",
            "content_analyzer": "Analyze your content performance",
            "title_optimizer": "Optimize your video titles",
            "engagement_analyzer": "Analyze your audience engagement",
            "growth_strategy": "Develop growth strategies",
            "seo_optimizer": "Optimize your SEO and discoverability"
        }
        
        result = {
            "suggested_tool": suggested_tool,
            "description": tool_descriptions.get(suggested_tool, "Specialized analysis tool"),
            "reason": f"Based on your message about '{message[:50]}...', this tool will provide the most relevant insights",
            "channel_context": {
                "size_tier": profile.channel_size_tier,
                "primary_challenge": profile.challenges[0] if profile.challenges else "General optimization"
            }
        }
        
        return create_success_response("Tool suggestion generated", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error suggesting tool for agent {agent_id}: {e}")
        return create_error_response("Failed to suggest tool", str(e))

@router.get("/analysis-history/{agent_id}")
async def get_analysis_history(
    agent_id: str,
    limit: int = 10,
    current_user: Dict = Depends(get_current_user)
):
    """Get analysis history for an agent"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # In a real implementation, this would fetch from database
        # For now, return mock data structure
        
        from .agent_personalities import get_agent_personality
        agent = get_agent_personality(agent_id)
        
        # Mock analysis history
        history = [
            {
                "id": f"analysis_{i}",
                "tool_name": "performance_analyzer",
                "timestamp": "2024-01-15T10:30:00Z",
                "summary": f"Performance analysis #{i+1}",
                "confidence_score": 0.85,
                "key_insights": [
                    "CTR above average",
                    "Retention needs improvement",
                    "Strong engagement rate"
                ]
            }
            for i in range(min(limit, 5))
        ]
        
        result = {
            "agent": {
                "id": agent_id,
                "name": agent["name"],
                "role": agent["role"]
            },
            "analysis_history": history,
            "total_analyses": len(history)
        }
        
        return create_success_response("Analysis history retrieved", result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis history for agent {agent_id}: {e}")
        return create_error_response("Failed to retrieve analysis history", str(e))

@router.post("/batch-analysis/{agent_id}")
async def run_batch_analysis(
    agent_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Run multiple tools in batch for comprehensive analysis"""
    try:
        if agent_id not in ["1", "2", "3", "4", "5"]:
            raise HTTPException(status_code=400, detail="Invalid agent ID")
        
        user_id = current_user["id"]
        
        # Get request body
        body = await request.json()
        tools_to_run = body.get("tools", [])
        context = body.get("context", {})
        
        if not tools_to_run:
            # Default tool sets for each agent
            default_tools = {
                "1": ["performance_analyzer", "benchmark_comparator"],
                "2": ["content_analyzer", "title_optimizer"],
                "3": ["engagement_analyzer", "community_health"],
                "4": ["growth_strategy", "algorithm_optimizer"],
                "5": ["seo_optimizer", "metadata_analyzer"]
            }
            tools_to_run = default_tools.get(agent_id, ["performance_analyzer"])
        
        # Get user's channel profile
        channel_analyzer = get_channel_analyzer()
        profile = await channel_analyzer.get_channel_profile(user_id)
        
        # Execute all tools
        agent_tools = get_agent_tools()
        results = []
        
        for tool_name in tools_to_run:
            try:
                result = agent_tools.execute_tool(agent_id, tool_name, profile, context)
                results.append({
                    "tool_name": result.tool_name,
                    "analysis": result.analysis,
                    "recommendations": result.recommendations[:3],  # Top 3 recommendations
                    "action_items": result.action_items[:3],  # Top 3 action items
                    "confidence_score": result.confidence_score,
                    "timestamp": result.timestamp.isoformat()
                })
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                results.append({
                    "tool_name": tool_name,
                    "error": str(e),
                    "confidence_score": 0.0
                })
        
        # Generate comprehensive summary
        summary = self._generate_batch_summary(results, profile)
        
        result_data = {
            "agent_id": agent_id,
            "tools_executed": len(results),
            "individual_results": results,
            "comprehensive_summary": summary,
            "channel_context": {
                "name": profile.channel_name,
                "size_tier": profile.channel_size_tier,
                "niche": profile.niche
            }
        }
        
        return create_success_response("Batch analysis completed", result_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running batch analysis for agent {agent_id}: {e}")
        return create_error_response("Failed to run batch analysis", str(e))

def _generate_batch_summary(results: List[Dict], profile) -> Dict[str, Any]:
    """Generate comprehensive summary from batch analysis results"""
    
    all_recommendations = []
    all_actions = []
    avg_confidence = 0.0
    
    successful_results = [r for r in results if "error" not in r]
    
    for result in successful_results:
        all_recommendations.extend(result.get("recommendations", []))
        all_actions.extend(result.get("action_items", []))
        avg_confidence += result.get("confidence_score", 0.0)
    
    if successful_results:
        avg_confidence /= len(successful_results)
    
    # Deduplicate and prioritize
    unique_recommendations = list(dict.fromkeys(all_recommendations))[:5]
    unique_actions = list(dict.fromkeys(all_actions))[:5]
    
    return {
        "overall_confidence": round(avg_confidence, 2),
        "top_recommendations": unique_recommendations,
        "priority_actions": unique_actions,
        "analysis_quality": "high" if avg_confidence > 0.8 else "moderate" if avg_confidence > 0.6 else "basic",
        "tools_successful": len(successful_results),
        "tools_failed": len(results) - len(successful_results)
    }
