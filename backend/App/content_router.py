"""
Content generation router for AI-powered content creation
Handles script generation, title generation, and description generation
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Import authentication and utilities
from backend.App.auth_middleware import get_current_user
from backend.App.rate_limiter import limiter, get_rate_limit
from backend.App.api_models import create_success_response, create_error_response

# Import AI services
from backend.App.model_integrations import create_agent_call_to_integration, generate_agent_response
from backend.App.agent_personalities import get_agent_personality

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/content", tags=["content"])

@router.post("/generate-script")
@limiter.limit(get_rate_limit("authenticated", "content_generation"))
async def generate_script(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Generate AI-powered video script based on title, description, and parameters"""
    try:
        body = await request.json()
        
        # Extract parameters
        title = body.get("title", "").strip()
        description = body.get("description", "").strip()
        content_idea = body.get("contentIdea", "").strip()
        pillar = body.get("pillar", "General")
        script_type = body.get("type", "tutorial")
        length = body.get("length", "medium")
        tone = body.get("tone", "engaging")
        agent_id = body.get("agent_id", "1")
        
        # Validate required fields
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        
        # Get agent personality for context
        agent = get_agent_personality(agent_id)
        
        # Get enhanced user context for personalization
        user_id = current_user["id"]

        # Import enhanced context services
        try:
            from backend.App.enhanced_user_context import EnhancedUserContextService
            from backend.App.audience_insights_agent import AudienceInsightsAgent

            # Get enhanced user context with performance data
            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            # Get audience insights for personalization
            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for user {user_id}: {e}")
            enhanced_context = {}
            audience_insights = {}

        # Build enhanced context for personalization
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})

        # Build highly specialized prompt with enhanced user context
        script_prompt = f"""
        You are {agent['name']}, {agent['role']}. Create a specialized YouTube video script that showcases your unique expertise and personality.

        CONTENT DETAILS:
        - Title: {title}
        - Content Idea: {content_idea if content_idea else 'No specific idea provided - use title and description for context'}
        - Description: {description if description else 'No additional description provided'}
        - Content Pillar: {pillar}
        - Script Type: {script_type}
        - Target Length: {length}
        - Tone: {tone}
        - Agent Expertise: {agent.get('expertise', 'General content creation')}

        CHANNEL PERFORMANCE CONTEXT:
        - Channel Size: {channel_context.get('subscriber_count', 'Unknown')} subscribers
        - Average CTR: {channel_context.get('recent_ctr', 'Unknown')}%
        - Average Retention: {channel_context.get('recent_retention', 'Unknown')}%
        - Top Performing Content Types: {performance_context.get('successful_content_patterns', 'General content')}
        - Audience Engagement Style: {audience_context.get('engagement_preferences', 'Standard engagement')}

        AUDIENCE INSIGHTS:
        - Primary Demographics: {audience_context.get('primary_age_group', 'General audience')}
        - Content Preferences: {audience_context.get('content_preferences', 'Varied interests')}
        - Engagement Patterns: {audience_context.get('peak_engagement_times', 'Standard patterns')}
        - Communication Style: {audience_context.get('preferred_communication_style', 'Professional and engaging')}

        CRITICAL INSTRUCTION - BE SPECIFIC AND PERSONALIZED:
        This script must be HIGHLY SPECIFIC and ACTIONABLE, not generic. Use the content idea to create something unique that only an expert in {pillar} would know.

        PERSONALIZATION REQUIREMENTS:
        - Tailor content complexity to match your audience's engagement patterns
        - Use communication style that resonates with your {audience_context.get('primary_age_group', 'general')} audience
        - Reference performance patterns that work for your channel size ({channel_context.get('subscriber_count', 'growing')} subscribers)
        - Include hooks and techniques similar to your top-performing content

        REQUIRED SPECIFICITY:
        - Include specific tools, software, platforms, or apps used in {pillar}
        - Mention exact numbers, percentages, metrics, or benchmarks
        - Reference real examples, case studies, or scenarios from {pillar}
        - Use industry-specific terminology and jargon
        - Address specific problems that {pillar} practitioners face
        - Provide advanced techniques or insider knowledge
        - Include specific steps with exact actions to take

        EXPERT SCRIPT STRUCTURE:

        1. PERFORMANCE-OPTIMIZED HOOK (0-15 seconds):
        Based on your channel's {channel_context.get('recent_ctr', 'average')}% CTR performance, create a hook that:
        - Uses a specific statistic, result, or claim directly related to the content idea
        - Addresses a common {pillar} problem that the content idea specifically solves
        - Mentions an exact tool, technique, or method you'll reveal
        - Promises a specific transformation or result viewers will achieve
        - Matches the engagement style that works for your audience

        2. CREDIBILITY INTRO (15-30 seconds):
        - Establish expertise in this specific area of {pillar}
        - Mention relevant experience, tools, or results related to the content idea
        - Reference specific platforms, software, or methodologies you use
        - Preview the exact, measurable value viewers will get

        3. RETENTION-OPTIMIZED MAIN CONTENT (Write the complete spoken content):
        With your current {channel_context.get('recent_retention', 'average')}% retention rate, structure content to maintain engagement:
        - Complete step-by-step explanations with specific actions and exact settings
        - Name specific tools, software, platforms, or apps (TubeBuddy, Canva, Photoshop, etc.)
        - Include real examples with actual numbers, metrics, or results you create
        - Mention specific configurations, settings, or parameters in detail
        - Explain common mistakes with exact solutions in full sentences
        - Share advanced techniques that demonstrate {pillar} expertise
        - Provide specific benchmarks or targets with complete explanations
        - Use pacing and engagement techniques that work for your audience demographic
        - Include retention hooks every 30-45 seconds to maintain {audience_context.get('attention_span', 'standard')} attention spans

        4. EXPERT ENGAGEMENT:
        - Ask specific questions about viewers' {pillar} tools or experience
        - Reference current {pillar} trends, updates, or industry changes
        - Encourage sharing of specific results, metrics, or experiences
        - Create discussions around specific {pillar} challenges

        5. ACTIONABLE CALL TO ACTION:
        - Suggest specific next steps related to the content idea
        - Recommend particular tools, resources, or platforms
        - Mention specific {pillar} topics for future videos
        - Provide exact resources or links (mention them specifically)

        CONTENT TYPE SPECIFIC REQUIREMENTS:
        """
        
        # Add type-specific requirements
        if script_type == "tutorial":
            script_prompt += """
        - Break down complex concepts into simple steps
        - Use clear, actionable language
        - Include practical examples and demonstrations
        - Anticipate common questions and address them
        """
        elif script_type == "review":
            script_prompt += """
        - Provide balanced, honest assessment
        - Include both pros and cons
        - Share personal experience and insights
        - Help viewers make informed decisions
        """
        elif script_type == "entertainment":
            script_prompt += """
        - Focus on storytelling and engagement
        - Use humor and personality
        - Create emotional connection with viewers
        - Keep energy high throughout
        """
        elif script_type == "educational":
            script_prompt += """
        - Present information clearly and logically
        - Use examples and analogies for complex topics
        - Include key takeaways and summaries
        - Make learning enjoyable and accessible
        """
        
        script_prompt += f"""

        CRITICAL FINAL REQUIREMENTS:
        - Generate a COMPLETE, FULL script with NO placeholders, brackets, or [INSERT X HERE] text
        - Write out every single word that should be spoken - this is the final script
        - NO placeholders like [Your Name], [Tool Name], [Number], [Example] - fill in everything
        - Use real, specific examples, tools, numbers, and case studies
        - Make up realistic but specific data points, metrics, and examples if needed
        - Write as if you are {agent['name']} speaking directly to the camera
        - Include natural speech patterns, pauses, and conversational flow
        - The script should be 100% ready to read aloud without any editing

        ABSOLUTELY NO PLACEHOLDERS ALLOWED:
        ❌ Don't write: "Use [tool name] to achieve [result]"
        ✅ Do write: "Use TubeBuddy's A/B testing feature to achieve a 40% CTR increase"

        ❌ Don't write: "I increased my [metric] by [percentage]"
        ✅ Do write: "I increased my click-through rate from 2.1% to 8.7% in just 90 days"

        EXAMPLE OF WHAT WE WANT:
        "Hey everyone, it's {agent['name']} here, and today I'm going to show you the exact thumbnail optimization strategy that increased my click-through rate from 2.1% to 8.7% in just 90 days. I've tested over 200 thumbnails using TubeBuddy's A/B testing feature, and I've discovered three specific design principles that consistently outperform everything else..."

        Generate a complete, word-for-word script exactly like this example - specific, detailed, and ready to read aloud.
        """
        
        # Call AI model for script generation
        result = await create_agent_call_to_integration(
            agent_type="boss_agent",
            use_case="content_generation",
            prompt_data={
                "prompt": script_prompt,
                "analysis_depth": "deep",
                "system_message": f"You are {agent['name']}, an expert YouTube content creator specializing in {pillar} content. Write complete, word-for-word scripts with NO placeholders or brackets. Every sentence should be ready to speak aloud. Use specific tools, numbers, and examples - never write [insert X] or [your tool]. Create engaging, professional scripts that drive viewer engagement and retention."
            }
        )
        
        if result.get("success"):
            script_content = result.get("content", "")
            
            # Log successful generation
            logger.info(f"Script generated successfully for user {current_user['id']}, title: {title[:50]}...")
            
            return create_success_response(
                "Script generated successfully",
                {
                    "script": script_content,
                    "metadata": {
                        "title": title,
                        "pillar": pillar,
                        "type": script_type,
                        "length": length,
                        "tone": tone,
                        "agent": agent['name'],
                        "generated_at": datetime.utcnow().isoformat(),
                        "word_count": len(script_content.split()) if script_content else 0
                    }
                }
            )
        else:
            # AI generation failed, return error
            logger.error(f"AI script generation failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail="Failed to generate script with AI")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in script generation: {e}")
        return create_error_response("Script generation failed", str(e))

@router.post("/generate-title")
@limiter.limit(get_rate_limit("authenticated", "content_generation"))
async def generate_title(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Generate AI-powered video titles based on topic and pillar"""
    try:
        body = await request.json()
        
        topic = body.get("topic", "").strip()
        content_idea = body.get("contentIdea", "").strip()
        pillar = body.get("pillar", "General")
        agent_id = body.get("agent_id", "1")
        count = min(body.get("count", 5), 10)  # Limit to max 10 suggestions
        
        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")

        # Get enhanced user context for title personalization
        user_id = current_user["id"]
        try:
            from backend.App.enhanced_user_context import EnhancedUserContextService
            from backend.App.audience_insights_agent import AudienceInsightsAgent

            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for title generation: {e}")
            enhanced_context = {}
            audience_insights = {}

        # Get agent personality
        agent = get_agent_personality(agent_id)

        # Extract performance context
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})

        # Build specialized prompt for title generation with performance data
        title_prompt = f"""
        You are {agent['name']}, {agent['role']}. Generate {count} highly specific YouTube video titles for:

        Topic: {topic}
        Content Idea: {content_idea if content_idea else 'Use topic for context'}
        Content Pillar: {pillar}

        CHANNEL PERFORMANCE CONTEXT:
        - Channel Size: {channel_context.get('subscriber_count', 'Growing')} subscribers
        - Current CTR: {channel_context.get('recent_ctr', 'Average')}%
        - Audience Demographics: {audience_context.get('primary_age_group', 'General audience')}
        - Top Performing Content: {performance_context.get('successful_content_patterns', 'Varied content')}
        - Audience Engagement Style: {audience_context.get('engagement_preferences', 'Standard engagement')}

        CRITICAL REQUIREMENTS:
        1. Titles must be SPECIFIC to {pillar} - not generic
        2. Include exact tools, numbers, or specific outcomes when possible
        3. Use {pillar} industry terminology and jargon
        4. Reference specific problems that {pillar} practitioners face
        5. Mention specific techniques, methods, or strategies
        6. Keep under 60 characters for optimal YouTube display
        7. Create curiosity about specific {pillar} knowledge
        8. Optimize for your audience demographic ({audience_context.get('primary_age_group', 'general audience')})
        9. Use language and complexity level that matches your {channel_context.get('subscriber_count', 'growing')} subscriber channel

        EXAMPLES OF SPECIFICITY:
        - Instead of "How to Get More Views" → "How I Got 2M Views Using This YouTube Algorithm Hack"
        - Instead of "Productivity Tips" → "Notion Template That Saves Me 10 Hours/Week"
        - Instead of "Gaming Guide" → "Valorant Crosshair Settings That Boosted My Rank to Immortal"

        Return exactly {count} titles, each on a new line, without numbering or bullets.
        Make them irresistible to {pillar} practitioners while being truthful and valuable.
        """
        
        # Call AI model
        result = await create_agent_call_to_integration(
            agent_type="boss_agent",
            use_case="content_generation",
            prompt_data={
                "prompt": title_prompt,
                "analysis_depth": "standard",
                "system_message": f"You are {agent['name']}, an expert at creating viral YouTube titles that drive clicks and engagement."
            }
        )
        
        if result.get("success"):
            titles_text = result.get("content", "")
            titles = [title.strip() for title in titles_text.split('\n') if title.strip()]
            
            return create_success_response(
                "Titles generated successfully",
                {
                    "titles": titles[:count],  # Ensure we don't exceed requested count
                    "metadata": {
                        "topic": topic,
                        "pillar": pillar,
                        "agent": agent['name'],
                        "generated_at": datetime.utcnow().isoformat()
                    }
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate titles with AI")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in title generation: {e}")
        return create_error_response("Title generation failed", str(e))

@router.post("/generate-description")
@limiter.limit(get_rate_limit("authenticated", "content_generation"))
async def generate_description(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Generate AI-powered video description based on title and content details"""
    try:
        body = await request.json()
        
        title = body.get("title", "").strip()
        pillar = body.get("pillar", "General")
        agent_id = body.get("agent_id", "1")
        keywords = body.get("keywords", [])
        
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")

        # Get enhanced user context for description personalization
        user_id = current_user["id"]
        try:
            from backend.App.enhanced_user_context import EnhancedUserContextService
            from backend.App.audience_insights_agent import AudienceInsightsAgent

            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for description generation: {e}")
            enhanced_context = {}
            audience_insights = {}

        # Get agent personality
        agent = get_agent_personality(agent_id)

        # Extract performance context
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})

        # Build enhanced prompt for description generation
        description_prompt = f"""
        Create a compelling YouTube video description for:

        Title: {title}
        Content Pillar: {pillar}
        Keywords to include: {', '.join(keywords) if keywords else 'None specified'}

        CHANNEL CONTEXT:
        - Channel Size: {channel_context.get('subscriber_count', 'Growing')} subscribers
        - Audience Demographics: {audience_context.get('primary_age_group', 'General audience')}
        - Engagement Style: {audience_context.get('engagement_preferences', 'Standard engagement')}
        - Top Performing Content: {performance_context.get('successful_content_patterns', 'Varied content')}

        Requirements:
        1. First 125 characters should be compelling (visible in search)
        2. Include relevant keywords naturally
        3. Add clear value proposition tailored to {audience_context.get('primary_age_group', 'your audience')}
        4. Include call-to-action that matches your {audience_context.get('engagement_preferences', 'standard')} engagement style
        5. Add relevant hashtags at the end
        6. Keep it engaging and informative for {channel_context.get('subscriber_count', 'growing')} subscriber channel
        7. Optimize for YouTube SEO
        8. Use language complexity appropriate for your audience demographic
        
        Structure:
        - Hook/Value proposition (first 2 lines)
        - Content overview
        - Call to action
        - Relevant hashtags
        
        Agent Context: You are {agent['name']}, {agent['role']}. Write in your voice and expertise area.
        """
        
        # Call AI model
        result = await create_agent_call_to_integration(
            agent_type="boss_agent",
            use_case="content_generation",
            prompt_data={
                "prompt": description_prompt,
                "analysis_depth": "standard",
                "system_message": f"You are {agent['name']}, an expert at writing YouTube descriptions that drive engagement and discovery."
            }
        )
        
        if result.get("success"):
            description_content = result.get("content", "")
            
            return create_success_response(
                "Description generated successfully",
                {
                    "description": description_content,
                    "metadata": {
                        "title": title,
                        "pillar": pillar,
                        "agent": agent['name'],
                        "generated_at": datetime.utcnow().isoformat(),
                        "character_count": len(description_content)
                    }
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate description with AI")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in description generation: {e}")
        return create_error_response("Description generation failed", str(e))
