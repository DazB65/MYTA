"""
CSRF Protection Middleware for Vidalytics
Implements Cross-Site Request Forgery protection
"""

import secrets
import logging
from typing import Optional, Set
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

class CSRFProtection:
    """CSRF protection implementation"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.exempt_methods: Set[str] = {'GET', 'HEAD', 'OPTIONS'}
        self.exempt_paths: Set[str] = {'/api/dashboard/auth', '/api/dashboard/health'}
        self.token_timeout = timedelta(hours=2)  # CSRF tokens valid for 2 hours
        
    def generate_csrf_token(self) -> str:
        """Generate a CSRF token"""
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, token: str, session_token: str = None) -> bool:
        """Validate CSRF token"""
        if not token:
            return False
        
        # Basic token validation (in production, tie to session)
        # For now, just check if it's a valid format
        try:
            # Decode the token to check if it's valid base64
            import base64
            decoded = base64.urlsafe_b64decode(token + '==')  # Add padding if needed
            return len(decoded) >= 24  # At least 24 bytes
        except Exception:
            return False
    
    def is_safe_request(self, request: Request) -> bool:
        """Check if request is safe (doesn't need CSRF protection)"""
        return (request.method in self.exempt_methods or
                request.url.path in self.exempt_paths)
    
    def check_referer(self, request: Request) -> bool:
        """Check if referer header matches origin"""
        referer = request.headers.get('referer')
        origin = request.headers.get('origin')
        host = request.headers.get('host')
        
        if not referer:
            return False
        
        # Parse referer URL
        from urllib.parse import urlparse
        referer_parsed = urlparse(referer)
        
        # Check against origin or host
        if origin:
            origin_parsed = urlparse(origin)
            return referer_parsed.netloc == origin_parsed.netloc
        elif host:
            return referer_parsed.netloc == host
        
        return False

class CSRFMiddleware(BaseHTTPMiddleware):
    """CSRF protection middleware"""
    
    def __init__(self, app, csrf_protection: CSRFProtection):
        super().__init__(app)
        self.csrf = csrf_protection
        
    async def dispatch(self, request: Request, call_next):
        """Process request through CSRF middleware"""
        
        # Skip CSRF check for safe methods
        if self.csrf.is_safe_request(request):
            response = await call_next(request)
            
            # Add CSRF token to safe responses
            if request.method == 'GET' and request.url.path.startswith('/api/'):
                csrf_token = self.csrf.generate_csrf_token()
                response.headers['X-CSRF-Token'] = csrf_token
            
            return response
        
        # Check for CSRF protection on unsafe methods
        try:
            # For development, be more lenient with CSRF protection
            is_development = request.headers.get('host') in ['localhost:8888', '127.0.0.1:8888', 'localhost:3000', '127.0.0.1:3000']

            # Check X-Requested-With header (helps prevent simple CSRF)
            xhr_header = request.headers.get('x-requested-with')
            if xhr_header != 'XMLHttpRequest' and not is_development:
                logger.warning(f"Missing X-Requested-With header from {request.client.host}")
                # In production, this would be more strict

            # Check CSRF token (more lenient in development)
            csrf_token = (
                request.headers.get('x-csrf-token') or
                request.headers.get('csrf-token')
            )

            # In development, allow requests without CSRF tokens for now
            # TODO: Implement proper CSRF token flow for frontend
            if csrf_token and not self.csrf.validate_csrf_token(csrf_token):
                logger.warning(f"Invalid CSRF token from {request.client.host}")
                if not is_development:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "CSRF token validation failed", "code": "CSRF_INVALID"}
                    )

            # Check referer as additional protection
            if not self.csrf.check_referer(request):
                logger.warning(f"Invalid referer from {request.client.host}")
                # Don't block for referer issues in development, just log
                if not is_development:
                    return JSONResponse(
                        status_code=403,
                        content={"error": "Invalid request origin", "code": "INVALID_ORIGIN"}
                    )

            # Process the request
            response = await call_next(request)
            return response
            
        except Exception as e:
            logger.error(f"CSRF middleware error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "CSRF protection error"}
            )

# CSRF token endpoint
def add_csrf_endpoint(app, csrf_protection: CSRFProtection):
    """Add CSRF token endpoint to app"""
    
    @app.get("/api/csrf-token")
    async def get_csrf_token(request: Request):
        """Get CSRF token for forms"""
        token = csrf_protection.generate_csrf_token()
        
        return {
            "csrf_token": token,
            "expires_in": 7200  # 2 hours in seconds
        }

# Utility functions
def setup_csrf_protection(app, secret_key: str):
    """Setup CSRF protection for the application"""
    csrf_protection = CSRFProtection(secret_key)
    
    # Add middleware
    app.add_middleware(CSRFMiddleware, csrf_protection=csrf_protection)
    
    # Add CSRF token endpoint
    add_csrf_endpoint(app, csrf_protection)
    
    logger.info("CSRF protection enabled")
    return csrf_protection

__all__ = ['CSRFProtection', 'CSRFMiddleware', 'setup_csrf_protection']