"""
Supabase Client for MYTA Backend
Handles database operations and authentication with Supabase
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
import logging
from datetime import datetime

from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.DATABASE)

class SupabaseService:
    """Service for handling Supabase database operations via REST API"""

    def __init__(self):
        self.url = os.getenv('VITE_SUPABASE_URL')
        self.key = os.getenv('VITE_SUPABASE_ANON_KEY')

        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be provided in environment variables")

        # Remove trailing slash if present
        self.url = self.url.rstrip('/')
        self.rest_url = f"{self.url}/rest/v1"

        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }

        logger.info("Supabase HTTP client initialized successfully")

    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Make HTTP request to Supabase REST API"""
        try:
            url = f"{self.rest_url}/{endpoint}"

            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=30
            )

            if response.status_code in [200, 201, 204]:
                try:
                    return {'success': True, 'data': response.json() if response.content else []}
                except json.JSONDecodeError:
                    return {'success': True, 'data': []}
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"Supabase API error: {error_msg}")
                return {'success': False, 'error': error_msg}

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {'success': False, 'error': str(e)}
    
    # User Management
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user record"""
        user_data['created_at'] = datetime.utcnow().isoformat()
        result = self._make_request('POST', 'users', user_data)
        if result['success']:
            logger.info(f"User created successfully: {user_data.get('id', 'unknown')}")
        return result

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user by ID"""
        result = self._make_request('GET', 'users', params={'id': f'eq.{user_id}'})
        if result['success'] and result['data']:
            return {'success': True, 'data': result['data'][0]}
        elif result['success']:
            return {'success': False, 'error': 'User not found'}
        return result

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data"""
        updates['updated_at'] = datetime.utcnow().isoformat()
        return self._make_request('PATCH', 'users', updates, params={'id': f'eq.{user_id}'})
    
    # Channel Management
    def get_channel_info(self, user_id: str) -> Dict[str, Any]:
        """Get channel information for user"""
        try:
            result = self.client.table('channels').select('*').eq('user_id', user_id).execute()
            if result.data:
                return {'success': True, 'data': result.data[0]}
            else:
                return {'success': False, 'error': 'Channel not found'}
        except Exception as e:
            logger.error(f"Error getting channel info: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_channel_info(self, user_id: str, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update channel information"""
        try:
            channel_data['updated_at'] = datetime.utcnow().isoformat()
            
            # Try to update first
            result = self.client.table('channels').update(channel_data).eq('user_id', user_id).execute()
            
            if not result.data:
                # If no rows updated, insert new record
                channel_data['user_id'] = user_id
                result = self.client.table('channels').insert(channel_data).execute()
            
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error updating channel info: {e}")
            return {'success': False, 'error': str(e)}
    
    # Analytics Management
    def get_analytics(self, user_id: str, timeframe: str = '30d') -> Dict[str, Any]:
        """Get analytics data for user"""
        try:
            result = self.client.table('analytics').select('*').eq('user_id', user_id).execute()
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {'success': False, 'error': str(e)}
    
    def store_analytics(self, user_id: str, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store analytics data"""
        try:
            analytics_data['user_id'] = user_id
            analytics_data['created_at'] = datetime.utcnow().isoformat()
            
            result = self.client.table('analytics').insert(analytics_data).execute()
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error storing analytics: {e}")
            return {'success': False, 'error': str(e)}
    
    # Conversation Management
    def store_conversation(self, user_id: str, role: str, content: str, metadata: Dict = None) -> Dict[str, Any]:
        """Store conversation message"""
        try:
            conversation_data = {
                'user_id': user_id,
                'role': role,
                'content': content,
                'metadata': metadata or {},
                'created_at': datetime.utcnow().isoformat()
            }
            
            result = self.client.table('conversations').insert(conversation_data).execute()
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error storing conversation: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_conversation_history(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get conversation history for user"""
        try:
            result = (self.client.table('conversations')
                     .select('*')
                     .eq('user_id', user_id)
                     .order('created_at', desc=True)
                     .limit(limit)
                     .execute())
            
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return {'success': False, 'error': str(e)}
    
    # Content Cards Management
    def get_content_cards(self, user_id: str) -> Dict[str, Any]:
        """Get content cards for user"""
        try:
            result = self.client.table('content_cards').select('*').eq('user_id', user_id).execute()
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error getting content cards: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_content_card(self, user_id: str, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new content card"""
        try:
            card_data['user_id'] = user_id
            card_data['created_at'] = datetime.utcnow().isoformat()
            
            result = self.client.table('content_cards').insert(card_data).execute()
            return {'success': True, 'data': result.data}
        except Exception as e:
            logger.error(f"Error creating content card: {e}")
            return {'success': False, 'error': str(e)}
    
    # Generic CRUD operations
    def select(self, table: str, columns: str = '*', filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generic select operation"""
        params = {}
        if columns != '*':
            params['select'] = columns

        if filters:
            for key, value in filters.items():
                params[key] = f'eq.{value}'

        return self._make_request('GET', table, params=params)

    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generic insert operation"""
        data['created_at'] = datetime.utcnow().isoformat()
        return self._make_request('POST', table, data)

    def update(self, table: str, data: Dict[str, Any], filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generic update operation"""
        data['updated_at'] = datetime.utcnow().isoformat()
        params = {}

        for key, value in filters.items():
            params[key] = f'eq.{value}'

        return self._make_request('PATCH', table, data, params=params)

    def delete(self, table: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Generic delete operation"""
        params = {}

        for key, value in filters.items():
            params[key] = f'eq.{value}'

        return self._make_request('DELETE', table, params=params)

# Global service instance
_supabase_service: Optional[SupabaseService] = None

def get_supabase_service() -> SupabaseService:
    """Get or create global Supabase service instance"""
    global _supabase_service
    if _supabase_service is None:
        _supabase_service = SupabaseService()
    return _supabase_service
