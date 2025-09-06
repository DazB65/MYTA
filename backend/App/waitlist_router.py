"""
Waitlist Router for MYTA
Handles waitlist form submissions and email management
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator
import httpx
import user_agents

from backend.App.supabase_client import get_supabase_service
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)

# Create router
router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])

class WaitlistSignup(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    youtube_channel_name: Optional[str] = None
    youtube_channel_url: Optional[str] = None
    subscriber_count: Optional[int] = None
    subscriber_range: Optional[str] = None
    content_niche: Optional[str] = None
    signup_source: str = "landing_page"
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    referral_code: Optional[str] = None

    @validator('subscriber_range')
    def validate_subscriber_range(cls, v):
        if v and v not in ['0-1k', '1k-10k', '10k-100k', '100k-1M', '1M+', 'prefer_not_to_say']:
            raise ValueError('Invalid subscriber range')
        return v

    @validator('youtube_channel_url')
    def validate_youtube_url(cls, v):
        if v and not (v.startswith('https://youtube.com/') or v.startswith('https://www.youtube.com/')):
            raise ValueError('Invalid YouTube URL format')
        return v

class WaitlistResponse(BaseModel):
    success: bool
    message: str
    waitlist_id: Optional[str] = None

def extract_device_info(user_agent_string: str) -> Dict[str, Any]:
    """Extract device and browser information from user agent"""
    try:
        ua = user_agents.parse(user_agent_string)
        return {
            "browser": {
                "family": ua.browser.family,
                "version": ua.browser.version_string
            },
            "os": {
                "family": ua.os.family,
                "version": ua.os.version_string
            },
            "device": {
                "family": ua.device.family,
                "brand": ua.device.brand,
                "model": ua.device.model
            },
            "is_mobile": ua.is_mobile,
            "is_tablet": ua.is_tablet,
            "is_pc": ua.is_pc,
            "is_bot": ua.is_bot
        }
    except Exception as e:
        logger.warning(f"Failed to parse user agent: {e}")
        return {"raw": user_agent_string}

async def get_location_data(ip_address: str) -> Dict[str, Any]:
    """Get location data from IP address using a free service"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{ip_address}")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return {
                        "country": data.get("country"),
                        "country_code": data.get("countryCode"),
                        "region": data.get("regionName"),
                        "city": data.get("city"),
                        "timezone": data.get("timezone"),
                        "lat": data.get("lat"),
                        "lon": data.get("lon")
                    }
    except Exception as e:
        logger.warning(f"Failed to get location data for IP {ip_address}: {e}")
    
    return {}

async def send_welcome_email(email: str, name: Optional[str], waitlist_id: str):
    """Send welcome email to new waitlist subscriber"""
    try:
        # This will be implemented when we set up Resend
        logger.info(f"Welcome email queued for {email} (waitlist_id: {waitlist_id})")
        
        # Update the waitlist record to mark welcome email as sent
        supabase = get_supabase_service()
        await supabase.update(
            "waitlist",
            {"welcome_email_sent": True, "welcome_email_sent_at": datetime.utcnow().isoformat()},
            f"id.eq.{waitlist_id}"
        )
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {e}")

@router.post("/signup", response_model=WaitlistResponse)
async def signup_for_waitlist(
    signup_data: WaitlistSignup,
    request: Request,
    background_tasks: BackgroundTasks
):
    """Handle waitlist signup form submission"""
    try:
        supabase = get_supabase_service()
        
        # Get client IP and user agent
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Extract device and browser info
        device_info = extract_device_info(user_agent)
        
        # Get location data in background
        location_data = await get_location_data(client_ip)
        
        # Prepare waitlist data
        waitlist_data = {
            "email": signup_data.email,
            "name": signup_data.name,
            "youtube_channel_name": signup_data.youtube_channel_name,
            "youtube_channel_url": signup_data.youtube_channel_url,
            "subscriber_count": signup_data.subscriber_count,
            "subscriber_range": signup_data.subscriber_range,
            "content_niche": signup_data.content_niche,
            "signup_source": signup_data.signup_source,
            "utm_source": signup_data.utm_source,
            "utm_medium": signup_data.utm_medium,
            "utm_campaign": signup_data.utm_campaign,
            "referral_code": signup_data.referral_code,
            "ip_address": client_ip,
            "user_agent": user_agent,
            "device_info": device_info,
            "location_data": location_data,
            "status": "active"
        }
        
        # Insert into database
        result = await supabase.insert("waitlist", waitlist_data)
        
        if result and len(result) > 0:
            waitlist_id = result[0]["id"]
            
            # Queue welcome email
            background_tasks.add_task(
                send_welcome_email,
                signup_data.email,
                signup_data.name,
                waitlist_id
            )
            
            logger.info(f"New waitlist signup: {signup_data.email} (ID: {waitlist_id})")
            
            return WaitlistResponse(
                success=True,
                message="Successfully joined the waitlist! Check your email for a welcome message.",
                waitlist_id=waitlist_id
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save waitlist signup")
            
    except Exception as e:
        if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
            logger.warning(f"Duplicate email signup attempt: {signup_data.email}")
            return WaitlistResponse(
                success=True,
                message="You're already on our waitlist! We'll keep you updated.",
                waitlist_id=None
            )
        else:
            logger.error(f"Error processing waitlist signup: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stats")
async def get_waitlist_stats():
    """Get basic waitlist statistics (for admin use)"""
    try:
        supabase = get_supabase_service()
        
        # Get total signups
        total_result = await supabase.select("waitlist", "id", count="exact")
        total_signups = total_result.get("count", 0) if total_result else 0
        
        # Get signups by source
        source_result = await supabase.select(
            "waitlist", 
            "signup_source, count(*)",
            group_by="signup_source"
        )
        
        # Get signups by niche
        niche_result = await supabase.select(
            "waitlist",
            "content_niche, count(*)",
            group_by="content_niche"
        )
        
        return {
            "total_signups": total_signups,
            "by_source": source_result or [],
            "by_niche": niche_result or []
        }
        
    except Exception as e:
        logger.error(f"Error getting waitlist stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")

@router.post("/unsubscribe/{waitlist_id}")
async def unsubscribe_from_waitlist(waitlist_id: str):
    """Handle unsubscribe requests"""
    try:
        supabase = get_supabase_service()
        
        result = await supabase.update(
            "waitlist",
            {
                "unsubscribed": True,
                "unsubscribed_at": datetime.utcnow().isoformat(),
                "status": "unsubscribed"
            },
            f"id.eq.{waitlist_id}"
        )
        
        if result:
            return {"success": True, "message": "Successfully unsubscribed"}
        else:
            raise HTTPException(status_code=404, detail="Waitlist entry not found")
            
    except Exception as e:
        logger.error(f"Error unsubscribing {waitlist_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to unsubscribe")
