"""
API Versioning System for MYTA
Provides backward compatibility and smooth API evolution
"""

import re
from typing import Dict, Any, Optional, List, Callable
from fastapi import Request, HTTPException, Depends
from fastapi.routing import APIRoute
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class APIVersion(Enum):
    """Supported API versions"""
    V1 = "v1"
    V2 = "v2"
    
    @classmethod
    def from_string(cls, version_str: str) -> 'APIVersion':
        """Parse version string to enum"""
        # Remove 'v' prefix if present
        clean_version = version_str.lower().replace('v', '')
        
        version_map = {
            '1': cls.V1,
            '1.0': cls.V1,
            '2': cls.V2,
            '2.0': cls.V2
        }
        
        if clean_version in version_map:
            return version_map[clean_version]
        
        raise ValueError(f"Unsupported API version: {version_str}")
    
    @property
    def numeric(self) -> float:
        """Get numeric version for comparison"""
        return float(self.value.replace('v', ''))

class VersionedResponse:
    """Response wrapper that handles version-specific formatting"""
    
    def __init__(self, data: Any, version: APIVersion):
        self.data = data
        self.version = version
    
    def format(self) -> Dict[str, Any]:
        """Format response based on API version"""
        if self.version == APIVersion.V1:
            return self._format_v1()
        elif self.version == APIVersion.V2:
            return self._format_v2()
        else:
            return self._format_v2()  # Default to latest
    
    def _format_v1(self) -> Dict[str, Any]:
        """Format for API v1 (legacy format)"""
        if isinstance(self.data, dict) and 'status' in self.data:
            # V1 format: simple structure
            return {
                'success': self.data.get('status') == 'success',
                'data': self.data.get('data'),
                'message': self.data.get('message', ''),
                'error': self.data.get('error')
            }
        return self.data
    
    def _format_v2(self) -> Dict[str, Any]:
        """Format for API v2 (current format)"""
        if isinstance(self.data, dict):
            # V2 format: enhanced structure with metadata
            return {
                'status': self.data.get('status', 'success'),
                'data': self.data.get('data'),
                'message': self.data.get('message', ''),
                'metadata': {
                    'version': self.version.value,
                    'timestamp': self.data.get('timestamp'),
                    'request_id': self.data.get('request_id')
                },
                'error': self.data.get('error'),
                'pagination': self.data.get('pagination')
            }
        return self.data

class APIVersionExtractor:
    """Extracts API version from requests"""
    
    @staticmethod
    def from_header(request: Request) -> Optional[APIVersion]:
        """Extract version from Accept header"""
        accept_header = request.headers.get('accept', '')
        
        # Look for version in Accept header: application/vnd.myta.v2+json
        version_match = re.search(r'application/vnd\.myta\.v(\d+)', accept_header)
        if version_match:
            try:
                return APIVersion.from_string(f"v{version_match.group(1)}")
            except ValueError:
                pass
        
        return None
    
    @staticmethod
    def from_path(request: Request) -> Optional[APIVersion]:
        """Extract version from URL path"""
        path = request.url.path
        
        # Look for version in path: /api/v2/...
        version_match = re.search(r'/api/v(\d+)/', path)
        if version_match:
            try:
                return APIVersion.from_string(f"v{version_match.group(1)}")
            except ValueError:
                pass
        
        return None
    
    @staticmethod
    def from_query(request: Request) -> Optional[APIVersion]:
        """Extract version from query parameter"""
        version_param = request.query_params.get('version') or request.query_params.get('api_version')
        if version_param:
            try:
                return APIVersion.from_string(version_param)
            except ValueError:
                pass
        
        return None

def get_api_version(request: Request) -> APIVersion:
    """
    Determine API version from request
    Priority: Header > Path > Query > Default
    """
    extractor = APIVersionExtractor()
    
    # Try different extraction methods in order of preference
    version = (
        extractor.from_header(request) or
        extractor.from_path(request) or
        extractor.from_query(request)
    )
    
    # Default to latest version if none specified
    if version is None:
        version = APIVersion.V2
        logger.debug(f"No API version specified, defaulting to {version.value}")
    else:
        logger.debug(f"API version {version.value} detected from request")
    
    return version

class VersionedRoute(APIRoute):
    """Custom route that handles API versioning"""
    
    def __init__(self, *args, **kwargs):
        self.min_version = kwargs.pop('min_version', APIVersion.V1)
        self.max_version = kwargs.pop('max_version', APIVersion.V2)
        self.deprecated_versions = kwargs.pop('deprecated_versions', [])
        super().__init__(*args, **kwargs)
    
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def versioned_route_handler(request: Request) -> Any:
            # Get API version
            api_version = get_api_version(request)
            
            # Check if version is supported
            if api_version.numeric < self.min_version.numeric:
                raise HTTPException(
                    status_code=400,
                    detail=f"API version {api_version.value} is no longer supported. Minimum version: {self.min_version.value}"
                )
            
            if api_version.numeric > self.max_version.numeric:
                raise HTTPException(
                    status_code=400,
                    detail=f"API version {api_version.value} is not yet available. Maximum version: {self.max_version.value}"
                )
            
            # Add deprecation warning if needed
            if api_version in self.deprecated_versions:
                logger.warning(f"API version {api_version.value} is deprecated")
                # You could add a response header here: X-API-Deprecation-Warning
            
            # Add version to request state
            request.state.api_version = api_version
            
            # Execute original handler
            response = await original_route_handler(request)
            
            # Wrap response with version formatting
            if hasattr(response, 'body') and isinstance(response.body, (dict, list)):
                versioned_response = VersionedResponse(response.body, api_version)
                response.body = versioned_response.format()
            
            return response
        
        return versioned_route_handler

def versioned_endpoint(
    min_version: APIVersion = APIVersion.V1,
    max_version: APIVersion = APIVersion.V2,
    deprecated_versions: List[APIVersion] = None
):
    """Decorator for versioned endpoints"""
    def decorator(func):
        func._min_version = min_version
        func._max_version = max_version
        func._deprecated_versions = deprecated_versions or []
        return func
    return decorator

class APIVersionMiddleware:
    """Middleware to handle API versioning globally"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # Skip versioning for non-API routes
            if not request.url.path.startswith('/api/'):
                await self.app(scope, receive, send)
                return
            
            # Get API version
            api_version = get_api_version(request)
            
            # Add version info to headers
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    headers[b"x-api-version"] = api_version.value.encode()
                    
                    # Add deprecation warning if needed
                    if api_version == APIVersion.V1:
                        headers[b"x-api-deprecation-warning"] = b"API v1 is deprecated. Please upgrade to v2."
                    
                    message["headers"] = list(headers.items())
                
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

# Version-specific data transformers
class DataTransformer:
    """Transforms data between API versions"""
    
    @staticmethod
    def transform_user_data(data: Dict[str, Any], target_version: APIVersion) -> Dict[str, Any]:
        """Transform user data for different API versions"""
        if target_version == APIVersion.V1:
            # V1: Simple user object
            return {
                'id': data.get('id'),
                'name': data.get('name'),
                'email': data.get('email'),
                'created_at': data.get('created_at')
            }
        else:
            # V2: Enhanced user object with additional fields
            return {
                'id': data.get('id'),
                'name': data.get('name'),
                'email': data.get('email'),
                'profile': {
                    'avatar_url': data.get('avatar_url'),
                    'bio': data.get('bio'),
                    'location': data.get('location')
                },
                'subscription': {
                    'tier': data.get('subscription_tier'),
                    'status': data.get('subscription_status')
                },
                'preferences': data.get('preferences', {}),
                'created_at': data.get('created_at'),
                'updated_at': data.get('updated_at')
            }
    
    @staticmethod
    def transform_video_data(data: Dict[str, Any], target_version: APIVersion) -> Dict[str, Any]:
        """Transform video data for different API versions"""
        if target_version == APIVersion.V1:
            # V1: Basic video info
            return {
                'id': data.get('id'),
                'title': data.get('title'),
                'description': data.get('description'),
                'url': data.get('url'),
                'thumbnail': data.get('thumbnail_url'),
                'views': data.get('view_count'),
                'likes': data.get('like_count'),
                'published': data.get('published_at')
            }
        else:
            # V2: Enhanced video object with analytics
            return {
                'id': data.get('id'),
                'title': data.get('title'),
                'description': data.get('description'),
                'url': data.get('url'),
                'thumbnails': {
                    'default': data.get('thumbnail_url'),
                    'medium': data.get('thumbnail_medium'),
                    'high': data.get('thumbnail_high')
                },
                'statistics': {
                    'view_count': data.get('view_count'),
                    'like_count': data.get('like_count'),
                    'comment_count': data.get('comment_count'),
                    'share_count': data.get('share_count')
                },
                'analytics': {
                    'engagement_rate': data.get('engagement_rate'),
                    'ctr': data.get('click_through_rate'),
                    'retention_rate': data.get('retention_rate')
                },
                'metadata': {
                    'duration': data.get('duration'),
                    'category': data.get('category'),
                    'tags': data.get('tags', []),
                    'language': data.get('language')
                },
                'published_at': data.get('published_at'),
                'updated_at': data.get('updated_at')
            }

# Utility functions
def get_current_api_version() -> APIVersion:
    """Get the current API version from request context"""
    from fastapi import Request
    from starlette.requests import Request as StarletteRequest
    
    # This would be set by middleware or dependency
    # Implementation depends on your FastAPI setup
    return APIVersion.V2  # Default fallback

def create_versioned_response(data: Any, version: APIVersion = None) -> Dict[str, Any]:
    """Create a properly versioned response"""
    if version is None:
        version = get_current_api_version()
    
    versioned_response = VersionedResponse(data, version)
    return versioned_response.format()
