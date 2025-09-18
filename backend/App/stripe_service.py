"""
Stripe Service for MYTA
Handles Stripe API operations for billing and subscriptions
"""

import os
import stripe
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class StripeService:
    """Service for handling Stripe API operations"""
    
    def __init__(self):
        # Initialize Stripe with secret key from environment
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
        
        if not stripe.api_key:
            logger.error("STRIPE_SECRET_KEY not found in environment variables")
            raise ValueError("Stripe secret key is required")
    
    def create_checkout_session(
        self, 
        price_id: str, 
        customer_email: str,
        customer_id: Optional[str] = None,
        success_url: str = None,
        cancel_url: str = None,
        metadata: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Create a Stripe Checkout session"""
        try:
            # Default URLs if not provided
            if not success_url:
                success_url = "https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}"
            if not cancel_url:
                cancel_url = "https://your-domain.com/cancel"
            
            session_params = {
                'payment_method_types': ['card'],
                'line_items': [{
                    'price': price_id,
                    'quantity': 1,
                }],
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
            
            session = stripe.checkout.Session.create(**session_params)
            
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
