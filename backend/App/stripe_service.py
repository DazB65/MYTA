"""
Stripe Service for MYTA
Handles Stripe API operations for billing and subscriptions
"""

import os
import stripe
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class StripeService:
    """Service for handling Stripe API operations"""

    def __init__(self):
        # Use MYTA logging system
        from .logging_config import get_logger, LogCategory
        self.logger = get_logger(__name__, LogCategory.API)

        self.logger.info("🔄 Initializing StripeService...")

        # Initialize Stripe with secret key from environment
        stripe_secret = os.getenv('STRIPE_SECRET_KEY')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')

        self.logger.info(f"🔑 Stripe secret key found: {bool(stripe_secret)}")
        self.logger.info(f"🔑 Stripe publishable key found: {bool(self.publishable_key)}")

        if not stripe_secret:
            self.logger.error("❌ STRIPE_SECRET_KEY not found in environment variables")
            raise ValueError("Stripe secret key is required")

        self.logger.info("🔄 Setting Stripe API key...")
        stripe.api_key = stripe_secret
        self.logger.info("✅ Stripe API key set successfully")

        # Test Stripe connection
        self.logger.info("🔄 Testing Stripe connection...")
        try:
            account = stripe.Account.retrieve()
            self.logger.info(f"✅ Stripe connection successful! Account ID: {account.id}")
        except Exception as e:
            self.logger.error(f"❌ Stripe connection failed: {e}")
            raise
    
    def create_checkout_session(
        self,
        line_items: List[Dict[str, Any]] = None,
        price_id: str = None,
        customer_email: str = None,
        customer_id: Optional[str] = None,
        quantity: int = 1,
        success_url: str = None,
        cancel_url: str = None,
        metadata: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Create a Stripe Checkout session"""
        # Handle both new line_items format and legacy price_id format
        if line_items:
            self.logger.info(f"🔄 Creating checkout session with {len(line_items)} line items, customer_email: {customer_email}")
        else:
            self.logger.info(f"🔄 Creating checkout session for price_id: {price_id}, customer_email: {customer_email}")
            line_items = [{
                'price': price_id,
                'quantity': quantity,
            }]

        try:
            # Default URLs if not provided
            if not success_url:
                success_url = "http://localhost:3000/success"
            if not cancel_url:
                cancel_url = "http://localhost:3000/cancel"

            session_params = {
                'payment_method_types': ['card'],
                'line_items': line_items,
                'mode': 'subscription',
                'success_url': success_url,
                'cancel_url': cancel_url,
                'metadata': metadata or {}
            }
            
            # Use existing customer or create new one
            if customer_id:
                session_params['customer'] = customer_id
            else:
                session_params['customer_email'] = customer_email

            logger.info(f"About to call Stripe API with params: {session_params}")
            session = stripe.checkout.Session.create(**session_params)
            logger.info(f"Stripe checkout session created successfully: {session.id}")
            
            return {
                'success': True,
                'session_id': session.id,
                'checkout_url': session.url
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating checkout session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def create_customer_portal_session(
        self, 
        customer_id: str,
        return_url: str = None
    ) -> Dict[str, Any]:
        """Create a Stripe Customer Portal session"""
        try:
            if not return_url:
                return_url = "https://your-domain.com/settings"
            
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )
            
            return {
                'success': True,
                'portal_url': session.url
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating portal session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            logger.error(f"Error creating portal session: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details from Stripe"""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return {
                'success': True,
                'customer': customer
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error getting customer: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_customer(
        self, 
        email: str, 
        name: str = None,
        metadata: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Create a new Stripe customer"""
        try:
            customer_params = {
                'email': email,
                'metadata': metadata or {}
            }
            
            if name:
                customer_params['name'] = name
            
            customer = stripe.Customer.create(**customer_params)
            
            return {
                'success': True,
                'customer': customer
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating customer: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details from Stripe"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return {
                'success': True,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error getting subscription: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a Stripe subscription"""
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            return {
                'success': True,
                'subscription': subscription
            }
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error canceling subscription: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Stripe webhook signature"""
        try:
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            if not webhook_secret:
                logger.error("STRIPE_WEBHOOK_SECRET not found in environment")
                return False
            
            stripe.Webhook.construct_event(payload, signature, webhook_secret)
            return True
            
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid Stripe webhook signature")
            return False
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False

# Global service instance
_stripe_service = None

def get_stripe_service() -> StripeService:
    """Get the global Stripe service instance"""
    global _stripe_service
    if _stripe_service is None:
        _stripe_service = StripeService()
    return _stripe_service
