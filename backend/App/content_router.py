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

# Helper functions for enhanced context
async def get_user_voice_profile(user_id: str, voice_analyzer, enhanced_context: Dict) -> Dict[str, Any]:
    """Get user's voice profile for content generation"""
    try:
        # Get channel content for voice analysis
        channel_content = enhanced_context.get('recent_content', [])
        channel_info = enhanced_context.get('channel_info', {})

        if channel_content:
            voice_profile = await voice_analyzer.analyze_channel_voice(channel_content, channel_info)
            return voice_profile
        else:
            # Return fallback voice profile
            return {
                "voice_characteristics": {
                    "tone": "Professional yet approachable",
                    "formality_level": "Semi-formal",
                    "personality": "Educational expert"
                },
                "writing_style": {
                    "sentence_structure": "Clear and concise",
                    "vocabulary_level": "Industry-specific, accessible",
                    "pacing": "Steady, methodical"
                }
            }
    except Exception as e:
        logger.warning(f"Could not get voice profile for user {user_id}: {e}")
        return {}

async def get_competitive_context(user_id: str, enhanced_context: Dict) -> Dict[str, Any]:
    """Get competitive insights for content differentiation"""
    try:
        # Extract competitive intelligence from enhanced context
        competitive_data = enhanced_context.get('competitive_intelligence', {})
        return {
            'market_gaps': competitive_data.get('content_gaps', []),
            'differentiation_opportunities': competitive_data.get('opportunities', []),
            'competitor_weaknesses': competitive_data.get('competitor_weaknesses', []),
            'trending_in_niche': competitive_data.get('trending_topics', [])
        }
    except Exception as e:
        logger.warning(f"Could not get competitive context for user {user_id}: {e}")
        return {}

async def get_trending_context(user_id: str, enhanced_context: Dict) -> Dict[str, Any]:
    """Get trending opportunities for content"""
    try:
        trending_data = enhanced_context.get('trending_opportunities', {})
        return {
            'hot_topics': trending_data.get('hot_topics', []),
            'emerging_trends': trending_data.get('emerging_trends', []),
            'seasonal_opportunities': trending_data.get('seasonal', []),
            'niche_trends': trending_data.get('niche_specific', [])
        }
    except Exception as e:
        logger.warning(f"Could not get trending context for user {user_id}: {e}")
        return {}

def get_agent_specialization_for_content(agent_id: str, content_type: str, pillar: str) -> Dict[str, Any]:
    """Get agent-specific specialization for content generation"""

    # Agent-specific content generation specializations
    specializations = {
        "1": {  # Alex - Analytics Team Member
            "focus": "Data-driven content optimization",
            "unique_approach": "Performance metrics and analytics-backed content strategy",
            "content_angle": "Measurable results and strategic insights",
            "special_elements": ["Performance data", "Metrics analysis", "ROI focus", "Strategic planning"],
            "tone_modifier": "Professional and data-backed"
        },
        "2": {  # Levi - Content Team Member
            "focus": "Creative storytelling and production excellence",
            "unique_approach": "Engaging narratives and visual storytelling techniques",
            "content_angle": "Creative execution and audience engagement",
            "special_elements": ["Storytelling hooks", "Visual techniques", "Creative formats", "Trend integration"],
            "tone_modifier": "Energetic and creative"
        },
        "3": {  # Maya - Engagement Team Member
            "focus": "Community building and authentic connections",
            "unique_approach": "Relationship-focused content that builds community",
            "content_angle": "Audience connection and community engagement",
            "special_elements": ["Community building", "Authentic connections", "Engagement strategies", "Relationship focus"],
            "tone_modifier": "Warm and community-focused"
        },
        "4": {  # Zara - Growth & Optimization Expert
            "focus": "Scalable growth and algorithm optimization",
            "unique_approach": "Growth-hacking techniques and systematic scaling",
            "content_angle": "Viral potential and growth optimization",
            "special_elements": ["Growth strategies", "Algorithm optimization", "Scaling techniques", "Viral elements"],
            "tone_modifier": "Strategic and growth-focused"
        },
        "5": {  # Kai - Technical & SEO Specialist
            "focus": "Technical optimization and discoverability",
            "unique_approach": "SEO-optimized content with technical precision",
            "content_angle": "Search optimization and technical excellence",
            "special_elements": ["SEO optimization", "Technical details", "Platform mechanics", "Discoverability"],
            "tone_modifier": "Technical and precise"
        }
    }

    return specializations.get(agent_id, specializations["1"])

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
        
        # Get agent personality and specialization for context
        agent = get_agent_personality(agent_id)
        agent_specialization = get_agent_specialization_for_content(agent_id, script_type, pillar)
        
        # Get enhanced user context for personalization
        user_id = current_user["id"]

        # Import enhanced context services
        try:
            from backend.App.enhanced_user_context import EnhancedUserContextService
            from backend.App.audience_insights_agent import AudienceInsightsAgent
            from backend.App.voice_analyzer import get_voice_analyzer
            from backend.App.competitive_analysis_agent import CompetitiveAnalysisAgent

            # Get enhanced user context with performance data
            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            # Get audience insights for personalization
            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

            # Get voice profile for style matching
            voice_analyzer = get_voice_analyzer()
            voice_profile = await get_user_voice_profile(user_id, voice_analyzer, enhanced_context)

            # Get competitive insights for differentiation
            competitive_insights = await get_competitive_context(user_id, enhanced_context)

            # Get trending opportunities
            trending_context = await get_trending_context(user_id, enhanced_context)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for user {user_id}: {e}")
            enhanced_context = {}
            audience_insights = {}
            voice_profile = {}
            competitive_insights = {}
            trending_context = {}

        # Build enhanced context for personalization
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})
        voice_characteristics = voice_profile.get('voice_characteristics', {})
        writing_style = voice_profile.get('writing_style', {})

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

        VOICE MATCHING PROFILE:
        - Tone: {voice_characteristics.get('tone', 'Professional yet approachable')}
        - Formality Level: {voice_characteristics.get('formality_level', 'Semi-formal')}
        - Personality: {voice_characteristics.get('personality', 'Educational expert')}
        - Sentence Structure: {writing_style.get('sentence_structure', 'Clear and concise')}
        - Vocabulary Level: {writing_style.get('vocabulary_level', 'Industry-specific, accessible')}
        - Pacing: {writing_style.get('pacing', 'Steady, methodical')}

        COMPETITIVE INTELLIGENCE:
        - Market Gaps: {competitive_insights.get('market_gaps', ['General opportunities'])}
        - Differentiation Opportunities: {competitive_insights.get('differentiation_opportunities', ['Unique perspective'])}
        - Trending in Niche: {trending_context.get('niche_trends', ['Current topics'])}
        - Hot Topics: {trending_context.get('hot_topics', ['Popular subjects'])}

        CRITICAL INSTRUCTION - BE SPECIFIC AND PERSONALIZED:
        This script must be HIGHLY SPECIFIC and ACTIONABLE, not generic. Use the content idea to create something unique that only an expert in {pillar} would know.

        PERSONALIZATION REQUIREMENTS:
        - Tailor content complexity to match your audience's engagement patterns
        - Use communication style that resonates with your {audience_context.get('primary_age_group', 'general')} audience
        - Reference performance patterns that work for your channel size ({channel_context.get('subscriber_count', 'growing')} subscribers)
        - Include hooks and techniques similar to your top-performing content

        VOICE MATCHING REQUIREMENTS:
        - Match your established tone: {voice_characteristics.get('tone', 'professional yet approachable')}
        - Use your typical formality level: {voice_characteristics.get('formality_level', 'semi-formal')}
        - Reflect your personality: {voice_characteristics.get('personality', 'educational expert')}
        - Follow your sentence structure patterns: {writing_style.get('sentence_structure', 'clear and concise')}
        - Use vocabulary at your level: {writing_style.get('vocabulary_level', 'industry-specific, accessible')}
        - Match your content pacing: {writing_style.get('pacing', 'steady, methodical')}

        COMPETITIVE DIFFERENTIATION:
        - Address market gaps: {competitive_insights.get('market_gaps', ['general opportunities'])}
        - Leverage differentiation opportunities: {competitive_insights.get('differentiation_opportunities', ['unique perspective'])}
        - Capitalize on trending topics: {trending_context.get('hot_topics', ['popular subjects'])}
        - Include niche-specific trends: {trending_context.get('niche_trends', ['current topics'])}

        AGENT SPECIALIZATION ({agent['name']} - {agent['role']}):
        - Unique Focus: {agent_specialization['focus']}
        - Specialized Approach: {agent_specialization['unique_approach']}
        - Content Angle: {agent_specialization['content_angle']}
        - Special Elements to Include: {agent_specialization['special_elements']}
        - Tone Modifier: {agent_specialization['tone_modifier']}

        REQUIRED SPECIFICITY:
        - Include specific tools, software, platforms, or apps used in {pillar}
        - Mention exact numbers, percentages, metrics, or benchmarks
        - Reference real examples, case studies, or scenarios from {pillar}
        - Use industry-specific terminology and jargon
        - Address specific problems that {pillar} practitioners face
        - Provide advanced techniques or insider knowledge
        - Include specific steps with exact actions to take

        AGENT SPECIALIZATION REQUIREMENTS:
        - Apply {agent['name']}'s unique expertise: {agent_specialization['focus']}
        - Use {agent['name']}'s specialized approach: {agent_specialization['unique_approach']}
        - Emphasize {agent['name']}'s content angle: {agent_specialization['content_angle']}
        - Include {agent['name']}'s special elements: {agent_specialization['special_elements']}
        - Maintain {agent['name']}'s tone: {agent_specialization['tone_modifier']}

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
            from backend.App.voice_analyzer import get_voice_analyzer

            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

            # Get voice profile for style matching
            voice_analyzer = get_voice_analyzer()
            voice_profile = await get_user_voice_profile(user_id, voice_analyzer, enhanced_context)

            # Get competitive and trending insights
            competitive_insights = await get_competitive_context(user_id, enhanced_context)
            trending_context = await get_trending_context(user_id, enhanced_context)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for title generation: {e}")
            enhanced_context = {}
            audience_insights = {}
            voice_profile = {}
            competitive_insights = {}
            trending_context = {}

        # Get agent personality and specialization
        agent = get_agent_personality(agent_id)
        agent_specialization = get_agent_specialization_for_content(agent_id, "title", pillar)

        # Extract performance context
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})
        voice_characteristics = voice_profile.get('voice_characteristics', {})
        writing_style = voice_profile.get('writing_style', {})

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

        VOICE MATCHING PROFILE:
        - Channel Tone: {voice_characteristics.get('tone', 'Professional yet approachable')}
        - Formality Level: {voice_characteristics.get('formality_level', 'Semi-formal')}
        - Personality: {voice_characteristics.get('personality', 'Educational expert')}
        - Vocabulary Style: {writing_style.get('vocabulary_level', 'Industry-specific, accessible')}

        COMPETITIVE INTELLIGENCE:
        - Market Gaps: {competitive_insights.get('market_gaps', ['General opportunities'])}
        - Trending Topics: {trending_context.get('hot_topics', ['Popular subjects'])}
        - Niche Trends: {trending_context.get('niche_trends', ['Current topics'])}
        - Differentiation Opportunities: {competitive_insights.get('differentiation_opportunities', ['Unique perspective'])}

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
        10. Match your channel's tone: {voice_characteristics.get('tone', 'professional yet approachable')}
        11. Use your typical formality level: {voice_characteristics.get('formality_level', 'semi-formal')}
        12. Incorporate trending topics: {trending_context.get('hot_topics', ['popular subjects'])}
        13. Address market gaps: {competitive_insights.get('market_gaps', ['general opportunities'])}
        14. Apply {agent['name']}'s expertise: {agent_specialization['focus']}
        15. Use {agent['name']}'s approach: {agent_specialization['content_angle']}
        16. Include {agent['name']}'s special elements: {agent_specialization['special_elements']}

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
            from backend.App.voice_analyzer import get_voice_analyzer

            context_service = EnhancedUserContextService()
            enhanced_context = await context_service.get_enhanced_context(user_id)

            audience_agent = AudienceInsightsAgent()
            audience_insights = await audience_agent.get_audience_context_for_content(user_id)

            # Get voice profile for style matching
            voice_analyzer = get_voice_analyzer()
            voice_profile = await get_user_voice_profile(user_id, voice_analyzer, enhanced_context)

            # Get competitive and trending insights
            competitive_insights = await get_competitive_context(user_id, enhanced_context)
            trending_context = await get_trending_context(user_id, enhanced_context)

        except Exception as e:
            logger.warning(f"Could not fetch enhanced context for description generation: {e}")
            enhanced_context = {}
            audience_insights = {}
            voice_profile = {}
            competitive_insights = {}
            trending_context = {}

        # Get agent personality and specialization
        agent = get_agent_personality(agent_id)
        agent_specialization = get_agent_specialization_for_content(agent_id, "description", pillar)

        # Extract performance context
        performance_context = enhanced_context.get('performance_intelligence', {})
        channel_context = enhanced_context.get('channel_info', {})
        audience_context = audience_insights.get('demographics', {})
        voice_characteristics = voice_profile.get('voice_characteristics', {})
        writing_style = voice_profile.get('writing_style', {})

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

        VOICE MATCHING PROFILE:
        - Channel Tone: {voice_characteristics.get('tone', 'Professional yet approachable')}
        - Formality Level: {voice_characteristics.get('formality_level', 'Semi-formal')}
        - Personality: {voice_characteristics.get('personality', 'Educational expert')}
        - Writing Style: {writing_style.get('sentence_structure', 'Clear and concise')}
        - Vocabulary Level: {writing_style.get('vocabulary_level', 'Industry-specific, accessible')}

        COMPETITIVE INTELLIGENCE:
        - Market Gaps: {competitive_insights.get('market_gaps', ['General opportunities'])}
        - Trending Topics: {trending_context.get('hot_topics', ['Popular subjects'])}
        - Differentiation Opportunities: {competitive_insights.get('differentiation_opportunities', ['Unique perspective'])}

        Requirements:
        1. First 125 characters should be compelling (visible in search)
        2. Include relevant keywords naturally
        3. Add clear value proposition tailored to {audience_context.get('primary_age_group', 'your audience')}
        4. Include call-to-action that matches your {audience_context.get('engagement_preferences', 'standard')} engagement style
        5. Add relevant hashtags at the end
        6. Keep it engaging and informative for {channel_context.get('subscriber_count', 'growing')} subscriber channel
        7. Optimize for YouTube SEO
        8. Use language complexity appropriate for your audience demographic
        9. Match your channel's tone: {voice_characteristics.get('tone', 'professional yet approachable')}
        10. Use your typical formality level: {voice_characteristics.get('formality_level', 'semi-formal')}
        11. Write in your established personality: {voice_characteristics.get('personality', 'educational expert')}
        12. Follow your sentence structure patterns: {writing_style.get('sentence_structure', 'clear and concise')}
        13. Incorporate trending elements: {trending_context.get('hot_topics', ['popular subjects'])}
        14. Address market gaps: {competitive_insights.get('market_gaps', ['general opportunities'])}
        15. Apply {agent['name']}'s expertise: {agent_specialization['focus']}
        16. Use {agent['name']}'s specialized approach: {agent_specialization['unique_approach']}
        17. Emphasize {agent['name']}'s content angle: {agent_specialization['content_angle']}
        
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
