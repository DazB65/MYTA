import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import json
from database import db_manager

# Load environment variables from .env file (overriding system env vars for security)
from dotenv import dotenv_values
env_vars = dotenv_values()

# Get API key from .env file first, fallback to system env if not found
api_key = env_vars.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def get_user_context(user_id: str) -> Dict:
    """Get context for a specific user from database"""
    return db_manager.get_user_context(user_id)

def update_user_context(user_id: str, key: str, value):
    """Update a specific part of user context in database"""
    if key == "channel_info":
        return db_manager.update_channel_info(user_id, value)
    else:
        # For other context updates, we'll handle them as needed
        # For now, just return the current context
        return get_user_context(user_id)

def add_to_conversation_history(user_id: str, role: str, content: str):
    """Add a message to the conversation history in database"""
    return db_manager.add_conversation_message(user_id, role, content)

def create_messages_with_context(user_id: str, user_message: str) -> List[Dict]:
    """Create a messages array with system prompt and conversation history"""
    context = get_user_context(user_id)
    
    # Extract channel info for the context
    ch = context["channel_info"]
    
    # Calculate channel insights for more specific advice
    subscriber_tier = "new" if ch['subscriber_count'] < 1000 else "growing" if ch['subscriber_count'] < 10000 else "established" if ch['subscriber_count'] < 100000 else "large"
    ctr_performance = "low" if ch['ctr'] < 3 else "average" if ch['ctr'] < 6 else "good" if ch['ctr'] < 10 else "excellent"
    retention_performance = "low" if ch['retention'] < 30 else "average" if ch['retention'] < 50 else "good" if ch['retention'] < 70 else "excellent"
    
    # Create a detailed system prompt with context
    system_prompt = f"""
    You are Vidalytics, an expert AI assistant specifically for {ch['name']}, a {ch['niche']} YouTube channel.
    
    CRITICAL: Always provide advice SPECIFICALLY for this channel's situation. Never give generic YouTube advice.
    
    === {ch['name'].upper()} CHANNEL PROFILE ===
    🎯 Niche: {ch['niche']} (tailor ALL advice to this niche specifically)
    📺 Content Type: {ch['content_type']}
    👥 Subscriber Tier: {subscriber_tier.title()} ({ch['subscriber_count']:,} subscribers)
    👀 Average Views: {ch['avg_view_count']:,} per video
    📊 CTR Performance: {ctr_performance.title()} ({ch['ctr']}% - industry average for {ch['niche']} is 3-5%)
    ⏱️ Retention Performance: {retention_performance.title()} ({ch['retention']}% - good {ch['niche']} channels retain 40-60%)
    📅 Upload Schedule: {ch['upload_frequency']}
    ⏰ Video Length: {ch['video_length']} (analyze if optimal for {ch['niche']})
    💰 Monetization: {ch['monetization_status']}
    🎯 Primary Goal: {ch['primary_goal']}
    📝 Channel Notes: {ch['notes']}
    
    === YOUR MISSION ===
    Provide hyper-specific advice for {ch['name']} in the {ch['niche']} niche at the {subscriber_tier} level.
    
    ALWAYS consider:
    ✅ Their {ch['niche']} audience expectations and preferences
    ✅ Strategies that work specifically for {subscriber_tier} channels ({ch['subscriber_count']:,} subs)
    ✅ How to improve their {ctr_performance} CTR from {ch['ctr']}%
    ✅ How to boost their {retention_performance} retention from {ch['retention']}%
    ✅ Content ideas trending in {ch['niche']} right now
    ✅ Monetization strategies appropriate for {ch['subscriber_count']:,} subscribers
    ✅ Competition analysis within the {ch['niche']} space
    ✅ Their stated goal: {ch['primary_goal']}
    
    RESPONSE STYLE:
    🎯 Start responses with their channel name when relevant
    📊 Reference their specific metrics when giving advice
    🎬 Suggest {ch['niche']}-specific content ideas, not generic ones
    📈 Give concrete numbers and benchmarks for their tier
    🔥 Mention competitors or trends in their {ch['niche']} when helpful
    ⚡ Prioritize advice that addresses their weakest metrics first
    
    NEVER give generic advice. Always make it specific to {ch['name']}'s situation in {ch['niche']}.
    """
    
    # Create messages array starting with system prompt
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    messages.extend(context["conversation_history"])
    
    # Add the current user message
    messages.append({"role": "user", "content": user_message})
    
    return messages

async def get_ai_response(user_message: str, user_id: str = "default_user", skip_quick_action: bool = False):
    """
    Get a response from the OpenAI service with context
    
    Args:
        user_message: The message from the user
        user_id: Identifier for the user (to maintain context)
        skip_quick_action: Skip quick action detection to prevent recursion
        
    Returns:
        str: The AI's response
    """
    try:
        # Check if this is a quick action request (only if not skipping)
        if not skip_quick_action:
            quick_action = detect_quick_action(user_message)
            if quick_action:
                # Route to quick action handler
                from main import quick_action as handle_quick_action
                from pydantic.v1 import BaseModel
                
                class QuickActionRequest(BaseModel):
                    action: str
                    user_id: str = "default_user"
                    context: str = ""
                
                request = QuickActionRequest(action=quick_action, user_id=user_id, context=user_message)
                result = await handle_quick_action(request)
                if result and result.get('response'):
                    # Store the conversation in history
                    add_to_conversation_history(user_id, "user", user_message)
                    add_to_conversation_history(user_id, "assistant", result['response'])
                    return result['response']
        
        # Create messages with context
        messages = create_messages_with_context(user_id, user_message)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        # Get the response content
        ai_response = response.choices[0].message.content
        
        # Store the conversation in history
        add_to_conversation_history(user_id, "user", user_message)
        add_to_conversation_history(user_id, "assistant", ai_response)
        
        return ai_response
    except Exception as e:
        print(f"Error calling OpenAI service: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

def detect_quick_action(message: str) -> str:
    """Detect if a user message is requesting a quick action"""
    message_lower = message.lower()
    
    # Script generation keywords
    if any(word in message_lower for word in ['generate script', 'create script', 'write script', 'script for', 'video script']):
        return 'generate_script'
    
    # Hook improvement keywords  
    if any(word in message_lower for word in ['improve hook', 'better hook', 'hook ideas', 'opening hook', 'video hook']):
        return 'improve_hooks'
    
    # Title optimization keywords
    if any(word in message_lower for word in ['optimize title', 'better title', 'title ideas', 'improve title', 'title optimization']):
        return 'optimize_title'
    
    # Video ideas keywords
    if any(word in message_lower for word in ['video ideas', 'content ideas', 'what should i make', 'video suggestions', 'content suggestions']):
        return 'get_ideas'
    
    return None

# This function is now defined properly below after line 185

def extract_channel_info(user_id: str, message: str) -> dict:
    """Extract channel information from user message and update context"""
    try:
        # Simple keyword extraction - in a real app, you'd use more sophisticated NLP
        if "niche" in message.lower() or "category" in message.lower():
            # Look for common niches
            niches = ["gaming", "tech", "beauty", "fitness", "education", "finance", 
                     "cooking", "travel", "vlog", "review", "tutorial"]
            for niche in niches:
                if niche in message.lower():
                    update_user_context(user_id, "channel_info", {"niche": niche})
        
        # Extract subscriber count
        if "subscriber" in message.lower() or "sub" in message.lower():
            import re
            sub_matches = re.findall(r'(\d+)[k]?\s*(?:subscriber|sub)', message.lower())
            if sub_matches:
                count = int(sub_matches[0])
                if 'k' in message.lower():
                    count *= 1000
                update_user_context(user_id, "channel_info", {"subscriber_count": count})
        
        # Extract content type
        content_types = ["tutorial", "vlog", "review", "gameplay", "reaction", "commentary", "educational"]
        for content_type in content_types:
            if content_type in message.lower():
                update_user_context(user_id, "channel_info", {"content_type": content_type})
        
        # Get updated context
        context = get_user_context(user_id)
        context["channel_info"]["last_message"] = message
        return context["channel_info"]
    
    except Exception as e:
        print(f"Error extracting channel info: {e}")
        # Return current context even if extraction fails
        context = get_user_context(user_id)
        return context["channel_info"]     