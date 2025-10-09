"""
Enhanced Error Handling System for MYTA
Provides comprehensive error tracking, categorization, and recovery mechanisms
"""

import traceback
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import json

from .redis_service import get_redis_service
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.ERROR)

class ErrorSeverity(str, Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(str, Enum):
    """Error categories for better classification"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATABASE = "database"
    EXTERNAL_API = "external_api"
    NETWORK = "network"
    SYSTEM = "system"
    BUSINESS_LOGIC = "business_logic"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"

class ErrorCode(str, Enum):
    """Standardized error codes"""
    # Validation errors (1000-1999)
    INVALID_INPUT = "1001"
    MISSING_REQUIRED_FIELD = "1002"
    INVALID_FORMAT = "1003"
    
    # Authentication errors (2000-2999)
    INVALID_CREDENTIALS = "2001"
    TOKEN_EXPIRED = "2002"
    TOKEN_INVALID = "2003"
    
    # Authorization errors (3000-3999)
    INSUFFICIENT_PERMISSIONS = "3001"
    RESOURCE_FORBIDDEN = "3002"
    
    # Database errors (4000-4999)
    DATABASE_CONNECTION_FAILED = "4001"
    QUERY_FAILED = "4002"
    CONSTRAINT_VIOLATION = "4003"
    RECORD_NOT_FOUND = "4004"
    
    # External API errors (5000-5999)
    EXTERNAL_SERVICE_UNAVAILABLE = "5001"
    API_RATE_LIMIT_EXCEEDED = "5002"
    RATE_LIMIT_EXCEEDED = "5002"  # Alias for consistency
    INVALID_API_RESPONSE = "5003"
    
    # System errors (6000-6999)
    INTERNAL_SERVER_ERROR = "6001"
    SERVICE_UNAVAILABLE = "6002"
    TIMEOUT_ERROR = "6003"
    MEMORY_ERROR = "6004"

class MYTAError(Exception):
    """Base exception class for MYTA application errors"""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Dict[str, Any] = None,
        user_message: str = None,
        recoverable: bool = True
    ):
        self.message = message
        self.error_code = error_code
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.user_message = user_message or self._get_user_friendly_message()
        self.recoverable = recoverable
        self.error_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        
        super().__init__(self.message)
    
    def _get_user_friendly_message(self) -> str:
        """Generate user-friendly error messages"""
        user_messages = {
            ErrorCode.INVALID_INPUT: "Please check your input and try again.",
            ErrorCode.MISSING_REQUIRED_FIELD: "Some required information is missing.",
            ErrorCode.INVALID_CREDENTIALS: "Invalid username or password.",
            ErrorCode.TOKEN_EXPIRED: "Your session has expired. Please log in again.",
            ErrorCode.INSUFFICIENT_PERMISSIONS: "You don't have permission to perform this action.",
            ErrorCode.DATABASE_CONNECTION_FAILED: "We're experiencing technical difficulties. Please try again later.",
            ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE: "External service is temporarily unavailable.",
            ErrorCode.INTERNAL_SERVER_ERROR: "Something went wrong on our end. We're working to fix it.",
            ErrorCode.RATE_LIMIT_EXCEEDED: "Too many requests. Please wait a moment and try again."
        }
        
        return user_messages.get(self.error_code, "An unexpected error occurred.")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging and API responses"""
        return {
            "error_id": self.error_id,
            "error_code": self.error_code.value,
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "user_message": self.user_message,
            "details": self.details,
            "recoverable": self.recoverable,
            "timestamp": self.timestamp.isoformat()
        }

class ErrorTracker:
    """Tracks and analyzes application errors"""
    
    def __init__(self):
        self.redis_service = get_redis_service()
    
    def track_error(self, error: MYTAError, request: Request = None, user_id: str = None):
        """Track an error occurrence"""
        try:
            error_data = error.to_dict()
            
            # Add request context if available
            if request:
                error_data["request"] = {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "user_agent": request.headers.get("user-agent"),
                    "ip_address": request.client.host if request.client else None
                }
            
            if user_id:
                error_data["user_id"] = user_id
            
            # Log the error
            logger.error(
                f"Error tracked: {error.error_code.value} - {error.message}",
                extra={
                    "error_data": error_data,
                    "category": error.category.value,
                    "severity": error.severity.value
                }
            )
            
            # Store in Redis for analysis
            if self.redis_service.is_available():
                # Store individual error
                error_key = f"error:{error.error_id}"
                self.redis_service.set(error_key, error_data, 86400)  # 24 hours
                
                # Update error counters
                self._update_error_counters(error)
                
                # Track error patterns
                self._track_error_patterns(error, user_id)
        
        except Exception as e:
            logger.error(f"Failed to track error: {e}")
    
    def _update_error_counters(self, error: MYTAError):
        """Update error occurrence counters"""
        try:
            current_hour = datetime.utcnow().strftime("%Y-%m-%d-%H")
            
            # Increment counters
            counters = [
                f"error_count:total:{current_hour}",
                f"error_count:category:{error.category.value}:{current_hour}",
                f"error_count:severity:{error.severity.value}:{current_hour}",
                f"error_count:code:{error.error_code.value}:{current_hour}"
            ]
            
            for counter in counters:
                self.redis_service.client.incr(counter)
                self.redis_service.client.expire(counter, 604800)  # 7 days
        
        except Exception as e:
            logger.error(f"Failed to update error counters: {e}")
    
    def _track_error_patterns(self, error: MYTAError, user_id: str = None):
        """Track error patterns for analysis"""
        try:
            if user_id:
                # Track user-specific error patterns
                user_error_key = f"user_errors:{user_id}"
                error_summary = {
                    "error_code": error.error_code.value,
                    "category": error.category.value,
                    "timestamp": error.timestamp.isoformat()
                }
                
                # Add to user error list (keep last 50)
                self.redis_service.client.lpush(user_error_key, json.dumps(error_summary))
                self.redis_service.client.ltrim(user_error_key, 0, 49)
                self.redis_service.client.expire(user_error_key, 604800)  # 7 days
        
        except Exception as e:
            logger.error(f"Failed to track error patterns: {e}")
    
    def get_error_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get error statistics for the specified time period"""
        try:
            if not self.redis_service.is_available():
                return {"status": "unavailable", "message": "Redis not available"}
            
            stats = {
                "total_errors": 0,
                "by_category": {},
                "by_severity": {},
                "by_code": {},
                "time_period_hours": hours
            }
            
            current_time = datetime.utcnow()
            
            for hour_offset in range(hours):
                hour_key = (current_time.replace(minute=0, second=0, microsecond=0)).strftime("%Y-%m-%d-%H")
                
                # Get total errors for this hour
                total_key = f"error_count:total:{hour_key}"
                hour_total = self.redis_service.client.get(total_key)
                if hour_total:
                    stats["total_errors"] += int(hour_total)
                
                # Get category breakdown
                for category in ErrorCategory:
                    cat_key = f"error_count:category:{category.value}:{hour_key}"
                    cat_count = self.redis_service.client.get(cat_key)
                    if cat_count:
                        stats["by_category"][category.value] = stats["by_category"].get(category.value, 0) + int(cat_count)
                
                # Get severity breakdown
                for severity in ErrorSeverity:
                    sev_key = f"error_count:severity:{severity.value}:{hour_key}"
                    sev_count = self.redis_service.client.get(sev_key)
                    if sev_count:
                        stats["by_severity"][severity.value] = stats["by_severity"].get(severity.value, 0) + int(sev_count)
            
            return stats
        
        except Exception as e:
            logger.error(f"Failed to get error stats: {e}")
            return {"status": "error", "message": str(e)}

# Global error tracker instance
error_tracker = ErrorTracker()

def create_error_response(error: MYTAError, request: Request = None, user_id: str = None) -> JSONResponse:
    """Create a standardized error response"""
    
    # Track the error
    error_tracker.track_error(error, request, user_id)
    
    # Determine HTTP status code
    status_code_map = {
        ErrorCategory.VALIDATION: 400,
        ErrorCategory.AUTHENTICATION: 401,
        ErrorCategory.AUTHORIZATION: 403,
        ErrorCategory.DATABASE: 500,
        ErrorCategory.EXTERNAL_API: 502,
        ErrorCategory.NETWORK: 503,
        ErrorCategory.SYSTEM: 500,
        ErrorCategory.BUSINESS_LOGIC: 422,
        ErrorCategory.RATE_LIMIT: 429,
        ErrorCategory.TIMEOUT: 504
    }
    
    status_code = status_code_map.get(error.category, 500)
    
    # Create response data
    response_data = {
        "status": "error",
        "error": {
            "code": error.error_code.value,
            "message": error.user_message,
            "category": error.category.value,
            "recoverable": error.recoverable,
            "error_id": error.error_id
        },
        "timestamp": error.timestamp.isoformat()
    }
    
    # Add details for development environment
    import os
    if os.getenv("ENVIRONMENT") == "development":
        response_data["error"]["details"] = error.details
        response_data["error"]["internal_message"] = error.message
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )

# Convenience functions for common errors
def validation_error(message: str, details: Dict = None) -> MYTAError:
    return MYTAError(
        message=message,
        error_code=ErrorCode.INVALID_INPUT,
        category=ErrorCategory.VALIDATION,
        severity=ErrorSeverity.LOW,
        details=details
    )

def authentication_error(message: str = "Authentication failed") -> MYTAError:
    return MYTAError(
        message=message,
        error_code=ErrorCode.INVALID_CREDENTIALS,
        category=ErrorCategory.AUTHENTICATION,
        severity=ErrorSeverity.MEDIUM
    )

def database_error(message: str, details: Dict = None) -> MYTAError:
    return MYTAError(
        message=message,
        error_code=ErrorCode.DATABASE_CONNECTION_FAILED,
        category=ErrorCategory.DATABASE,
        severity=ErrorSeverity.HIGH,
        details=details,
        recoverable=False
    )

def external_api_error(message: str, service: str = None) -> MYTAError:
    return MYTAError(
        message=message,
        error_code=ErrorCode.EXTERNAL_SERVICE_UNAVAILABLE,
        category=ErrorCategory.EXTERNAL_API,
        severity=ErrorSeverity.MEDIUM,
        details={"service": service} if service else None
    )
