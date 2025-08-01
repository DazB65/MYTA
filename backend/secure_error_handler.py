"""
Secure Error Handler for Vidalytics
Prevents information disclosure through error messages
"""

import logging
import traceback
from typing import Dict, Any, Optional
from enum import Enum

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from security_config import get_security_config

logger = logging.getLogger(__name__)

class ErrorLevel(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityError(Exception):
    """Security-related error"""
    def __init__(self, message: str, level: ErrorLevel = ErrorLevel.MEDIUM):
        self.message = message
        self.level = level
        super().__init__(message)

class SecureErrorHandler:
    """Handles errors securely without information disclosure"""
    
    def __init__(self):
        self.security_config = get_security_config()
        self.is_production = self.security_config.is_production()
        
        # Safe error messages for production
        self.safe_messages = {
            400: "Invalid request",
            401: "Authentication required",
            403: "Access denied",
            404: "Resource not found",
            405: "Method not allowed",
            422: "Invalid input data",
            429: "Too many requests",
            500: "Internal server error",
            502: "Service temporarily unavailable",
            503: "Service unavailable"
        }
    
    def create_error_response(
        self, 
        status_code: int, 
        error: Exception, 
        request: Request,
        include_details: bool = False
    ) -> JSONResponse:
        """Create secure error response"""
        
        # Generate error ID for tracking
        import uuid
        error_id = str(uuid.uuid4())[:8]
        
        # Log the actual error with full details
        self._log_error(error, request, error_id, status_code)
        
        # Create safe response
        response_data = {
            "error": True,
            "message": self._get_safe_message(status_code, error),
            "error_id": error_id,
            "timestamp": self._get_timestamp()
        }
        
        # Add debug info only in development
        if not self.is_production and include_details:
            response_data["debug"] = {
                "error_type": type(error).__name__,
                "details": str(error)[:500]  # Truncate long messages
            }
        
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
    
    def _get_safe_message(self, status_code: int, error: Exception) -> str:
        """Get safe error message for public consumption"""
        
        # Use predefined safe messages
        if status_code in self.safe_messages:
            base_message = self.safe_messages[status_code]
        else:
            base_message = "An error occurred"
        
        # For specific error types, provide more context
        if isinstance(error, HTTPException):
            # HTTPException details can be shown (they're usually safe)
            return error.detail if error.detail else base_message
        elif isinstance(error, ValueError):
            # Validation errors can be shown
            return str(error) if len(str(error)) < 100 else base_message
        elif isinstance(error, SecurityError):
            # Security errors should use generic messages
            return base_message
        else:
            # All other errors get generic messages
            return base_message
    
    def _log_error(
        self, 
        error: Exception, 
        request: Request, 
        error_id: str, 
        status_code: int
    ):
        """Log error with full details for debugging"""
        
        # Extract safe request info
        request_info = {
            "method": request.method,
            "path": str(request.url.path),
            "query": str(request.url.query)[:200],  # Truncate long queries
            "user_agent": request.headers.get("user-agent", "unknown")[:100],
            "ip": request.client.host if request.client else "unknown",
            "error_id": error_id
        }
        
        # Determine log level based on status code
        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING
        else:
            log_level = logging.INFO
        
        # Log the error
        logger.log(
            log_level,
            f"Error {error_id}: {type(error).__name__} - {str(error)} | "
            f"Request: {request_info['method']} {request_info['path']} | "
            f"IP: {request_info['ip']} | Status: {status_code}"
        )
        
        # Log full traceback for 500 errors
        if status_code >= 500:
            logger.error(f"Full traceback for error {error_id}:\n{traceback.format_exc()}")
    
    def _get_timestamp(self) -> str:
        """Get ISO timestamp"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
    
    def sanitize_error_details(self, details: Any) -> Dict[str, Any]:
        """Sanitize error details for safe logging"""
        
        if isinstance(details, dict):
            sanitized = {}
            for key, value in details.items():
                # Skip sensitive keys
                if key.lower() in ['password', 'token', 'secret', 'key', 'auth']:
                    sanitized[key] = "[REDACTED]"
                else:
                    sanitized[key] = self.sanitize_error_details(value)
            return sanitized
        elif isinstance(details, list):
            return [self.sanitize_error_details(item) for item in details[:10]]  # Limit list size
        elif isinstance(details, str):
            # Truncate long strings and check for sensitive patterns
            if any(pattern in details.lower() for pattern in ['password', 'token', 'secret']):
                return "[REDACTED]"
            return details[:500]  # Truncate long strings
        else:
            return str(details)[:100] if details is not None else None

# Global error handler instance
secure_error_handler = SecureErrorHandler()

def create_secure_exception_handlers(app):
    """Add secure exception handlers to FastAPI app"""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler with secure error responses"""
        return secure_error_handler.create_error_response(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            error=exc,
            request=request
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """HTTP exception handler"""
        return secure_error_handler.create_error_response(
            status_code=exc.status_code,
            error=exc,
            request=request,
            include_details=True  # HTTPException details are usually safe
        )
    
    @app.exception_handler(ValueError)
    async def validation_exception_handler(request: Request, exc: ValueError):
        """Validation exception handler"""
        return secure_error_handler.create_error_response(
            status_code=400,
            error=exc,
            request=request,
            include_details=True  # Validation errors are usually safe
        )
    
    logger.info("Secure exception handlers registered")

# Utility functions for application use
def log_security_event(
    event: str, 
    request: Request, 
    level: ErrorLevel = ErrorLevel.MEDIUM,
    details: Optional[Dict[str, Any]] = None
):
    """Log security-related events"""
    
    # Sanitize details
    safe_details = secure_error_handler.sanitize_error_details(details) if details else {}
    
    # Extract request info safely
    request_info = {
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown")[:100],
        "path": str(request.url.path),
        "method": request.method
    }
    
    log_message = f"SECURITY EVENT: {event} | Request: {request_info} | Details: {safe_details}"
    
    # Log at appropriate level
    if level == ErrorLevel.CRITICAL:
        logger.critical(log_message)
    elif level == ErrorLevel.HIGH:
        logger.error(log_message)
    elif level == ErrorLevel.MEDIUM:
        logger.warning(log_message)
    else:
        logger.info(log_message)

def create_user_friendly_error(message: str, code: str = None) -> HTTPException:
    """Create user-friendly error that's safe to display"""
    
    # Sanitize the message
    safe_message = secure_error_handler._get_safe_message(400, ValueError(message))
    
    return HTTPException(
        status_code=400,
        detail=safe_message,
        headers={"X-Error-Code": code} if code else None
    )

__all__ = [
    'SecureErrorHandler',
    'SecurityError',
    'ErrorLevel',
    'secure_error_handler',
    'create_secure_exception_handlers',
    'log_security_event',
    'create_user_friendly_error'
]