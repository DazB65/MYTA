"""
Security Middleware for CreatorMate API
Implements security headers, input validation, and request sanitization
"""

import time
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from security_config import get_security_config

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for API protection"""
    
    def __init__(self, app, max_request_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.security_config = get_security_config()
        self.max_request_size = max_request_size
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request through security middleware"""
        start_time = time.time()
        
        try:
            # 1. Check request size
            if await self._check_request_size(request):
                return JSONResponse(
                    status_code=413,
                    content={"error": "Request too large", "max_size": f"{self.max_request_size} bytes"}
                )
            
            # 2. Validate request headers
            if not self._validate_headers(request):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Invalid request headers"}
                )
            
            # 3. Process the request
            response = await call_next(request)
            
            # 4. Add security headers to response
            self._add_security_headers(response)
            
            # 5. Log request (without sensitive data)
            self._log_request(request, response, time.time() - start_time)
            
            return response
            
        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Internal security error"}
            )
    
    async def _check_request_size(self, request: Request) -> bool:
        """Check if request size exceeds limit"""
        try:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_request_size:
                logger.warning(f"Request size {content_length} exceeds limit {self.max_request_size}")
                return True
        except (ValueError, TypeError):
            pass
        return False
    
    def _validate_headers(self, request: Request) -> bool:
        """Validate request headers for security"""
        # Check for suspicious headers
        suspicious_headers = [
            "x-forwarded-host",
            "x-original-url", 
            "x-rewrite-url"
        ]
        
        for header in suspicious_headers:
            if header in request.headers:
                value = request.headers[header]
                if self._is_suspicious_value(value):
                    logger.warning(f"Suspicious header detected: {header}={value}")
                    return False
        
        return True
    
    def _is_suspicious_value(self, value: str) -> bool:
        """Check if a value contains suspicious content"""
        suspicious_patterns = [
            "<script",
            "javascript:",
            "data:text/html",
            "vbscript:",
            "../",
            "..\\",
            "eval(",
            "expression("
        ]
        
        value_lower = value.lower()
        return any(pattern in value_lower for pattern in suspicious_patterns)
    
    def _add_security_headers(self, response: Response):
        """Add security headers to response"""
        security_headers = self.security_config.get_security_headers()
        
        for header, value in security_headers.items():
            if value:  # Only add non-empty headers
                response.headers[header] = value
    
    def _log_request(self, request: Request, response: Response, duration: float):
        """Log request details (without sensitive information)"""
        # Extract safe information for logging
        log_data = {
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_agent": request.headers.get("user-agent", "unknown")[:100],  # Truncate
            "ip": request.client.host if request.client else "unknown"
        }
        
        # Don't log sensitive paths in detail
        sensitive_paths = ["/auth/", "/oauth/", "/token/"]
        if any(path in log_data["path"] for path in sensitive_paths):
            log_data["path"] = "[SENSITIVE_PATH]"
        
        if response.status_code >= 400:
            logger.warning(f"Request failed: {log_data}")
        else:
            logger.info(f"Request processed: {log_data}")

class InputValidationMiddleware(BaseHTTPMiddleware):
    """Middleware for input validation and sanitization"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Validate and sanitize input"""
        try:
            # Only validate POST/PUT requests with JSON content
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.headers.get("content-type", "")
                if "application/json" in content_type:
                    # Read and validate JSON body
                    body = await request.body()
                    if body:
                        try:
                            import json
                            data = json.loads(body)
                            
                            # Validate JSON structure
                            if not self._validate_json_structure(data):
                                return JSONResponse(
                                    status_code=400,
                                    content={"error": "Invalid JSON structure"}
                                )
                            
                            # Sanitize the data
                            sanitized_data = self._sanitize_data(data)
                            
                            # Replace request body with sanitized data
                            request._body = json.dumps(sanitized_data).encode()
                            
                        except json.JSONDecodeError:
                            return JSONResponse(
                                status_code=400,
                                content={"error": "Invalid JSON format"}
                            )
            
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"Input validation error: {e}")
            return JSONResponse(
                status_code=500,
                content={"error": "Input validation failed"}
            )
    
    def _validate_json_structure(self, data: Any) -> bool:
        """Validate JSON structure for security"""
        # Check for excessively nested structures
        if self._get_nesting_depth(data) > 10:
            logger.warning("JSON nesting depth exceeds limit")
            return False
        
        # Check for excessively large arrays
        if isinstance(data, list) and len(data) > 1000:
            logger.warning("JSON array size exceeds limit")
            return False
        
        return True
    
    def _get_nesting_depth(self, obj: Any, depth: int = 0) -> int:
        """Calculate nesting depth of JSON object"""
        if depth > 15:  # Prevent infinite recursion
            return depth
        
        if isinstance(obj, dict):
            return max([self._get_nesting_depth(v, depth + 1) for v in obj.values()] + [depth])
        elif isinstance(obj, list):
            return max([self._get_nesting_depth(item, depth + 1) for item in obj] + [depth])
        else:
            return depth
    
    def _sanitize_data(self, data: Any) -> Any:
        """Sanitize data to prevent XSS and injection attacks"""
        if isinstance(data, str):
            return self._sanitize_string(data)
        elif isinstance(data, dict):
            return {k: self._sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        else:
            return data
    
    def _sanitize_string(self, value: str) -> str:
        """Sanitize string values"""
        if not isinstance(value, str):
            return value
        
        # Remove potentially dangerous characters/patterns
        dangerous_patterns = [
            ("<script", "&lt;script"),
            ("</script>", "&lt;/script&gt;"),
            ("javascript:", ""),
            ("vbscript:", ""),
            ("data:text/html", ""),
            ("eval(", ""),
            ("expression(", "")
        ]
        
        sanitized = value
        for pattern, replacement in dangerous_patterns:
            sanitized = sanitized.replace(pattern, replacement)
        
        # Limit string length
        if len(sanitized) > 10000:  # 10KB limit per string
            sanitized = sanitized[:10000]
            logger.warning("String truncated due to length limit")
        
        return sanitized

def add_security_middleware(app):
    """Add security middleware to FastAPI app"""
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(InputValidationMiddleware)
    logger.info("Security middleware added to application")