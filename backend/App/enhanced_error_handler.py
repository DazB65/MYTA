"""
Enhanced Error Handler for Vidalytics
Provides structured error responses with proper logging and monitoring
"""

import traceback
from typing import Dict, Any, Optional, Union
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

from backend.App.exceptions import (
    VidalyticsException, ErrorCategory, ErrorSeverity,
    AuthenticationError, AuthorizationError, ValidationError,
    ExternalAPIError, DatabaseError, AgentCommunicationError,
    RateLimitError, CacheError, ConfigurationError,
    BusinessLogicError, SystemError
)
from backend.logging_config import get_logger, LogCategory


logger = get_logger(__name__, LogCategory.ERROR)


class EnhancedErrorHandler:
    """Enhanced error handler with structured responses and logging"""
    
    def __init__(self):
        self.error_mappers = {
            AuthenticationError: self._handle_authentication_error,
            AuthorizationError: self._handle_authorization_error,
            ValidationError: self._handle_validation_error,
            ExternalAPIError: self._handle_external_api_error,
            DatabaseError: self._handle_database_error,
            AgentCommunicationError: self._handle_agent_error,
            RateLimitError: self._handle_rate_limit_error,
            CacheError: self._handle_cache_error,
            ConfigurationError: self._handle_configuration_error,
            BusinessLogicError: self._handle_business_logic_error,
            SystemError: self._handle_system_error,
            VidalyticsException: self._handle_base_exception
        }
    
    def handle_exception(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle any exception and return structured response"""
        
        # Handle FastAPI validation errors
        if isinstance(exc, RequestValidationError):
            return self._handle_fastapi_validation_error(request, exc)
        
        # Handle FastAPI HTTP exceptions
        if isinstance(exc, (HTTPException, StarletteHTTPException)):
            return self._handle_http_exception(request, exc)
        
        # Handle Vidalytics specific exceptions
        for exc_type, handler in self.error_mappers.items():
            if isinstance(exc, exc_type):
                return handler(request, exc)
        
        # Handle unexpected exceptions
        return self._handle_unexpected_error(request, exc)
    
    def _handle_authentication_error(
        self,
        request: Request,
        exc: AuthenticationError
    ) -> JSONResponse:
        """Handle authentication errors"""
        self._log_security_event(request, exc)
        
        return JSONResponse(
            status_code=401,
            content=self._build_error_response(exc),
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    def _handle_authorization_error(
        self,
        request: Request,
        exc: AuthorizationError
    ) -> JSONResponse:
        """Handle authorization errors"""
        self._log_security_event(request, exc)
        
        return JSONResponse(
            status_code=403,
            content=self._build_error_response(exc)
        )
    
    def _handle_validation_error(
        self,
        request: Request,
        exc: ValidationError
    ) -> JSONResponse:
        """Handle validation errors"""
        self._log_user_error(request, exc)
        
        return JSONResponse(
            status_code=422,
            content=self._build_error_response(exc)
        )
    
    def _handle_external_api_error(
        self,
        request: Request,
        exc: ExternalAPIError
    ) -> JSONResponse:
        """Handle external API errors"""
        self._log_external_error(request, exc)
        
        # Map external API status codes
        status_code = 503  # Service Unavailable
        if hasattr(exc, 'status_code') and exc.status_code:
            if exc.status_code == 429:
                status_code = 429  # Too Many Requests
            elif 400 <= exc.status_code < 500:
                status_code = 422  # Unprocessable Entity
        
        return JSONResponse(
            status_code=status_code,
            content=self._build_error_response(exc),
            headers={"Retry-After": str(exc.retry_after)} if exc.retry_after else {}
        )
    
    def _handle_database_error(
        self,
        request: Request,
        exc: DatabaseError
    ) -> JSONResponse:
        """Handle database errors"""
        self._log_system_error(request, exc)
        
        # Don't expose database details to users
        safe_exc = SystemError(
            message="Database operation failed",
            component="database",
            user_message="Service temporarily unavailable. Please try again."
        )
        
        return JSONResponse(
            status_code=503,
            content=self._build_error_response(safe_exc)
        )
    
    def _handle_agent_error(
        self,
        request: Request,
        exc: AgentCommunicationError
    ) -> JSONResponse:
        """Handle agent communication errors"""
        self._log_agent_error(request, exc)
        
        return JSONResponse(
            status_code=503,
            content=self._build_error_response(exc)
        )
    
    def _handle_rate_limit_error(
        self,
        request: Request,
        exc: RateLimitError
    ) -> JSONResponse:
        """Handle rate limiting errors"""
        self._log_user_error(request, exc)
        
        return JSONResponse(
            status_code=429,
            content=self._build_error_response(exc),
            headers={"Retry-After": str(exc.retry_after)} if exc.retry_after else {}
        )
    
    def _handle_cache_error(
        self,
        request: Request,
        exc: CacheError
    ) -> JSONResponse:
        """Handle cache errors"""
        self._log_system_error(request, exc)
        
        # Cache errors shouldn't stop the request, but we'll log them
        # In a real implementation, you might want to continue without cache
        return JSONResponse(
            status_code=503,
            content=self._build_error_response(exc)
        )
    
    def _handle_configuration_error(
        self,
        request: Request,
        exc: ConfigurationError
    ) -> JSONResponse:
        """Handle configuration errors"""
        self._log_system_error(request, exc)
        
        return JSONResponse(
            status_code=500,
            content=self._build_error_response(exc)
        )
    
    def _handle_business_logic_error(
        self,
        request: Request,
        exc: BusinessLogicError
    ) -> JSONResponse:
        """Handle business logic errors"""
        self._log_user_error(request, exc)
        
        return JSONResponse(
            status_code=422,
            content=self._build_error_response(exc)
        )
    
    def _handle_system_error(
        self,
        request: Request,
        exc: SystemError
    ) -> JSONResponse:
        """Handle system errors"""
        self._log_system_error(request, exc)
        
        return JSONResponse(
            status_code=500,
            content=self._build_error_response(exc)
        )
    
    def _handle_base_exception(
        self,
        request: Request,
        exc: VidalyticsException
    ) -> JSONResponse:
        """Handle base Vidalytics exceptions"""
        self._log_error(request, exc)
        
        return JSONResponse(
            status_code=500,
            content=self._build_error_response(exc)
        )
    
    def _handle_fastapi_validation_error(
        self,
        request: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        """Handle FastAPI validation errors"""
        field_errors = {}
        for error in exc.errors():
            field_path = ".".join(str(x) for x in error["loc"][1:])  # Skip 'body'
            if field_path not in field_errors:
                field_errors[field_path] = []
            field_errors[field_path].append(error["msg"])
        
        validation_exc = ValidationError(
            message="Request validation failed",
            field_errors=field_errors,
            error_code="REQUEST_VALIDATION_ERROR"
        )
        
        self._log_user_error(request, validation_exc)
        
        return JSONResponse(
            status_code=422,
            content=self._build_error_response(validation_exc)
        )
    
    def _handle_http_exception(
        self,
        request: Request,
        exc: Union[HTTPException, StarletteHTTPException]
    ) -> JSONResponse:
        """Handle FastAPI HTTP exceptions"""
        # Convert to Vidalytics exception for consistent handling
        if exc.status_code == 404:
            cm_exc = BusinessLogicError(
                message="Resource not found",
                error_code="RESOURCE_NOT_FOUND",
                user_message="The requested resource was not found"
            )
        elif exc.status_code == 405:
            cm_exc = BusinessLogicError(
                message="Method not allowed",
                error_code="METHOD_NOT_ALLOWED",
                user_message="This operation is not allowed"
            )
        else:
            cm_exc = SystemError(
                message=str(exc.detail),
                error_code=f"HTTP_{exc.status_code}",
                user_message=str(exc.detail)
            )
        
        self._log_error(request, cm_exc)
        
        return JSONResponse(
            status_code=exc.status_code,
            content=self._build_error_response(cm_exc)
        )
    
    def _handle_unexpected_error(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions"""
        # Create a system error for unexpected exceptions
        system_exc = SystemError(
            message=f"Unexpected error: {type(exc).__name__}",
            component="unknown",
            error_code="UNEXPECTED_ERROR",
            user_message="An unexpected error occurred. Please try again later.",
            details={"exception_type": type(exc).__name__}
        )
        
        # Log the original exception with full traceback
        logger.error(
            f"Unexpected exception in {request.method} {request.url.path}",
            extra={
                "category": LogCategory.ERROR.value,
                "metadata": {
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "traceback": traceback.format_exc(),
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "error_id": system_exc.error_id
                }
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=500,
            content=self._build_error_response(system_exc)
        )
    
    def _build_error_response(self, exc: VidalyticsException) -> Dict[str, Any]:
        """Build structured error response"""
        response = {
            "success": False,
            "error": {
                "error_id": exc.error_id,
                "error_code": exc.error_code,
                "message": exc.user_message,
                "category": exc.category.value,
                "timestamp": exc.timestamp.isoformat()
            }
        }
        
        # Add field errors for validation errors
        if isinstance(exc, ValidationError) and exc.field_errors:
            response["error"]["field_errors"] = exc.field_errors
        
        # Add retry information if available
        if exc.retry_after:
            response["error"]["retry_after"] = exc.retry_after
        
        # Add details in development mode (you might want to make this configurable)
        import os
        if os.getenv("DEBUG", "false").lower() == "true":
            response["error"]["details"] = exc.details
            response["error"]["internal_message"] = exc.message
        
        return response
    
    def _log_security_event(self, request: Request, exc: VidalyticsException):
        """Log security-related events"""
        logger.warning(
            f"Security event: {exc.message}",
            extra={
                "category": LogCategory.SECURITY.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "error_code": exc.error_code,
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "client_ip": self._get_client_ip(request),
                    "user_agent": request.headers.get("user-agent"),
                    "details": exc.details
                }
            }
        )
    
    def _log_external_error(self, request: Request, exc: ExternalAPIError):
        """Log external API errors"""
        logger.error(
            f"External API error: {exc.service} - {exc.message}",
            extra={
                "category": LogCategory.EXTERNAL_API.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "service": exc.service,
                    "status_code": getattr(exc, 'status_code', None),
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "details": exc.details
                }
            }
        )
    
    def _log_agent_error(self, request: Request, exc: AgentCommunicationError):
        """Log agent communication errors"""
        logger.error(
            f"Agent error: {exc.agent_type} - {exc.message}",
            extra={
                "category": LogCategory.AGENT.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "agent_type": exc.agent_type,
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "details": exc.details
                }
            }
        )
    
    def _log_system_error(self, request: Request, exc: VidalyticsException):
        """Log system errors"""
        logger.error(
            f"System error: {exc.message}",
            extra={
                "category": LogCategory.SYSTEM.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "error_code": exc.error_code,
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "details": exc.details
                }
            }
        )
    
    def _log_user_error(self, request: Request, exc: VidalyticsException):
        """Log user-related errors"""
        logger.info(
            f"User error: {exc.message}",
            extra={
                "category": LogCategory.USER_ACTION.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "error_code": exc.error_code,
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "details": exc.details
                }
            }
        )
    
    def _log_error(self, request: Request, exc: VidalyticsException):
        """Log general errors"""
        log_level = {
            ErrorSeverity.LOW: logger.info,
            ErrorSeverity.MEDIUM: logger.warning,
            ErrorSeverity.HIGH: logger.error,
            ErrorSeverity.CRITICAL: logger.critical
        }.get(exc.severity, logger.error)
        
        log_level(
            f"Error: {exc.message}",
            extra={
                "category": LogCategory.ERROR.value,
                "metadata": {
                    "error_id": exc.error_id,
                    "error_code": exc.error_code,
                    "category": exc.category.value,
                    "severity": exc.severity.value,
                    "request_method": request.method,
                    "request_path": request.url.path,
                    "details": exc.details
                }
            }
        )
    
    def _get_client_ip(self, request: Request) -> Optional[str]:
        """Extract client IP from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return None


# Global error handler instance
_error_handler = EnhancedErrorHandler()


def get_error_handler() -> EnhancedErrorHandler:
    """Get global error handler instance"""
    return _error_handler


def setup_error_handlers(app):
    """Setup error handlers for FastAPI app"""
    error_handler = get_error_handler()
    
    # Add exception handlers
    app.add_exception_handler(VidalyticsException, error_handler.handle_exception)
    app.add_exception_handler(RequestValidationError, error_handler.handle_exception)
    app.add_exception_handler(HTTPException, error_handler.handle_exception)
    app.add_exception_handler(Exception, error_handler.handle_exception)