"""
Proactive Agent Base Class
Enhances agents with proactive collaboration capabilities
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

from backend.App.proactive_agent_collaboration import (
    analyze_for_collaboration_opportunities,
    generate_proactive_insights,
    get_relevant_insights_for_agent,
    ProactiveInsight,
    CollaborationSuggestion
)

logger = logging.getLogger(__name__)

class ProactiveAgentMixin:
    """Mixin class that adds proactive collaboration capabilities to agents"""
    
    def __init__(self):
        self.agent_name = getattr(self, 'agent_name', self.__class__.__name__.lower())
        self.collaboration_enabled = True
        self.insight_sharing_enabled = True
        self.proactive_suggestions_enabled = True
    
    async def analyze_with_proactive_collaboration(
        self, 
        analysis_method, 
        *args, 
        user_context: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Enhanced analysis method that includes proactive collaboration
        
        Args:
            analysis_method: The original analysis method to call
            *args: Arguments for the analysis method
            user_context: User context for collaboration
            **kwargs: Keyword arguments for the analysis method
        
        Returns:
            Enhanced analysis results with collaboration insights
        """
        
        # Step 1: Get relevant insights from other agents
        relevant_insights = []
        if self.collaboration_enabled and user_context:
            try:
                relevant_insights = await get_relevant_insights_for_agent(
                    self.agent_name, 
                    user_context
                )
                
                if relevant_insights:
                    logger.info(f"🔍 {self.agent_name} received {len(relevant_insights)} relevant insights from other agents")
                    
                    # Add insights to context for enhanced analysis
                    if 'shared_insights' not in kwargs:
                        kwargs['shared_insights'] = relevant_insights
                    
            except Exception as e:
                logger.warning(f"Failed to get relevant insights for {self.agent_name}: {e}")
        
        # Step 2: Perform the original analysis
        try:
            if asyncio.iscoroutinefunction(analysis_method):
                analysis_results = await analysis_method(*args, **kwargs)
            else:
                analysis_results = analysis_method(*args, **kwargs)
        except Exception as e:
            logger.error(f"Analysis method failed for {self.agent_name}: {e}")
            analysis_results = {"error": str(e), "success": False}
        
        # Step 3: Generate proactive insights for other agents
        proactive_insights = []
        if self.insight_sharing_enabled and user_context and analysis_results.get("success", True):
            try:
                proactive_insights = await generate_proactive_insights(
                    self.agent_name,
                    analysis_results,
                    user_context
                )
                
                if proactive_insights:
                    logger.info(f"💡 {self.agent_name} generated {len(proactive_insights)} insights for other agents")
                
            except Exception as e:
                logger.warning(f"Failed to generate proactive insights for {self.agent_name}: {e}")
        
        # Step 4: Analyze for collaboration opportunities
        collaboration_suggestions = []
        if self.proactive_suggestions_enabled and user_context and analysis_results.get("success", True):
            try:
                collaboration_suggestions = await analyze_for_collaboration_opportunities(
                    self.agent_name,
                    analysis_results,
                    user_context
                )
                
                if collaboration_suggestions:
                    logger.info(f"🤝 {self.agent_name} suggests {len(collaboration_suggestions)} collaboration opportunities")
                
            except Exception as e:
                logger.warning(f"Failed to analyze collaboration opportunities for {self.agent_name}: {e}")
        
        # Step 5: Enhance results with collaboration data
        enhanced_results = analysis_results.copy() if isinstance(analysis_results, dict) else {"analysis": analysis_results}
        
        # Add collaboration metadata
        enhanced_results.update({
            "collaboration_metadata": {
                "agent_name": self.agent_name,
                "received_insights": len(relevant_insights),
                "generated_insights": len(proactive_insights),
                "collaboration_suggestions": len(collaboration_suggestions),
                "collaboration_enabled": self.collaboration_enabled,
                "analysis_timestamp": datetime.now().isoformat()
            }
        })
        
        # Add collaboration suggestions if any
        if collaboration_suggestions:
            enhanced_results["collaboration_suggestions"] = [
                {
                    "suggested_agents": suggestion.suggested_agents,
                    "reason": suggestion.collaboration_reason.value,
                    "expected_outcome": suggestion.expected_outcome,
                    "confidence": suggestion.confidence_score,
                    "urgency": suggestion.urgency_level.value
                }
                for suggestion in collaboration_suggestions
            ]
        
        # Add received insights summary
        if relevant_insights:
            enhanced_results["received_insights"] = [
                {
                    "source_agent": insight.source_agent,
                    "insight_type": insight.insight_type.value,
                    "interpretation": insight.insight_data.get("interpretation", ""),
                    "confidence": insight.confidence_score,
                    "urgency": insight.urgency_level.value
                }
                for insight in relevant_insights
            ]
        
        return enhanced_results
    
    def format_collaboration_summary(self, enhanced_results: Dict[str, Any]) -> str:
        """Format collaboration information for user display"""
        
        collaboration_meta = enhanced_results.get("collaboration_metadata", {})
        collaboration_suggestions = enhanced_results.get("collaboration_suggestions", [])
        received_insights = enhanced_results.get("received_insights", [])
        
        summary_parts = []
        
        # Add collaboration activity summary
        if collaboration_meta.get("received_insights", 0) > 0:
            summary_parts.append(f"📥 Incorporated insights from {collaboration_meta['received_insights']} other agents")
        
        if collaboration_meta.get("generated_insights", 0) > 0:
            summary_parts.append(f"💡 Shared {collaboration_meta['generated_insights']} insights with other agents")
        
        # Add collaboration suggestions
        if collaboration_suggestions:
            summary_parts.append(f"\n🤝 **Collaboration Opportunities:**")
            for suggestion in collaboration_suggestions[:3]:  # Show top 3 suggestions
                agents = ", ".join(suggestion["suggested_agents"])
                summary_parts.append(f"• Collaborate with {agents}: {suggestion['expected_outcome']}")
        
        # Add received insights summary
        if received_insights:
            summary_parts.append(f"\n🔍 **Insights from Other Agents:**")
            for insight in received_insights[:3]:  # Show top 3 insights
                summary_parts.append(f"• {insight['source_agent']}: {insight['interpretation']}")
        
        return "\n".join(summary_parts) if summary_parts else ""
    
    async def suggest_agent_collaboration(
        self, 
        target_agents: List[str], 
        reason: str, 
        expected_outcome: str,
        user_context: Dict[str, Any]
    ) -> bool:
        """Manually suggest collaboration with specific agents"""
        
        try:
            # This would trigger the collaboration suggestion system
            logger.info(f"🤝 {self.agent_name} manually suggests collaboration with {target_agents}: {reason}")
            
            # In a real implementation, this would create a collaboration suggestion
            # and potentially initiate a collaboration session
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to suggest collaboration for {self.agent_name}: {e}")
            return False
    
    def enable_collaboration(self, 
                           collaboration: bool = True, 
                           insight_sharing: bool = True, 
                           proactive_suggestions: bool = True):
        """Enable or disable collaboration features"""
        
        self.collaboration_enabled = collaboration
        self.insight_sharing_enabled = insight_sharing
        self.proactive_suggestions_enabled = proactive_suggestions
        
        logger.info(f"🔧 {self.agent_name} collaboration settings: "
                   f"collaboration={collaboration}, "
                   f"insight_sharing={insight_sharing}, "
                   f"proactive_suggestions={proactive_suggestions}")

class ProactiveAgent(ProactiveAgentMixin, ABC):
    """Abstract base class for proactive agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        super().__init__()
    
    @abstractmethod
    async def analyze(self, *args, **kwargs) -> Dict[str, Any]:
        """Abstract method for agent analysis - must be implemented by subclasses"""
        pass
    
    async def analyze_with_collaboration(self, *args, **kwargs) -> Dict[str, Any]:
        """Perform analysis with proactive collaboration"""
        return await self.analyze_with_proactive_collaboration(
            self.analyze, 
            *args, 
            **kwargs
        )

def enhance_agent_with_proactive_collaboration(agent_class):
    """Decorator to enhance existing agent classes with proactive collaboration"""
    
    class EnhancedAgent(ProactiveAgentMixin, agent_class):
        def __init__(self, *args, **kwargs):
            agent_class.__init__(self, *args, **kwargs)
            ProactiveAgentMixin.__init__(self)
            
            # Set agent name from class if not already set
            if not hasattr(self, 'agent_name'):
                self.agent_name = agent_class.__name__.lower().replace('agent', '')
    
    return EnhancedAgent

# Example usage:
# @enhance_agent_with_proactive_collaboration
# class ContentAnalysisAgent:
#     def analyze_content(self, content_data):
#         # Original analysis logic
#         return analysis_results
#
# # Now the agent has proactive collaboration capabilities:
# agent = ContentAnalysisAgent()
# enhanced_results = await agent.analyze_with_proactive_collaboration(
#     agent.analyze_content, 
#     content_data, 
#     user_context=user_context
# )
