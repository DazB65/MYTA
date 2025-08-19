"""
Subscription Router for MYTA
Handles subscription management, billing, and LemonSqueezy integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from backend.App.lemonsqueezy_service import get_lemonsqueezy_service
from backend.App.auth_middleware import get_current_user
from backend.App.response_utils import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/subscription", tags=["subscription"])

@router.get("/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        # This would typically fetch from your Supabase subscription_plans table
        # For now, return mock data that matches your frontend
        plans = [
            {
                "id": "free",
                "name": "Free Plan",
                "price_monthly": 0,
                "price_yearly": 0,
                "features": [
                    "5 AI requests per day",
                    "1 video analysis per week", 
                    "Basic analytics",
                    "Community support"
                ],
                "limits": {
                    "ai_requests": 150,
                    "video_analysis": 4
                }
            },
            {
                "id": "pro",
                "name": "Pro Plan",
                "price_monthly": 2999,  # $29.99
                "price_yearly": 29999,  # $299.99
                "features": [
                    "Unlimited AI requests",
                    "Unlimited video analysis",
                    "Advanced analytics",
                    "Priority support",
                    "Custom agents",
                    "Export capabilities"
                ],
                "limits": {
                    "ai_requests": -1,  # unlimited
                    "video_analysis": -1
                }
            }
        ]
        
        return create_success_response("Subscription plans retrieved", {"plans": plans})
        
    except Exception as e:
        logger.error(f"Error getting subscription plans: {e}")
        return create_error_response("Failed to get subscription plans", str(e))

@router.get("/current")
async def get_current_subscription(current_user: Dict = Depends(get_current_user)):
    """Get current user's subscription details"""
    try:
        user_id = current_user["id"]
        
        # TODO: Query Supabase for user's current subscription
        # For now, return mock data
        subscription = {
            "id": "free",
            "name": "Free Plan",
            "status": "active",
            "current_period_start": "2024-01-01T00:00:00Z",
            "current_period_end": "2024-02-01T00:00:00Z",
            "cancel_at_period_end": False
        }
        
        return create_success_response("Current subscription retrieved", {"subscription": subscription})
        
    except Exception as e:
        logger.error(f"Error getting current subscription: {e}")
        return create_error_response("Failed to get current subscription", str(e))

@router.get("/usage")
async def get_usage_stats(current_user: Dict = Depends(get_current_user)):
    """Get current user's usage statistics"""
    try:
        user_id = current_user["id"]
        
        # TODO: Query Supabase usage_tracking table
        # For now, return mock data
        usage = {
            "ai_requests": 47,
            "video_analysis": 2,
            "period_start": "2024-01-01T00:00:00Z",
            "period_end": "2024-02-01T00:00:00Z"
        }
        
        return create_success_response("Usage statistics retrieved", {"usage": usage})
        
    except Exception as e:
        logger.error(f"Error getting usage stats: {e}")
        return create_error_response("Failed to get usage statistics", str(e))

@router.post("/checkout")
async def create_checkout_session(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a checkout session for subscription upgrade"""
    try:
        body = await request.json()
        plan_id = body.get("plan_id")
        billing_cycle = body.get("billing_cycle", "monthly")  # monthly or yearly
        
        if not plan_id:
            raise HTTPException(status_code=400, detail="Plan ID is required")
        
        lemonsqueezy = get_lemonsqueezy_service()
        user_email = current_user.get("email", "user@example.com")
        
        # TODO: Map plan_id to LemonSqueezy variant_id
        # For now, use a placeholder
        variant_id = "your_variant_id_here"
        
        custom_data = {
            "user_id": current_user["id"],
            "plan_id": plan_id,
            "billing_cycle": billing_cycle
        }
        
        result = lemonsqueezy.create_checkout_url(
            variant_id=variant_id,
            user_email=user_email,
            custom_data=custom_data
        )
        
        if result["success"]:
            return create_success_response(
                "Checkout session created",
                {
                    "checkout_url": result["checkout_url"],
                    "checkout_id": result["checkout_id"]
                }
            )
        else:
            return create_error_response("Failed to create checkout session", result["error"])
            
    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        return create_error_response("Failed to create checkout session", str(e))

@router.post("/cancel")
async def cancel_subscription(current_user: Dict = Depends(get_current_user)):
    """Cancel user's current subscription"""
    try:
        user_id = current_user["id"]
        
        # TODO: Get user's LemonSqueezy subscription ID from Supabase
        # TODO: Call LemonSqueezy API to cancel subscription
        # TODO: Update subscription status in Supabase
        
        return create_success_response("Subscription cancelled successfully")
        
    except Exception as e:
        logger.error(f"Error cancelling subscription: {e}")
        return create_error_response("Failed to cancel subscription", str(e))

@router.get("/billing-history")
async def get_billing_history(current_user: Dict = Depends(get_current_user)):
    """Get user's billing history"""
    try:
        user_id = current_user["id"]
        
        # TODO: Query Supabase billing_history table
        # For now, return mock data
        history = [
            {
                "id": "1",
                "description": "MYTA Pro Plan - January 2024",
                "amount": 2999,
                "currency": "USD",
                "status": "paid",
                "created_at": "2024-01-15T00:00:00Z",
                "invoice_url": "https://example.com/invoice/1"
            }
        ]
        
        return create_success_response("Billing history retrieved", {"history": history})
        
    except Exception as e:
        logger.error(f"Error getting billing history: {e}")
        return create_error_response("Failed to get billing history", str(e))

@router.post("/webhook")
async def handle_lemonsqueezy_webhook(
    request: Request,
    x_signature: str = Header(None, alias="X-Signature")
):
    """Handle LemonSqueezy webhooks"""
    try:
        payload = await request.body()
        
        lemonsqueezy = get_lemonsqueezy_service()
        
        # Verify webhook signature
        if not lemonsqueezy.verify_webhook_signature(payload, x_signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Parse webhook data
        webhook_data = json.loads(payload.decode('utf-8'))
        event_name = webhook_data.get('meta', {}).get('event_name')
        
        logger.info(f"Received LemonSqueezy webhook: {event_name}")
        
        # Handle different webhook events
        if event_name == 'subscription_created':
            await handle_subscription_created(webhook_data)
        elif event_name == 'subscription_updated':
            await handle_subscription_updated(webhook_data)
        elif event_name == 'subscription_cancelled':
            await handle_subscription_cancelled(webhook_data)
        elif event_name == 'order_created':
            await handle_order_created(webhook_data)
        
        return JSONResponse(content={"status": "success"})
        
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

async def handle_subscription_created(webhook_data: Dict):
    """Handle subscription created webhook"""
    # TODO: Create subscription record in Supabase
    pass

async def handle_subscription_updated(webhook_data: Dict):
    """Handle subscription updated webhook"""
    # TODO: Update subscription record in Supabase
    pass

async def handle_subscription_cancelled(webhook_data: Dict):
    """Handle subscription cancelled webhook"""
    # TODO: Update subscription status in Supabase
    pass

async def handle_order_created(webhook_data: Dict):
    """Handle order created webhook"""
    # TODO: Create billing history record in Supabase
    pass
