"""
Usage Tracking Middleware for MYTA
Automatically tracks usage for various actions and enforces limits
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Dict, Any, Optional
import json
from uuid import UUID

from .usage_tracking_service import get_usage_tracking_service, UsageType
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)

class UsageTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically track usage and enforce limits"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.usage_service = get_usage_tracking_service()
        
        # Define which endpoints should track usage
        self.usage_tracking_rules = {
            # AI Conversation endpoints
            "/api/chat": {
                "usage_type": UsageType.AI_CONVERSATIONS,
                "methods": ["POST"],
                "cost_estimate": 0.05  # Estimated cost per conversation
            },
            "/api/agents/": {  # Any agent endpoint
                "usage_type": UsageType.AI_CONVERSATIONS,
                "methods": ["POST"],
                "cost_estimate": 0.05
            },
            "/api/content/generate-title": {
                "usage_type": UsageType.AI_CONVERSATIONS,
                "methods": ["POST"],
                "cost_estimate": 0.03
            },
            "/api/content/generate-description": {
                "usage_type": UsageType.AI_CONVERSATIONS,
                "methods": ["POST"],
                "cost_estimate": 0.03
            },
            "/api/content/generate-script": {
                "usage_type": UsageType.AI_CONVERSATIONS,
                "methods": ["POST"],
                "cost_estimate": 0.08
            },
            
            # Video Analysis endpoints
            "/api/analytics/video-analysis": {
                "usage_type": UsageType.VIDEO_ANALYSIS,
                "methods": ["POST"],
                "cost_estimate": 0.02
            },
            "/api/analytics/content-performance": {
                "usage_type": UsageType.VIDEO_ANALYSIS,
                "methods": ["GET"],
                "cost_estimate": 0.01
            },
            
            # Research Projects
            "/api/research/projects": {
                "usage_type": UsageType.RESEARCH_PROJECTS,
                "methods": ["POST"],
                "cost_estimate": 0.0
            }
        }
    
    async def dispatch(self, request: Request, call_next):
        """Process request with usage tracking"""
        
        # Skip tracking for non-API endpoints
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
        
        # Skip tracking for auth and subscription endpoints
        skip_paths = ["/api/auth/", "/api/subscription/", "/api/health"]
        if any(request.url.path.startswith(path) for path in skip_paths):
            return await call_next(request)
        
        # Check if this endpoint should track usage
        tracking_rule = self._get_tracking_rule(request.url.path, request.method)
        if not tracking_rule:
            return await call_next(request)
        
        # Get current user (simplified for now)
        try:
            # TODO: Implement proper user extraction from request
            # For now, skip user authentication in middleware
            # This should be handled by individual route handlers
            return await call_next(request)

            # user_id = UUID("test-user-id")  # Mock user for testing
        except Exception:
            # If we can't get user, proceed without tracking
            return await call_next(request)
        
        # Check usage limits before processing request
        try:
            limit_check = await self.usage_service.check_usage_limit(
                user_id=user_id,
                usage_type=tracking_rule["usage_type"]
            )
            
            if not limit_check["can_use"]:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "status": "error",
                        "message": f"Usage limit exceeded for {tracking_rule['usage_type'].replace('_', ' ')}",
                        "data": {
                            "usage_type": tracking_rule["usage_type"],
                            "current_usage": limit_check["current_usage"],
                            "limit": limit_check["limit"],
                            "percentage_used": limit_check["percentage_used"]
                        }
                    }
                )
        except Exception as e:
            logger.error(f"Error checking usage limits: {e}")
            # Continue with request if limit check fails
        
        # Process the request
        response = await call_next(request)
        
        # Track usage only if request was successful
        if response.status_code < 400:
            try:
                # Extract metadata from request
                metadata = await self._extract_metadata(request, tracking_rule)
                
                # Track the usage
                await self.usage_service.track_usage(
                    user_id=user_id,
                    usage_type=tracking_rule["usage_type"],
                    amount=1,
                    cost_estimate=tracking_rule.get("cost_estimate", 0.0),
                    metadata=metadata
                )
                
                logger.info(f"Tracked usage: {tracking_rule['usage_type']} for user {user_id}")
                
            except Exception as e:
                logger.error(f"Error tracking usage: {e}")
                # Don't fail the request if tracking fails
        
        return response
    
    def _get_tracking_rule(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """Get tracking rule for a given path and method"""
        
        # Check exact matches first
        if path in self.usage_tracking_rules:
            rule = self.usage_tracking_rules[path]
            if method in rule["methods"]:
                return rule
        
        # Check prefix matches (for dynamic routes)
        for rule_path, rule in self.usage_tracking_rules.items():
            if rule_path.endswith("/") and path.startswith(rule_path):
                if method in rule["methods"]:
                    return rule
        
        return None
    
    async def _extract_metadata(self, request: Request, tracking_rule: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from request for tracking"""
        metadata = {
            "endpoint": request.url.path,
            "method": request.method,
            "user_agent": request.headers.get("user-agent", ""),
            "ip_address": request.client.host if request.client else ""
        }
        
        # Add specific metadata based on usage type
        try:
            if tracking_rule["usage_type"] == UsageType.AI_CONVERSATIONS:
                # Try to get request body for AI conversations
                if request.method == "POST":
                    body = await self._get_request_body(request)
                    if body:
                        metadata.update({
                            "agent_id": body.get("agent_id"),
                            "message_length": len(body.get("message", "")),
                            "conversation_type": body.get("type", "chat")
                        })
            
        except Exception as e:
            logger.warning(f"Error extracting metadata: {e}")
        
        return metadata
    
    async def _get_request_body(self, request: Request) -> Optional[Dict[str, Any]]:
        """Safely get request body as JSON"""
        try:
            # Check if body was already consumed
            if hasattr(request, "_body"):
                body_bytes = request._body
            else:
                body_bytes = await request.body()
            
            if body_bytes:
                return json.loads(body_bytes.decode())
        except Exception:
            pass
        
        return None

# Usage tracking decorator for manual tracking
def track_usage(usage_type: str, cost_estimate: float = 0.0):
    """Decorator to manually track usage for specific functions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get user from kwargs or args
            user_id = None
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, dict) and "id" in arg:
                    try:
                        user_id = UUID(arg["id"])
                        break
                    except (ValueError, TypeError):
                        continue
            
            if user_id:
                usage_service = get_usage_tracking_service()
                try:
                    # Check limits before execution
                    limit_check = await usage_service.check_usage_limit(user_id, usage_type)
                    if not limit_check["can_use"]:
                        raise HTTPException(
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail=f"Usage limit exceeded for {usage_type.replace('_', ' ')}"
                        )
                    
                    # Execute function
                    result = await func(*args, **kwargs)
                    
                    # Track usage after successful execution
                    await usage_service.track_usage(
                        user_id=user_id,
                        usage_type=usage_type,
                        cost_estimate=cost_estimate,
                        metadata={"function": func.__name__}
                    )
                    
                    return result
                    
                except HTTPException:
                    raise
                except Exception as e:
                    logger.error(f"Error in usage tracking decorator: {e}")
                    # Execute function even if tracking fails
                    return await func(*args, **kwargs)
            else:
                # Execute function without tracking if no user found
                return await func(*args, **kwargs)
        
        return wrapper
    return decorator

# Helper function to check limits in route handlers
async def check_usage_limit_or_raise(user_id: UUID, usage_type: str):
    """Check usage limit and raise HTTPException if exceeded"""
    usage_service = get_usage_tracking_service()
    limit_check = await usage_service.check_usage_limit(user_id, usage_type)
    
    if not limit_check["can_use"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Usage limit exceeded for {usage_type.replace('_', ' ')}",
            headers={
                "X-Usage-Type": usage_type,
                "X-Current-Usage": str(limit_check["current_usage"]),
                "X-Usage-Limit": str(limit_check["limit"]),
                "X-Usage-Percentage": str(limit_check["percentage_used"])
            }
        )
    
    return limit_check
