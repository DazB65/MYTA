"""
Subscription Router for MYTA
Handles subscription management, billing, and LemonSqueezy integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from .lemonsqueezy_service import get_lemonsqueezy_service
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .usage_tracking_service import get_usage_tracking_service, UsageType
from .logging_config import get_logger, LogCategory

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
                "id": "solo",
                "name": "Solo Creator",
                "description": "Perfect for new YouTubers getting started",
                "price_monthly": 4.99,
                "price_yearly": 49.99,
                "features": [
                    "All 5 AI Agents with full personalities",
                    "25 AI conversations/month",
                    "Basic content pillars (up to 10)",
                    "Task management (up to 25 tasks)",
                    "Goal tracking (3 goals)",
                    "5 video analyses/month",
                    "3 research projects/month",
                    "Email support (48h response)"
                ],
                "limits": {
                    "ai_conversations": 25,
                    "agents_count": 5,
                    "content_pillars": 10,
                    "goals": 3,
                    "team_members": 1,
                    "research_projects": 3,
                    "video_analysis": 5,
                    "team_collaboration": false
                },
                "trial_days": 7
            },
            {
                "id": "solo_pro",
                "name": "Solo Pro",
                "description": "Full-featured plan for serious solo creators",
                "price_monthly": 14.99,
                "price_yearly": 149.99,
                "features": [
                    "All 5 AI Agents with full personalities",
                    "100 AI conversations/month",
                    "Unlimited content pillars",
                    "Advanced task management (unlimited)",
                    "Unlimited goal tracking",
                    "25 video analyses/month",
                    "Unlimited research projects",
                    "Advanced analytics and insights",
                    "Priority support (24h response)",
                    "Custom agent personalities"
                ],
                "limits": {
                    "ai_conversations": 100,
                    "agents_count": 5,
                    "content_pillars": -1,
                    "goals": -1,
                    "team_members": 1,
                    "research_projects": -1,
                    "video_analysis": 25,
                    "team_collaboration": false
                },
                "popular": true,
                "trial_days": 14
            },
            {
                "id": "teams",
                "name": "Teams",
                "description": "For teams and agencies managing multiple channels",
                "price_monthly": 29.99,
                "price_yearly": 299.99,
                "price_per_seat": 9.99,
                "features": [
                    "All 5 AI Agents with full personalities",
                    "250 AI conversations/month (shared across team)",
                    "Unlimited content pillars",
                    "Advanced task management (unlimited)",
                    "Unlimited goal tracking",
                    "50 video analyses/month (shared across team)",
                    "Unlimited research projects",
                    "Team collaboration features",
                    "Team notes and shared workspaces",
                    "Role-based permissions",
                    "Advanced team analytics",
                    "Priority support (12h response)",
                    "Custom integrations"
                ],
                "limits": {
                    "ai_conversations": 250,
                    "agents_count": 5,
                    "content_pillars": -1,
                    "goals": -1,
                    "team_members": 1,  # Base plan includes 1 seat
                    "max_team_members": 20,
                    "research_projects": -1,
                    "video_analysis": 50,
                    "team_collaboration": true
                },
                "trial_days": 14
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
            "id": "solo_pro",
            "name": "Solo Pro",
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
        usage_service = get_usage_tracking_service()

        # Get comprehensive usage summary
        usage_summary = await usage_service.get_usage_summary(user_id)

        return create_success_response("Usage statistics retrieved", usage_summary)

    except Exception as e:
        logger.error(f"Error getting usage stats: {e}")
        return create_error_response("Failed to get usage statistics", str(e))

@router.post("/track-usage")
async def track_usage(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Track usage for the current user"""
    try:
        body = await request.json()
        user_id = current_user["id"]

        usage_type = body.get("usage_type")
        amount = body.get("amount", 1)
        cost_estimate = body.get("cost_estimate", 0.0)
        metadata = body.get("metadata", {})

        if not usage_type:
            raise HTTPException(status_code=400, detail="Usage type is required")

        usage_service = get_usage_tracking_service()

        # Track the usage
        result = await usage_service.track_usage(
            user_id=user_id,
            usage_type=usage_type,
            amount=amount,
            cost_estimate=cost_estimate,
            metadata=metadata
        )

        return create_success_response("Usage tracked successfully", result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking usage: {e}")
        return create_error_response("Failed to track usage", str(e))

@router.get("/check-limit/{usage_type}")
async def check_usage_limit(
    usage_type: str,
    current_user: Dict = Depends(get_current_user)
):
    """Check if user can perform an action based on usage limits"""
    try:
        user_id = current_user["id"]
        usage_service = get_usage_tracking_service()

        result = await usage_service.check_usage_limit(user_id, usage_type)

        return create_success_response("Usage limit checked", result)

    except Exception as e:
        logger.error(f"Error checking usage limit: {e}")
        return create_error_response("Failed to check usage limit", str(e))

@router.get("/alerts")
async def get_usage_alerts(
    unread_only: bool = True,
    current_user: Dict = Depends(get_current_user)
):
    """Get usage alerts for the current user"""
    try:
        user_id = current_user["id"]
        usage_service = get_usage_tracking_service()

        alerts = await usage_service.get_usage_alerts(user_id, unread_only=unread_only)

        return create_success_response("Usage alerts retrieved", {"alerts": alerts})

    except Exception as e:
        logger.error(f"Error getting usage alerts: {e}")
        return create_error_response("Failed to get usage alerts", str(e))

@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Mark a usage alert as read"""
    try:
        user_id = current_user["id"]
        usage_service = get_usage_tracking_service()

        success = await usage_service.mark_alert_read(alert_id, user_id)

        if success:
            return create_success_response("Alert marked as read", {})
        else:
            return create_error_response("Failed to mark alert as read", "Alert not found")

    except Exception as e:
        logger.error(f"Error marking alert as read: {e}")
        return create_error_response("Failed to mark alert as read", str(e))

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
        team_seats = body.get("team_seats", 1)  # Number of team seats for Teams plan

        if not plan_id:
            raise HTTPException(status_code=400, detail="Plan ID is required")

        # Calculate total price for Teams plan with additional seats
        total_price = None
        if plan_id == "teams":
            base_price = 29.99 if billing_cycle == "monthly" else 299.99
            seat_price = 9.99 if billing_cycle == "monthly" else 99.99
            additional_seats = max(0, team_seats - 1)  # First seat included in base
            total_price = base_price + (additional_seats * seat_price)

        lemonsqueezy = get_lemonsqueezy_service()
        user_email = current_user.get("email", "user@example.com")

        # TODO: Map plan_id to LemonSqueezy variant_id
        # For now, use a placeholder
        variant_id = "your_variant_id_here"

        custom_data = {
            "user_id": current_user["id"],
            "plan_id": plan_id,
            "billing_cycle": billing_cycle,
            "team_seats": team_seats,
            "total_price": total_price
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
                    "checkout_id": result["checkout_id"],
                    "total_price": total_price,
                    "team_seats": team_seats
                }
            )
        else:
            return create_error_response("Failed to create checkout session", result["error"])

    except Exception as e:
        logger.error(f"Error creating checkout session: {e}")
        return create_error_response("Failed to create checkout session", str(e))

@router.post("/calculate-team-price")
async def calculate_team_price(request: Request):
    """Calculate total price for Teams plan with additional seats"""
    try:
        body = await request.json()
        team_seats = body.get("team_seats", 1)
        billing_cycle = body.get("billing_cycle", "monthly")

        if team_seats < 1 or team_seats > 20:
            raise HTTPException(status_code=400, detail="Team seats must be between 1 and 20")

        # Calculate pricing for Teams plan
        base_price = 29.99 if billing_cycle == "monthly" else 299.99
        seat_price = 9.99 if billing_cycle == "monthly" else 99.99
        additional_seats = max(0, team_seats - 1)  # First seat included in base
        total_price = base_price + (additional_seats * seat_price)

        return create_success_response(
            "Team price calculated",
            {
                "base_price": base_price,
                "seat_price": seat_price,
                "additional_seats": additional_seats,
                "total_price": total_price,
                "team_seats": team_seats,
                "billing_cycle": billing_cycle,
                "price_per_person": round(total_price / team_seats, 2)
            }
        )

    except Exception as e:
        logger.error(f"Error calculating team price: {e}")
        return create_error_response("Failed to calculate team price", str(e))

@router.post("/seats/add")
async def add_team_seats(request: Request, current_user: Dict = Depends(get_current_user)):
    """Add additional seats to Teams subscription"""
    try:
        body = await request.json()
        additional_seats = body.get("additional_seats", 1)

        if additional_seats < 1 or additional_seats > 10:
            raise HTTPException(status_code=400, detail="Additional seats must be between 1 and 10")

        user_id = current_user["id"]

        # TODO: Get current subscription from Supabase
        # TODO: Verify user has Teams subscription
        # TODO: Check current seat count and max limit (20 total)

        # For now, return mock data
        current_seats = 3  # Mock current seat count
        new_total_seats = current_seats + additional_seats

        if new_total_seats > 20:
            raise HTTPException(status_code=400, detail="Maximum 20 team members allowed")

        # Calculate additional cost
        seat_price = 9.99  # Monthly price per seat
        additional_cost = additional_seats * seat_price

        # TODO: Create LemonSqueezy checkout for additional seats
        # TODO: Update subscription in Supabase after payment

        return create_success_response(
            "Additional seats added successfully",
            {
                "additional_seats": additional_seats,
                "new_total_seats": new_total_seats,
                "additional_cost": additional_cost,
                "seat_price": seat_price
            }
        )

    except Exception as e:
        logger.error(f"Error adding team seats: {e}")
        return create_error_response("Failed to add team seats", str(e))

@router.post("/seats/remove")
async def remove_team_seats(request: Request, current_user: Dict = Depends(get_current_user)):
    """Remove seats from Teams subscription"""
    try:
        body = await request.json()
        seats_to_remove = body.get("seats_to_remove", 1)

        if seats_to_remove < 1:
            raise HTTPException(status_code=400, detail="Must remove at least 1 seat")

        user_id = current_user["id"]

        # TODO: Get current subscription from Supabase
        # TODO: Verify user has Teams subscription
        # TODO: Check current seat count

        # For now, return mock data
        current_seats = 5  # Mock current seat count
        new_total_seats = current_seats - seats_to_remove

        if new_total_seats < 1:
            raise HTTPException(status_code=400, detail="Must keep at least 1 seat (owner)")

        # Calculate cost reduction (will be applied to next billing cycle)
        seat_price = 9.99  # Monthly price per seat
        cost_reduction = seats_to_remove * seat_price

        # TODO: Update LemonSqueezy subscription
        # TODO: Update subscription in Supabase

        return create_success_response(
            "Team seats removed successfully",
            {
                "seats_removed": seats_to_remove,
                "new_total_seats": new_total_seats,
                "cost_reduction": cost_reduction,
                "effective_next_billing": True
            }
        )

    except Exception as e:
        logger.error(f"Error removing team seats: {e}")
        return create_error_response("Failed to remove team seats", str(e))

@router.get("/seats/current")
async def get_current_seats(current_user: Dict = Depends(get_current_user)):
    """Get current seat information for Teams subscription"""
    try:
        user_id = current_user["id"]

        # TODO: Get current subscription from Supabase
        # TODO: Verify user has Teams subscription

        # For now, return mock data
        seat_info = {
            "current_seats": 3,
            "max_seats": 20,
            "seat_price_monthly": 9.99,
            "seat_price_yearly": 99.99,
            "total_monthly_cost": 29.99 + (2 * 9.99),  # Base + additional seats
            "team_members": [
                {
                    "id": "1",
                    "email": "owner@example.com",
                    "role": "owner",
                    "status": "active",
                    "joined_at": "2024-01-01T00:00:00Z"
                },
                {
                    "id": "2",
                    "email": "member1@example.com",
                    "role": "member",
                    "status": "active",
                    "joined_at": "2024-01-15T00:00:00Z"
                },
                {
                    "id": "3",
                    "email": "member2@example.com",
                    "role": "member",
                    "status": "pending",
                    "joined_at": "2024-01-20T00:00:00Z"
                }
            ]
        }

        return create_success_response("Current seat information retrieved", seat_info)

    except Exception as e:
        logger.error(f"Error getting current seats: {e}")
        return create_error_response("Failed to get current seats", str(e))

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
