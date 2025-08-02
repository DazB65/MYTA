"""
Rate limiting middleware for Vidalytics API
Implements configurable rate limiting to prevent abuse
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

# Create limiter instance using client IP address
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Rate limit configurations
RATE_LIMITS = {
    # Public endpoints - more restrictive
    "public": {
        "default": "100/minute",
        "health": "60/minute",
        "chat": "30/minute",
        "generate": "10/minute",
        "oauth": "20/minute"
    },
    # Authenticated endpoints - less restrictive
    "authenticated": {
        "default": "200/minute",
        "chat": "60/minute",
        "analytics": "100/minute",
        "youtube": "50/minute"
    }
}

def get_rate_limit(endpoint_type: str = "public", operation: str = "default") -> str:
    """Get rate limit for specific endpoint and operation"""
    limits = RATE_LIMITS.get(endpoint_type, RATE_LIMITS["public"])
    return limits.get(operation, limits["default"])

# Custom error handler for rate limit exceeded
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors"""
    response = JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded", 
            "message": f"Rate limit exceeded: {exc.detail}",
            "retry_after": getattr(exc, 'retry_after', 60)
        }
    )
    response.headers["Retry-After"] = str(getattr(exc, 'retry_after', 60))
    return response