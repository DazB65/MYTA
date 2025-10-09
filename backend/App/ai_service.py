"""
AI Service for MYTA
Handles AI model integration with OpenAI and Anthropic APIs
"""

import os
import asyncio
import hashlib
from typing import Dict, List, Optional, Any, AsyncGenerator
from datetime import datetime
import json

try:
    import openai
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .redis_service import get_redis_service
from .error_handler import MYTAError, ErrorCode, ErrorCategory, ErrorSeverity
from .enhanced_caching_service import (
    get_cache_service, cache_ai_response, get_cached_ai_response,
    CacheType, cached
)
from .circuit_breaker import get_openai_circuit_breaker, CircuitBreakerError
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class AIProvider:
    """AI provider configuration"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class AIService:
    """Service for handling AI model interactions"""
    
    def __init__(self):
        self.provider = os.getenv("AI_MODEL_PROVIDER", "openai")
        self.model_name = os.getenv("AI_MODEL_NAME", "gpt-3.5-turbo")
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        self.timeout = int(os.getenv("AI_TIMEOUT_SECONDS", "30"))
        
        self.redis_service = get_redis_service()
        
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI service clients"""
        try:
            # Initialize OpenAI client
            if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
                self.openai_client = AsyncOpenAI(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    timeout=self.timeout
                )
                logger.info("OpenAI client initialized successfully")
            
            # Initialize Anthropic client
            if ANTHROPIC_AVAILABLE and os.getenv("ANTHROPIC_API_KEY"):
                self.anthropic_client = AsyncAnthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY"),
                    timeout=self.timeout
                )
                logger.info("Anthropic client initialized successfully")
            
            # Check if at least one client is available
            if not self.openai_client and not self.anthropic_client:
                logger.warning("No AI clients available - running in demo mode")
        
        except Exception as e:
            logger.error(f"Failed to initialize AI clients: {e}")
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.openai_client is not None or self.anthropic_client is not None
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        agent_id: str = "1",
        user_id: str = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate AI response for given messages"""

        if not self.is_available():
            return self._get_fallback_response(messages, agent_id)

        # Check cache first (only for non-streaming requests)
        if not stream and user_id:
            query_text = json.dumps(messages, sort_keys=True)
            cached_response = get_cached_ai_response(user_id, query_text, self.model_name)
            if cached_response:
                logger.info(f"Cache hit for user {user_id}, agent {agent_id}")
                return cached_response

        try:
            # Add rate limiting check
            if user_id and not await self._check_rate_limit(user_id):
                raise MYTAError(
                    message="AI request rate limit exceeded",
                    error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
                    category=ErrorCategory.RATE_LIMIT,
                    severity=ErrorSeverity.MEDIUM
                )
            
            # Get agent personality and enhance messages with user context
            enhanced_messages = await self._enhance_messages_with_agent_personality(messages, agent_id, user_id)
            
            # Generate response based on provider
            if self.provider == AIProvider.OPENAI and self.openai_client:
                response = await self._generate_openai_response(enhanced_messages, stream)
            elif self.provider == AIProvider.ANTHROPIC and self.anthropic_client:
                response = await self._generate_anthropic_response(enhanced_messages, stream)
            else:
                # Fallback to available provider
                if self.openai_client:
                    response = await self._generate_openai_response(enhanced_messages, stream)
                elif self.anthropic_client:
                    response = await self._generate_anthropic_response(enhanced_messages, stream)
                else:
                    return self._get_fallback_response(messages, agent_id)
            
            # Cache the response using enhanced caching service
            if user_id and not stream and response:
                query_text = json.dumps(messages, sort_keys=True)
                cache_ai_response(
                    user_id=user_id,
                    query=query_text,
                    response=response,
                    model=self.model_name,
                    ttl=3600  # Cache for 1 hour
                )
                logger.info(f"Cached AI response for user {user_id}, agent {agent_id}")

            return response
        
        except MYTAError:
            raise
        except Exception as e:
            logger.error(f"AI generation error: {e}")

            # Check if it's a quota/rate limit error - use fallback instead of raising error
            error_str = str(e).lower()
            if any(keyword in error_str for keyword in ["quota", "rate limit", "insufficient", "exceeded"]):
                logger.warning("AI service quota exceeded, using fallback response")
                return self._get_fallback_response(messages, agent_id)

            # For other errors, still use fallback but log as error
            logger.error(f"AI service error, using fallback: {e}")
            return self._get_fallback_response(messages, agent_id)
    
    async def _generate_openai_response(self, messages: List[Dict], stream: bool = False) -> Dict[str, Any]:
        """Generate response using OpenAI API with circuit breaker protection"""
        circuit_breaker = get_openai_circuit_breaker()

        async def _make_openai_call():
            # Try the configured model first, fallback to gpt-3.5-turbo if needed
            model_to_use = self.model_name

            try:
                response = await self.openai_client.chat.completions.create(
                    model=model_to_use,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    stream=stream
                )
            except Exception as e:
                if "model" in str(e).lower() and "not found" in str(e).lower():
                    # Fallback to gpt-3.5-turbo
                    logger.warning(f"Model {model_to_use} not available, falling back to gpt-3.5-turbo")
                    model_to_use = "gpt-3.5-turbo"
                    response = await self.openai_client.chat.completions.create(
                        model=model_to_use,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        stream=stream
                    )
                else:
                    raise
            
            if stream:
                return {"stream": response, "provider": "openai"}
            else:
                return {
                    "content": response.choices[0].message.content,
                    "provider": "openai",
                    "model": model_to_use,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }

        try:
            return await circuit_breaker.call(_make_openai_call)
        except CircuitBreakerError as e:
            logger.error(f"OpenAI circuit breaker open: {e}")
            raise MYTAError(
                message="OpenAI service temporarily unavailable",
                error_code=ErrorCode.EXTERNAL_API_ERROR,
                category=ErrorCategory.EXTERNAL_SERVICE,
                severity=ErrorSeverity.HIGH,
                details={"circuit_breaker": "open", "service": "openai"}
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _generate_anthropic_response(self, messages: List[Dict], stream: bool = False) -> Dict[str, Any]:
        """Generate response using Anthropic API"""
        try:
            # Convert messages to Anthropic format
            anthropic_messages = self._convert_to_anthropic_format(messages)
            
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",  # Default Anthropic model
                messages=anthropic_messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=stream
            )
            
            if stream:
                return {"stream": response, "provider": "anthropic"}
            else:
                return {
                    "content": response.content[0].text,
                    "provider": "anthropic",
                    "model": "claude-3-sonnet-20240229",
                    "usage": {
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
        
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def _convert_to_anthropic_format(self, messages: List[Dict]) -> List[Dict]:
        """Convert OpenAI format messages to Anthropic format"""
        anthropic_messages = []
        
        for message in messages:
            if message["role"] == "system":
                # Anthropic handles system messages differently
                continue
            elif message["role"] in ["user", "assistant"]:
                anthropic_messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        return anthropic_messages
    
    async def _enhance_messages_with_agent_personality(self, messages: List[Dict], agent_id: str, user_id: str = None) -> List[Dict]:
        """Add agent personality and user-specific context to the conversation"""

        if user_id:
            # Use personalized response generator for user-specific prompts
            from .personalized_responses import get_response_generator

            try:
                response_generator = get_response_generator()
                user_message = messages[-1]["content"] if messages else ""

                personalized_prompt = await response_generator.generate_personalized_prompt(
                    user_message=user_message,
                    agent_id=agent_id,
                    user_id=user_id,
                    conversation_context=messages[:-1] if len(messages) > 1 else None
                )

                # Add system message with personalized prompt
                enhanced_messages = [
                    {
                        "role": "system",
                        "content": personalized_prompt
                    }
                ]

                # Add conversation history
                enhanced_messages.extend(messages)

                return enhanced_messages

            except Exception as e:
                logger.error(f"Error generating personalized prompt: {e}")
                # Fallback to basic agent personality

        # Fallback to basic agent personality
        from .agent_personalities import get_agent_personality

        agent_personality = get_agent_personality(agent_id)

        # Add system message with agent personality
        enhanced_messages = [
            {
                "role": "system",
                "content": agent_personality["system_prompt"]
            }
        ]

        # Add conversation history
        enhanced_messages.extend(messages)

        return enhanced_messages
    
    async def _check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limits"""
        if not self.redis_service.is_available():
            return True  # Allow if Redis unavailable
        
        rate_limit = self.redis_service.check_rate_limit(
            identifier=f"ai_requests:{user_id}",
            limit=20,  # 20 requests per hour
            window_seconds=3600
        )
        
        return rate_limit["allowed"]
    
    async def _cache_response(self, user_id: str, agent_id: str, messages: List[Dict], response: Dict):
        """Cache AI response for analytics"""
        try:
            if not self.redis_service.is_available():
                return
            
            cache_data = {
                "user_id": user_id,
                "agent_id": agent_id,
                "messages_count": len(messages),
                "response": response,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            cache_key = f"ai_response:{user_id}:{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            self.redis_service.set(cache_key, cache_data, 86400)  # 24 hours
        
        except Exception as e:
            logger.error(f"Failed to cache AI response: {e}")
    
    def _get_fallback_response(self, messages: List[Dict], agent_id: str) -> Dict[str, Any]:
        """Generate fallback response when AI service unavailable"""
        from .agent_personalities import get_agent_personality
        
        agent_personality = get_agent_personality(agent_id)
        
        fallback_responses = [
            f"Hi! I'm {agent_personality['name']}, your {agent_personality['role']}. I'm currently in demo mode, but I'm here to help with {agent_personality['expertise']}!",
            f"As your {agent_personality['role']}, I'd love to help you with that! This is a demo response - the full AI integration will provide detailed, personalized advice.",
            f"Great question! I specialize in {agent_personality['expertise']} and would normally provide detailed insights here. This is a placeholder response for demo purposes.",
            f"I'm {agent_personality['name']}, and I'm excited to help you succeed! This demo response shows how I'll provide {agent_personality['expertise']} guidance once fully integrated."
        ]
        
        import random
        response_content = random.choice(fallback_responses)
        
        return {
            "content": response_content,
            "provider": "fallback",
            "model": "demo",
            "usage": {"total_tokens": 0},
            "timestamp": datetime.utcnow().isoformat(),
            "is_demo": True
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get AI service status"""
        return {
            "available": self.is_available(),
            "provider": self.provider,
            "model": self.model_name,
            "clients": {
                "openai": self.openai_client is not None,
                "anthropic": self.anthropic_client is not None
            },
            "configuration": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "timeout": self.timeout
            }
        }

# Global AI service instance
_ai_service: Optional[AIService] = None

def get_ai_service() -> AIService:
    """Get or create global AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
