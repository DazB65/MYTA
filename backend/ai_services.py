import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict
import json

# Load environment variables
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Simple in-memory context store
# In a production app, you'd use a database
context_store = {}

def get_user_context(user_id: str) -> Dict:
    """Get context for a specific user"""
    if user_id not in context_store:
        # Initialize with default context
        context_store[user_id] = {
            "conversation_history": [],
            "channel_info": {
                "name": "Unknown",
                "niche": "Unknown",
                "subscriber_count": 0,
                "avg_view_count": 0,
                "content_type": "Unknown",
                "ctr": 0,
                "retention": 0,
                "upload_frequency": "Unknown",
                "video_length": "Unknown",
                "monetization_status": "Unknown",
                "primary_goal": "Unknown",
                "notes": ""
            }
        }
    return context_store[user_id]

def update_user_context(user_id: str, key: str, value):
    """Update a specific part of user context"""
    if user_id not in context_store:
        get_user_context(user_id)
    
    if key == "channel_info":
        context_store[user_id]["channel_info"].update(value)
    else:
        context_store[user_id][key] = value
    
    return context_store[user_id]

def add_to_conversation_history(user_id: str, role: str, content: str):
    """Add a message to the conversation history"""
    if user_id not in context_store:
        get_user_context(user_id)
    
    # Keep only the last 10 messages to avoid token limits
    if len(context_store[user_id]["conversation_history"]) >= 10:
        context_store[user_id]["conversation_history"] = context_store[user_id]["conversation_history"][-9:]
    
    context_store[user_id]["conversation_history"].append({"role": role, "content": content})

def create_messages_with_context(user_id: str, user_message: str) -> List[Dict]:
    """Create a messages array with system prompt and conversation history"""
    context = get_user_context(user_id)
    
    # Extract channel info for the context
    ch = context["channel_info"]
    
    # Create a detailed system prompt with context
    system_prompt = f"""
    You are CreatorMate, an expert AI assistant for YouTube content creators.
    
    Creator's channel information:
    - Channel Name: {ch['name']}
    - Niche: {ch['niche']}
    - Content Type: {ch['content_type']}
    - Subscribers: {ch['subscriber_count']}
    - Average Views: {ch['avg_view_count']}
    - CTR: {ch['ctr']}%
    - Retention: {ch['retention']}%
    - Upload Frequency: {ch['upload_frequency']}
    - Average Video Length: {ch['video_length']}
    - Monetization Status: {ch['monetization_status']}
    - Primary Goal: {ch['primary_goal']}
    - Additional Notes: {ch['notes']}
    
    Your expertise includes:
    - Content strategy and optimization for YouTube algorithms
    - Title and thumbnail optimization for higher CTR
    - Audience retention techniques and hook creation
    - SEO and keyword research for YouTube
    - Script writing and content structure
    - Channel growth strategies specific to the creator's niche
    - Monetization tactics appropriate for their subscriber level
    - Trending topic identification in their content category
    
    Provide specific, actionable advice backed by current best practices.
    Be direct and fact-based, avoiding vague suggestions.
    Focus on concrete strategies creators can implement immediately.
    When appropriate, structure your advice in clear, numbered steps.
    
    Tailor your advice to their specific niche, subscriber level, and stated goals.
    Consider their current metrics (CTR, retention, etc.) when suggesting improvements.
    """
    
    # Create messages array starting with system prompt
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    messages.extend(context["conversation_history"])
    
    # Add the current user message
    messages.append({"role": "user", "content": user_message})
    
    return messages

async def get_ai_response(user_message: str, user_id: str = "default_user"):
    """
    Get a response from the OpenAI service with context
    
    Args:
        user_message: The message from the user
        user_id: Identifier for the user (to maintain context)
        
    Returns:
        str: The AI's response
    """
    try:
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

# Function to extract channel info from user message
def extract_channel_info(user_id: str, message: str):
    """
    Attempt to extract channel information from user messages
    """
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
    def extract_channel_info(user_id: str, message: str) -> dict:
        """Extract channel information from user message - wrapper for existing functionality"""
        context = get_user_context(user_id)
        # Your existing code already handles channel info extraction in create_messages_with_context
        # This is just a wrapper to match main.py's expected function name
        context["channel_info"]["last_message"] = message
        return context["channel_info"]     