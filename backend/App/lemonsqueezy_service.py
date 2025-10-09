"""
LemonSqueezy Integration Service for MYTA
Handles subscription management, payments, and webhooks
"""

import os
import hmac
import hashlib
import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.PAYMENT)

class LemonSqueezyService:
    """Service for handling LemonSqueezy API operations"""
    
    def __init__(self):
        self.api_key = os.getenv('LEMONSQUEEZY_API_KEY')
        self.store_id = os.getenv('LEMONSQUEEZY_STORE_ID')
        self.webhook_secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
        self.environment = os.getenv('LEMONSQUEEZY_ENVIRONMENT', 'sandbox')
        
        if self.environment == 'sandbox':
            self.base_url = 'https://api.lemonsqueezy.com/v1'
        else:
            self.base_url = 'https://api.lemonsqueezy.com/v1'
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
        }
    
    def create_checkout_url(self, variant_id: str, user_email: str, 
                          custom_data: Dict = None) -> Dict[str, Any]:
        """Create a checkout URL for a subscription"""
        try:
            checkout_data = {
                "data": {
                    "type": "checkouts",
                    "attributes": {
                        "product_options": {
                            "enabled_variants": [variant_id]
                        },
                        "checkout_options": {
                            "embed": False,
                            "media": True,
                            "logo": True
                        },
                        "checkout_data": {
                            "email": user_email,
                            "custom": custom_data or {}
                        },
                        "expires_at": None
                    },
                    "relationships": {
                        "store": {
                            "data": {
                                "type": "stores",
                                "id": self.store_id
                            }
                        },
                        "variant": {
                            "data": {
                                "type": "variants",
                                "id": variant_id
                            }
                        }
                    }
                }
            }
            
            response = requests.post(
                f'{self.base_url}/checkouts',
                headers=self.headers,
                json=checkout_data
            )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    'success': True,
                    'checkout_url': data['data']['attributes']['url'],
                    'checkout_id': data['data']['id']
                }
            else:
                logger.error(f"Failed to create checkout: {response.text}")
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Error creating checkout: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details from LemonSqueezy"""
        try:
            response = requests.get(
                f'{self.base_url}/subscriptions/{subscription_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Error getting subscription: {e}")
            return {'success': False, 'error': str(e)}
    
    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription"""
        try:
            cancel_data = {
                "data": {
                    "type": "subscriptions",
                    "id": subscription_id,
                    "attributes": {
                        "cancelled": True
                    }
                }
            }
            
            response = requests.patch(
                f'{self.base_url}/subscriptions/{subscription_id}',
                headers=self.headers,
                json=cancel_data
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Error cancelling subscription: {e}")
            return {'success': False, 'error': str(e)}
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature from LemonSqueezy"""
        try:
            expected_signature = hmac.new(
                self.webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return False
    
    def get_products(self) -> Dict[str, Any]:
        """Get all products from the store"""
        try:
            response = requests.get(
                f'{self.base_url}/products',
                headers=self.headers,
                params={'filter[store_id]': self.store_id}
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_variants(self, product_id: str) -> Dict[str, Any]:
        """Get variants for a product"""
        try:
            response = requests.get(
                f'{self.base_url}/variants',
                headers=self.headers,
                params={'filter[product_id]': product_id}
            )
            
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.text}
                
        except Exception as e:
            logger.error(f"Error getting variants: {e}")
            return {'success': False, 'error': str(e)}

# Global service instance
_lemonsqueezy_service: Optional[LemonSqueezyService] = None

def get_lemonsqueezy_service() -> LemonSqueezyService:
    """Get or create global LemonSqueezy service instance"""
    global _lemonsqueezy_service
    if _lemonsqueezy_service is None:
        _lemonsqueezy_service = LemonSqueezyService()
    return _lemonsqueezy_service
