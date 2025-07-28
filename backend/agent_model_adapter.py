"""
Agent Model Adapter
Bridges individual agents with the centralized model_integrations system
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from model_integrations import get_model_integration, ModelResponse
from connection_pool import get_openai_client

logger = logging.getLogger(__name__)

class AgentModelAdapter:
    """
    Adapter to help migrate agents from direct model calls to model_integrations
    """
    
    def __init__(self):
        self.model_integration = get_model_integration()
    
    async def generate_response(
        self,
        agent_type: str,
        messages: List[Dict[str, str]],
        analysis_depth: str = "standard",
        context: Optional[Dict[str, Any]] = None
    ) -> ModelResponse:
        """
        Generate response using the centralized model integration system
        
        Args:
            agent_type: Type of agent (boss_agent, content_analysis, etc.)
            messages: Messages in OpenAI format
            analysis_depth: Analysis depth (quick/standard/deep)
            context: Additional context
            
        Returns:
            ModelResponse with generated content
        """
        try:
            # Add context to messages if provided
            if context:
                context_message = {
                    "role": "system", 
                    "content": f"Additional context: {context}"
                }
                messages = [context_message] + messages
            
            return await self.model_integration.generate_response(
                agent_type, messages, analysis_depth
            )
            
        except Exception as e:
            logger.error(f"Error generating response for {agent_type}: {e}")
            # Return error response
            return ModelResponse(
                content=f"Error generating response: {str(e)}",
                provider="unknown",
                model="unknown", 
                tokens_used=0,
                processing_time=0,
                success=False,
                error_message=str(e)
            )
    
    async def generate_simple_response(
        self,
        agent_type: str,
        prompt: str,
        system_message: str = "You are a specialized AI assistant for YouTube content creators.",
        analysis_depth: str = "standard"
    ) -> str:
        """
        Simplified interface for single prompt -> response
        
        Args:
            agent_type: Type of agent
            prompt: The user prompt
            system_message: System prompt
            analysis_depth: Analysis depth
            
        Returns:
            Generated response text
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.generate_response(agent_type, messages, analysis_depth)
        
        if response.success:
            return response.content
        else:
            logger.error(f"Failed to generate response: {response.error_message}")
            return f"Error: {response.error_message}"
    
    def get_available_models_for_agent(self, agent_type: str) -> Dict[str, Any]:
        """Get available models for a specific agent type"""
        try:
            config = self.model_integration.model_configs.get(agent_type)
            if not config:
                return {"error": f"No configuration found for agent type: {agent_type}"}
            
            return {
                "primary_model": {
                    "provider": config.provider.value,
                    "model": config.model_name,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature
                },
                "fallback_model": {
                    "provider": config.fallback_model.provider.value if config.fallback_model else None,
                    "model": config.fallback_model.model_name if config.fallback_model else None,
                    "max_tokens": config.fallback_model.max_tokens if config.fallback_model else None,
                    "temperature": config.fallback_model.temperature if config.fallback_model else None
                } if config.fallback_model else None
            }
        except Exception as e:
            logger.error(f"Error getting models for {agent_type}: {e}")
            return {"error": str(e)}

# Global instance
_agent_model_adapter = None

def get_agent_model_adapter() -> AgentModelAdapter:
    """Get global agent model adapter instance"""
    global _agent_model_adapter
    if _agent_model_adapter is None:
        _agent_model_adapter = AgentModelAdapter()
    return _agent_model_adapter

async def migrate_openai_call_to_integration(
    agent_type: str,
    openai_messages: List[Dict[str, str]],
    analysis_depth: str = "standard"
) -> str:
    """
    Helper function to migrate existing OpenAI calls to use model_integrations
    
    Args:
        agent_type: Agent type for model selection
        openai_messages: Messages in OpenAI format
        analysis_depth: Analysis depth
        
    Returns:
        Response content string
    """
    adapter = get_agent_model_adapter()
    response = await adapter.generate_response(agent_type, openai_messages, analysis_depth)
    
    if response.success:
        logger.info(f"Successfully generated response using {response.provider.value} {response.model}")
        return response.content
    else:
        logger.error(f"Failed to generate response: {response.error_message}")
        # Fallback to original OpenAI client if available
        try:
            client = get_openai_client()
            if client:
                logger.info("Falling back to direct OpenAI client")
                fallback_response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.chat.completions.create(
                        model="gpt-4o",
                        messages=openai_messages,
                        max_tokens=2000,
                        temperature=0.3
                    )
                )
                return fallback_response.choices[0].message.content
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
        
        return f"Error: Unable to generate response - {response.error_message}"