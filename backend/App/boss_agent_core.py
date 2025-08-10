"""
Core Boss Agent System for Vidalytics
Main orchestration logic for the hierarchical multi-agent system
"""

import asyncio
import uuid
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from backend.App.agent_models import QueryType, Priority, Context, TokenBudget, AgentRequest, AgentResponse
from backend.App.intent_classifier import get_intent_classifier
from backend.App.voice_analyzer import get_voice_analyzer
from backend.App.agent_coordinators import get_agent_coordinators
from backend import get_agent_cache
from backend.App.data_access_monitor import get_data_access_monitor
from backend.App.enhanced_user_context import get_enhanced_context_manager
from backend.App.realtime_data_pipeline import get_data_pipeline
from backend.model_integrations import create_agent_call_to_integration
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class BossAgent:
    """Main orchestration agent that coordinates specialized agents"""
    
    # Standardized voice and personality across all agents
    AGENT_VOICE_PROFILE = {
        "tone": "Expert yet approachable YouTube strategist",
        "personality": "Data-driven, actionable, encouraging",
        "communication_style": "Direct answers first, then context",
        "expertise_level": "Professional consultant with deep YouTube knowledge",
        "response_format": "Specific numbers + context + actionable next step"
    }
    
    def __init__(self, openai_api_key: str):
        # Store API key for backward compatibility but use centralized integration
        self.openai_api_key = openai_api_key
        self.intent_classifier = get_intent_classifier()
        self.voice_analyzer = get_voice_analyzer()
        
        # Initialize specialized agents
        self.agents = get_agent_coordinators()
        
        self.cache = get_agent_cache()
        self.monitor = get_data_access_monitor()
    
    def _get_voice_guidelines(self) -> str:
        """Get standardized voice guidelines for all agent prompts"""
        return f"""
        VOICE & PERSONALITY GUIDELINES:
        • Tone: {self.AGENT_VOICE_PROFILE['tone']}
        • Personality: {self.AGENT_VOICE_PROFILE['personality']}
        • Style: {self.AGENT_VOICE_PROFILE['communication_style']}
        • Expertise: {self.AGENT_VOICE_PROFILE['expertise_level']}
        • Format: {self.AGENT_VOICE_PROFILE['response_format']}
        
        RESPONSE STANDARDS:
        ✓ Start with specific numbers/data answering their exact question
        ✓ Provide context relative to YouTube benchmarks
        ✓ Include one actionable next step
        ✓ Use encouraging, professional tone
        ✓ Keep response focused and under 200 words unless complex analysis requested
        """
    
    async def generate_voice_matched_content(self, content_type: str, topic: str, user_context: Dict) -> Dict[str, Any]:
        """Generate content that matches the user's channel voice"""
        try:
            # Get channel content for voice analysis
            channel_content = await self._get_channel_content(user_context)
            
            # Analyze channel voice
            voice_profile = await self.voice_analyzer.analyze_channel_voice(
                channel_content,
                user_context.get('channel_info', {})
            )
            
            # Generate matched content
            generated_content = await self.voice_analyzer.generate_voice_matched_content(
                content_type,
                topic,
                voice_profile
            )
            
            return {
                'success': True,
                'content': generated_content.get('content'),
                'style_match_score': generated_content.get('style_match_score'),
                'voice_profile': voice_profile
            }
            
        except Exception as e:
            logger.error(f"Voice-matched content generation failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _get_channel_content(self, user_context: Dict) -> List[Dict]:
        """Get channel content for voice analysis"""
        try:
            channel_id = user_context.get('channel_info', {}).get('channel_id')
            if not channel_id:
                return []
            
            # Import YouTube integration
            from backend.youtube_api_integration import get_youtube_integration
            youtube_service = get_youtube_integration()
            
            # Get recent videos with transcripts
            videos = await youtube_service.get_recent_videos(
                channel_id=channel_id,
                count=10,  # Analyze last 10 videos
                include_transcripts=True
            )
            
            return [{
                'title': video.title,
                'description': video.description,
                'transcript': video.transcript if hasattr(video, 'transcript') else None
            } for video in videos]
            
        except Exception as e:
            logger.error(f"Error getting channel content: {e}")
            return []
    
    async def process_user_query(self, message: str, user_context: Dict) -> Dict[str, Any]:
        """
        Main entry point for processing user queries
        
        Args:
            message: User's message
            user_context: User channel context and data
            
        Returns:
            Synthesized response from appropriate agents
        """
        
        try:
            # Monitor query start
            user_id = user_context.get('user_id', 'unknown')
            await self.monitor.log_event(user_id, 'query_processing', 'boss_agent', 'start', 
                                        {'message_preview': message[:50]})
            
            # Get enhanced real-time context
            if user_id:
                # Register user activity for data pipeline
                await get_data_pipeline().register_user_activity(user_id, "chat")
                
                # Get enhanced context with real-time data
                try:
                    enhanced_context = await get_enhanced_context_manager().get_enhanced_context(user_id)
                    channel_info = enhanced_context.get("channel_info", {})
                    
                    logger.info(f"📈 Enhanced context for {user_id}: {len(channel_info)} channel data points")
                    
                except Exception as e:
                    logger.warning(f"Failed to get enhanced context for {user_id}: {e}")
                    enhanced_context = user_context
                    channel_info = user_context.get("channel_info", {})
            else:
                enhanced_context = user_context
                channel_info = user_context.get("channel_info", {})
            
            # Handle direct answer patterns first
            direct_response = await self._handle_direct_queries(message, channel_info)
            if direct_response:
                return direct_response
            
            # Step 1: Parse message and classify intent
            intent, parameters = await self.intent_classifier.classify_intent(message, user_context)
            
            logger.info(f"Classified intent: {intent.value} with parameters: {parameters}")
            
            # Step 2: Check cache for existing response
            cached_response = self.cache.get(message, user_context, intent.value)
            if cached_response:
                logger.info(f"Returning cached response for intent: {intent.value}")
                return cached_response
            
            # Step 3: Determine which agents to activate
            active_agents = self._determine_agents(intent, parameters)
            
            # Step 4: Create agent requests with enhanced context
            requests = self._create_agent_requests(intent, parameters, enhanced_context)
            
            # Step 5: Execute agents (parallel where possible)
            agent_responses = await self._execute_agents(active_agents, requests)
            
            # Step 6: Synthesize final response with enhanced context
            final_response = await self._synthesize_response(intent, agent_responses, enhanced_context, message)
            
            # Step 7: Cache the response
            if final_response.get("success", False):
                self.cache.set(message, user_context, final_response, intent.value)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Boss agent processing failed: {e}")
            return {
                "success": False,
                "response": "I encountered an error processing your request. Please try again.",
                "error": str(e)
            }
    
    async def _handle_direct_queries(self, message: str, channel_info: Dict) -> Optional[Dict[str, Any]]:
        """Handle common direct queries with immediate responses"""
        message_lower = message.lower()
        
        # Total views query
        if "total views" in message_lower or "total view" in message_lower:
            total_views = channel_info.get('total_view_count', 0)
            if total_views > 0:
                return {
                    "success": True,
                    "response": f"Your channel has {total_views:,} total views.",
                    "intent": "content_analysis",
                    "agents_used": ["direct_answer"],
                    "processing_time": 0.1,
                    "confidence": 1.0
                }
        
        # Subscriber count query
        elif "how many subscribers" in message_lower or "subscriber count" in message_lower:
            subscribers = channel_info.get('subscriber_count', 0)
            return {
                "success": True,
                "response": f"You have {subscribers:,} subscribers.",
                "intent": "audience",
                "agents_used": ["direct_answer"],
                "processing_time": 0.1,
                "confidence": 1.0
            }
        
        return None
    
    def _determine_agents(self, intent: QueryType, parameters: Dict) -> List[QueryType]:
        """Determine which agents should be activated based on intent"""
        
        # Primary agent based on intent
        active_agents = [intent] if intent != QueryType.GENERAL else []
        
        # Enhanced multi-agent coordination based on query complexity
        if parameters.get("competitors"):
            if QueryType.COMPETITIVE_ANALYSIS not in active_agents:
                active_agents.append(QueryType.COMPETITIVE_ANALYSIS)
        
        # For comprehensive analysis questions, activate multiple agents
        if intent == QueryType.GENERAL or len(active_agents) == 0:
            # Default to content analysis for general questions
            active_agents = [QueryType.CONTENT_ANALYSIS, QueryType.AUDIENCE_INSIGHTS]
        
        # Remove duplicates and ensure we have at least one agent
        active_agents = list(set(active_agents))
        if not active_agents:
            active_agents = [QueryType.CONTENT_ANALYSIS]  # Default fallback
        
        return active_agents
    
    def _create_agent_requests(self, intent: QueryType, parameters: Dict, user_context: Dict) -> List[AgentRequest]:
        """Create agent requests with proper context"""
        
        # Extract time period
        time_period = parameters.get("time_period", "last_30d")
        
        # Create context - properly access nested channel_info
        channel_info = user_context.get("channel_info", {})
        # Use channel_id if available, fallback to name
        channel_identifier = channel_info.get("channel_id") or channel_info.get("name", "unknown")
        context = Context(
            channel_id=channel_identifier,
            time_period=time_period,
            specific_videos=parameters.get("specific_videos", []),
            competitors=parameters.get("competitors", [])
        )
        
        # Create request with full user context
        request = AgentRequest(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            query_type=intent,
            priority=Priority.MEDIUM,
            context=context,
            token_budget=TokenBudget(input_tokens=3000, output_tokens=1500),
            user_context=user_context  # Store full user context for specialized agents
        )
        
        return [request]
    
    async def _execute_agents(self, active_agents: List[QueryType], requests: List[AgentRequest]) -> List[AgentResponse]:
        """Execute the specified agents with their requests"""
        
        tasks = []
        for agent_type in active_agents:
            if agent_type in self.agents:
                agent = self.agents[agent_type]
                # Use the first request for now (could be enhanced for multiple requests)
                task = agent.process_request(requests[0])
                tasks.append(task)
        
        # Execute agents in parallel with enhanced error handling
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Enhanced error handling and response validation
        valid_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, AgentResponse) and response.success:
                valid_responses.append(response)
            elif isinstance(response, Exception):
                logger.error(f"Agent {active_agents[i].value if i < len(active_agents) else 'unknown'} failed: {response}")
        
        return valid_responses
    
    async def _synthesize_response(self, intent: QueryType, agent_responses: List[AgentResponse], user_context: Dict, message: str) -> Dict[str, Any]:
        """Synthesize final response from agent outputs"""
        
        if not agent_responses:
            return {
                "success": False,
                "response": "I couldn't gather the analytics data you requested. Please try again or be more specific about what you'd like to know.",
                "intent": intent.value
            }
        
        # Collect insights from all agents
        all_insights = []
        all_recommendations = []
        
        for response in agent_responses:
            data = response.data
            if "insights" in data:
                all_insights.append(f"**{response.agent_id.replace('_', ' ').title()}:**\n{data['insights']}")
            
            if "recommendations" in data:
                all_recommendations.extend(data.get("recommendations", []))
        
        # Create synthesis prompt
        channel_info = user_context.get("channel_info", {})
        
        synthesis_prompt = f"""
        You are Vidalytics's AI assistant. Provide an expert, data-driven response to this YouTube creator's question.
        
        {self._get_voice_guidelines()}
        
        CREATOR'S QUESTION: "{message}"
        DETECTED INTENT: {intent.value.replace('_', ' ').title()}
        CHANNEL: {channel_info.get('name', 'Creator')}
        
        AI AGENT ANALYSIS:
        {chr(10).join(all_insights)}
        
        RESPONSE GUIDELINES:
        1. **DIRECT ANSWER FIRST**: Start with exact numbers answering their specific question
        2. **DATA-DRIVEN**: Use only the real metrics provided above - no generic estimates
        3. **CONTEXT-AWARE**: Reference their channel's specific performance levels
        4. **ACTIONABLE**: Include 1-2 specific next steps if relevant to their question
        5. **PROFESSIONAL TONE**: Expert but approachable, like a seasoned YouTube strategist
        """
        
        try:
            # Use centralized model integration
            result = await create_agent_call_to_integration(
                agent_type="boss_agent",
                use_case="response_synthesis",
                prompt_data={
                    "prompt": synthesis_prompt,
                    "analysis_depth": "standard",
                    "system_message": "You are the main Vidalytics AI orchestrating agent responses."
                }
            )
            
            synthesized_response = result["content"] if result["success"] else "Unable to synthesize response"
            
        except Exception as e:
            logger.error(f"Response synthesis failed: {e}")
            # Fallback to simple concatenation
            synthesized_response = f"Based on your {intent.value.replace('_', ' ')} request, here's what I found:\n\n" + "\n\n".join(all_insights)
        
        return {
            "success": True,
            "response": synthesized_response,
            "intent": intent.value,
            "agents_used": [r.agent_id for r in agent_responses],
            "recommendations": all_recommendations[:5],  # Top 5 recommendations
            "processing_time": sum(r.processing_time for r in agent_responses),
            "confidence": sum(r.confidence for r in agent_responses) / len(agent_responses)
        }

# Initialize boss agent instance
boss_agent = None

def get_boss_agent():
    """Get or create boss agent instance"""
    global boss_agent
    if boss_agent is None:
        # Load from .env file first for security
        from dotenv import dotenv_values
        env_vars = dotenv_values()
        api_key = env_vars.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        boss_agent = BossAgent(api_key)
    return boss_agent

async def process_user_message(message: str, user_context: Dict) -> Dict[str, Any]:
    """
    Main function to process user messages through the boss agent system
    
    Args:
        message: User's message
        user_context: User channel context
        
    Returns:
        Processed response from boss agent orchestration
    """
    agent = get_boss_agent()
    return await agent.process_user_query(message, user_context)