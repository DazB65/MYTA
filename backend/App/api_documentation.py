"""
Enhanced API Documentation System for MYTA
Provides comprehensive API documentation with examples and versioning
"""

from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional, List
import json
from datetime import datetime

class APIDocumentationConfig:
    """Configuration for API documentation"""
    
    def __init__(self):
        self.title = "MYTA - My YouTube Agent API"
        self.description = """
        ## MYTA API Documentation
        
        Welcome to the MYTA (My YouTube Agent) API! This comprehensive API provides powerful tools for YouTube content creators to analyze, optimize, and grow their channels using AI-powered insights.
        
        ### Key Features
        
        - **AI-Powered Analysis**: Get intelligent insights about your YouTube content
        - **Multi-Agent System**: Specialized AI agents for different aspects of content optimization
        - **Real-time Analytics**: Live data from YouTube API with caching for performance
        - **Background Processing**: Heavy operations handled asynchronously
        - **Circuit Breaker Protection**: Fault-tolerant external API integration
        
        ### Authentication
        
        All API endpoints require authentication using JWT tokens. Include your token in the Authorization header:
        ```
        Authorization: Bearer your_jwt_token_here
        ```
        
        ### Rate Limiting
        
        API requests are rate-limited based on your subscription tier:
        - **Free Tier**: 100 requests/hour
        - **Pro Tier**: 1,000 requests/hour  
        - **Enterprise Tier**: 10,000 requests/hour
        
        ### API Versioning
        
        This API supports versioning through multiple methods:
        1. **URL Path**: `/api/v2/endpoint`
        2. **Accept Header**: `Accept: application/vnd.myta.v2+json`
        3. **Query Parameter**: `?version=v2`
        
        Current version: **v2** (recommended)
        Supported versions: v1 (deprecated), v2
        
        ### Error Handling
        
        The API uses standard HTTP status codes and returns detailed error information:
        
        ```json
        {
          "status": "error",
          "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input parameters",
            "details": {
              "field": "video_id",
              "reason": "Required field missing"
            }
          },
          "metadata": {
            "version": "v2",
            "timestamp": "2024-01-15T10:30:00Z",
            "request_id": "req_123456"
          }
        }
        ```
        
        ### SDKs and Libraries
        
        Official SDKs are available for:
        - **Python**: `pip install myta-python`
        - **JavaScript/Node.js**: `npm install myta-js`
        - **PHP**: `composer require myta/php-sdk`
        
        ### Support
        
        - **Documentation**: [https://docs.myytagent.app](https://docs.myytagent.app)
        - **Support**: [support@myytagent.app](mailto:support@myytagent.app)
        - **Status Page**: [https://status.myytagent.app](https://status.myytagent.app)
        """
        self.version = "2.0.0"
        self.contact = {
            "name": "MYTA Support",
            "email": "support@myytagent.app",
            "url": "https://myytagent.app/support"
        }
        self.license_info = {
            "name": "Proprietary",
            "url": "https://myytagent.app/terms"
        }
        self.servers = [
            {
                "url": "https://api.myytagent.app",
                "description": "Production server"
            },
            {
                "url": "https://staging-api.myytagent.app", 
                "description": "Staging server"
            },
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            }
        ]

def create_custom_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """Create enhanced OpenAPI schema with custom documentation"""
    config = APIDocumentationConfig()
    
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=config.title,
        version=config.version,
        description=config.description,
        routes=app.routes,
        servers=config.servers
    )
    
    # Add contact and license information
    openapi_schema["info"]["contact"] = config.contact
    openapi_schema["info"]["license"] = config.license_info
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for authentication"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key for service-to-service authentication"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"ApiKeyAuth": []}
    ]
    
    # Add custom tags with descriptions
    openapi_schema["tags"] = [
        {
            "name": "Authentication",
            "description": "User authentication and session management"
        },
        {
            "name": "AI Agents",
            "description": "AI-powered content analysis and optimization agents"
        },
        {
            "name": "YouTube Analytics",
            "description": "YouTube data fetching and analytics processing"
        },
        {
            "name": "Background Jobs",
            "description": "Asynchronous task processing and job management"
        },
        {
            "name": "User Management",
            "description": "User profile and subscription management"
        },
        {
            "name": "Health & Monitoring",
            "description": "System health checks and monitoring endpoints"
        }
    ]
    
    # Add examples to common response schemas
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}
    
    # Add common response schemas
    openapi_schema["components"]["schemas"].update({
        "SuccessResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "success"},
                "data": {"type": "object", "description": "Response data"},
                "message": {"type": "string", "example": "Operation completed successfully"},
                "metadata": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "string", "example": "v2"},
                        "timestamp": {"type": "string", "format": "date-time"},
                        "request_id": {"type": "string", "example": "req_123456"}
                    }
                }
            },
            "required": ["status", "data"]
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "error"},
                "error": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "example": "VALIDATION_ERROR"},
                        "message": {"type": "string", "example": "Invalid input parameters"},
                        "details": {"type": "object", "description": "Additional error details"}
                    },
                    "required": ["code", "message"]
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "version": {"type": "string", "example": "v2"},
                        "timestamp": {"type": "string", "format": "date-time"},
                        "request_id": {"type": "string", "example": "req_123456"}
                    }
                }
            },
            "required": ["status", "error"]
        },
        "PaginatedResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "success"},
                "data": {
                    "type": "array",
                    "items": {"type": "object"}
                },
                "pagination": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "limit": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 100},
                        "pages": {"type": "integer", "example": 5},
                        "has_next": {"type": "boolean", "example": True},
                        "has_prev": {"type": "boolean", "example": False}
                    }
                }
            }
        }
    })
    
    # Add rate limiting information
    openapi_schema["info"]["x-rate-limiting"] = {
        "free": "100 requests/hour",
        "pro": "1,000 requests/hour", 
        "enterprise": "10,000 requests/hour"
    }
    
    # Add webhook information
    openapi_schema["info"]["x-webhooks"] = {
        "description": "MYTA supports webhooks for real-time notifications",
        "events": [
            "video.analyzed",
            "channel.audit.completed",
            "subscription.updated",
            "job.completed"
        ]
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_api_documentation(app: FastAPI):
    """Setup enhanced API documentation"""
    
    @app.get("/openapi.json", include_in_schema=False)
    async def get_openapi_endpoint():
        return create_custom_openapi_schema(app)
    
    @app.get("/docs", include_in_schema=False)
    async def get_swagger_documentation():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="MYTA API Documentation",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
            swagger_favicon_url="https://myytagent.app/favicon.ico"
        )
    
    @app.get("/redoc", include_in_schema=False)
    async def get_redoc_documentation():
        return get_redoc_html(
            openapi_url="/openapi.json",
            title="MYTA API Documentation",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
            redoc_favicon_url="https://myytagent.app/favicon.ico"
        )
    
    @app.get("/api-status", include_in_schema=False)
    async def get_api_status():
        """Get API status and health information"""
        return {
            "status": "operational",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "operational",
                "redis": "operational", 
                "openai": "operational",
                "youtube": "operational"
            },
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc",
                "openapi": "/openapi.json"
            }
        }

# Example usage in main.py:
"""
from fastapi import FastAPI
from .api_documentation import setup_api_documentation

app = FastAPI()
setup_api_documentation(app)
"""
