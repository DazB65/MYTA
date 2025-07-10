from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
import traceback
# Import from the same directory
from ai_services import get_ai_response, extract_channel_info, update_user_context, get_user_context
from insights_engine import insights_engine
from boss_agent import process_user_message
from agent_cache import get_agent_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CreatorMate API", version="1.0.0")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception handler caught: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )

# Validation error handler
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": str(exc)
        }
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    user_id: str = "default_user"
    
    class Config:
        str_strip_whitespace = True
        min_anystr_length = 1
        max_anystr_length = 2000

class QuickActionRequest(BaseModel):
    action: str
    user_id: str = "default_user"
    context: str = ""
    
    class Config:
        str_strip_whitespace = True

@app.post("/api/agent/chat")
async def chat(message: ChatMessage):
    """Endpoint to handle chat messages from the user"""
    try:
        # Validate input
        if not message.message or not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(message.message) > 2000:
            raise HTTPException(status_code=400, detail="Message too long (max 2000 characters)")
        
        logger.info(f"Processing chat message from user: {message.user_id}")
        
        # Extract any channel info from the message
        extract_channel_info(message.user_id, message.message)
        
        # Get user context for boss agent
        user_context = get_user_context(message.user_id)
        
        # Process through boss agent orchestration system
        boss_response = await process_user_message(message.message, user_context)
        
        if boss_response.get("success", False):
            response = boss_response["response"]
            
            # Log boss agent usage for analytics
            logger.info(f"Boss agent used: {boss_response.get('agents_used', [])} "
                       f"Intent: {boss_response.get('intent', 'unknown')} "
                       f"Confidence: {boss_response.get('confidence', 0):.2f}")
        else:
            # Fallback to original AI service if boss agent fails
            logger.warning("Boss agent failed, falling back to original AI service")
            response = await get_ai_response(message.message, message.user_id)
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate AI response")
        
        return {"response": response, "status": "success"}
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error in chat endpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@app.get("/api/agent/status")
def agent_status():
    """Endpoint to check if the AI agent is running"""
    try:
        # You could add actual health checks here
        # For example, test OpenAI API connectivity
        return {
            "status": "online",
            "version": "1.0.0",
            "model": "gpt-4o",
            "timestamp": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"Error in agent status endpoint: {e}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")

class ChannelInfo(BaseModel):
    name: str = "Unknown"
    niche: str = "Unknown"
    content_type: str = "Unknown"
    subscriber_count: int = 0
    avg_view_count: int = 0
    ctr: float = 0
    retention: float = 0
    upload_frequency: str = "Unknown"
    video_length: str = "Unknown"
    monetization_status: str = "Unknown"
    primary_goal: str = "Unknown"
    notes: str = ""
    user_id: str = "default_user"
    
    class Config:
        str_strip_whitespace = True
        
    def validate_metrics(self):
        """Validate channel metrics are within reasonable ranges"""
        if self.subscriber_count < 0:
            raise ValueError("Subscriber count cannot be negative")
        if self.avg_view_count < 0:
            raise ValueError("Average view count cannot be negative")
        if not (0 <= self.ctr <= 100):
            raise ValueError("CTR must be between 0 and 100")
        if not (0 <= self.retention <= 100):
            raise ValueError("Retention must be between 0 and 100")
        if len(self.notes) > 1000:
            raise ValueError("Notes cannot exceed 1000 characters")

@app.post("/api/agent/set-channel-info")
async def set_channel_info(channel_info: ChannelInfo):
    """Endpoint to manually set channel information"""
    try:
        # Validate channel info
        channel_info.validate_metrics()
        
        logger.info(f"Updating channel info for user: {channel_info.user_id}")
        
        # Extract channel info fields
        info = {
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
            "notes": channel_info.notes
        }
        
        # Update user context
        result = update_user_context(channel_info.user_id, "channel_info", info)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update channel information")
        
        return {"status": "success", "message": "Channel information updated successfully"}
    
    except ValueError as e:
        logger.error(f"Validation error in set_channel_info: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in set_channel_info: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update channel information")

@app.post("/api/agent/quick-action")
async def quick_action(request: QuickActionRequest):
    """Handle quick actions from the user interface"""
    try:
        logger.info(f"Processing quick action '{request.action}' for user: {request.user_id}")
        
        # Get user context for personalization
        context = get_user_context(request.user_id)
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
            
            Topic/Context: {request.context}
            
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
            
            Current Hook/Context: {request.context}
            
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
            
            Current Title/Topic: {request.context}
            
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
            
            CONTENT STRATEGY FOR:
            🎯 {ch['name']} - {ch['niche']} Channel
            👥 {subscriber_tier.title()} Channel ({ch['subscriber_count']:,} subscribers)
            🎬 Content Style: {ch['content_type']}
            📊 Performance: {ch['ctr']}% CTR, {ch['retention']}% retention
            🎯 Goal: {ch['primary_goal']}
            
            Context/Theme: {request.context}
            
            Generate 15 video ideas SPECIFICALLY for {ch['niche']} audience:
            
            🔥 TRENDING {ch['niche'].upper()} (5 ideas):
            - Current hot topics in {ch['niche']} community
            - Viral {ch['niche']} trends right now
            - {ch['niche']} news/updates worth covering
            
            ♻️ EVERGREEN {ch['niche'].upper()} (5 ideas):
            - {ch['niche']} fundamentals that always perform
            - Common {ch['niche']} problems to solve
            - {ch['niche']} guides for beginners
            
            📺 SERIES CONCEPTS (5 ideas):
            - Multi-part {ch['niche']} series that build audience
            - {ch['niche']} challenges/experiments
            - {ch['niche']} comparison series
            
            For each idea, explain:
            - Why it works for {subscriber_tier} {ch['niche']} channels
            - Expected CTR/retention for {ch['niche']} audience
            - How it supports their goal: {ch['primary_goal']}
            """
        }
        
        # Get the appropriate prompt
        prompt = action_prompts.get(request.action.lower().replace(" ", "_"))
        if not prompt:
            raise HTTPException(status_code=400, detail=f"Unknown action: {request.action}")
        
        # Get AI response
        response = await get_ai_response(prompt, request.user_id)
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate response")
        
        return {
            "action": request.action,
            "response": response,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in quick_action: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to process quick action")

@app.get("/api/agent/insights/{user_id}")
async def get_insights(user_id: str):
    """Get dynamic insights for a user"""
    try:
        logger.info(f"Getting insights for user: {user_id}")
        
        # Generate new insights
        new_insights = insights_engine.generate_insights_for_user(user_id, limit=3)
        
        # Get existing insights
        existing_insights = insights_engine.get_user_insights(user_id, limit=5)
        
        # Combine and deduplicate
        all_insights = new_insights + existing_insights
        seen_titles = set()
        unique_insights = []
        
        for insight in all_insights:
            if insight["title"] not in seen_titles:
                seen_titles.add(insight["title"])
                unique_insights.append(insight)
        
        return {
            "insights": unique_insights[:5],
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in get_insights: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get insights")

@app.post("/api/agent/generate-insights")
async def generate_insights(request: ChatMessage):
    """Generate new insights for a user"""
    try:
        logger.info(f"Generating insights for user: {request.user_id}")
        
        # Generate fresh insights
        insights = insights_engine.generate_insights_for_user(request.user_id, limit=3)
        
        return {
            "insights": insights,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in generate_insights: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate insights")

@app.get("/api/agent/context/{user_id}")
async def get_user_context_endpoint(user_id: str):
    """Get user context including channel information"""
    try:
        logger.info(f"Getting context for user: {user_id}")
        
        # Get user context
        context = get_user_context(user_id)
        
        return {
            "channel_info": context["channel_info"],
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in get_user_context_endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get user context")

@app.post("/api/agent/analytics")
async def analytics_query(message: ChatMessage):
    """Advanced analytics endpoint using boss agent orchestration"""
    try:
        # Validate input
        if not message.message or not message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        logger.info(f"Processing analytics query from user: {message.user_id}")
        
        # Get user context
        user_context = get_user_context(message.user_id)
        
        # Process through boss agent with enhanced context
        boss_response = await process_user_message(message.message, user_context)
        
        if not boss_response.get("success", False):
            raise HTTPException(status_code=500, detail="Failed to process analytics query")
        
        return {
            "response": boss_response["response"],
            "metadata": {
                "intent": boss_response.get("intent", "unknown"),
                "agents_used": boss_response.get("agents_used", []),
                "confidence": boss_response.get("confidence", 0),
                "processing_time": boss_response.get("processing_time", 0),
                "recommendations": boss_response.get("recommendations", [])
            },
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analytics_query: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to process analytics query")

@app.get("/api/agent/cache/stats")
async def get_cache_stats():
    """Get agent cache performance statistics"""
    try:
        cache = get_agent_cache()
        stats = cache.get_stats()
        
        return {
            "cache_stats": stats,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get cache statistics")

@app.post("/api/agent/cache/clear")
async def clear_cache():
    """Clear expired cache entries"""
    try:
        cache = get_agent_cache()
        cleared_count = cache.clear_expired()
        
        return {
            "cleared_entries": cleared_count,
            "message": f"Cleared {cleared_count} expired cache entries",
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear cache")

@app.post("/api/content/generate")
async def generate_content_endpoint(request: QuickActionRequest):
    """Generate content like scripts, calendars, topic research"""
    try:
        logger.info(f"Generating content type '{request.action}' for user: {request.user_id}")
        
        # Get user context for personalization
        context = get_user_context(request.user_id)
        ch = context["channel_info"]
        
        # Enhanced content generation prompts
        content_prompts = {
            "script_template": f"""
            As a YouTube content creation expert, create a comprehensive script template for {ch['name']} channel.
            
            Channel Context:
            - Niche: {ch['niche']}
            - Content Type: {ch['content_type']}
            - Subscribers: {ch['subscriber_count']}
            - Average Views: {ch['avg_view_count']}
            - Video Length: {ch['video_length']}
            - Primary Goal: {ch['primary_goal']}
            
            Create a detailed script template with:
            1. Pre-production checklist
            2. Hook templates (3 variations)
            3. Introduction structure
            4. Main content framework
            5. Transition phrases
            6. Call-to-action templates
            7. Outro structure
            8. Engagement prompts
            
            Make it specific to their niche and optimized for their audience size.
            """,
            
            "content_calendar": f"""
            As a YouTube content strategist, create a 4-week content calendar for {ch['name']} channel.
            
            Channel Context:
            - Niche: {ch['niche']}
            - Upload Frequency: {ch['upload_frequency']}
            - Subscriber Count: {ch['subscriber_count']}
            - Primary Goal: {ch['primary_goal']}
            
            Create a detailed calendar with:
            1. Weekly themes aligned with their niche
            2. Specific video topics for each upload day
            3. Content mix (educational, entertainment, trending)
            4. Seasonal/timely content opportunities
            5. Series ideas for consistent viewership
            6. Optimal posting times
            7. Cross-promotion opportunities
            
            Format as a clear weekly breakdown with actionable video ideas.
            """,
            
            "topic_research": f"""
            As a YouTube trend researcher, provide comprehensive topic research for {ch['name']} channel.
            
            Channel Context:
            - Niche: {ch['niche']}
            - Current Performance: {ch['avg_view_count']} avg views
            - Subscriber Count: {ch['subscriber_count']}
            - Primary Goal: {ch['primary_goal']}
            
            Provide:
            1. 15 trending topics in their niche (with search volume indicators)
            2. 10 evergreen content ideas
            3. 5 seasonal/timely opportunities
            4. Competitor analysis insights
            5. Keyword research for SEO
            6. Content gaps in their niche
            7. Audience questions to answer
            
            Include rationale for why each topic would perform well for their channel.
            """
        }
        
        # Get the appropriate prompt
        prompt = content_prompts.get(request.action.lower())
        if not prompt:
            # Fall back to quick action if not found
            return await quick_action(request)
        
        # Get AI response
        response = await get_ai_response(prompt, request.user_id)
        
        if not response:
            raise HTTPException(status_code=500, detail="Failed to generate content")
        
        return {
            "content_type": request.action,
            "response": response,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_content_endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate content")

@app.get("/api/analytics/performance/{user_id}")
async def get_performance_analytics(user_id: str):
    """Get performance analytics for a user's channel"""
    try:
        logger.info(f"Getting analytics for user: {user_id}")
        
        # Get user context
        context = get_user_context(user_id)
        ch = context["channel_info"]
        
        # Generate simulated analytics based on channel info
        # In a real implementation, this would connect to YouTube Analytics API
        analytics = {
            "total_views": ch["avg_view_count"] * 10,  # Estimate based on avg views
            "subscriber_growth": max(5, ch["subscriber_count"] * 0.05),  # 5% growth estimate
            "engagement_rate": max(2.0, ch["ctr"] * 0.8),  # Estimate engagement from CTR
            "top_performing_videos": [
                {
                    "title": f"Top {ch['niche']} Tips for Beginners",
                    "views": ch["avg_view_count"] * 1.5,
                    "ctr": ch["ctr"] * 1.2,
                    "retention": ch["retention"] * 1.1
                },
                {
                    "title": f"Advanced {ch['niche']} Strategies",
                    "views": ch["avg_view_count"] * 1.3,
                    "ctr": ch["ctr"] * 1.1,
                    "retention": ch["retention"] * 1.0
                }
            ],
            "performance_trends": {
                "views_trend": "up",
                "ctr_trend": "stable",
                "retention_trend": "up"
            }
        }
        
        return {
            "analytics": analytics,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in get_performance_analytics: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get analytics")

@app.post("/api/tools/seo-analyze")
async def seo_analyze_endpoint(request: ChatMessage):
    """Analyze and optimize video SEO"""
    try:
        logger.info(f"SEO analysis for user: {request.user_id}")
        
        # Get user context
        context = get_user_context(request.user_id)
        ch = context["channel_info"]
        
        prompt = f"""
        As a YouTube SEO expert, analyze and optimize the following content for {ch['name']} channel.
        
        Channel Context:
        - Niche: {ch['niche']}
        - Current CTR: {ch['ctr']}%
        - Subscriber Count: {ch['subscriber_count']}
        - Primary Goal: {ch['primary_goal']}
        
        Content to analyze: {request.message}
        
        Provide:
        1. SEO Score (1-10) with explanation
        2. Title optimization suggestions
        3. Description improvements
        4. Relevant tags and keywords
        5. Thumbnail text recommendations
        6. Competitor analysis insights
        7. Search volume estimates
        
        Give specific, actionable recommendations.
        """
        
        response = await get_ai_response(prompt, request.user_id)
        
        return {
            "analysis": response,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in seo_analyze_endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to analyze SEO")

@app.get("/api/export/data/{user_id}")
async def export_user_data(user_id: str, format: str = "json"):
    """Export user data in various formats"""
    try:
        logger.info(f"Exporting data for user: {user_id} in format: {format}")
        
        # Get user context and insights
        context = get_user_context(user_id)
        insights = insights_engine.get_user_insights(user_id, limit=10)
        
        # Get analytics data
        analytics_response = await get_performance_analytics(user_id)
        analytics = analytics_response.get("analytics", {})
        
        # Compile export data
        export_data = {
            "user_id": user_id,
            "export_timestamp": datetime.now().isoformat(),
            "channel_info": context["channel_info"],
            "recent_insights": insights,
            "performance_analytics": analytics,
            "conversation_history": context.get("conversation_history", [])[-10:],  # Last 10 messages
            "export_format": format
        }
        
        if format.lower() == "csv":
            # Convert to CSV format for basic data
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write channel info
            writer.writerow(["Channel Information"])
            writer.writerow(["Field", "Value"])
            for key, value in context["channel_info"].items():
                writer.writerow([key, value])
            
            writer.writerow([])  # Empty row
            writer.writerow(["Recent Insights"])
            writer.writerow(["Title", "Type", "Content"])
            for insight in insights:
                writer.writerow([insight["title"], insight["type"], insight["content"]])
            
            csv_content = output.getvalue()
            output.close()
            
            from fastapi.responses import PlainTextResponse
            return PlainTextResponse(
                content=csv_content,
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=creatormate_data_{user_id}.csv"}
            )
        
        # Default to JSON format
        return {
            "export_data": export_data,
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in export_user_data: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to export data")

@app.post("/api/reports/generate")
async def generate_report(request: ChatMessage):
    """Generate comprehensive reports for users"""
    try:
        logger.info(f"Generating report for user: {request.user_id}")
        
        # Get user context
        context = get_user_context(request.user_id)
        ch = context["channel_info"]
        
        # Get insights and analytics
        insights = insights_engine.get_user_insights(request.user_id, limit=5)
        analytics_response = await get_performance_analytics(request.user_id)
        analytics = analytics_response.get("analytics", {})
        
        # Generate comprehensive report
        report_prompt = f"""
        As a YouTube analytics expert, create a comprehensive monthly report for {ch['name']} channel.
        
        Channel Information:
        - Name: {ch['name']}
        - Niche: {ch['niche']}
        - Subscribers: {ch['subscriber_count']}
        - Average Views: {ch['avg_view_count']}
        - CTR: {ch['ctr']}%
        - Retention: {ch['retention']}%
        - Primary Goal: {ch['primary_goal']}
        
        Performance Analytics:
        - Total Views: {analytics.get('total_views', 0)}
        - Engagement Rate: {analytics.get('engagement_rate', 0)}%
        - Subscriber Growth: {analytics.get('subscriber_growth', 0)}%
        
        Recent Insights:
        {chr(10).join([f"- {insight['title']}: {insight['content']}" for insight in insights])}
        
        Report Type: {request.message}
        
        Create a detailed report including:
        1. Executive Summary
        2. Channel Performance Overview
        3. Content Performance Analysis
        4. Audience Engagement Metrics
        5. Growth Opportunities
        6. Competitive Analysis
        7. Recommendations for Next Month
        8. Action Items with Timeline
        
        Format the report professionally with clear sections and actionable insights.
        """
        
        response = await get_ai_response(report_prompt, request.user_id)
        
        return {
            "report": response,
            "report_type": request.message,
            "generated_at": datetime.now().isoformat(),
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Unexpected error in generate_report: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate report")

# Add a health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # You could add more comprehensive health checks here
        # For example, check database connectivity, external API status, etc.
        return {
            "status": "healthy",
            "timestamp": str(datetime.now()),
            "service": "CreatorMate API",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")
# Mount static files - serve React build files
try:
    app.mount("/", StaticFiles(directory="../frontend-dist", html=True), name="static")
    logger.info("Successfully mounted React build files from ../frontend-dist")
except Exception as e:
    logger.error(f"Failed to mount static files: {e}")
    # Fallback to old frontend if React build doesn't exist
    try:
        app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
        logger.info("Fallback: serving old frontend from ../frontend")
    except Exception as fallback_error:
        logger.error(f"Fallback also failed: {fallback_error}")
        raise