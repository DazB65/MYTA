"""
Multi-Model API Integration for CreatorMate Agent System
Handles OpenAI, Anthropic Claude, and Google Gemini integrations with fallback logic
"""

import os
import asyncio
import logging
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import openai
from openai import OpenAI
import time

from config import get_settings
from constants import DEFAULT_TEMPERATURE, MAX_TOKENS_PER_REQUEST

def get_api_key(provider: str) -> str:
    """Get API key for specific provider"""
    settings = get_settings()
    if provider == "openai":
        return settings.openai_api_key
    elif provider == "anthropic":
        return settings.anthropic_api_key  
    elif provider == "google":
        return settings.google_api_key
    return None

# Configure logging
logger = logging.getLogger(__name__)

# Try importing optional dependencies
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not installed. Claude models will be unavailable.")

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google Generative AI library not installed. Gemini models will be unavailable.")

class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"

class ModelType(Enum):
    # OpenAI Models
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    
    # Anthropic Models
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_HAIKU = "claude-3-5-haiku-20241022"
    
    # Google Models
    GEMINI_PRO = "gemini-2.0-flash-exp"
    GEMINI_FLASH = "gemini-1.5-flash"

@dataclass
class ModelConfig:
    """Configuration for a specific model"""
    provider: ModelProvider
    model_name: str
    max_tokens: int
    temperature: float = 0.2
    fallback_model: Optional['ModelConfig'] = None

@dataclass
class ModelResponse:
    """Standardized response from any model"""
    content: str
    provider: ModelProvider
    model: str
    tokens_used: int
    processing_time: float
    success: bool
    error_message: Optional[str] = None

class ModelIntegration:
    """Unified interface for all AI model providers"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.google_client = None
        
        # Initialize available clients
        self._init_openai()
        self._init_anthropic()
        self._init_google()
        
        # Define model configurations with fallbacks
        self.model_configs = {
            # Boss Agent - Primary: Claude Sonnet, Fallback: GPT-4o
            "boss_agent": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=ModelType.CLAUDE_SONNET.value,
                max_tokens=2000,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.OPENAI,
                    model_name=ModelType.GPT_4O.value,
                    max_tokens=2000,
                    temperature=0.3
                )
            ),
            
            # Content Analysis - Primary: Gemini, Fallback: Claude Sonnet
            "content_analysis": ModelConfig(
                provider=ModelProvider.GOOGLE,
                model_name=ModelType.GEMINI_PRO.value,
                max_tokens=4000,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.ANTHROPIC,
                    model_name=ModelType.CLAUDE_SONNET.value,
                    max_tokens=4000,
                    temperature=0.2
                )
            ),
            
            # Audience Insights - Primary: Claude Sonnet, Fallback: Claude Haiku
            "audience_insights": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=ModelType.CLAUDE_SONNET.value,
                max_tokens=3000,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.ANTHROPIC,
                    model_name=ModelType.CLAUDE_HAIKU.value,
                    max_tokens=2000,
                    temperature=0.2
                )
            ),
            
            # SEO & Discoverability - Claude Haiku (cost-effective)
            "seo_discoverability": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=ModelType.CLAUDE_HAIKU.value,
                max_tokens=2000,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.OPENAI,
                    model_name=ModelType.GPT_4O_MINI.value,
                    max_tokens=2000,
                    temperature=0.1
                )
            ),
            
            # Competitive Analysis - Primary: Gemini, Fallback: Claude Sonnet
            "competitive_analysis": ModelConfig(
                provider=ModelProvider.GOOGLE,
                model_name=ModelType.GEMINI_PRO.value,
                max_tokens=5000,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.ANTHROPIC,
                    model_name=ModelType.CLAUDE_SONNET.value,
                    max_tokens=4000,
                    temperature=0.2
                )
            ),
            
            # Monetization Strategy - Primary: Claude Haiku, Fallback: Claude Sonnet
            "monetization_strategy": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=ModelType.CLAUDE_HAIKU.value,
                max_tokens=2500,
                temperature=DEFAULT_TEMPERATURE,
                fallback_model=ModelConfig(
                    provider=ModelProvider.ANTHROPIC,
                    model_name=ModelType.CLAUDE_SONNET.value,
                    max_tokens=3000,
                    temperature=0.2
                )
            )
        }
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        api_key = get_api_key("openai")
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("OpenAI API key not available")
    
    def _init_anthropic(self):
        """Initialize Anthropic Claude client"""
        if not ANTHROPIC_AVAILABLE:
            logger.warning("Anthropic library not available")
            return
            
        api_key = get_api_key("anthropic")
        if api_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=api_key)
                logger.info("Anthropic client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
        else:
            logger.warning("Anthropic API key not available")
    
    def _init_google(self):
        """Initialize Google Gemini client"""
        if not GOOGLE_AVAILABLE:
            logger.warning("Google Generative AI library not available")
            return
            
        api_key = get_api_key("google")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.google_client = genai
                logger.info("Google Gemini client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google client: {e}")
        else:
            logger.warning("Google API key not available")
    
    async def generate_response(
        self, 
        agent_type: str, 
        messages: List[Dict[str, str]], 
        analysis_depth: str = "standard"
    ) -> ModelResponse:
        """
        Generate response using appropriate model for agent type with fallback
        
        Args:
            agent_type: Type of agent requesting the response
            messages: List of messages in OpenAI format
            analysis_depth: Analysis depth (quick/standard/deep)
            
        Returns:
            ModelResponse with generated content
        """
        
        start_time = time.time()
        
        # Get model configuration for agent type
        config = self.model_configs.get(agent_type)
        if not config:
            logger.error(f"No model configuration found for agent type: {agent_type}")
            return ModelResponse(
                content="Model configuration error",
                provider=ModelProvider.OPENAI,
                model="unknown",
                tokens_used=0,
                processing_time=0,
                success=False,
                error_message=f"No configuration for agent type: {agent_type}"
            )
        
        # Adjust token limits based on analysis depth
        max_tokens = self._adjust_tokens_for_depth(config.max_tokens, analysis_depth)
        
        # Try primary model first
        response = await self._try_model(config, messages, max_tokens)
        
        # If primary model fails, try fallback
        if not response.success and config.fallback_model:
            logger.warning(f"Primary model failed for {agent_type}, trying fallback")
            fallback_max_tokens = self._adjust_tokens_for_depth(
                config.fallback_model.max_tokens, 
                analysis_depth
            )
            response = await self._try_model(config.fallback_model, messages, fallback_max_tokens)
        
        response.processing_time = time.time() - start_time
        return response
    
    def _adjust_tokens_for_depth(self, base_tokens: int, depth: str) -> int:
        """Adjust token limits based on analysis depth"""
        multipliers = {
            "quick": 0.6,
            "standard": 1.0,
            "deep": 1.5
        }
        return int(base_tokens * multipliers.get(depth, 1.0))
    
    async def _try_model(
        self, 
        config: ModelConfig, 
        messages: List[Dict[str, str]], 
        max_tokens: int
    ) -> ModelResponse:
        """Try to generate response with specific model configuration"""
        
        try:
            if config.provider == ModelProvider.OPENAI:
                return await self._openai_generate(config, messages, max_tokens)
            elif config.provider == ModelProvider.ANTHROPIC:
                return await self._anthropic_generate(config, messages, max_tokens)
            elif config.provider == ModelProvider.GOOGLE:
                return await self._google_generate(config, messages, max_tokens)
            else:
                return ModelResponse(
                    content="Unsupported provider",
                    provider=config.provider,
                    model=config.model_name,
                    tokens_used=0,
                    processing_time=0,
                    success=False,
                    error_message=f"Unsupported provider: {config.provider}"
                )
        except Exception as e:
            logger.error(f"Error with {config.provider.value} model {config.model_name}: {e}")
            return ModelResponse(
                content="",
                provider=config.provider,
                model=config.model_name,
                tokens_used=0,
                processing_time=0,
                success=False,
                error_message=str(e)
            )
    
    async def _openai_generate(
        self, 
        config: ModelConfig, 
        messages: List[Dict[str, str]], 
        max_tokens: int
    ) -> ModelResponse:
        """Generate response using OpenAI"""
        
        if not self.openai_client:
            raise Exception("OpenAI client not initialized")
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.openai_client.chat.completions.create(
                    model=config.model_name,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=config.temperature
                )
            )
            
            return ModelResponse(
                content=response.choices[0].message.content,
                provider=ModelProvider.OPENAI,
                model=config.model_name,
                tokens_used=response.usage.total_tokens,
                processing_time=0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")
    
    async def _anthropic_generate(
        self, 
        config: ModelConfig, 
        messages: List[Dict[str, str]], 
        max_tokens: int
    ) -> ModelResponse:
        """Generate response using Anthropic Claude"""
        
        if not self.anthropic_client:
            raise Exception("Anthropic client not initialized")
        
        try:
            # Convert OpenAI format to Anthropic format
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.anthropic_client.messages.create(
                    model=config.model_name,
                    max_tokens=max_tokens,
                    temperature=config.temperature,
                    system=system_message,
                    messages=user_messages
                )
            )
            
            return ModelResponse(
                content=response.content[0].text,
                provider=ModelProvider.ANTHROPIC,
                model=config.model_name,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                processing_time=0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {e}")
    
    async def _google_generate(
        self, 
        config: ModelConfig, 
        messages: List[Dict[str, str]], 
        max_tokens: int
    ) -> ModelResponse:
        """Generate response using Google Gemini"""
        
        if not self.google_client:
            raise Exception("Google client not initialized")
        
        try:
            # Convert OpenAI format to Gemini format
            prompt_parts = []
            for msg in messages:
                if msg["role"] == "system":
                    prompt_parts.append(f"System: {msg['content']}")
                elif msg["role"] == "user":
                    prompt_parts.append(f"User: {msg['content']}")
                elif msg["role"] == "assistant":
                    prompt_parts.append(f"Assistant: {msg['content']}")
            
            prompt = "\n\n".join(prompt_parts)
            
            model = self.google_client.GenerativeModel(config.model_name)
            
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": config.temperature,
            }
            
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            )
            
            return ModelResponse(
                content=response.text,
                provider=ModelProvider.GOOGLE,
                model=config.model_name,
                tokens_used=response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
                processing_time=0,
                success=True
            )
            
        except Exception as e:
            raise Exception(f"Google API error: {e}")
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models by provider"""
        available = {}
        
        if self.openai_client:
            available["openai"] = [ModelType.GPT_4O.value, ModelType.GPT_4O_MINI.value]
        
        if self.anthropic_client:
            available["anthropic"] = [ModelType.CLAUDE_SONNET.value, ModelType.CLAUDE_HAIKU.value]
        
        if self.google_client:
            available["google"] = [ModelType.GEMINI_PRO.value, ModelType.GEMINI_FLASH.value]
        
        return available
    
    def get_model_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all model integrations"""
        return {
            "openai": {
                "available": self.openai_client is not None,
                "models": [ModelType.GPT_4O.value, ModelType.GPT_4O_MINI.value] if self.openai_client else []
            },
            "anthropic": {
                "available": self.anthropic_client is not None,
                "models": [ModelType.CLAUDE_SONNET.value, ModelType.CLAUDE_HAIKU.value] if self.anthropic_client else []
            },
            "google": {
                "available": self.google_client is not None,
                "models": [ModelType.GEMINI_PRO.value, ModelType.GEMINI_FLASH.value] if self.google_client else []
            }
        }

# Global model integration instance
_model_integration = None

def get_model_integration() -> ModelIntegration:
    """Get or create global model integration instance"""
    global _model_integration
    if _model_integration is None:
        _model_integration = ModelIntegration()
    return _model_integration

async def generate_agent_response(
    agent_type: str, 
    prompt: str, 
    analysis_depth: str = "standard",
    context: Optional[Dict[str, Any]] = None
) -> ModelResponse:
    """
    Convenience function to generate response for specific agent type
    
    Args:
        agent_type: Type of agent (boss_agent, content_analysis, etc.)
        prompt: The prompt to send to the model
        analysis_depth: Analysis depth level
        context: Additional context for the prompt
        
    Returns:
        ModelResponse with generated content
    """
    
    integration = get_model_integration()
    
    # Create messages in OpenAI format
    messages = [
        {"role": "system", "content": "You are a specialized AI assistant for YouTube content creators."},
        {"role": "user", "content": prompt}
    ]
    
    # Add context if provided
    if context:
        context_str = f"Context: {context}"
        messages.insert(1, {"role": "system", "content": context_str})
    
    return await integration.generate_response(agent_type, messages, analysis_depth)

async def create_agent_call_to_integration(
    agent_type: str, 
    use_case: str, 
    prompt_data: dict
) -> dict:
    """
    Simple developer API for centralized AI model integration
    
    Args:
        agent_type: Type of agent (boss_agent, content_analysis, etc.)
        use_case: Specific use case (content_analysis, audience_insights, seo_optimization, etc.)
        prompt_data: Dictionary containing prompt, context, analysis_depth, etc.
        
    Returns:
        Dict with response, model info, tokens used, and success status
    """
    try:
        integration = get_model_integration()
        
        # Extract prompt data
        prompt = prompt_data.get('prompt', '')
        context = prompt_data.get('context', {})
        analysis_depth = prompt_data.get('analysis_depth', 'standard')
        system_message = prompt_data.get('system_message', 'You are a specialized AI assistant for YouTube content creators.')
        
        # Create messages in OpenAI format
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        # Add context if provided
        if context:
            context_str = f"Context: {context}"
            messages.insert(1, {"role": "system", "content": context_str})
        
        # Generate response using centralized integration
        response = await integration.generate_response(agent_type, messages, analysis_depth)
        
        # Return standardized response format
        return {
            "success": response.success,
            "content": response.content,
            "provider": response.provider.value,
            "model": response.model,
            "tokens_used": response.tokens_used,
            "processing_time": response.processing_time,
            "error_message": response.error_message,
            "agent_type": agent_type,
            "use_case": use_case
        }
        
    except Exception as e:
        logger.error(f"Error in create_agent_call_to_integration: {e}")
        return {
            "success": False,
            "content": "",
            "provider": "unknown",
            "model": "unknown",
            "tokens_used": 0,
            "processing_time": 0,
            "error_message": str(e),
            "agent_type": agent_type,
            "use_case": use_case
        }

def get_integration_status() -> Dict[str, Any]:
    """
    Get comprehensive status of all model integrations
    Required by agent_router.py
    
    Returns:
        Dict with detailed status of all providers and models
    """
    try:
        integration = get_model_integration()
        model_status = integration.get_model_status()
        
        # Count total available models
        total_models = sum(len(provider["models"]) for provider in model_status.values())
        available_providers = sum(1 for provider in model_status.values() if provider["available"])
        
        return {
            "status": "healthy" if available_providers > 0 else "degraded",
            "available_providers": available_providers,
            "total_providers": len(model_status),
            "total_models": total_models,
            "providers": model_status,
            "agent_configurations": {
                agent_type: {
                    "primary_model": f"{config.provider.value}:{config.model_name}",
                    "fallback_model": f"{config.fallback_model.provider.value}:{config.fallback_model.model_name}" if config.fallback_model else None,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature
                }
                for agent_type, config in integration.model_configs.items()
            },
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        return {
            "status": "error",
            "available_providers": 0,
            "total_providers": 0,
            "total_models": 0,
            "providers": {},
            "agent_configurations": {},
            "error_message": str(e),
            "timestamp": time.time()
        }