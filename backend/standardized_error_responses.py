"""
Standardized Error Response System for Vidalytics
Provides consistent error handling and response formats across all agents and endpoints
"""

import logging
import traceback
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ErrorCategory(Enum):
    """Categories of errors for better handling"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization" 
    VALIDATION = "validation"
    NOT_FOUND = "not_found"
    RATE_LIMIT = "rate_limit"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    PROCESSING = "processing"
    SYSTEM = "system"
    AGENT_DOMAIN = "agent_domain"
    NETWORK = "network"
    TIMEOUT = "timeout"

class ErrorSeverity(Enum):
    """Severity levels for errors"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ErrorDetail:
    """Detailed error information"""
    field: Optional[str] = None
    code: Optional[str] = None
    message: str = ""
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"message": self.message}
        if self.field:
            result["field"] = self.field
        if self.code:
            result["code"] = self.code
        if self.context:
            result["context"] = self.context
        return result

@dataclass
class StandardErrorResponse:
    """Standardized error response structure"""
    success: bool = False
    error_id: str = ""
    error_category: ErrorCategory = ErrorCategory.SYSTEM
    error_code: str = ""
    message: str = ""
    details: List[ErrorDetail] = None
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    timestamp: str = ""
    request_id: Optional[str] = None
    agent_type: Optional[str] = None
    retry_after: Optional[int] = None
    documentation_url: Optional[str] = None
    support_reference: Optional[str] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = []
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.error_id:
            self.error_id = f"{self.error_category.value}_{int(datetime.now().timestamp())}"
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "success": self.success,
            "error": {
                "id": self.error_id,
                "category": self.error_category.value,
                "code": self.error_code,
                "message": self.message,
                "severity": self.severity.value,
                "timestamp": self.timestamp
            }
        }
        
        if self.details:
            result["error"]["details"] = [detail.to_dict() for detail in self.details]
        
        if self.request_id:
            result["error"]["request_id"] = self.request_id
            
        if self.agent_type:
            result["error"]["agent_type"] = self.agent_type
            
        if self.retry_after:
            result["error"]["retry_after"] = self.retry_after
            
        if self.documentation_url:
            result["error"]["documentation_url"] = self.documentation_url
            
        if self.support_reference:
            result["error"]["support_reference"] = self.support_reference
        
        return result
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

class ErrorResponseBuilder:
    """Builder class for creating standardized error responses"""
    
    def __init__(self):
        self.response = StandardErrorResponse()
    
    def category(self, category: ErrorCategory) -> 'ErrorResponseBuilder':
        """Set error category"""
        self.response.error_category = category
        return self
    
    def code(self, code: str) -> 'ErrorResponseBuilder':
        """Set error code"""
        self.response.error_code = code
        return self
    
    def message(self, message: str) -> 'ErrorResponseBuilder':
        """Set error message"""
        self.response.message = message
        return self
    
    def severity(self, severity: ErrorSeverity) -> 'ErrorResponseBuilder':
        """Set error severity"""
        self.response.severity = severity
        return self
    
    def request_id(self, request_id: str) -> 'ErrorResponseBuilder':
        """Set request ID"""
        self.response.request_id = request_id
        return self
    
    def agent_type(self, agent_type: str) -> 'ErrorResponseBuilder':
        """Set agent type"""
        self.response.agent_type = agent_type
        return self
    
    def add_detail(self, message: str, field: str = None, code: str = None, 
                  context: Dict[str, Any] = None) -> 'ErrorResponseBuilder':
        """Add error detail"""
        self.response.details.append(ErrorDetail(
            field=field,
            code=code,
            message=message,
            context=context
        ))
        return self
    
    def retry_after(self, seconds: int) -> 'ErrorResponseBuilder':
        """Set retry after seconds"""
        self.response.retry_after = seconds
        return self
    
    def documentation(self, url: str) -> 'ErrorResponseBuilder':
        """Set documentation URL"""
        self.response.documentation_url = url
        return self
    
    def support_reference(self, reference: str) -> 'ErrorResponseBuilder':
        """Set support reference"""
        self.response.support_reference = reference
        return self
    
    def build(self) -> StandardErrorResponse:
        """Build the error response"""
        return self.response

class StandardizedErrorHandler:
    """Central error handling with logging and response formatting"""
    
    # HTTP status code mapping for different error categories
    HTTP_STATUS_MAPPING = {
        ErrorCategory.AUTHENTICATION: 401,
        ErrorCategory.AUTHORIZATION: 403,
        ErrorCategory.VALIDATION: 400,
        ErrorCategory.NOT_FOUND: 404,
        ErrorCategory.RATE_LIMIT: 429,
        ErrorCategory.EXTERNAL_API: 502,
        ErrorCategory.DATABASE: 500,
        ErrorCategory.PROCESSING: 422,
        ErrorCategory.SYSTEM: 500,
        ErrorCategory.AGENT_DOMAIN: 400,
        ErrorCategory.NETWORK: 503,
        ErrorCategory.TIMEOUT: 504
    }
    
    def __init__(self, service_name: str = "Vidalytics"):
        self.service_name = service_name
        self.error_counts = {category: 0 for category in ErrorCategory}
    
    def handle_exception(self, exception: Exception, request_id: str = None, 
                        agent_type: str = None, context: Dict[str, Any] = None) -> StandardErrorResponse:
        """Handle any exception and convert to standardized error response"""
        
        # Determine error category based on exception type
        category = self._categorize_exception(exception)
        
        # Build error response
        builder = ErrorResponseBuilder()
        builder.category(category)
        builder.message(str(exception))
        builder.severity(self._determine_severity(exception, category))
        
        if request_id:
            builder.request_id(request_id)
        if agent_type:
            builder.agent_type(agent_type)
        
        # Add exception details
        builder.add_detail(
            message=f"{type(exception).__name__}: {str(exception)}",
            code=type(exception).__name__.upper(),
            context={
                "exception_type": type(exception).__name__,
                "traceback": traceback.format_exc() if logger.isEnabledFor(logging.DEBUG) else None,
                **(context or {})
            }
        )
        
        error_response = builder.build()
        
        # Log the error
        self._log_error(error_response, exception)
        
        # Update error counts
        self.error_counts[category] += 1
        
        return error_response
    
    def _categorize_exception(self, exception: Exception) -> ErrorCategory:
        """Categorize exception into error category"""
        exception_name = type(exception).__name__.lower()
        
        if "auth" in exception_name or "permission" in exception_name:
            return ErrorCategory.AUTHENTICATION
        elif "validation" in exception_name or "value" in exception_name:
            return ErrorCategory.VALIDATION
        elif "notfound" in exception_name or "missing" in exception_name:
            return ErrorCategory.NOT_FOUND
        elif "timeout" in exception_name:
            return ErrorCategory.TIMEOUT
        elif "connection" in exception_name or "network" in exception_name:
            return ErrorCategory.NETWORK
        elif "database" in exception_name or "sqlite" in exception_name:
            return ErrorCategory.DATABASE
        elif "rate" in exception_name or "limit" in exception_name:
            return ErrorCategory.RATE_LIMIT
        else:
            return ErrorCategory.SYSTEM
    
    def _determine_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determine error severity"""
        critical_categories = [ErrorCategory.SYSTEM, ErrorCategory.DATABASE]
        high_categories = [ErrorCategory.EXTERNAL_API, ErrorCategory.NETWORK, ErrorCategory.TIMEOUT]
        
        if category in critical_categories:
            return ErrorSeverity.CRITICAL
        elif category in high_categories:
            return ErrorSeverity.HIGH
        elif category == ErrorCategory.RATE_LIMIT:
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW
    
    def _log_error(self, error_response: StandardErrorResponse, exception: Exception):
        """Log error with appropriate level"""
        log_data = {
            "error_id": error_response.error_id,
            "category": error_response.error_category.value,
            "code": error_response.error_code,
            "severity": error_response.severity.value,
            "request_id": error_response.request_id,
            "agent_type": error_response.agent_type
        }
        
        if error_response.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"Critical error: {error_response.message}", extra=log_data, exc_info=exception)
        elif error_response.severity == ErrorSeverity.HIGH:
            logger.error(f"High severity error: {error_response.message}", extra=log_data, exc_info=exception)
        elif error_response.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"Medium severity error: {error_response.message}", extra=log_data)
        else:
            logger.info(f"Low severity error: {error_response.message}", extra=log_data)
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return {
            "service": self.service_name,
            "error_counts": {cat.value: count for cat, count in self.error_counts.items()},
            "total_errors": sum(self.error_counts.values()),
            "timestamp": datetime.now().isoformat()
        }

# Predefined error response factories
class CommonErrors:
    """Factory class for common error responses"""
    
    @staticmethod
    def authentication_required(request_id: str = None) -> StandardErrorResponse:
        """Authentication required error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.AUTHENTICATION)
                .code("AUTH_REQUIRED")
                .message("Authentication is required to access this resource")
                .severity(ErrorSeverity.MEDIUM)
                .request_id(request_id)
                .documentation("https://docs.Vidalytics.ai/authentication")
                .build())
    
    @staticmethod
    def invalid_token(request_id: str = None) -> StandardErrorResponse:
        """Invalid token error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.AUTHENTICATION)
                .code("INVALID_TOKEN")
                .message("The provided authentication token is invalid or expired")
                .severity(ErrorSeverity.HIGH)
                .request_id(request_id)
                .build())
    
    @staticmethod
    def validation_failed(errors: List[Dict[str, str]], request_id: str = None) -> StandardErrorResponse:
        """Validation failed error"""
        builder = (ErrorResponseBuilder()
                   .category(ErrorCategory.VALIDATION)
                   .code("VALIDATION_FAILED")
                   .message("Request validation failed")
                   .severity(ErrorSeverity.LOW)
                   .request_id(request_id))
        
        for error in errors:
            builder.add_detail(
                message=error.get("message", "Validation error"),
                field=error.get("field"),
                code=error.get("code")
            )
        
        return builder.build()
    
    @staticmethod
    def rate_limit_exceeded(limit_type: str, retry_after: int, request_id: str = None) -> StandardErrorResponse:
        """Rate limit exceeded error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.RATE_LIMIT)
                .code("RATE_LIMIT_EXCEEDED")
                .message(f"Rate limit exceeded for {limit_type}")
                .severity(ErrorSeverity.MEDIUM)
                .request_id(request_id)
                .retry_after(retry_after)
                .add_detail(f"Rate limit exceeded for {limit_type}", code="RATE_LIMIT")
                .build())
    
    @staticmethod
    def agent_domain_mismatch(agent_type: str, request_id: str = None) -> StandardErrorResponse:
        """Agent domain mismatch error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.AGENT_DOMAIN)
                .code("DOMAIN_MISMATCH")
                .message(f"Request is outside the domain of {agent_type} agent")
                .severity(ErrorSeverity.LOW)
                .request_id(request_id)
                .agent_type(agent_type)
                .add_detail(
                    message="This request should be handled by a different specialized agent",
                    code="WRONG_AGENT",
                    context={"suggested_action": "Route request to appropriate agent"}
                )
                .build())
    
    @staticmethod
    def external_api_error(api_name: str, status_code: int, request_id: str = None) -> StandardErrorResponse:
        """External API error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.EXTERNAL_API)
                .code("EXTERNAL_API_ERROR")
                .message(f"External API {api_name} returned an error")
                .severity(ErrorSeverity.HIGH)
                .request_id(request_id)
                .add_detail(
                    message=f"{api_name} API error (status: {status_code})",
                    code=f"API_ERROR_{status_code}",
                    context={"api_name": api_name, "status_code": status_code}
                )
                .build())
    
    @staticmethod
    def database_error(operation: str, request_id: str = None) -> StandardErrorResponse:
        """Database error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.DATABASE)
                .code("DATABASE_ERROR")
                .message(f"Database operation failed: {operation}")
                .severity(ErrorSeverity.CRITICAL)
                .request_id(request_id)
                .support_reference("database_team@Vidalytics.ai")
                .build())
    
    @staticmethod
    def processing_timeout(operation: str, timeout_seconds: int, request_id: str = None) -> StandardErrorResponse:
        """Processing timeout error"""
        return (ErrorResponseBuilder()
                .category(ErrorCategory.TIMEOUT)
                .code("PROCESSING_TIMEOUT")
                .message(f"Operation '{operation}' timed out after {timeout_seconds} seconds")
                .severity(ErrorSeverity.HIGH)
                .request_id(request_id)
                .add_detail(
                    message=f"Operation exceeded maximum processing time",
                    code="TIMEOUT", 
                    context={"operation": operation, "timeout_seconds": timeout_seconds}
                )
                .build())

# Global error handler instance
_error_handler: Optional[StandardizedErrorHandler] = None

def get_error_handler() -> StandardizedErrorHandler:
    """Get or create global error handler instance"""
    global _error_handler
    if _error_handler is None:
        _error_handler = StandardizedErrorHandler()
    return _error_handler

def handle_exception(exception: Exception, request_id: str = None, 
                    agent_type: str = None, context: Dict[str, Any] = None) -> StandardErrorResponse:
    """Convenience function to handle exceptions"""
    return get_error_handler().handle_exception(exception, request_id, agent_type, context)

def create_error_response() -> ErrorResponseBuilder:
    """Create a new error response builder"""
    return ErrorResponseBuilder()

# Decorator for automatic error handling
def handle_errors(agent_type: str = None):
    """Decorator to automatically handle and format errors"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                request_id = kwargs.get('request_id') or getattr(args[0] if args else None, 'request_id', None)
                error_response = handle_exception(e, request_id, agent_type)
                
                # For FastAPI endpoints, raise HTTPException
                try:
                    from fastapi import HTTPException
                    status_code = StandardizedErrorHandler.HTTP_STATUS_MAPPING.get(
                        error_response.error_category, 500
                    )
                    raise HTTPException(status_code=status_code, detail=error_response.to_dict())
                except ImportError:
                    # Return error response directly if FastAPI not available
                    return error_response.to_dict()
        
        return wrapper
    return decorator