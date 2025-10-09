"""
Boss Agent Authentication Module for Vidalytics
Provides authentication and authorization for specialized agents
"""

import logging
from typing import Dict, Any, Optional
from .security_config import get_boss_agent_secret

logger = logging.getLogger(__name__)

class SpecializedAgentAuthMixin:
    """
    Authentication mixin for specialized agents to validate boss agent requests
    Provides methods for validating boss agent requests and generating secure responses
    """
    
    def __init__(self, *args, **kwargs):
        # Accept any arguments to support multiple inheritance
        # Only use what we need, ignore the rest
        self.agent_type = "specialized_agent"
        self.agent_id = "unknown"
        self.hierarchical_role = "specialized_agent"

        # Call super() to continue the MRO chain
        super().__init__(*args, **kwargs)
    
    def _validate_boss_agent_request(self, request_data: Dict[str, Any]) -> bool:
        """
        Validate that request comes from authorized boss agent
        
        Args:
            request_data: Request data from boss agent
            
        Returns:
            True if request is valid, False otherwise
        """
        # Check for boss agent signature
        if not request_data.get('from_boss_agent', False):
            logger.warning(f"Request missing boss agent signature: {self.agent_type}")
            return False
        
        # Check for boss agent callback URL
        if 'boss_agent_callback_url' not in request_data:
            logger.warning(f"Request missing boss agent callback URL: {self.agent_type}")
            return False
        
        # Check for boss agent secret
        boss_agent_secret = get_boss_agent_secret()
        request_secret = request_data.get('boss_agent_secret')
        
        if not request_secret or request_secret != boss_agent_secret:
            logger.warning(f"Invalid boss agent secret: {self.agent_type}")
            return False
        
        return True
    
    def _create_unauthorized_response(self, request_id: str) -> Dict[str, Any]:
        """
        Create response for unauthorized requests
        
        Args:
            request_id: Original request ID
            
        Returns:
            Error response dictionary
        """
        return {
            'agent_type': self.agent_type,
            'agent_id': self.agent_id,
            'hierarchical_role': self.hierarchical_role,
            'request_id': request_id,
            'status': 'error',
            'error': 'Unauthorized request',
            'message': 'This agent only accepts requests from the authorized boss agent',
            'for_boss_agent_only': True
        }
    
    def _create_domain_mismatch_response(self, request_id: str) -> Dict[str, Any]:
        """
        Create response for requests outside agent's domain
        
        Args:
            request_id: Original request ID
            
        Returns:
            Error response dictionary
        """
        return {
            'agent_type': self.agent_type,
            'agent_id': self.agent_id,
            'hierarchical_role': self.hierarchical_role,
            'request_id': request_id,
            'status': 'error',
            'error': 'Domain mismatch',
            'message': f'This request should be handled by a different specialized agent, not {self.agent_type}',
            'for_boss_agent_only': True
        }