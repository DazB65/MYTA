"""
Monitoring Middleware for CreatorMate
Provides request tracking, performance monitoring, and observability
"""

import time
import uuid
import logging
from typing import Callable, Dict, Any, Optional
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from logging_config import (
    get_logging_manager, 
    LogCategory, 
    request_id_context,
    user_id_context,
    session_id_context,
    log_performance_metrics,
    log_security_event,
    get_logger
)


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Middleware for tracking requests and performance metrics"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger(__name__, LogCategory.API)
        self.performance_logger = get_logging_manager().get_performance_logger()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request with monitoring"""
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Set request context
        get_logging_manager().set_request_context(request_id)
        
        # Extract user information if available
        user_id = await self._extract_user_id(request)
        if user_id:
            user_id_context.set(user_id)
        
        # Log request start
        self.logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                'category': LogCategory.API.value,
                'request_id': request_id,
                'metadata': {
                    'method': request.method,
                    'path': request.url.path,
                    'query_params': dict(request.query_params),
                    'user_agent': request.headers.get('user-agent'),
                    'ip_address': self._get_client_ip(request),
                    'user_id': user_id
                }
            }
        )
        
        # Process request
        response = None
        error = None
        
        try:
            response = await call_next(request)
            
        except Exception as e:
            error = e
            self.logger.error(
                f"Request failed: {request.method} {request.url.path} - {str(e)}",
                extra={
                    'category': LogCategory.ERROR.value,
                    'request_id': request_id,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            
            # Create error response
            response = JSONResponse(
                status_code=500,
                content={'error': 'Internal server error', 'request_id': request_id}
            )
        
        finally:
            # Calculate metrics
            duration_ms = (time.time() - start_time) * 1000
            status_code = response.status_code if response else 500
            
            # Add request ID to response headers
            if response:
                response.headers['X-Request-ID'] = request_id
            
            # Log request completion
            log_level = logging.ERROR if error or status_code >= 400 else logging.INFO
            self.logger.log(
                log_level,
                f"Request completed: {request.method} {request.url.path} "
                f"{status_code} in {duration_ms:.1f}ms",
                extra={
                    'category': LogCategory.API.value,
                    'request_id': request_id,
                    'duration_ms': duration_ms,
                    'metadata': {
                        'status_code': status_code,
                        'response_size': self._get_response_size(response),
                        'success': error is None and status_code < 400
                    }
                }
            )
            
            # Log performance metrics
            log_performance_metrics(
                'http_request',
                method=request.method,
                path=request.url.path,
                status_code=status_code,
                duration_ms=duration_ms,
                request_size=await self._get_request_size(request),
                response_size=self._get_response_size(response),
                user_id=user_id
            )
            
            # Log security events for suspicious requests
            await self._check_security_events(request, response, duration_ms)
            
            # Clear request context
            get_logging_manager().clear_request_context()
        
        return response
    
    async def _extract_user_id(self, request: Request) -> Optional[str]:
        """Extract user ID from request if available"""
        try:
            # Try to get from Authorization header
            auth_header = request.headers.get('authorization')
            if auth_header and auth_header.startswith('Bearer '):
                # This would require importing auth middleware
                # For now, just return None
                pass
            
            # Try to get from request state (set by auth middleware)
            return getattr(request.state, 'user_id', None)
            
        except Exception:
            return None
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get('x-forwarded-for')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        forwarded = request.headers.get('x-forwarded')
        if forwarded:
            return forwarded.split(',')[0].strip()
        
        real_ip = request.headers.get('x-real-ip')
        if real_ip:
            return real_ip
        
        # Fallback to direct client
        if hasattr(request, 'client') and request.client:
            return request.client.host
        
        return 'unknown'
    
    async def _get_request_size(self, request: Request) -> int:
        """Get request body size"""
        try:
            content_length = request.headers.get('content-length')
            if content_length:
                return int(content_length)
        except (ValueError, TypeError):
            pass
        
        return 0
    
    def _get_response_size(self, response: Response) -> int:
        """Get response body size"""
        try:
            if hasattr(response, 'headers') and 'content-length' in response.headers:
                return int(response.headers['content-length'])
            
            if hasattr(response, 'body') and response.body:
                return len(response.body)
                
        except (ValueError, TypeError, AttributeError):
            pass
        
        return 0
    
    async def _check_security_events(self, request: Request, response: Response, duration_ms: float):
        """Check for security events and log them"""
        try:
            # Check for slow requests (potential DoS)
            if duration_ms > 30000:  # 30 seconds
                log_security_event(
                    'slow_request',
                    f"Very slow request: {request.method} {request.url.path} took {duration_ms:.1f}ms",
                    severity='WARNING',
                    ip_address=self._get_client_ip(request),
                    additional_info={
                        'duration_ms': duration_ms,
                        'path': request.url.path,
                        'method': request.method
                    }
                )
            
            # Check for potential attacks based on status codes
            if response and response.status_code == 404:
                # Log potential path traversal attempts
                path = request.url.path
                if '..' in path or path.startswith('/admin') or path.startswith('/.'):
                    log_security_event(
                        'suspicious_path',
                        f"Suspicious path access attempt: {path}",
                        severity='WARNING',
                        ip_address=self._get_client_ip(request),
                        additional_info={'path': path}
                    )
            
            # Check for too many requests from same IP (basic rate limiting detection)
            # This would require a more sophisticated implementation with redis/memory cache
            
        except Exception as e:
            self.logger.error(f"Error checking security events: {e}")


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Middleware for health check and system monitoring"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger(__name__, LogCategory.SYSTEM)
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Track system health metrics"""
        self.request_count += 1
        
        try:
            response = await call_next(request)
            
            if response.status_code >= 500:
                self.error_count += 1
                
                # Log system error
                self.logger.error(
                    f"System error: {response.status_code} for {request.url.path}",
                    extra={
                        'category': LogCategory.SYSTEM.value,
                        'metadata': {
                            'status_code': response.status_code,
                            'path': request.url.path,
                            'total_requests': self.request_count,
                            'total_errors': self.error_count,
                            'error_rate': self.error_count / self.request_count
                        }
                    }
                )
            
            return response
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(
                f"Unhandled system error: {str(e)}",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'total_requests': self.request_count,
                        'total_errors': self.error_count
                    }
                },
                exc_info=True
            )
            raise
    
    def get_health_stats(self) -> Dict[str, Any]:
        """Get current health statistics"""
        uptime_seconds = time.time() - self.start_time
        
        return {
            'uptime_seconds': uptime_seconds,
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate': self.error_count / max(self.request_count, 1),
            'requests_per_second': self.request_count / max(uptime_seconds, 1)
        }


class AgentMonitoringMiddleware:
    """Middleware specifically for monitoring AI agent operations"""
    
    def __init__(self):
        self.logger = get_logger(__name__, LogCategory.AGENT)
        self.performance_logger = get_logging_manager().get_performance_logger()
    
    async def log_agent_request(self, agent_type: str, operation: str, 
                               request_data: Dict[str, Any], user_id: str = None):
        """Log agent request start"""
        self.logger.info(
            f"Agent request: {agent_type} {operation}",
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': user_id,
                'metadata': {
                    'agent_type': agent_type,
                    'operation': operation,
                    'request_size': len(str(request_data)),
                    'has_context': bool(request_data.get('context')),
                    'analysis_depth': request_data.get('analysis_depth', 'standard')
                }
            }
        )
    
    async def log_agent_response(self, agent_type: str, operation: str,
                                response_data: Dict[str, Any], duration_ms: float,
                                success: bool = True, error: Exception = None,
                                user_id: str = None):
        """Log agent response completion"""
        
        # Extract token usage if available
        token_usage = response_data.get('token_usage', {})
        
        log_level = logging.ERROR if error else logging.INFO
        message = f"Agent response: {agent_type} {operation} "
        message += f"{'✓' if success else '✗'} {duration_ms:.1f}ms"
        
        if token_usage:
            total_tokens = token_usage.get('total_tokens', 0)
            message += f" ({total_tokens} tokens)"
        
        self.logger.log(
            log_level,
            message,
            extra={
                'category': LogCategory.AGENT.value,
                'user_id': user_id,
                'duration_ms': duration_ms,
                'metadata': {
                    'agent_type': agent_type,
                    'operation': operation,
                    'success': success,
                    'token_usage': token_usage,
                    'response_size': len(str(response_data)),
                    'confidence_score': response_data.get('confidence_score'),
                    'error_type': type(error).__name__ if error else None,
                    'error_message': str(error) if error else None
                }
            },
            exc_info=error is not None
        )
        
        # Log performance metrics
        log_performance_metrics(
            'agent_operation',
            agent_type=agent_type,
            operation=operation,
            duration_ms=duration_ms,
            token_usage=token_usage,
            success=success,
            user_id=user_id
        )


# Context manager for agent monitoring
@asynccontextmanager
async def monitor_agent_operation(agent_type: str, operation: str, 
                                request_data: Dict[str, Any], user_id: str = None):
    """Context manager for monitoring agent operations"""
    monitor = AgentMonitoringMiddleware()
    start_time = time.time()
    
    await monitor.log_agent_request(agent_type, operation, request_data, user_id)
    
    try:
        yield monitor
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        await monitor.log_agent_response(
            agent_type, operation, {}, duration_ms, 
            success=False, error=e, user_id=user_id
        )
        raise
    
    else:
        duration_ms = (time.time() - start_time) * 1000
        # Note: response data should be logged by the caller
        # This is just to ensure we have a completion log if response logging is missed


# Database operation monitoring
class DatabaseMonitor:
    """Monitor for database operations"""
    
    def __init__(self):
        self.logger = get_logger(__name__, LogCategory.DATABASE)
        self.performance_logger = get_logging_manager().get_performance_logger()
    
    def log_query(self, operation: str, table: str, query: str, 
                 duration_ms: float, rows_affected: int = 0, 
                 success: bool = True, error: Exception = None):
        """Log database query execution"""
        
        log_level = logging.ERROR if error else logging.DEBUG
        message = f"DB {operation} {table} {rows_affected} rows {duration_ms:.1f}ms"
        
        self.logger.log(
            log_level,
            message,
            extra={
                'category': LogCategory.DATABASE.value,
                'duration_ms': duration_ms,
                'metadata': {
                    'operation': operation,
                    'table': table,
                    'query_hash': hash(query) % 10000,  # Hash for privacy
                    'rows_affected': rows_affected,
                    'success': success,
                    'error_type': type(error).__name__ if error else None
                }
            },
            exc_info=error is not None
        )
        
        # Log performance metrics
        log_performance_metrics(
            'database_operation',
            operation=operation,
            table=table,
            duration_ms=duration_ms,
            rows_affected=rows_affected,
            success=success
        )


# Global instances
_health_middleware: Optional[HealthCheckMiddleware] = None
_agent_monitor: Optional[AgentMonitoringMiddleware] = None
_db_monitor: Optional[DatabaseMonitor] = None


def get_health_middleware() -> HealthCheckMiddleware:
    """Get global health middleware instance"""
    global _health_middleware
    if _health_middleware is None:
        _health_middleware = HealthCheckMiddleware(None)
    return _health_middleware


def get_agent_monitor() -> AgentMonitoringMiddleware:
    """Get global agent monitor instance"""
    global _agent_monitor
    if _agent_monitor is None:
        _agent_monitor = AgentMonitoringMiddleware()
    return _agent_monitor


def get_database_monitor() -> DatabaseMonitor:
    """Get global database monitor instance"""
    global _db_monitor
    if _db_monitor is None:
        _db_monitor = DatabaseMonitor()
    return _db_monitor


def setup_monitoring_middleware(app: FastAPI) -> None:
    """Set up all monitoring middleware for FastAPI app"""
    
    # Add request tracking middleware
    app.add_middleware(RequestTrackingMiddleware)
    
    # Add health check middleware
    global _health_middleware
    _health_middleware = HealthCheckMiddleware(None)
    app.add_middleware(type(_health_middleware))
    
    # Add health check endpoint
    @app.get("/health/detailed")
    async def detailed_health():
        """Detailed health check endpoint"""
        stats = _health_middleware.get_health_stats() if _health_middleware else {}
        
        return {
            "status": "healthy" if stats.get('error_rate', 0) < 0.1 else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "stats": stats,
            "version": "1.0.0",  # Get from config
            "environment": str(get_logging_manager().settings.environment)
        }
    
    # Log middleware setup
    logger = get_logger(__name__, LogCategory.SYSTEM)
    logger.info(
        "Monitoring middleware configured",
        extra={
            'category': LogCategory.SYSTEM.value,
            'metadata': {
                'middleware_count': len(app.user_middleware),
                'environment': str(get_logging_manager().settings.environment)
            }
        }
    )