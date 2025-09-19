"""
Stripe Router for MYTA
Handles Stripe billing and subscription endpoints
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import json
import stripe
from datetime import datetime

from backend.App.stripe_service import get_stripe_service
from backend.App.auth_middleware import get_current_user, get_optional_user
from backend.App.api_models import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

# Configure logging
logger = get_logger(__name__, LogCategory.API)

# Pydantic models for request validation
class CheckoutSessionRequest(BaseModel):
    plan_id: str
    billing_cycle: str

# Create router
router = APIRouter(prefix="/api/stripe", tags=["Stripe Billing"])

# MYTA Stripe Price IDs
STRIPE_PRICE_IDS = {
    'basic': {
        'monthly': 'price_1S8pq3A4NbLKuuGeAXxxeENx',
        'yearly': 'price_1S8pr7A4NbLKuuGeFTQs4lG5'
    },
    'solo_pro': {
        'monthly': 'price_1S8pucA4NbLKuuGeU13Jvpfa',
        'yearly': 'price_1S8pv4A4NbLKuuGe5Cs1xl8O'
    },
    'teams': {
        'monthly': 'price_1S8pw0A4NbLKuuGeVAJjroZG',
        'yearly': 'price_1S8pwNA4NbLKuuGeTBVbDjLP',
        'monthly_per_seat': 'price_1S8pzaA4NbLKuuGeHnVRJfTc',
        'yearly_per_seat': 'price_1S8q01A4NbLKuuGeeYQ1Dav1'
    }
}

@router.post("/test-endpoint")
async def test_endpoint():
    """Simple test endpoint to check if basic routing works"""
    logger.info("🔄 Test endpoint reached successfully!")
    return {"status": "success", "message": "Test endpoint working"}

@router.get("/create-checkout-session")
async def create_checkout_session_get(
    plan_id: str,
    billing_cycle: str = "monthly",
    pricing_type: str = "fixed",
    team_seats: int = 1,
    customer_email: str = "demo@example.com"
):
    """Create a Stripe Checkout session using GET with query parameters"""
    try:
        logger.info("🔄 Starting checkout session creation via GET...")
        logger.info(f"🔄 Parameters: plan_id={plan_id}, billing_cycle={billing_cycle}, pricing_type={pricing_type}, team_seats={team_seats}")

        if not plan_id:
            return JSONResponse(
                status_code=400,
                content={"error": "Plan ID is required"}
            )

        if plan_id not in STRIPE_PRICE_IDS:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid plan ID: {plan_id}"}
            )

        # Get the appropriate price ID
        try:
            if plan_id == "teams" and pricing_type == "per_seat":
                price_id = STRIPE_PRICE_IDS[plan_id][f"{billing_cycle}_per_seat"]
            else:
                price_id = STRIPE_PRICE_IDS[plan_id][billing_cycle]
        except KeyError:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid billing cycle or pricing type: {billing_cycle}, {pricing_type}"}
            )

        logger.info(f"🔄 Found price ID: {price_id}")

        # Create checkout session
        stripe_service = get_stripe_service()

        # Handle Teams plan with base + additional seats pricing
        if plan_id == "teams" and pricing_type == "per_seat" and team_seats > 1:
            # Teams plan: Base plan + additional seats
            base_price_id = STRIPE_PRICE_IDS['teams']['monthly'] if billing_cycle == 'monthly' else STRIPE_PRICE_IDS['teams']['yearly']
            per_seat_price_id = price_id  # This is already the per-seat price ID
            additional_seats = team_seats - 1  # Subtract 1 because base includes 1 seat

            line_items = [
                {
                    'price': base_price_id,
                    'quantity': 1,
                },
                {
                    'price': per_seat_price_id,
                    'quantity': additional_seats,
                }
            ]

            logger.info(f"🔄 Teams pricing: Base ({base_price_id}) + {additional_seats} additional seats ({per_seat_price_id})")

            result = stripe_service.create_checkout_session(
                line_items=line_items,
                customer_email=customer_email,
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel"
            )
        else:
            # Standard single-item pricing for all other plans
            quantity = 1
            logger.info(f"🔄 Standard pricing: quantity {quantity} for price_id: {price_id}")

            result = stripe_service.create_checkout_session(
                price_id=price_id,
                customer_email=customer_email,
                quantity=quantity,
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel"
            )

        if result.get("success"):
            logger.info(f"🔄 Checkout session created successfully: {result.get('checkout_url')}")
            return JSONResponse(content={
                "checkout_url": result.get("checkout_url"),
                "session_id": result.get("session_id")
            })
        else:
            logger.error(f"❌ Failed to create checkout session: {result.get('error')}")
            return JSONResponse(
                status_code=500,
                content={"error": result.get("error", "Failed to create checkout session")}
            )

    except Exception as e:
        logger.error(f"❌ Error creating checkout session: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/create-checkout-session-v2")
async def create_checkout_session_v2(request: Request):
    """Create a Stripe Checkout session for subscription"""
    try:
        logger.info("🔄 Starting checkout session creation...")

        # Parse JSON manually (no Pydantic models to avoid timeout)
        try:
            body_bytes = await request.body()
            logger.info(f"🔄 Body bytes length: {len(body_bytes)}")

            if body_bytes:
                import json
                body = json.loads(body_bytes.decode('utf-8'))
                logger.info(f"🔄 Request body parsed: {body}")
            else:
                logger.warning("🔄 Empty request body")
                body = {}
        except Exception as e:
            logger.error(f"❌ Error parsing request body: {e}")
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid JSON in request body"}
            )

        plan_id = body.get("plan_id")
        billing_cycle = body.get("billing_cycle", "monthly")
        pricing_type = body.get("pricing_type", "fixed")
        team_seats = body.get("team_seats", 1)
        success_url = body.get("success_url", "http://localhost:3000/success")
        cancel_url = body.get("cancel_url", "http://localhost:3000/cancel")

        logger.info(f"🔄 Parsed parameters: plan_id={plan_id}, billing_cycle={billing_cycle}, pricing_type={pricing_type}")

        if not plan_id:
            return JSONResponse(
                status_code=400,
                content={"error": "Plan ID is required"}
            )

        if plan_id not in STRIPE_PRICE_IDS:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid plan ID: {plan_id}"}
            )

        # Get the appropriate price ID
        try:
            if plan_id == "teams" and pricing_type == "per_seat":
                price_id = STRIPE_PRICE_IDS[plan_id][f"{billing_cycle}_per_seat"]
            else:
                price_id = STRIPE_PRICE_IDS[plan_id][billing_cycle]
        except KeyError:
            return JSONResponse(
                status_code=400,
                content={"error": f"Invalid billing cycle or pricing type: {billing_cycle}, {pricing_type}"}
            )

        logger.info(f"🔄 Found price ID: {price_id}")

        # Use demo email (no authentication to avoid dependency injection timeout)
        customer_email = body.get("customer_email", "demo@example.com")

        logger.info(f"🔄 Creating checkout session for {customer_email}")

        # Create checkout session
        stripe_service = get_stripe_service()

        result = stripe_service.create_checkout_session(
            price_id=price_id,
            customer_email=customer_email,
            success_url=success_url,
            cancel_url=cancel_url
        )

        logger.info(f"🔄 Stripe service returned result: {result}")

        if result.get("success"):
            logger.info(f"🔄 Checkout session created successfully: {result.get('checkout_url')}")
            return JSONResponse(content={
                "checkout_url": result.get("checkout_url"),
                "session_id": result.get("session_id")
            })
        else:
            logger.error(f"❌ Failed to create checkout session: {result.get('error')}")
            return JSONResponse(
                status_code=500,
                content={"error": result.get("error", "Failed to create checkout session")}
            )

    except Exception as e:
        logger.error(f"❌ Error creating Stripe checkout session: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@router.post("/create-portal-session")
async def create_portal_session(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a Stripe Customer Portal session"""
    try:
        body = await request.json()
        customer_id = body.get("customer_id")
        return_url = body.get("return_url")

        if not customer_id:
            raise HTTPException(status_code=400, detail="Customer ID is required")

        stripe_service = get_stripe_service()

        result = stripe_service.create_customer_portal_session(
            customer_id=customer_id,
            return_url=return_url
        )

        if result["success"]:
            return create_success_response(
                "Portal session created successfully",
                {"portal_url": result["portal_url"]}
            )
        else:
            return create_error_response("Failed to create portal session", result["error"])

    except Exception as e:
        logger.error(f"Error creating Stripe portal session: {e}")
        return create_error_response("Failed to create portal session", str(e))

@router.get("/customer/{customer_id}")
async def get_customer(
    customer_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get Stripe customer details"""
    try:
        stripe_service = get_stripe_service()
        result = stripe_service.get_customer(customer_id)

        if result["success"]:
            return create_success_response(
                "Customer retrieved successfully",
                {"customer": result["customer"]}
            )
        else:
            return create_error_response("Failed to get customer", result["error"])

    except Exception as e:
        logger.error(f"Error getting Stripe customer: {e}")
        return create_error_response("Failed to get customer", str(e))

@router.post("/create-customer")
async def create_customer(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new Stripe customer"""
    try:
        body = await request.json()
        email = body.get("email") or current_user.get("email")
        name = body.get("name") or current_user.get("name", "")

        if not email:
            raise HTTPException(status_code=400, detail="Email is required")

        stripe_service = get_stripe_service()
        
        metadata = {
            "user_id": str(current_user["id"])
        }

        result = stripe_service.create_customer(
            email=email,
            name=name,
            metadata=metadata
        )

        if result["success"]:
            return create_success_response(
                "Customer created successfully",
                {"customer": result["customer"]}
            )
        else:
            return create_error_response("Failed to create customer", result["error"])

    except Exception as e:
        logger.error(f"Error creating Stripe customer: {e}")
        return create_error_response("Failed to create customer", str(e))

@router.get("/subscription/{subscription_id}")
async def get_subscription(
    subscription_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get Stripe subscription details"""
    try:
        stripe_service = get_stripe_service()
        result = stripe_service.get_subscription(subscription_id)

        if result["success"]:
            return create_success_response(
                "Subscription retrieved successfully",
                {"subscription": result["subscription"]}
            )
        else:
            return create_error_response("Failed to get subscription", result["error"])

    except Exception as e:
        logger.error(f"Error getting Stripe subscription: {e}")
        return create_error_response("Failed to get subscription", str(e))

@router.post("/cancel-subscription")
async def cancel_subscription(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Cancel a Stripe subscription"""
    try:
        body = await request.json()
        subscription_id = body.get("subscription_id")

        if not subscription_id:
            raise HTTPException(status_code=400, detail="Subscription ID is required")

        stripe_service = get_stripe_service()
        result = stripe_service.cancel_subscription(subscription_id)

        if result["success"]:
            return create_success_response(
                "Subscription cancelled successfully",
                {"subscription": result["subscription"]}
            )
        else:
            return create_error_response("Failed to cancel subscription", result["error"])

    except Exception as e:
        logger.error(f"Error cancelling Stripe subscription: {e}")
        return create_error_response("Failed to cancel subscription", str(e))

@router.get("/price-ids")
async def get_price_ids():
    """Get all MYTA Stripe price IDs"""
    return create_success_response(
        "Price IDs retrieved successfully",
        {"price_ids": STRIPE_PRICE_IDS}
    )

@router.get("/test-service")
async def test_stripe_service():
    """Test Stripe service initialization"""
    try:
        logger.info("🔄 Testing Stripe service initialization...")
        stripe_service = get_stripe_service()
        logger.info("✅ Stripe service created successfully!")

        return create_success_response(
            "Stripe service test successful",
            {"status": "working", "service_created": True}
        )
    except Exception as e:
        logger.error(f"❌ Stripe service test failed: {e}")
        return create_error_response("Stripe service test failed", str(e))

@router.post("/webhook")
async def handle_stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature")
):
    """Handle Stripe webhooks"""
    try:
        payload = await request.body()

        stripe_service = get_stripe_service()

        # Verify webhook signature
        if not stripe_service.verify_webhook_signature(payload, stripe_signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

        # Parse webhook data
        event = json.loads(payload.decode('utf-8'))
        event_type = event.get('type')

        logger.info(f"Received Stripe webhook: {event_type}")

        # Handle different webhook events
        if event_type == 'checkout.session.completed':
            await handle_checkout_completed(event)
        elif event_type == 'customer.subscription.created':
            await handle_subscription_created(event)
        elif event_type == 'customer.subscription.updated':
            await handle_subscription_updated(event)
        elif event_type == 'customer.subscription.deleted':
            await handle_subscription_cancelled(event)
        elif event_type == 'invoice.payment_succeeded':
            await handle_payment_succeeded(event)
        elif event_type == 'invoice.payment_failed':
            await handle_payment_failed(event)

        return JSONResponse(content={"status": "success"})

    except Exception as e:
        logger.error(f"Error handling Stripe webhook: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

async def handle_checkout_completed(event: Dict):
    """Handle checkout session completed webhook"""
    try:
        session = event['data']['object']
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        metadata = session.get('metadata', {})

        logger.info(f"Checkout completed for customer {customer_id}, subscription {subscription_id}")

        # TODO: Update user subscription in Supabase
        # - Store customer_id and subscription_id
        # - Update user's plan based on metadata
        # - Send welcome email

    except Exception as e:
        logger.error(f"Error handling checkout completed: {e}")

async def handle_subscription_created(event: Dict):
    """Handle subscription created webhook"""
    try:
        subscription = event['data']['object']
        customer_id = subscription.get('customer')
        subscription_id = subscription.get('id')

        logger.info(f"Subscription created: {subscription_id} for customer {customer_id}")

        # TODO: Create subscription record in Supabase

    except Exception as e:
        logger.error(f"Error handling subscription created: {e}")

async def handle_subscription_updated(event: Dict):
    """Handle subscription updated webhook"""
    try:
        subscription = event['data']['object']
        subscription_id = subscription.get('id')
        status = subscription.get('status')

        logger.info(f"Subscription updated: {subscription_id}, status: {status}")

        # TODO: Update subscription record in Supabase

    except Exception as e:
        logger.error(f"Error handling subscription updated: {e}")

async def handle_subscription_cancelled(event: Dict):
    """Handle subscription cancelled webhook"""
    try:
        subscription = event['data']['object']
        subscription_id = subscription.get('id')

        logger.info(f"Subscription cancelled: {subscription_id}")

        # TODO: Update subscription status in Supabase

    except Exception as e:
        logger.error(f"Error handling subscription cancelled: {e}")

async def handle_payment_succeeded(event: Dict):
    """Handle payment succeeded webhook"""
    try:
        invoice = event['data']['object']
        customer_id = invoice.get('customer')
        subscription_id = invoice.get('subscription')
        amount_paid = invoice.get('amount_paid')

        logger.info(f"Payment succeeded: ${amount_paid/100} for subscription {subscription_id}")

        # TODO: Create billing history record in Supabase

    except Exception as e:
        logger.error(f"Error handling payment succeeded: {e}")

async def handle_payment_failed(event: Dict):
    """Handle payment failed webhook"""
    try:
        invoice = event['data']['object']
        customer_id = invoice.get('customer')
        subscription_id = invoice.get('subscription')

        logger.info(f"Payment failed for subscription {subscription_id}")

        # TODO: Handle failed payment (send notification, update status)

    except Exception as e:
        logger.error(f"Error handling payment failed: {e}")
