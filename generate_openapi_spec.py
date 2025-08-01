#!/usr/bin/env python3
"""
OpenAPI Specification Generator for Vidalytics API
Generates comprehensive OpenAPI 3.0 specification with examples and validation
"""

import json
import yaml
import sys
import os
from typing import Dict, Any
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def generate_openapi_spec() -> Dict[str, Any]:
    """Generate comprehensive OpenAPI 3.0 specification"""
    
    spec = {
        "openapi": "3.0.3",
        "info": {
            "title": "Vidalytics Multi-Agent API",
            "version": "2.0.0",
            "description": """
**Vidalytics** is a sophisticated hierarchical multi-agent system designed for YouTube content creators 
to optimize their channel performance, content strategy, and audience engagement.

## Key Features

* **🤖 Multi-Agent Architecture**: Specialized AI agents for different aspects of content optimization
* **📊 YouTube Analytics**: Deep integration with YouTube Data API for comprehensive analytics
* **🎯 Content Pillars**: Strategic content organization and planning system
* **🔐 Session Management**: Secure Redis-based session handling
* **⚡ Real-time Chat**: Interactive AI-powered content advisory
* **📈 Performance Monitoring**: Advanced metrics and health monitoring

## Agent System

The system consists of specialized agents:
- **Boss Agent**: Central orchestrator using Claude 3.5 Sonnet
- **Content Analysis Agent**: Video performance analysis using Gemini 2.5 Pro
- **Audience Insights Agent**: Demographics and sentiment analysis using Claude 3.5 Sonnet
- **SEO & Discoverability Agent**: Search optimization using Claude 3.5 Haiku
- **Competitive Analysis Agent**: Market positioning using Gemini 2.5 Pro
- **Monetization Strategy Agent**: Revenue optimization using Claude 3.5 Haiku

## Authentication

The API uses Redis-based session management. Most endpoints require authentication.
Use the `/api/session/login` endpoint to create a session.
            """,
            "summary": "AI-powered YouTube optimization platform",
            "contact": {
                "name": "Vidalytics Support",
                "url": "https://github.com/Vidalytics/api",
                "email": "support@Vidalytics.com"
            },
            "license": {
                "name": "MIT License",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "http://localhost:8888",
                "description": "Development server"
            },
            {
                "url": "https://api.Vidalytics.com",
                "description": "Production server"
            }
        ],
        "security": [
            {
                "SessionCookie": []
            },
            {
                "BearerAuth": []
            }
        ],
        "tags": [
            {
                "name": "agent",
                "description": "Multi-agent system operations including chat, quick actions, and specialized agent interactions."
            },
            {
                "name": "session",
                "description": "Redis-based session management for secure authentication and user state."
            },
            {
                "name": "youtube",
                "description": "YouTube Data API integration for analytics, video data, and OAuth authentication."
            },
            {
                "name": "pillars",
                "description": "Content pillars management for strategic content organization and planning."
            },
            {
                "name": "analytics",
                "description": "Dashboard analytics and performance metrics for data-driven insights."
            },
            {
                "name": "oauth",
                "description": "OAuth 2.0 authentication flow for YouTube and other third-party integrations."
            },
            {
                "name": "content-cards",
                "description": "Content Studio functionality for content creation and management workflows."
            },
            {
                "name": "health",
                "description": "System health checks and monitoring endpoints for operational oversight."
            },
            {
                "name": "auth",
                "description": "User authentication and authorization endpoints."
            }
        ],
        "components": {
            "securitySchemes": {
                "SessionCookie": {
                    "type": "apiKey",
                    "in": "cookie",
                    "name": "Vidalytics_session",
                    "description": "Session-based authentication using secure HTTP-only cookies"
                },
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "description": "Bearer token authentication using session ID"
                }
            },
            "schemas": generate_schemas(),
            "responses": generate_common_responses(),
            "parameters": generate_common_parameters(),
            "examples": generate_examples()
        },
        "paths": generate_paths()
    }
    
    return spec


def generate_schemas() -> Dict[str, Any]:
    """Generate common schema definitions"""
    return {
        "StandardResponse": {
            "type": "object",
            "required": ["success", "message", "timestamp"],
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Indicates if the request was successful"
                },
                "message": {
                    "type": "string",
                    "description": "Human-readable message describing the result"
                },
                "data": {
                    "type": "object",
                    "description": "Response data (structure varies by endpoint)"
                },
                "error": {
                    "$ref": "#/components/schemas/ErrorDetails"
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time",
                    "description": "ISO 8601 timestamp of the response"
                }
            }
        },
        "ErrorDetails": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Error code for programmatic handling"
                },
                "details": {
                    "type": "string",
                    "description": "Detailed error description"
                },
                "field": {
                    "type": "string",
                    "description": "Field name for validation errors"
                }
            }
        },
        "SessionData": {
            "type": "object",
            "required": ["session_id", "user_id", "created_at", "last_accessed", "expires_at", "status"],
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "Unique session identifier"
                },
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Session creation timestamp"
                },
                "last_accessed": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Last access timestamp"
                },
                "expires_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Session expiry timestamp"
                },
                "status": {
                    "type": "string",
                    "enum": ["active", "expired", "revoked"],
                    "description": "Session status"
                },
                "ip_address": {
                    "type": "string",
                    "description": "Client IP address"
                },
                "user_agent": {
                    "type": "string",
                    "description": "Client user agent"
                },
                "permissions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "User permissions"
                },
                "metadata": {
                    "type": "object",
                    "description": "Custom session metadata"
                }
            }
        },
        "LoginRequest": {
            "type": "object",
            "required": ["user_id"],
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "password": {
                    "type": "string",
                    "description": "User password (for demo purposes)"
                },
                "remember_me": {
                    "type": "boolean",
                    "default": False,
                    "description": "Extended session duration"
                },
                "metadata": {
                    "type": "object",
                    "description": "Additional session metadata"
                }
            }
        },
        "ChatRequest": {
            "type": "object",
            "required": ["message"],
            "properties": {
                "message": {
                    "type": "string",
                    "description": "User message to the AI agent"
                },
                "context": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {
                            "type": "string",
                            "description": "Conversation identifier for context"
                        },
                        "user_intent": {
                            "type": "string",
                            "description": "User's intent for better processing"
                        },
                        "current_page": {
                            "type": "string",
                            "description": "Current page/context in the application"
                        },
                        "video_id": {
                            "type": "string",
                            "description": "YouTube video ID for context"
                        }
                    }
                },
                "preferences": {
                    "type": "object",
                    "properties": {
                        "response_length": {
                            "type": "string",
                            "enum": ["brief", "standard", "detailed"],
                            "default": "standard"
                        },
                        "include_suggestions": {
                            "type": "boolean",
                            "default": True
                        },
                        "analysis_depth": {
                            "type": "string",
                            "enum": ["quick", "standard", "deep"],
                            "default": "standard"
                        }
                    }
                }
            }
        },
        "ChatResponse": {
            "allOf": [
                {"$ref": "#/components/schemas/StandardResponse"},
                {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "object",
                            "properties": {
                                "response": {
                                    "type": "string",
                                    "description": "AI agent response message"
                                },
                                "agent_type": {
                                    "type": "string",
                                    "description": "Type of agent that processed the request"
                                },
                                "delegated_agents": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of specialized agents consulted"
                                },
                                "confidence_score": {
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1,
                                    "description": "Confidence score of the response"
                                },
                                "conversation_id": {
                                    "type": "string",
                                    "description": "Conversation identifier"
                                },
                                "suggestions": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Suggestion"}
                                },
                                "related_insights": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Insight"}
                                }
                            }
                        }
                    }
                }
            ]
        },
        "Suggestion": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["quick_action", "content_idea", "optimization", "tool"]
                },
                "title": {
                    "type": "string",
                    "description": "Suggestion title"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description"
                },
                "action": {
                    "type": "string",
                    "description": "Action identifier for execution"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"]
                }
            }
        },
        "Insight": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["performance_metric", "trend", "opportunity", "warning"]
                },
                "title": {
                    "type": "string",
                    "description": "Insight title"
                },
                "value": {
                    "type": "string",
                    "description": "Insight value or metric"
                },
                "insight": {
                    "type": "string",
                    "description": "Detailed insight description"
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                }
            }
        },
        "PillarData": {
            "type": "object",
            "required": ["id", "name", "created_at", "video_count"],
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique pillar identifier"
                },
                "name": {
                    "type": "string",
                    "description": "Pillar name"
                },
                "description": {
                    "type": "string",
                    "description": "Pillar description"
                },
                "color": {
                    "type": "string",
                    "pattern": "^#[0-9A-Fa-f]{6}$",
                    "description": "Pillar color (hexadecimal)"
                },
                "created_at": {
                    "type": "string",
                    "format": "date-time"
                },
                "updated_at": {
                    "type": "string",
                    "format": "date-time"
                },
                "video_count": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of videos assigned to this pillar"
                },
                "analytics": {
                    "$ref": "#/components/schemas/PillarAnalytics"
                },
                "metadata": {
                    "type": "object",
                    "description": "Custom pillar metadata"
                }
            }
        },
        "PillarAnalytics": {
            "type": "object",
            "properties": {
                "timeframe": {
                    "type": "string",
                    "description": "Analytics time period"
                },
                "total_views": {
                    "type": "integer",
                    "minimum": 0
                },
                "total_watch_time_hours": {
                    "type": "number",
                    "minimum": 0
                },
                "average_ctr": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "average_retention": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "engagement_rate": {
                    "type": "number",
                    "minimum": 0
                },
                "subscriber_growth": {
                    "type": "integer"
                },
                "revenue": {
                    "type": "number",
                    "minimum": 0
                },
                "performance_trend": {
                    "type": "string",
                    "enum": ["increasing", "decreasing", "stable"]
                }
            }
        },
        "VideoData": {
            "type": "object",
            "properties": {
                "video_id": {
                    "type": "string",
                    "description": "YouTube video ID"
                },
                "title": {
                    "type": "string",
                    "description": "Video title"
                },
                "description": {
                    "type": "string",
                    "description": "Video description"
                },
                "published_at": {
                    "type": "string",
                    "format": "date-time"
                },
                "duration": {
                    "type": "string",
                    "description": "Video duration in ISO 8601 format"
                },
                "thumbnail_url": {
                    "type": "string",
                    "format": "uri",
                    "description": "Video thumbnail URL"
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "category": {
                    "type": "string",
                    "description": "Video category"
                },
                "analytics": {
                    "$ref": "#/components/schemas/VideoAnalytics"
                }
            }
        },
        "VideoAnalytics": {
            "type": "object",
            "properties": {
                "views": {
                    "type": "integer",
                    "minimum": 0
                },
                "likes": {
                    "type": "integer",
                    "minimum": 0
                },
                "dislikes": {
                    "type": "integer",
                    "minimum": 0
                },
                "comments": {
                    "type": "integer",
                    "minimum": 0
                },
                "shares": {
                    "type": "integer",
                    "minimum": 0
                },
                "click_through_rate": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                },
                "average_view_duration": {
                    "type": "string",
                    "description": "Average view duration in MM:SS format"
                },
                "retention_curve": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "timestamp": {
                                "type": "integer",
                                "description": "Time in seconds"
                            },
                            "retention": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1
                            }
                        }
                    }
                }
            }
        },
        "HealthResponse": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["healthy", "degraded", "unhealthy"]
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "service": {
                    "type": "string"
                },
                "version": {
                    "type": "string"
                },
                "overall_health": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1
                }
            }
        }
    }


def generate_common_responses() -> Dict[str, Any]:
    """Generate common response definitions"""
    return {
        "UnauthorizedError": {
            "description": "Authentication credentials are missing or invalid",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Authentication required",
                        "error": {
                            "code": "AUTHENTICATION_REQUIRED",
                            "details": "Valid session required to access this endpoint"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        },
        "ForbiddenError": {
            "description": "The request is valid but the user lacks permissions",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Insufficient permissions",
                        "error": {
                            "code": "INSUFFICIENT_PERMISSIONS",
                            "details": "User lacks required permissions for this operation"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        },
        "NotFoundError": {
            "description": "The requested resource was not found",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Resource not found",
                        "error": {
                            "code": "RESOURCE_NOT_FOUND",
                            "details": "The requested resource does not exist"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        },
        "ValidationError": {
            "description": "Request validation failed",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Validation error",
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "details": "Required field is missing",
                            "field": "user_id"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        },
        "RateLimitError": {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Rate limit exceeded",
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "details": "Too many requests. Please try again later.",
                            "retry_after": 60
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            },
            "headers": {
                "X-RateLimit-Limit": {
                    "description": "Request limit per time window",
                    "schema": {"type": "integer"}
                },
                "X-RateLimit-Remaining": {
                    "description": "Remaining requests in current window",
                    "schema": {"type": "integer"}
                },
                "X-RateLimit-Reset": {
                    "description": "Time when the rate limit resets (Unix timestamp)",
                    "schema": {"type": "integer"}
                },
                "Retry-After": {
                    "description": "Seconds to wait before retrying",
                    "schema": {"type": "integer"}
                }
            }
        },
        "ServerError": {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/StandardResponse"},
                    "example": {
                        "success": False,
                        "message": "Internal server error",
                        "error": {
                            "code": "INTERNAL_SERVER_ERROR",
                            "details": "An unexpected error occurred"
                        },
                        "timestamp": "2024-01-01T12:00:00Z"
                    }
                }
            }
        }
    }


def generate_common_parameters() -> Dict[str, Any]:
    """Generate common parameter definitions"""
    return {
        "timeframe": {
            "name": "timeframe",
            "in": "query",
            "description": "Time period for analytics data",
            "required": False,
            "schema": {
                "type": "string",
                "enum": ["7d", "30d", "90d", "1y"],
                "default": "30d"
            }
        },
        "limit": {
            "name": "limit",
            "in": "query",
            "description": "Maximum number of items to return",
            "required": False,
            "schema": {
                "type": "integer",
                "minimum": 1,
                "maximum": 100,
                "default": 25
            }
        },
        "offset": {
            "name": "offset",
            "in": "query",
            "description": "Number of items to skip for pagination",
            "required": False,
            "schema": {
                "type": "integer",
                "minimum": 0,
                "default": 0
            }
        },
        "sort_by": {
            "name": "sort_by",
            "in": "query",
            "description": "Field to sort by",
            "required": False,
            "schema": {
                "type": "string",
                "default": "created_at"
            }
        },
        "order": {
            "name": "order",
            "in": "query",
            "description": "Sort order",
            "required": False,
            "schema": {
                "type": "string",
                "enum": ["asc", "desc"],
                "default": "desc"
            }
        }
    }


def generate_examples() -> Dict[str, Any]:
    """Generate example data"""
    return {
        "LoginSuccess": {
            "summary": "Successful login",
            "value": {
                "success": True,
                "message": "Login successful",
                "data": {
                    "session_id": "abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567",
                    "user_id": "creator123",
                    "expires_at": "2024-01-01T20:00:00Z",
                    "permissions": ["user"]
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        },
        "ChatResponse": {
            "summary": "AI chat response",
            "value": {
                "success": True,
                "message": "Response generated successfully",
                "data": {
                    "response": "Based on your channel analytics, here are some AI-powered suggestions for improving your thumbnails...",
                    "agent_type": "boss_agent",
                    "delegated_agents": ["content_analysis", "audience_insights"],
                    "confidence_score": 0.95,
                    "conversation_id": "conv_123",
                    "suggestions": [
                        {
                            "type": "quick_action",
                            "title": "Analyze Thumbnail Performance",
                            "description": "Get detailed analysis of your current thumbnails",
                            "action": "analyze_thumbnails",
                            "priority": "high"
                        }
                    ]
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        },
        "PillarList": {
            "summary": "List of content pillars",
            "value": {
                "success": True,
                "message": "Pillars retrieved successfully",
                "data": {
                    "pillars": [
                        {
                            "id": "pillar_123",
                            "name": "Educational Content",
                            "description": "Tutorials, how-to guides, and educational videos",
                            "color": "#3B82F6",
                            "created_at": "2024-01-01T10:00:00Z",
                            "video_count": 25,
                            "analytics": {
                                "total_views": 150000,
                                "average_ctr": 0.052,
                                "average_retention": 0.68,
                                "engagement_rate": 0.071
                            }
                        }
                    ],
                    "total_count": 5
                },
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
    }


def generate_paths() -> Dict[str, Any]:
    """Generate API paths with comprehensive documentation"""
    return {
        "/api/session/login": {
            "post": {
                "tags": ["session"],
                "summary": "Create new user session",
                "description": "Authenticate user and create a new session with secure cookie",
                "operationId": "login",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginRequest"},
                            "examples": {
                                "basic_login": {
                                    "summary": "Basic login",
                                    "value": {
                                        "user_id": "creator123",
                                        "password": "secure_password"
                                    }
                                },
                                "login_with_metadata": {
                                    "summary": "Login with metadata",
                                    "value": {
                                        "user_id": "creator123",
                                        "password": "secure_password",
                                        "remember_me": True,
                                        "metadata": {
                                            "device": "web",
                                            "app_version": "2.0.0",
                                            "browser": "Chrome"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/StandardResponse"},
                                "examples": {
                                    "login_success": {"$ref": "#/components/examples/LoginSuccess"}
                                }
                            }
                        },
                        "headers": {
                            "Set-Cookie": {
                                "description": "Session cookie",
                                "schema": {"type": "string"},
                                "example": "Vidalytics_session=abc123...; HttpOnly; Secure; SameSite=Strict"
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    "401": {"$ref": "#/components/responses/UnauthorizedError"},
                    "429": {"$ref": "#/components/responses/RateLimitError"},
                    "500": {"$ref": "#/components/responses/ServerError"}
                }
            }
        },
        "/api/agent/chat": {
            "post": {
                "tags": ["agent"],
                "summary": "Chat with AI agent system",
                "description": "Send a message to the multi-agent system and receive an AI-powered response",
                "operationId": "chat",
                "security": [{"SessionCookie": []}, {"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChatRequest"},
                            "examples": {
                                "basic_chat": {
                                    "summary": "Basic chat message",
                                    "value": {
                                        "message": "How can I improve my video thumbnails?"
                                    }
                                },
                                "contextual_chat": {
                                    "summary": "Chat with context",
                                    "value": {
                                        "message": "Analyze my latest video performance",
                                        "context": {
                                            "video_id": "dQw4w9WgXcQ",
                                            "user_intent": "video_analysis",
                                            "current_page": "dashboard"
                                        },
                                        "preferences": {
                                            "response_length": "detailed",
                                            "include_suggestions": True,
                                            "analysis_depth": "deep"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Chat response generated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ChatResponse"},
                                "examples": {
                                    "chat_response": {"$ref": "#/components/examples/ChatResponse"}
                                }
                            }
                        }
                    },
                    "401": {"$ref": "#/components/responses/UnauthorizedError"},
                    "429": {"$ref": "#/components/responses/RateLimitError"},
                    "500": {"$ref": "#/components/responses/ServerError"}
                }
            }
        },
        "/api/pillars": {
            "get": {
                "tags": ["pillars"],
                "summary": "List content pillars",
                "description": "Get all content pillars for the authenticated user",
                "operationId": "listPillars",
                "security": [{"SessionCookie": []}, {"BearerAuth": []}],
                "parameters": [
                    {
                        "name": "include_videos",
                        "in": "query",
                        "description": "Include assigned videos in response",
                        "required": False,
                        "schema": {"type": "boolean", "default": False}
                    },
                    {
                        "name": "include_analytics", 
                        "in": "query",
                        "description": "Include pillar performance analytics",
                        "required": False,
                        "schema": {"type": "boolean", "default": False}
                    },
                    {"$ref": "#/components/parameters/sort_by"},
                    {"$ref": "#/components/parameters/order"}
                ],
                "responses": {
                    "200": {
                        "description": "Pillars retrieved successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/StandardResponse"},
                                "examples": {
                                    "pillar_list": {"$ref": "#/components/examples/PillarList"}
                                }
                            }
                        }
                    },
                    "401": {"$ref": "#/components/responses/UnauthorizedError"},
                    "500": {"$ref": "#/components/responses/ServerError"}
                }
            },
            "post": {
                "tags": ["pillars"],
                "summary": "Create new content pillar",
                "description": "Create a new content pillar for organizing videos",
                "operationId": "createPillar",
                "security": [{"SessionCookie": []}, {"BearerAuth": []}],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["name"],
                                "properties": {
                                    "name": {"type": "string", "description": "Pillar name"},
                                    "description": {"type": "string", "description": "Pillar description"},
                                    "color": {
                                        "type": "string",
                                        "pattern": "^#[0-9A-Fa-f]{6}$",
                                        "description": "Pillar color (hex format)"
                                    },
                                    "metadata": {"type": "object", "description": "Custom metadata"}
                                }
                            },
                            "examples": {
                                "create_pillar": {
                                    "summary": "Create educational pillar",
                                    "value": {
                                        "name": "Educational Content",
                                        "description": "Tutorials and how-to videos",
                                        "color": "#3B82F6",
                                        "metadata": {
                                            "target_audience": "beginners",
                                            "content_frequency": "weekly"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Pillar created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/StandardResponse"}
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ValidationError"},
                    "401": {"$ref": "#/components/responses/UnauthorizedError"},
                    "500": {"$ref": "#/components/responses/ServerError"}
                }
            }
        },
        "/health": {
            "get": {
                "tags": ["health"],
                "summary": "Basic health check",
                "description": "Check if the API is running and healthy",
                "operationId": "healthCheck",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HealthResponse"},
                                "example": {
                                    "status": "healthy",
                                    "timestamp": "2024-01-01T12:00:00Z",
                                    "service": "Vidalytics Multi-Agent API",
                                    "version": "2.0.0"
                                }
                            }
                        }
                    },
                    "503": {
                        "description": "Service is unhealthy",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/HealthResponse"}
                            }
                        }
                    }
                }
            }
        }
    }


def main():
    """Generate and save OpenAPI specification"""
    print("🔄 Generating OpenAPI 3.0 specification...")
    
    try:
        # Generate specification
        spec = generate_openapi_spec()
        
        # Create docs directory if it doesn't exist
        docs_dir = "docs"
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        
        # Save as JSON
        json_path = os.path.join(docs_dir, "openapi.json")
        with open(json_path, 'w') as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)
        
        # Save as YAML
        yaml_path = os.path.join(docs_dir, "openapi.yaml")
        with open(yaml_path, 'w') as f:
            yaml.dump(spec, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ OpenAPI specification generated successfully!")
        print(f"   📄 JSON: {json_path}")
        print(f"   📄 YAML: {yaml_path}")
        print(f"   📊 Paths: {len(spec['paths'])}")
        print(f"   📋 Schemas: {len(spec['components']['schemas'])}")
        print(f"   📝 Examples: {len(spec['components']['examples'])}")
        
        # Generate stats
        total_endpoints = sum(len(methods) for methods in spec['paths'].values())
        print(f"   🔗 Total endpoints: {total_endpoints}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate OpenAPI specification: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)