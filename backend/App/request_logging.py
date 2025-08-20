"""
Request/Response Logging Middleware for MYTA
Provides comprehensive API call logging and performance tracking
"""

import time
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import asyncio

from backend.App.redis_service import get_redis_service
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)

class RequestLogger:
    """Handles request/response logging and performance tracking"""
    
    def __init__(self):
        self.redis_service = get_redis_service()
        
        # Sensitive headers to exclude from logging
        self.sensitive_headers = {
            "authorization", "cookie", "x-api-key", "x-auth-token",
            "authentication", "proxy-authorization"
        }
        
        # Endpoints to exclude from detailed logging
        self.exclude_endpoints = {
            "/health", "/metrics", "/favicon.ico", "/robots.txt"
        }
        
        # Endpoints that should not log request/response bodies
        self.exclude_body_endpoints = {
            "/api/auth/login", "/api/auth/register", "/api/settings"
        }
    
    async def log_request(self, request: Request) -> Dict[str, Any]:
        """Log incoming request and return request context"""
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Skip logging for excluded endpoints
        if any(request.url.path.startswith(endpoint) for endpoint in self.exclude_endpoints):
            return {"request_id": request_id, "start_time": start_time, "skip_logging": True}
        
        try:
            # Extract request information
            request_data = {
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "headers": self._filter_headers(dict(request.headers)),
                "client_ip": self._get_client_ip(request),
                "user_agent": request.headers.get("user-agent"),
                "timestamp": datetime.utcnow().isoformat(),
                "start_time": start_time
            }
            
            # Add request body for non-sensitive endpoints
            if not any(request.url.path.startswith(endpoint) for endpoint in self.exclude_body_endpoints):
                try:
                    if request.headers.get("content-type", "").startswith("application/json"):
                        body = await request.body()
                        if body:
                            request_data["body"] = json.loads(body.decode())
                except Exception as e:
                    request_data["body_error"] = str(e)
            
            # Log the request
            logger.info(
                f"Request: {request.method} {request.url.path}",
                extra={
                    "request_data": request_data,
                    "request_id": request_id
                }
            )
            
            # Store in Redis for correlation with response
            if self.redis_service.is_available():
                self.redis_service.set(f"request:{request_id}", request_data, 3600)  # 1 hour
            
            return {
                "request_id": request_id,
                "start_time": start_time,
                "skip_logging": False,
                "request_data": request_data
            }
        
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
            return {"request_id": request_id, "start_time": start_time, "skip_logging": True}
    
    async def log_response(self, request_context: Dict[str, Any], response: Response, 
                          error: Exception = None, user_id: str = None):
        """Log response and calculate performance metrics"""
        
        if request_context.get("skip_logging"):
            return
        
        try:
            request_id = request_context["request_id"]
            start_time = request_context["start_time"]
            end_time = time.time()
            duration_ms = round((end_time - start_time) * 1000, 2)
            
            # Extract response information
            response_data = {
                "request_id": request_id,
                "status_code": response.status_code,
                "headers": dict(response.headers) if hasattr(response, 'headers') else {},
                "duration_ms": duration_ms,
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id
            }
            
            # Add error information if present
            if error:
                response_data["error"] = {
                    "type": type(error).__name__,
                    "message": str(error)
                }
            
            # Add response body for JSON responses (excluding sensitive data)
            try:
                if (hasattr(response, 'body') and 
                    response.headers.get("content-type", "").startswith("application/json")):
                    
                    if hasattr(response, 'body'):
                        body_content = response.body
                        if isinstance(body_content, bytes):
                            body_content = body_content.decode()
                        
                        # Parse JSON and remove sensitive fields
                        try:
                            body_json = json.loads(body_content)
                            response_data["body"] = self._filter_response_body(body_json)
                        except json.JSONDecodeError:
                            response_data["body"] = body_content[:1000]  # First 1000 chars
            except Exception as e:
                response_data["body_error"] = str(e)
            
            # Determine log level based on status code
            if response.status_code >= 500:
                log_level = "error"
            elif response.status_code >= 400:
                log_level = "warning"
            else:
                log_level = "info"
            
            # Log the response
            getattr(logger, log_level)(
                f"Response: {response.status_code} - {duration_ms}ms",
                extra={
                    "response_data": response_data,
                    "request_id": request_id,
                    "duration_ms": duration_ms
                }
            )
            
            # Store performance metrics
            await self._store_performance_metrics(request_context, response_data)
            
            # Update Redis with complete request/response data
            if self.redis_service.is_available():
                complete_data = {
                    "request": request_context.get("request_data", {}),
                    "response": response_data
                }
                self.redis_service.set(f"request_complete:{request_id}", complete_data, 3600)
        
        except Exception as e:
            logger.error(f"Failed to log response: {e}")
    
    async def _store_performance_metrics(self, request_context: Dict, response_data: Dict):
        """Store performance metrics for analysis"""
        try:
            if not self.redis_service.is_available():
                return
            
            duration_ms = response_data["duration_ms"]
            status_code = response_data["status_code"]
            path = request_context.get("request_data", {}).get("path", "unknown")
            method = request_context.get("request_data", {}).get("method", "unknown")
            
            current_minute = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
            
            # Store metrics in Redis
            metrics_keys = [
                f"metrics:response_time:{current_minute}",
                f"metrics:status_code:{status_code}:{current_minute}",
                f"metrics:endpoint:{method}:{path}:{current_minute}",
                f"metrics:requests_total:{current_minute}"
            ]
            
            for key in metrics_keys:
                if "response_time" in key:
                    # Store response times for average calculation
                    self.redis_service.client.lpush(key, duration_ms)
                    self.redis_service.client.ltrim(key, 0, 999)  # Keep last 1000 entries
                else:
                    # Increment counters
                    self.redis_service.client.incr(key)
                
                # Set expiration
                self.redis_service.client.expire(key, 86400)  # 24 hours
        
        except Exception as e:
            logger.error(f"Failed to store performance metrics: {e}")
    
    def _filter_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Filter out sensitive headers"""
        return {
            key: value for key, value in headers.items()
            if key.lower() not in self.sensitive_headers
        }
    
    def _filter_response_body(self, body: Any) -> Any:
        """Filter sensitive data from response body"""
        if isinstance(body, dict):
            filtered = {}
            for key, value in body.items():
                if key.lower() in ["password", "token", "secret", "key", "auth"]:
                    filtered[key] = "[FILTERED]"
                elif isinstance(value, (dict, list)):
                    filtered[key] = self._filter_response_body(value)
                else:
                    filtered[key] = value
            return filtered
        elif isinstance(body, list):
            return [self._filter_response_body(item) for item in body]
        else:
            return body
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    def get_performance_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get performance metrics for the specified time period"""
        try:
            if not self.redis_service.is_available():
                return {"status": "unavailable"}
            
            metrics = {
                "time_period_minutes": minutes,
                "total_requests": 0,
                "average_response_time": 0,
                "status_codes": {},
                "endpoints": {},
                "response_times": []
            }
            
            current_time = datetime.utcnow()
            
            for minute_offset in range(minutes):
                minute_time = current_time.replace(second=0, microsecond=0)
                minute_key = minute_time.strftime("%Y-%m-%d-%H-%M")
                
                # Get total requests
                total_key = f"metrics:requests_total:{minute_key}"
                minute_total = self.redis_service.client.get(total_key)
                if minute_total:
                    metrics["total_requests"] += int(minute_total)
                
                # Get response times
                response_time_key = f"metrics:response_time:{minute_key}"
                response_times = self.redis_service.client.lrange(response_time_key, 0, -1)
                if response_times:
                    times = [float(t) for t in response_times]
                    metrics["response_times"].extend(times)
            
            # Calculate average response time
            if metrics["response_times"]:
                metrics["average_response_time"] = round(
                    sum(metrics["response_times"]) / len(metrics["response_times"]), 2
                )
            
            return metrics
        
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {"status": "error", "message": str(e)}

# Global request logger instance
request_logger = RequestLogger()

async def log_request_middleware(request: Request, call_next):
    """Middleware function for request/response logging"""
    
    # Log the request
    request_context = await request_logger.log_request(request)
    
    error = None
    response = None
    
    try:
        # Process the request
        response = await call_next(request)
    except Exception as e:
        error = e
        # Create error response
        response = JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"}
        )
    
    # Log the response
    await request_logger.log_response(request_context, response, error)
    
    return response
