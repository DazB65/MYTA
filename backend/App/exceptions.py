"""
Enhanced Exception Handling for Vidalytics
Provides specific exception types and structured error responses
"""

from typing import Optional, Dict, Any, List
from enum import Enum
import uuid
from datetime import datetime


class ErrorCategory(Enum):
    """Error categories for classification"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    EXTERNAL_API = "external_api"
    DATABASE = "database"
    AGENT_COMMUNICATION = "agent_communication"
    RATE_LIMIT = "rate_limit"
    CACHE = "cache"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class VidalyticsException(Exception):
    """Base exception for all Vidalytics-specific errors"""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None,
        retry_after: Optional[int] = None
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.error_code = error_code or f"{category.value.upper()}_ERROR"
        self.details = details or {}
        self.user_message = user_message or "An error occurred. Please try again."
        self.retry_after = retry_after
        self.error_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/response"""
        return {
            "error_id": self.error_id,
            "error_code": self.error_code,
            "message": self.message,
            "user_message": self.user_message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "retry_after": self.retry_after,
            "timestamp": self.timestamp.isoformat()
        }


# Authentication & Authorization Exceptions
class AuthenticationError(VidalyticsException):
    """Authentication failed"""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            user_message="Please log in to continue",
            **kwargs
        )


class AuthorizationError(VidalyticsException):
    """User lacks required permissions"""
    
    def __init__(self, message: str = "Insufficient permissions", **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            user_message="You don't have permission to perform this action",
            **kwargs
        )


class TokenExpiredError(AuthenticationError):
    """Authentication token has expired"""
    
    def __init__(self, message: str = "Authentication token expired", **kwargs):
        super().__init__(
            message=message,
            error_code="TOKEN_EXPIRED",
            user_message="Your session has expired. Please log in again",
            **kwargs
        )


class InvalidTokenError(AuthenticationError):
    """Invalid authentication token"""
    
    def __init__(self, message: str = "Invalid authentication token", **kwargs):
        super().__init__(
            message=message,
            error_code="INVALID_TOKEN",
            user_message="Invalid authentication. Please log in again",
            **kwargs
        )


# Validation Exceptions
class ValidationError(VidalyticsException):
    """Data validation failed"""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ):
        self.field_errors = field_errors or {}
        super().__init__(
            message=message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            details={"field_errors": self.field_errors},
            user_message="Please check your input and try again",
            **kwargs
        )


class RequiredFieldError(ValidationError):
    """Required field is missing"""
    
    def __init__(self, field_name: str, **kwargs):
        super().__init__(
            message=f"Required field '{field_name}' is missing",
            error_code="REQUIRED_FIELD_MISSING",
            field_errors={field_name: ["This field is required"]},
            user_message=f"Please provide a value for {field_name}",
            **kwargs
        )


class InvalidFieldValueError(ValidationError):
    """Field value is invalid"""
    
    def __init__(self, field_name: str, value: Any, expected: str, **kwargs):
        super().__init__(
            message=f"Invalid value for field '{field_name}': {value}. Expected: {expected}",
            error_code="INVALID_FIELD_VALUE",
            field_errors={field_name: [f"Expected {expected}, got {type(value).__name__}"]},
            user_message=f"Invalid value for {field_name}",
            **kwargs
        )


# External API Exceptions
class ExternalAPIError(VidalyticsException):
    """External API call failed"""
    
    def __init__(
        self,
        service: str,
        message: str = "External service error",
        status_code: Optional[int] = None,
        **kwargs
    ):
        self.service = service
        self.status_code = status_code
        super().__init__(
            message=f"{service}: {message}",
            category=ErrorCategory.EXTERNAL_API,
            severity=ErrorSeverity.HIGH,
            details={"service": service, "status_code": status_code},
            user_message="External service temporarily unavailable. Please try again later",
            **kwargs
        )


class YouTubeAPIError(ExternalAPIError):
    """YouTube API specific error"""
    
    def __init__(self, message: str = "YouTube API error", **kwargs):
        super().__init__(
            service="YouTube API",
            message=message,
            error_code="YOUTUBE_API_ERROR",
            **kwargs
        )


class OpenAIAPIError(ExternalAPIError):
    """OpenAI API specific error"""
    
    def __init__(self, message: str = "OpenAI API error", **kwargs):
        super().__init__(
            service="OpenAI API",
            message=message,
            error_code="OPENAI_API_ERROR",
            **kwargs
        )


class GoogleAIAPIError(ExternalAPIError):
    """Google AI API specific error"""
    
    def __init__(self, message: str = "Google AI API error", **kwargs):
        super().__init__(
            service="Google AI API",
            message=message,
            error_code="GOOGLE_AI_API_ERROR",
            **kwargs
        )


# Database Exceptions
class DatabaseError(VidalyticsException):
    """Database operation failed"""
    
    def __init__(self, message: str = "Database error", operation: str = "unknown", **kwargs):
        self.operation = operation
        super().__init__(
            message=f"Database {operation}: {message}",
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            details={"operation": operation},
            user_message="Database temporarily unavailable. Please try again",
            **kwargs
        )


class RecordNotFoundError(DatabaseError):
    """Database record not found"""
    
    def __init__(self, entity: str, identifier: Any, **kwargs):
        super().__init__(
            message=f"{entity} not found: {identifier}",
            operation="select",
            error_code="RECORD_NOT_FOUND",
            details={"entity": entity, "identifier": str(identifier)},
            user_message=f"{entity} not found",
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )


class DatabaseConnectionError(DatabaseError):
    """Database connection failed"""
    
    def __init__(self, message: str = "Database connection failed", **kwargs):
        super().__init__(
            message=message,
            operation="connect",
            error_code="DATABASE_CONNECTION_ERROR",
            severity=ErrorSeverity.CRITICAL,
            user_message="Service temporarily unavailable",
            **kwargs
        )


# Agent Communication Exceptions
class AgentCommunicationError(VidalyticsException):
    """Agent communication failed"""
    
    def __init__(
        self,
        agent_type: str,
        message: str = "Agent communication failed",
        **kwargs
    ):
        self.agent_type = agent_type
        super().__init__(
            message=f"{agent_type}: {message}",
            category=ErrorCategory.AGENT_COMMUNICATION,
            severity=ErrorSeverity.HIGH,
            details={"agent_type": agent_type},
            user_message="AI service temporarily unavailable. Please try again",
            **kwargs
        )


class AgentTimeoutError(AgentCommunicationError):
    """Agent request timed out"""
    
    def __init__(self, agent_type: str, timeout_seconds: int, **kwargs):
        super().__init__(
            agent_type=agent_type,
            message=f"Request timed out after {timeout_seconds} seconds",
            error_code="AGENT_TIMEOUT",
            details={"timeout_seconds": timeout_seconds},
            **kwargs
        )


class AgentAuthenticationError(AgentCommunicationError):
    """Agent authentication failed"""
    
    def __init__(self, agent_type: str, **kwargs):
        super().__init__(
            agent_type=agent_type,
            message="Agent authentication failed",
            error_code="AGENT_AUTH_ERROR",
            severity=ErrorSeverity.CRITICAL,
            **kwargs
        )


# Rate Limiting Exceptions
class RateLimitError(VidalyticsException):
    """Rate limit exceeded"""
    
    def __init__(
        self,
        limit: int,
        window: int,
        retry_after: int,
        resource: str = "API",
        **kwargs
    ):
        super().__init__(
            message=f"Rate limit exceeded: {limit} requests per {window} seconds",
            category=ErrorCategory.RATE_LIMIT,
            severity=ErrorSeverity.MEDIUM,
            error_code="RATE_LIMIT_EXCEEDED",
            details={"limit": limit, "window": window, "resource": resource},
            user_message=f"Too many requests. Please wait {retry_after} seconds",
            retry_after=retry_after,
            **kwargs
        )


# Cache Exceptions
class CacheError(VidalyticsException):
    """Cache operation failed"""
    
    def __init__(self, message: str = "Cache error", operation: str = "unknown", **kwargs):
        super().__init__(
            message=f"Cache {operation}: {message}",
            category=ErrorCategory.CACHE,
            severity=ErrorSeverity.MEDIUM,
            details={"operation": operation},
            user_message="Temporary performance issue. Please try again",
            **kwargs
        )


class CacheConnectionError(CacheError):
    """Cache connection failed"""
    
    def __init__(self, message: str = "Cache connection failed", **kwargs):
        super().__init__(
            message=message,
            operation="connect",
            error_code="CACHE_CONNECTION_ERROR",
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


# Configuration Exceptions
class ConfigurationError(VidalyticsException):
    """Configuration error"""
    
    def __init__(self, message: str = "Configuration error", config_key: str = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.CRITICAL,
            error_code="CONFIGURATION_ERROR",
            details={"config_key": config_key} if config_key else {},
            user_message="Service configuration issue. Please contact support",
            **kwargs
        )


class MissingConfigurationError(ConfigurationError):
    """Required configuration is missing"""
    
    def __init__(self, config_key: str, **kwargs):
        super().__init__(
            message=f"Missing required configuration: {config_key}",
            config_key=config_key,
            error_code="MISSING_CONFIGURATION",
            **kwargs
        )


# Business Logic Exceptions
class BusinessLogicError(VidalyticsException):
    """Business rule violation"""
    
    def __init__(self, message: str = "Business rule violation", rule: str = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.BUSINESS_LOGIC,
            severity=ErrorSeverity.MEDIUM,
            details={"rule": rule} if rule else {},
            **kwargs
        )


class InsufficientDataError(BusinessLogicError):
    """Insufficient data for operation"""
    
    def __init__(self, required_data: str, **kwargs):
        super().__init__(
            message=f"Insufficient data: {required_data}",
            error_code="INSUFFICIENT_DATA",
            user_message=f"Please provide {required_data} to continue",
            **kwargs
        )


class OperationNotAllowedError(BusinessLogicError):
    """Operation not allowed in current state"""
    
    def __init__(self, operation: str, current_state: str, **kwargs):
        super().__init__(
            message=f"Operation '{operation}' not allowed in state '{current_state}'",
            error_code="OPERATION_NOT_ALLOWED",
            details={"operation": operation, "current_state": current_state},
            user_message=f"Cannot {operation} in current state",
            **kwargs
        )


# System Exceptions
class SystemError(VidalyticsException):
    """System error"""
    
    def __init__(self, message: str = "System error", component: str = None, **kwargs):
        super().__init__(
            message=message,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            details={"component": component} if component else {},
            user_message="System temporarily unavailable. Please try again later",
            **kwargs
        )


class ServiceUnavailableError(SystemError):
    """Service is unavailable"""
    
    def __init__(self, service: str, **kwargs):
        super().__init__(
            message=f"Service unavailable: {service}",
            component=service,
            error_code="SERVICE_UNAVAILABLE",
            user_message=f"{service} is temporarily unavailable",
            **kwargs
        )


class MaintenanceModeError(SystemError):
    """System is in maintenance mode"""
    
    def __init__(self, **kwargs):
        super().__init__(
            message="System is in maintenance mode",
            error_code="MAINTENANCE_MODE",
            user_message="System is temporarily down for maintenance. Please try again later",
            **kwargs
        )