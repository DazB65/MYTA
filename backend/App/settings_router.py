"""
Settings Router for MYTA
Handles user settings and agent preferences with Supabase integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import uuid

from backend.App.supabase_client import get_supabase_service
from backend.App.auth_middleware import get_current_user
from backend.App.response_utils import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/settings", tags=["settings"])

# Default agent configurations
AGENT_CONFIGS = {
    "1": {"name": "Alex", "color": "blue", "expertise": "Analytics & Strategy"},
    "2": {"name": "Levi", "color": "yellow", "expertise": "Content Creation"},
    "3": {"name": "Maya", "color": "green", "expertise": "Audience Engagement"},
    "4": {"name": "Zara", "color": "purple", "expertise": "Growth & Optimization"},
    "5": {"name": "Kai", "color": "red", "expertise": "Technical & SEO"}
}

@router.get("/")
async def get_user_settings(current_user: Dict = Depends(get_current_user)):
    """Get all user settings"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get user settings
        result = supabase.select("user_settings", "*", {"user_id": user_id})
        
        if result["success"] and result["data"]:
            settings = result["data"][0]
            
            # Add agent configuration details
            agent_id = settings.get("selected_agent_id", "1")
            settings["agent_config"] = AGENT_CONFIGS.get(agent_id, AGENT_CONFIGS["1"])
            
            return create_success_response("User settings retrieved successfully", {"settings": settings})
        elif result["success"]:
            # Create default settings if none exist
            default_settings = await create_default_settings(user_id)
            return create_success_response("Default settings created", {"settings": default_settings})
        else:
            return create_error_response("Failed to retrieve user settings", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting user settings: {e}")
        return create_error_response("Failed to retrieve user settings", str(e))

@router.put("/")
async def update_user_settings(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update user settings"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Prepare update data
        update_data = {}
        
        # Validate and update specific fields
        if "selected_agent_id" in body:
            agent_id = str(body["selected_agent_id"])
            if agent_id in AGENT_CONFIGS:
                update_data["selected_agent_id"] = agent_id
        
        if "agent_name" in body:
            agent_name = body["agent_name"].strip()
            if agent_name:
                update_data["agent_name"] = agent_name
        
        if "theme" in body:
            if body["theme"] in ["light", "dark", "auto"]:
                update_data["theme"] = body["theme"]
        
        if "language" in body:
            update_data["language"] = body["language"]
        
        if "timezone" in body:
            update_data["timezone"] = body["timezone"]
        
        if "notifications" in body:
            update_data["notifications"] = body["notifications"]
        
        if "dashboard_layout" in body:
            update_data["dashboard_layout"] = body["dashboard_layout"]
        
        if "agent_preferences" in body:
            update_data["agent_preferences"] = body["agent_preferences"]
        
        if "privacy_settings" in body:
            update_data["privacy_settings"] = body["privacy_settings"]
        
        if "metadata" in body:
            update_data["metadata"] = body["metadata"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        supabase = get_supabase_service()
        
        # Check if settings exist
        existing = supabase.select("user_settings", "*", {"user_id": user_id})
        
        if existing["success"] and existing["data"]:
            # Update existing settings
            result = supabase.update("user_settings", update_data, {"user_id": user_id})
        else:
            # Create new settings with defaults
            default_settings = get_default_settings(user_id)
            default_settings.update(update_data)
            result = supabase.insert("user_settings", default_settings)
        
        if result["success"] and result["data"]:
            settings = result["data"][0]
            
            # Add agent configuration details
            agent_id = settings.get("selected_agent_id", "1")
            settings["agent_config"] = AGENT_CONFIGS.get(agent_id, AGENT_CONFIGS["1"])
            
            return create_success_response("Settings updated successfully", {"settings": settings})
        else:
            return create_error_response("Failed to update settings", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user settings: {e}")
        return create_error_response("Failed to update user settings", str(e))

@router.get("/agent")
async def get_agent_settings(current_user: Dict = Depends(get_current_user)):
    """Get agent-specific settings"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.select("user_settings", "selected_agent_id, agent_name, agent_preferences", {"user_id": user_id})
        
        if result["success"] and result["data"]:
            settings = result["data"][0]
            agent_id = settings.get("selected_agent_id", "1")
            
            agent_settings = {
                "selected_agent_id": agent_id,
                "agent_name": settings.get("agent_name", "My Agent"),
                "agent_preferences": settings.get("agent_preferences", {}),
                "agent_config": AGENT_CONFIGS.get(agent_id, AGENT_CONFIGS["1"]),
                "available_agents": AGENT_CONFIGS
            }
            
            return create_success_response("Agent settings retrieved successfully", {"agent_settings": agent_settings})
        else:
            # Return defaults if no settings exist
            default_agent_settings = {
                "selected_agent_id": "1",
                "agent_name": "My Agent",
                "agent_preferences": {
                    "voice_enabled": False,
                    "auto_suggestions": True,
                    "response_style": "balanced",
                    "expertise_level": "intermediate"
                },
                "agent_config": AGENT_CONFIGS["1"],
                "available_agents": AGENT_CONFIGS
            }
            
            return create_success_response("Default agent settings", {"agent_settings": default_agent_settings})
            
    except Exception as e:
        logger.error(f"Error getting agent settings: {e}")
        return create_error_response("Failed to retrieve agent settings", str(e))

@router.put("/agent")
async def update_agent_settings(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update agent-specific settings"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        update_data = {}
        
        if "selected_agent_id" in body:
            agent_id = str(body["selected_agent_id"])
            if agent_id in AGENT_CONFIGS:
                update_data["selected_agent_id"] = agent_id
        
        if "agent_name" in body:
            agent_name = body["agent_name"].strip()
            if agent_name:
                update_data["agent_name"] = agent_name
        
        if "agent_preferences" in body:
            update_data["agent_preferences"] = body["agent_preferences"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid agent fields to update")
        
        supabase = get_supabase_service()
        
        # Check if settings exist
        existing = supabase.select("user_settings", "*", {"user_id": user_id})
        
        if existing["success"] and existing["data"]:
            # Update existing settings
            result = supabase.update("user_settings", update_data, {"user_id": user_id})
        else:
            # Create new settings with defaults
            default_settings = get_default_settings(user_id)
            default_settings.update(update_data)
            result = supabase.insert("user_settings", default_settings)
        
        if result["success"] and result["data"]:
            settings = result["data"][0]
            agent_id = settings.get("selected_agent_id", "1")
            
            agent_settings = {
                "selected_agent_id": agent_id,
                "agent_name": settings.get("agent_name", "My Agent"),
                "agent_preferences": settings.get("agent_preferences", {}),
                "agent_config": AGENT_CONFIGS.get(agent_id, AGENT_CONFIGS["1"])
            }
            
            return create_success_response("Agent settings updated successfully", {"agent_settings": agent_settings})
        else:
            return create_error_response("Failed to update agent settings", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent settings: {e}")
        return create_error_response("Failed to update agent settings", str(e))

@router.get("/notifications")
async def get_notification_settings(current_user: Dict = Depends(get_current_user)):
    """Get notification preferences"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.select("user_settings", "notifications", {"user_id": user_id})
        
        if result["success"] and result["data"]:
            notifications = result["data"][0].get("notifications", {})
        else:
            notifications = {
                "email": True,
                "push": True,
                "marketing": False,
                "updates": True
            }
        
        return create_success_response("Notification settings retrieved", {"notifications": notifications})
        
    except Exception as e:
        logger.error(f"Error getting notification settings: {e}")
        return create_error_response("Failed to retrieve notification settings", str(e))

@router.put("/notifications")
async def update_notification_settings(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update notification preferences"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        notifications = body.get("notifications", {})
        if not notifications:
            raise HTTPException(status_code=400, detail="Notifications object is required")
        
        update_data = {"notifications": notifications}
        
        supabase = get_supabase_service()
        
        # Check if settings exist
        existing = supabase.select("user_settings", "*", {"user_id": user_id})
        
        if existing["success"] and existing["data"]:
            result = supabase.update("user_settings", update_data, {"user_id": user_id})
        else:
            default_settings = get_default_settings(user_id)
            default_settings.update(update_data)
            result = supabase.insert("user_settings", default_settings)
        
        if result["success"]:
            return create_success_response("Notification settings updated successfully", {"notifications": notifications})
        else:
            return create_error_response("Failed to update notification settings", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating notification settings: {e}")
        return create_error_response("Failed to update notification settings", str(e))

@router.delete("/")
async def reset_user_settings(current_user: Dict = Depends(get_current_user)):
    """Reset user settings to defaults"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Delete existing settings
        supabase.delete("user_settings", {"user_id": user_id})
        
        # Create default settings
        default_settings = await create_default_settings(user_id)
        
        return create_success_response("Settings reset to defaults", {"settings": default_settings})
        
    except Exception as e:
        logger.error(f"Error resetting user settings: {e}")
        return create_error_response("Failed to reset user settings", str(e))

def get_default_settings(user_id: str) -> Dict[str, Any]:
    """Get default settings for a user"""
    return {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "selected_agent_id": "1",
        "agent_name": "My Agent",
        "theme": "dark",
        "language": "en",
        "timezone": "UTC",
        "notifications": {
            "email": True,
            "push": True,
            "marketing": False,
            "updates": True
        },
        "dashboard_layout": {
            "sidebar_collapsed": False,
            "widget_order": ["stats", "tasks", "goals", "notes"],
            "default_view": "dashboard"
        },
        "agent_preferences": {
            "voice_enabled": False,
            "auto_suggestions": True,
            "response_style": "balanced",
            "expertise_level": "intermediate"
        },
        "privacy_settings": {
            "analytics_tracking": True,
            "data_sharing": False,
            "public_profile": False
        },
        "metadata": {}
    }

async def create_default_settings(user_id: str) -> Dict[str, Any]:
    """Create default settings for a user"""
    supabase = get_supabase_service()
    default_settings = get_default_settings(user_id)
    
    result = supabase.insert("user_settings", default_settings)
    
    if result["success"] and result["data"]:
        settings = result["data"][0]
        agent_id = settings.get("selected_agent_id", "1")
        settings["agent_config"] = AGENT_CONFIGS.get(agent_id, AGENT_CONFIGS["1"])
        return settings
    else:
        # Return defaults even if insert fails
        default_settings["agent_config"] = AGENT_CONFIGS["1"]
        return default_settings
