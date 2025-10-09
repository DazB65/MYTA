"""
Agent Adapters for Vidalytics
Provides adapter functions to connect agent router endpoints with specialized agents
"""

from typing import Dict, Any
import logging

# Import agent factories
from .content_analysis_agent import get_content_analysis_agent
from .audience_insights_agent import get_audience_insights_agent
from .seo_discoverability_agent import get_seo_discoverability_agent
from .competitive_analysis_agent import get_competitive_analysis_agent
from .monetization_strategy_agent import get_monetization_strategy_agent

logger = logging.getLogger(__name__)


async def process_content_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process content analysis request through the specialized agent"""
    try:
        agent = get_content_analysis_agent()
        return await agent.process_boss_agent_request(request_data)
    except Exception as e:
        logger.error(f"Content analysis adapter error: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent_type": "content_analysis"
        }


async def process_audience_insights_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process audience insights request through the specialized agent"""
    try:
        agent = get_audience_insights_agent()
        return await agent.process_boss_agent_request(request_data)
    except Exception as e:
        logger.error(f"Audience insights adapter error: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent_type": "audience_insights"
        }


async def process_seo_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process SEO discoverability request through the specialized agent"""
    try:
        agent = get_seo_discoverability_agent()
        return await agent.process_boss_agent_request(request_data)
    except Exception as e:
        logger.error(f"SEO discoverability adapter error: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent_type": "seo_discoverability"
        }


async def process_competitive_analysis_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process competitive analysis request through the specialized agent"""
    try:
        agent = get_competitive_analysis_agent()
        return await agent.process_boss_agent_request(request_data)
    except Exception as e:
        logger.error(f"Competitive analysis adapter error: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent_type": "competitive_analysis"
        }


async def process_monetization_strategy_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process monetization strategy request through the specialized agent"""
    try:
        agent = get_monetization_strategy_agent()
        return await agent.process_boss_agent_request(request_data)
    except Exception as e:
        logger.error(f"Monetization strategy adapter error: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent_type": "monetization_strategy"
        }