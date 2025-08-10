"""
Enhanced Security Middleware for Vidalytics
Implements comprehensive security headers and protections
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import hashlib
import secrets
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EnhancedSecurityMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive security middleware implementing:
    - Security headers (CSP, HSTS, X-Frame-Options, etc.)
    - Request ID tracking
    - Timing attack prevention
    - Security event logging
    """
    
    def __init__(self, app, strict_mode: bool = True):
        super().__init__(app)
        self.strict_mode = strict_mode
        self.csp_policy = self._build_csp_policy()
        
    def _build_csp_policy(self) -> str:
        """Build Content Security Policy based on mode"""
        if self.strict_mode:
            return (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.openai.com https://api.anthropic.com https://generativelanguage.googleapis.com; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'; "
                "upgrade-insecure-requests;"
            )
        else:
            return (
                "default-src 'self' http: https:; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline';"
            )
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add security headers to response"""
        
        # Generate request ID for tracking
        request_id = secrets.token_urlsafe(16)
        request.state.request_id = request_id
        
        # Log security-relevant request information
        self._log_security_event(request, request_id)
        
        # Add timing attack prevention delay for auth endpoints
        if request.url.path.startswith("/auth"):
            await self._add_timing_protection()
        
        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add comprehensive security headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), "
            "gyroscope=(), magnetometer=(), microphone=(), "
            "payment=(), usb=()"
        )
        
        # HSTS (HTTP Strict Transport Security)
        if self.strict_mode:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = self.csp_policy
        
        # Remove server identification headers
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)
        
        # Add security monitoring headers
        response.headers["X-Security-Mode"] = "strict" if self.strict_mode else "standard"
        
        return response
    
    def _log_security_event(self, request: Request, request_id: str):
        """Log security-relevant request information"""
        logger.info(f"Security Event - Request ID: {request_id}, "
                   f"Method: {request.method}, "
                   f"Path: {request.url.path}, "
                   f"Client: {request.client.host if request.client else 'unknown'}, "
                   f"Time: {datetime.utcnow().isoformat()}")
    
    async def _add_timing_protection(self):
        """Add random delay to prevent timing attacks on auth endpoints"""
        import asyncio
        delay = secrets.SystemRandom().uniform(0.01, 0.05)  # 10-50ms random delay
        await asyncio.sleep(delay)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse
    """
    
    def __init__(self, app, requests_per_minute: int = 60, burst_size: int = 10):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.request_counts = {}  # IP -> (count, window_start)
        self.cleanup_interval = 300  # Cleanup old entries every 5 minutes
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Implement rate limiting"""
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Cleanup old entries periodically
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(current_time)
            self.last_cleanup = current_time
        
        # Check rate limit
        if not self._check_rate_limit(client_ip, current_time):
            response = Response(
                content="Rate limit exceeded. Please try again later.",
                status_code=429,
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(current_time + 60))
                }
            )
            return response
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self._get_remaining_requests(client_ip, current_time)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(current_time + 60))
        
        return response
    
    def _check_rate_limit(self, client_ip: str, current_time: float) -> bool:
        """Check if request is within rate limit"""
        
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = (1, current_time)
            return True
        
        count, window_start = self.request_counts[client_ip]
        
        # Reset window if expired
        if current_time - window_start > 60:
            self.request_counts[client_ip] = (1, current_time)
            return True
        
        # Check if within limit
        if count < self.requests_per_minute:
            self.request_counts[client_ip] = (count + 1, window_start)
            return True
        
        # Check burst allowance
        if count < self.requests_per_minute + self.burst_size:
            self.request_counts[client_ip] = (count + 1, window_start)
            logger.warning(f"Rate limit burst for IP {client_ip}: {count + 1} requests")
            return True
        
        logger.warning(f"Rate limit exceeded for IP {client_ip}")
        return False
    
    def _get_remaining_requests(self, client_ip: str, current_time: float) -> int:
        """Get remaining requests for client"""
        
        if client_ip not in self.request_counts:
            return self.requests_per_minute
        
        count, window_start = self.request_counts[client_ip]
        
        if current_time - window_start > 60:
            return self.requests_per_minute
        
        return max(0, self.requests_per_minute - count)
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove old entries from request counts"""
        
        expired_ips = [
            ip for ip, (_, window_start) in self.request_counts.items()
            if current_time - window_start > 120  # Remove entries older than 2 minutes
        ]
        
        for ip in expired_ips:
            del self.request_counts[ip]
        
        if expired_ips:
            logger.info(f"Cleaned up {len(expired_ips)} expired rate limit entries")