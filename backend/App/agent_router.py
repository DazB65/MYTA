"""
Agent Router for Vidalytics
Contains all agent-related API endpoints extracted from main.py
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import traceback
from typing import Dict

# Import models
from .api_models import (
    ChatMessage, QuickActionRequest, AgentTaskRequest, AgentCallbackRequest,
    ModelStatusResponse, StandardResponse, ChatResponse,
    ChannelInfo, create_error_response, create_success_response
)

# Import services
from .ai_services import get_ai_response, extract_channel_info, update_user_context, get_user_context
# Import from parent directory for production deployment
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from boss_agent import process_user_message
from backups import get_agent_cache
from model_integrations import get_model_integration
from boss_agent_auth import validate_specialized_agent_request

# Import agent adapters
from agent_adapters import (
    process_content_analysis_request,
    process_audience_insights_request,
    process_seo_request,
    process_competitive_analysis_request,
    process_monetization_strategy_request
)

# Configure advanced logging
from logging_config import get_logger, LogCategory
logger = get_logger(__name__, LogCategory.AGENT)

# Create router
router = APIRouter(prefix="/api/agent", tags=["agent"])

# Import rate limiter from main app
from rate_limiter import limiter, get_rate_limit

# Security
security = HTTPBearer(auto_error=False)

# =============================================================================
# Authentication Functions
# =============================================================================

async def verify_agent_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify JWT token for internal agent communication"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        auth_result = validate_specialized_agent_request({"boss_agent_token": credentials.credentials})
        if not auth_result.is_valid:
            raise HTTPException(status_code=401, detail=auth_result.error_message)
        return auth_result
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

# =============================================================================
# Core Agent Endpoints
# =============================================================================

@router.post("/chat", response_model=ChatResponse)
@limiter.limit(get_rate_limit("public", "chat"))
async def chat(request: Request, message: ChatMessage):
    """Endpoint to handle chat messages from the user"""
    try:
        # Validate input
        if not message.message or not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(message.message) > 2000:
            raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")
        
        logger.info(
            "Processing chat message",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': message.user_id,
                'metadata': {
                    'action': 'chat_message',
                    'message_length': len(message.message),
                    'has_context': bool(message.context)
                }
            }
        )
        
        # Extract any channel info from the message
        extract_channel_info(message.user_id, message.message)
        
        # Get user context for boss agent
        user_context = get_user_context(message.user_id)
        
        # Process through boss agent orchestration system
        logger.info(
            "Processing message through boss agent",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': message.user_id,
                'metadata': {
                    'agent_type': 'boss_agent',
                    'message_preview': message.message[:50] + '...' if len(message.message) > 50 else message.message
                }
            }
        )
        boss_response = await process_user_message(message.message, user_context)
        
        logger.info(
            "Boss agent response received",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': message.user_id,
                'metadata': {
                    'agent_type': 'boss_agent',
                    'success': boss_response.get('success', False),
                    'agents_used': boss_response.get('agents_used', [])
                }
            }
        )
        if not boss_response.get("success", False):
            logger.error(
                "Boss agent processing failed",
                extra={
                    'category': LogCategory.AGENT.value,
                    'user_id': message.user_id,
                    'metadata': {
                        'agent_type': 'boss_agent',
                        'error_message': boss_response.get('error', 'Unknown error')
                    }
                }
            )
        
        if boss_response.get("success", False):
            response = boss_response["response"]
            
            # Log boss agent usage for analytics
            logger.info(f"✅ Boss agent used: {boss_response.get('agents_used', [])} "
                       f"Intent: {boss_response.get('intent', 'unknown')} "
                       f"Confidence: {boss_response.get('confidence', 0):.2f}")
        else:
            # Fallback to original AI service if boss agent fails
            logger.warning("❌ Boss agent failed, falling back to original AI service")
            response = await get_ai_response(message.message, message.user_id, skip_quick_action=True)
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate AI response")
        
        return ChatResponse(response=response, status="success")
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error in chat endpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            "Chat endpoint error",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': getattr(message, 'user_id', None),
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@router.get("/status")
@limiter.limit(get_rate_limit("public", "health"))
def agent_status(request: Request):
    """Endpoint to check if the AI agent system is running"""
    try:
        from .api_startup import get_system_status
        system_status = get_system_status()
        
        return {
            "status": "online" if system_status["ready_for_requests"] else "initializing",
            "version": "2.0.0",
            "system_health": system_status,
            "architecture": "hierarchical_multi_agent",
            "agents": ["boss_agent", "content_analysis", "audience_insights", "seo_discoverability", "competitive_analysis", "monetization_strategy"],
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"Error in agent status endpoint: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")

@router.post("/quick-action", response_model=StandardResponse)
@limiter.limit(get_rate_limit("public", "generate"))
async def quick_action(request: Request, action_request: QuickActionRequest):
    """Handle quick actions with enhanced multi-agent coordination"""
    try:
        logger.info(
            "Processing quick action",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': action_request.user_id,
                'metadata': {
                    'action': action_request.action,
                    'action_type': 'enhanced',
                    'has_context': bool(action_request.context)
                }
            }
        )
        
        # Get user context for personalization
        context = get_user_context(action_request.user_id)
        ch = context["channel_info"]
        
        # For script generation and hook analysis, use multi-agent coordination
        if action_request.action in ["generate_script", "improve_hooks"]:
            return await handle_enhanced_content_action(action_request, context)
        
        # For other actions, continue with existing logic
        return await handle_standard_quick_action(action_request, context)
        
    except Exception as e:
        logger.error(
            "Enhanced quick action failed",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': getattr(action_request, 'user_id', None),
                'metadata': {
                    'action': getattr(action_request, 'action', None),
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to process quick action")

async def handle_enhanced_content_action(action_request: QuickActionRequest, context: Dict) -> StandardResponse:
    """Handle content-related actions with multi-agent coordination"""
    try:
        from .boss_agent import get_boss_agent
        from .enhanced_user_context import get_enhanced_context_manager
        
        # Get enhanced context with real-time data
        enhanced_context_manager = get_enhanced_context_manager()
        enhanced_context = await enhanced_context_manager.get_enhanced_context(action_request.user_id)
        
        # Get boss agent for orchestration
        boss_agent = get_boss_agent()
        
        # Create enhanced prompt based on action type
        if action_request.action == "generate_script":
            enhanced_prompt = f"""
            I need a high-quality video script for my YouTube channel. Please use your content analysis capabilities to create a script that's optimized for my channel's performance.
            
            Context: {action_request.context}
            
            Please analyze my recent content performance and create a script that:
            1. Uses hook patterns that work well for my channel
            2. Is structured for optimal retention based on my analytics
            3. Includes engagement strategies that match my audience
            4. Incorporates successful elements from my top-performing videos
            
            Make this script data-driven and personalized to my channel's strengths.
            """
        else:  # improve_hooks
            enhanced_prompt = f"""
            I need to improve my video hooks to increase CTR. Please analyze my content performance and hook effectiveness to provide specific recommendations.
            
            Current hook/context: {action_request.context}
            
            Please:
            1. Analyze my current hook patterns and their effectiveness
            2. Identify what types of hooks work best for my channel
            3. Provide specific improved hooks based on my successful content
            4. Give me actionable strategies to improve my CTR based on my analytics
            
            Base this on my actual performance data and successful video patterns.
            """
        
        # Use boss agent with enhanced context
        response = await boss_agent.process_user_message(
            user_id=action_request.user_id,
            message=enhanced_prompt,
            user_context=enhanced_context,
            priority=1  # High priority for quick actions
        )
        
        return create_success_response(
            f"Enhanced {action_request.action.replace('_', ' ')} generated successfully",
            {"response": response}
        )
        
    except Exception as e:
        logger.error(f"Error in enhanced content action: {e}")
        # Fallback to standard handling
        return await handle_standard_quick_action(action_request, context)

async def handle_standard_quick_action(action_request: QuickActionRequest, context: Dict) -> StandardResponse:
    """Handle quick actions with existing logic"""
    try:
        ch = context["channel_info"]
        
        # Calculate performance insights for better targeting
        subscriber_tier = "new" if ch['subscriber_count'] < 1000 else "growing" if ch['subscriber_count'] < 10000 else "established" if ch['subscriber_count'] < 100000 else "large"
        ctr_performance = "low" if ch['ctr'] < 3 else "average" if ch['ctr'] < 6 else "good" if ch['ctr'] < 10 else "excellent"
        retention_performance = "low" if ch['retention'] < 30 else "average" if ch['retention'] < 50 else "good" if ch['retention'] < 70 else "excellent"
        
        # Define action prompts based on the action type
        action_prompts = {
            "generate_script": f"""
            As a {ch['niche']} YouTube expert, create a video script specifically for {ch['name']}.
            
            CHANNEL-SPECIFIC REQUIREMENTS:
            🎯 Niche: {ch['niche']} (script must match {ch['niche']} audience expectations)
            👥 Audience Size: {subscriber_tier.title()} channel ({ch['subscriber_count']:,} subs)
            📊 Current CTR: {ch['ctr']}% ({ctr_performance}) - hook must be {ch['niche']}-specific to improve this
            ⏱️ Retention: {ch['retention']}% ({retention_performance}) - structure for {ch['niche']} viewer attention span
            🎬 Content Style: {ch['content_type']}
            🎯 Channel Goal: {ch['primary_goal']}
            
            Topic/Context: {action_request.context}
            
            Create a {ch['niche']}-optimized script with:
            1. HOOK (0-15 sec): Specific to {ch['niche']} audience pain points/interests
            2. INTRODUCTION (15-30 sec): Establish credibility in {ch['niche']}
            3. MAIN CONTENT: Structure for {ch['niche']} viewers (attention patterns)
            4. ENGAGEMENT PROMPTS: {ch['niche']}-specific questions/calls
            5. CTA: Appropriate for {subscriber_tier} channels in {ch['niche']}
            6. OUTRO: {ch['niche']} community building
            
            Make it sound like a successful {ch['niche']} creator with {ch['subscriber_count']:,} subscribers would speak.
            """,
            
            "improve_hooks": f"""
            As a {ch['niche']} YouTube specialist, improve hooks specifically for {ch['name']}.
            
            HOOK OPTIMIZATION TARGET:
            🎯 Channel: {ch['name']} in {ch['niche']} niche
            📊 Current CTR: {ch['ctr']}% ({ctr_performance}) - MUST improve for {ch['niche']}
            ⏱️ Retention: {ch['retention']}% ({retention_performance}) 
            👥 Audience: {subscriber_tier.title()} {ch['niche']} viewers ({ch['subscriber_count']:,} subs)
            🎯 Goal: {ch['primary_goal']}
            
            Current Hook/Context: {action_request.context}
            
            Provide 5 {ch['niche']}-SPECIFIC hook strategies that work for {subscriber_tier} channels:
            1. {ch['niche']} Pattern Interrupts (what stops {ch['niche']} viewers scrolling)
            2. {ch['niche']} Curiosity Gaps (what {ch['niche']} audience desperately wants to know)
            3. {ch['niche']} Emotional Triggers (fears/desires specific to {ch['niche']} community)
            4. {ch['niche']} Value Propositions (outcomes {ch['niche']} viewers crave)
            5. {ch['niche']} Authority Signals (credibility markers in {ch['niche']} space)
            
            Include 3 ready-to-use hook examples for {ch['name']} that reference {ch['niche']} trends/pain points.
            Target improving CTR from {ch['ctr']}% to industry benchmark (6-8% for {ch['niche']}).
            """,
            
            "optimize_title": f"""
            As a {ch['niche']} YouTube SEO specialist, optimize titles for {ch['name']}.
            
            TITLE OPTIMIZATION TARGET:
            🎯 Channel: {ch['name']} ({ch['niche']} niche)
            📊 Current CTR: {ch['ctr']}% ({ctr_performance}) - need {ch['niche']}-optimized titles
            👥 Audience: {subscriber_tier.title()} {ch['niche']} channel ({ch['subscriber_count']:,} subs)
            🎯 Goal: {ch['primary_goal']}
            
            Current Title/Topic: {action_request.context}
            
            Provide {ch['niche']}-specific title optimization:
            1. {ch['niche']} Keyword Research (what {ch['niche']} audience searches for)
            2. {ch['niche']} Emotional Triggers (words that make {ch['niche']} viewers click)
            3. {ch['niche']} Authority Signals (credibility markers for {ch['niche']})
            4. {ch['niche']} Urgency/Scarcity (FOMO specific to {ch['niche']} community)
            5. {ch['niche']} Number/List Formats (what works in {ch['niche']})
            
            Provide 5 optimized title variations for {ch['name']} that:
            - Target {ch['niche']} keywords with search volume
            - Appeal to {subscriber_tier} {ch['niche']} audience
            - Could improve CTR from {ch['ctr']}% to 6-8%
            - Match successful {ch['niche']} titles on YouTube
            """,
            
            "get_ideas": f"""
            As a {ch['niche']} content strategist, generate video ideas specifically for {ch['name']}.
            
            IDEA GENERATION TARGET:
            🎯 Channel: {ch['name']} ({ch['niche']} niche)
            👥 Audience: {subscriber_tier.title()} {ch['niche']} channel ({ch['subscriber_count']:,} subs)
            📊 Performance: CTR {ch['ctr']}% ({ctr_performance}), Retention {ch['retention']}% ({retention_performance})
            🎯 Goal: {ch['primary_goal']}
            🎬 Content Style: {ch['content_type']}
            
            Context/Direction: {action_request.context}
            
            Generate 10 {ch['niche']}-specific video ideas that:
            1. Match {ch['niche']} trends and audience interests
            2. Suit {subscriber_tier} channels (realistic production for {ch['subscriber_count']:,} subs)
            3. Could improve CTR/retention based on current {ctr_performance}/{retention_performance} performance
            4. Align with {ch['primary_goal']} channel goal
            5. Work well for {ch['content_type']} content style
            
            For each idea provide:
            - Video Title (optimized for {ch['niche']} search)
            - Hook Angle (first 15 seconds)
            - Key Points (3-5 main topics)
            - CTA Strategy (appropriate for {subscriber_tier} channels)
            - Why it works for {ch['niche']} audience
            """,
            
            "thumbnail_ideas": f"""
            As a {ch['niche']} thumbnail specialist, design thumbnail concepts for {ch['name']}.
            
            THUMBNAIL DESIGN TARGET:
            🎯 Channel: {ch['name']} ({ch['niche']} niche)
            📊 Current CTR: {ch['ctr']}% ({ctr_performance}) - thumbnails must improve this
            👥 Audience: {subscriber_tier.title()} {ch['niche']} viewers ({ch['subscriber_count']:,} subs)
            🎬 Content Style: {ch['content_type']}
            
            Video Topic/Context: {action_request.context}
            
            Provide 3 {ch['niche']}-optimized thumbnail concepts:
            1. {ch['niche']} Visual Elements (colors, icons, symbols that resonate)
            2. {ch['niche']} Emotional Expressions (faces/reactions that {ch['niche']} audience clicks)
            3. {ch['niche']} Text Overlays (power words for {ch['niche']} community)
            4. {ch['niche']} Contrast/Colors (what stands out in {ch['niche']} feeds)
            5. {ch['niche']} Visual Hierarchy (how {ch['niche']} viewers scan thumbnails)
            
            For each concept describe:
            - Main Visual Focus
            - Color Scheme
            - Text Elements
            - Emotional Appeal
            - Why it works for {ch['niche']} and {subscriber_tier} channels
            
            Target improving CTR from {ch['ctr']}% to 6-8% for {ch['niche']} content.
            """
        }
        
        # Get the prompt for the requested action
        if action_request.action not in action_prompts:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action_request.action}")
        
        prompt = action_prompts[action_request.action]
        
        # Process through boss agent system for consistency
        user_context = get_user_context(action_request.user_id)
        boss_response = await process_user_message(prompt, user_context)
        
        if boss_response.get("success", False):
            response = boss_response["response"]
            logger.info(f"✅ Quick action '{action_request.action}' completed via boss agent")
        else:
            # Fallback to direct AI service
            response = await get_ai_response(prompt, action_request.user_id)
            logger.info(f"✅ Quick action '{action_request.action}' completed via fallback AI")
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate response for quick action")
        
        return create_success_response(
            message=f"Quick action '{action_request.action}' completed successfully",
            data={"response": response, "action": action_request.action}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in quick_action endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to process quick action")

# =============================================================================
# Specialized Agent Task Endpoints
# =============================================================================

@router.post("/task/content-analysis")
async def content_analysis_task(request: AgentTaskRequest, auth=Depends(verify_agent_token)):
    """Endpoint for Boss Agent to request content analysis"""
    try:
        logger.info(f"Processing content analysis task: {request.request_id}")
        
        # Convert request to format expected by agent
        agent_request_data = {
            "request_id": request.request_id,
            "query_type": request.query_type,
            "context": request.context,
            "token_budget": request.token_budget,
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": auth.request_id  # Pass through the authenticated token
        }
        
        # Process through specialized agent
        result = await process_content_analysis_request(agent_request_data)
        
        if result.get("success", False) or result.get("domain_match", True):
            return result
        else:
            return create_error_response("Content analysis failed", result.get("error", "Unknown error"))
    except Exception as e:
        logger.error(f"Content analysis task error: {e}")
        return create_error_response("Content analysis failed", str(e))

@router.post("/task/audience-insights")
async def audience_insights_task(request: AgentTaskRequest, auth=Depends(verify_agent_token)):
    """Endpoint for Boss Agent to request audience insights"""
    try:
        logger.info(f"Processing audience insights task: {request.request_id}")
        
        # Convert request to format expected by agent
        agent_request_data = {
            "request_id": request.request_id,
            "query_type": request.query_type,
            "context": request.context,
            "token_budget": request.token_budget,
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": auth.request_id
        }
        
        # Process through specialized agent
        result = await process_audience_insights_request(agent_request_data)
        
        if result.get("success", False) or result.get("domain_match", True):
            return result
        else:
            return create_error_response("Audience insights failed", result.get("error", "Unknown error"))
    except Exception as e:
        logger.error(f"Audience insights task error: {e}")
        return create_error_response("Audience insights failed", str(e))

@router.post("/task/seo-discoverability")
async def seo_discoverability_task(request: AgentTaskRequest, auth=Depends(verify_agent_token)):
    """Endpoint for Boss Agent to request SEO analysis"""
    try:
        logger.info(f"Processing SEO discoverability task: {request.request_id}")
        
        # Convert request to format expected by agent
        agent_request_data = {
            "request_id": request.request_id,
            "query_type": request.query_type,
            "context": request.context,
            "token_budget": request.token_budget,
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": auth.request_id
        }
        
        # Process through specialized agent
        result = await process_seo_request(agent_request_data)
        
        if result.get("success", False) or result.get("domain_match", True):
            return result
        else:
            return create_error_response("SEO analysis failed", result.get("error", "Unknown error"))
    except Exception as e:
        logger.error(f"SEO discoverability task error: {e}")
        return create_error_response("SEO analysis failed", str(e))

@router.post("/task/competitive-analysis")
async def competitive_analysis_task(request: AgentTaskRequest, auth=Depends(verify_agent_token)):
    """Endpoint for Boss Agent to request competitive analysis"""
    try:
        logger.info(f"Processing competitive analysis task: {request.request_id}")
        
        # Convert request to format expected by agent
        agent_request_data = {
            "request_id": request.request_id,
            "query_type": request.query_type,
            "context": request.context,
            "token_budget": request.token_budget,
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": auth.request_id
        }
        
        # Process through specialized agent
        result = await process_competitive_analysis_request(agent_request_data)
        
        if result.get("success", False) or result.get("domain_match", True):
            return result
        else:
            return create_error_response("Competitive analysis failed", result.get("error", "Unknown error"))
    except Exception as e:
        logger.error(f"Competitive analysis task error: {e}")
        return create_error_response("Competitive analysis failed", str(e))

@router.post("/task/monetization-strategy")
async def monetization_strategy_task(request: AgentTaskRequest, auth=Depends(verify_agent_token)):
    """Endpoint for Boss Agent to request monetization analysis"""
    try:
        logger.info(f"Processing monetization strategy task: {request.request_id}")
        
        # Convert request to format expected by agent
        agent_request_data = {
            "request_id": request.request_id,
            "query_type": request.query_type,
            "context": request.context,
            "token_budget": request.token_budget,
            "analysis_depth": request.analysis_depth,
            "boss_agent_token": auth.request_id
        }
        
        # Process through specialized agent
        result = await process_monetization_strategy_request(agent_request_data)
        
        if result.get("success", False) or result.get("domain_match", True):
            return result
        else:
            return create_error_response("Monetization analysis failed", result.get("error", "Unknown error"))
    except Exception as e:
        logger.error(f"Monetization strategy task error: {e}")
        return create_error_response("Monetization analysis failed", str(e))

# =============================================================================
# Agent System Management
# =============================================================================

@router.post("/callback")
async def agent_callback(request: AgentCallbackRequest, auth=Depends(verify_agent_token)):
    """Receive callbacks from specialized agents"""
    try:
        logger.info(f"Received callback from {request.agent_type} for request {request.request_id}")
        
        # Process the callback response
        cache = get_agent_cache()
        cache.store_agent_response(
            request.request_id,
            request.agent_type,
            request.response_data,
            request.processing_time
        )
        
        return create_success_response("Callback processed successfully")
    
    except Exception as e:
        logger.error(f"Error processing agent callback: {e}")
        return create_error_response("Callback processing failed", str(e))

@router.post("/set-channel-info")
@limiter.limit(get_rate_limit("authenticated", "channel_info"))
async def set_channel_info(channel_info: ChannelInfo, request: Request):
    """Set or update channel information for a user"""
    try:
        # For now, use default user ID
        user_id = "default_user"
        
        logger.info(
            "Setting channel info",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': user_id,
                'metadata': {
                    'channel_name': channel_info.name,
                    'niche': channel_info.niche
                }
            }
        )
        
        # Update user context with channel information
        update_user_context(user_id, "channel_info", {
            "name": channel_info.name,
            "niche": channel_info.niche,
            "content_type": channel_info.content_type,
            "subscriber_count": channel_info.subscriber_count,
            "avg_view_count": channel_info.avg_view_count,
            "ctr": channel_info.ctr,
            "retention": channel_info.retention,
            "upload_frequency": channel_info.upload_frequency,
            "video_length": channel_info.video_length,
            "monetization_status": channel_info.monetization_status,
            "primary_goal": channel_info.primary_goal,
            "notes": channel_info.notes or ""
        })
        
        logger.info(f"✅ Channel info updated successfully for user {user_id}")
        
        return create_success_response(
            "Channel information updated successfully",
            {"user_id": user_id, "channel_name": channel_info.name}
        )
        
    except Exception as e:
        logger.error(f"Error setting channel info: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update channel information")

@router.get("/model-status", response_model=ModelStatusResponse)
async def get_model_status():
    """Get status of all model integrations"""
    try:
        model_integration = get_model_integration()
        model_status = model_integration.get_model_status()
        available_models = model_integration.get_available_models()
        
        # Count active integrations
        active_integrations = [provider for provider, status in model_status.items() if status["available"]]
        
        return ModelStatusResponse(
            available_models=available_models,
            model_status=model_status,
            active_integrations=active_integrations
        )
    
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model status")

@router.get("/cache-stats")
async def get_cache_stats():
    """Get agent cache statistics"""
    try:
        cache = get_agent_cache()
        stats = cache.get_cache_stats()
        
        return create_success_response("Cache stats retrieved", stats)
    
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return create_error_response("Failed to get cache stats", str(e))

@router.post("/clear-cache")
async def clear_agent_cache():
    """Clear the agent cache"""
    try:
        cache = get_agent_cache()
        cleared_count = cache.clear_cache()
        
        return create_success_response(
            f"Cache cleared successfully",
            {"cleared_entries": cleared_count}
        )
    
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return create_error_response("Failed to clear cache", str(e))