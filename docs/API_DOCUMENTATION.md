# CreatorMate API Documentation

## Overview

The CreatorMate API is a comprehensive RESTful API that provides YouTube content creators with AI-powered tools for channel optimization, content strategy, and audience engagement. Built on FastAPI with a sophisticated multi-agent architecture, it offers scalable, secure, and intelligent solutions for content creators.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Multi-Agent System](#multi-agent-system)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [SDKs and Examples](#sdks-and-examples)
8. [Webhooks](#webhooks)
9. [Changelog](#changelog)

## Quick Start

### Base URL

```
Development: http://localhost:8888
Production: https://api.creatormate.com
```

### Making Your First Request

1. **Create a Session** (Login)
```bash
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_user_id",
    "metadata": {"device": "api_client"}
  }'
```

2. **Use the Session Cookie** for authenticated requests
```bash
curl -X GET "http://localhost:8888/api/agent/chat" \
  -H "Cookie: creatormate_session=your_session_id"
```

## Authentication

CreatorMate uses Redis-based session management for secure authentication.

### Session Management

#### Creating a Session (Login)
```http
POST /api/session/login
Content-Type: application/json

{
  "user_id": "string",
  "password": "string",
  "remember_me": false,
  "metadata": {
    "device": "web",
    "app_version": "1.0.0"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "session_id": "abc123...",
    "user_id": "your_user_id",
    "expires_at": "2024-01-01T20:00:00Z",
    "permissions": ["user"]
  }
}
```

#### Using Sessions

Sessions can be used in two ways:

1. **Cookie-based** (Recommended for web applications)
   - Session cookie is automatically set on login
   - Include cookie in subsequent requests

2. **Header-based** (Recommended for API clients)
   ```http
   Authorization: Bearer your_session_id
   ```

#### Session Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/session/login` | Create new session |
| POST | `/api/session/logout` | Revoke current session |
| POST | `/api/session/logout-all` | Revoke all other sessions |
| GET | `/api/session/current` | Get current session info |
| GET | `/api/session/list` | List all user sessions |
| PUT | `/api/session/update` | Update session metadata |
| DELETE | `/api/session/revoke/{session_id}` | Revoke specific session |

## API Endpoints

### Agent System

The core AI functionality is provided through the agent system.

#### Chat Interface
```http
POST /api/agent/chat
Content-Type: application/json
Cookie: creatormate_session=your_session_id

{
  "message": "How can I improve my video thumbnails?",
  "context": {
    "conversation_id": "optional_conversation_id",
    "metadata": {
      "page": "dashboard",
      "user_intent": "thumbnail_optimization"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Response generated successfully",
  "data": {
    "response": "Here are some AI-powered suggestions for improving your thumbnails...",
    "agent_type": "boss_agent",
    "confidence_score": 0.95,
    "conversation_id": "conv_123",
    "suggestions": [
      {
        "type": "quick_action",
        "title": "Analyze Thumbnail Performance",
        "action": "analyze_thumbnails"
      }
    ]
  }
}
```

#### Quick Actions
```http
POST /api/agent/quick-action
Content-Type: application/json

{
  "action_type": "generate_script",
  "parameters": {
    "topic": "How to optimize YouTube SEO",
    "duration": "10-15 minutes",
    "style": "educational"
  }
}
```

### YouTube Integration

#### Channel Analytics
```http
GET /api/youtube/analytics/channel/{channel_id}?timeframe=30d&metrics=views,engagement
```

#### Video Data
```http
GET /api/youtube/videos/{video_id}
```

#### OAuth Flow
```http
GET /api/oauth/youtube/authorize
POST /api/oauth/youtube/callback
GET /api/oauth/youtube/status
DELETE /api/oauth/youtube/disconnect
```

### Content Pillars

#### Pillar Management
```http
GET /api/pillars                    # List all pillars
POST /api/pillars                   # Create new pillar
GET /api/pillars/{pillar_id}        # Get pillar details
PUT /api/pillars/{pillar_id}        # Update pillar
DELETE /api/pillars/{pillar_id}     # Delete pillar
```

#### Video Assignment
```http
POST /api/pillars/{pillar_id}/videos/{video_id}  # Assign video to pillar
DELETE /api/pillars/{pillar_id}/videos/{video_id}  # Remove video from pillar
```

### Analytics

#### Dashboard Metrics
```http
GET /api/analytics/dashboard?timeframe=7d
```

#### Performance Reports
```http
GET /api/analytics/performance/{metric_type}?start_date=2024-01-01&end_date=2024-01-31
```

## Multi-Agent System

CreatorMate's multi-agent architecture provides specialized AI capabilities:

### Agent Types

1. **Boss Agent** - Central orchestrator
   - **Model**: Claude 3.5 Sonnet
   - **Purpose**: User communication, agent delegation, response synthesis
   - **Endpoints**: `/api/agent/chat`, `/api/agent/quick-action`

2. **Content Analysis Agent** - Video performance analysis
   - **Model**: Gemini 2.5 Pro (primary), Claude 3.5 Sonnet (fallback)
   - **Purpose**: Video hooks, titles, thumbnails, retention analysis
   - **Cache TTL**: 1-4 hours

3. **Audience Insights Agent** - Demographics and sentiment
   - **Model**: Claude 3.5 Sonnet (primary), Claude 3.5 Haiku (fallback)
   - **Purpose**: Audience behavior, demographics, community health
   - **Cache TTL**: 30 minutes - 4 hours

4. **SEO & Discoverability Agent** - Search optimization
   - **Model**: Claude 3.5 Haiku
   - **Purpose**: Keyword research, search optimization, algorithm analysis
   - **Cache TTL**: 2-6 hours

5. **Competitive Analysis Agent** - Market positioning
   - **Model**: Gemini 2.5 Pro (primary), Claude 3.5 Sonnet (fallback)
   - **Purpose**: Competitor benchmarking, market analysis
   - **Cache TTL**: 2-12 hours

6. **Monetization Strategy Agent** - Revenue optimization
   - **Model**: Claude 3.5 Haiku (primary), Claude 3.5 Sonnet (fallback)
   - **Purpose**: Revenue strategies, sponsorship opportunities, RPM/CPM analysis
   - **Cache TTL**: 2-8 hours

### Agent Communication

Agents communicate using a standardized protocol:

```json
{
  "request_id": "uuid4_string",
  "query_type": "content_analysis|audience_insights|seo_discoverability|competitive_analysis|monetization_strategy",
  "context": {
    "channel_id": "channel_identifier",
    "time_period": "last_7d|last_30d|last_90d",
    "specific_videos": ["video_id1", "video_id2"],
    "analysis_depth": "quick|standard|deep"
  },
  "token_budget": {
    "input_tokens": 3000,
    "output_tokens": 1500
  },
  "boss_agent_token": "jwt_authentication_token"
}
```

## Error Handling

The API uses standard HTTP status codes and provides detailed error information:

### Standard Response Format

**Success Response:**
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": "Specific error details",
    "field": "field_name"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `VALIDATION_ERROR` | Request validation failed |
| 401 | `AUTHENTICATION_REQUIRED` | Valid session required |
| 403 | `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| 404 | `RESOURCE_NOT_FOUND` | Requested resource not found |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_SERVER_ERROR` | Server error occurred |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable |

### Agent-Specific Errors

```json
{
  "success": false,
  "message": "Agent processing failed",
  "error": {
    "code": "AGENT_ERROR",
    "agent_type": "content_analysis",
    "details": "Model API rate limit exceeded",
    "retry_after": 60
  }
}
```

## Rate Limiting

The API implements intelligent rate limiting based on user type and endpoint:

### Rate Limit Tiers

| Tier | Requests/Minute | Burst Limit |
|------|-----------------|-------------|
| Public | 60 | 10 |
| Authenticated | 300 | 50 |
| Premium | 1000 | 100 |
| Admin | 5000 | 500 |

### Rate Limit Headers

```http
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 60
```

### Endpoint-Specific Limits

| Endpoint Category | Rate Limit |
|-------------------|------------|
| Authentication | 10/minute |
| Agent Chat | 100/minute |
| Quick Actions | 50/minute |
| Analytics | 200/minute |
| Health Checks | 1000/minute |

## SDKs and Examples

### Python SDK Example

```python
import requests
from creatormate_sdk import CreatorMateClient

# Initialize client
client = CreatorMateClient(
    base_url="http://localhost:8888",
    user_id="your_user_id"
)

# Login and create session
session = client.login(password="your_password")

# Chat with AI agent
response = client.chat("How can I improve my CTR?")
print(response.message)

# Get channel analytics
analytics = client.youtube.get_channel_analytics(
    timeframe="30d",
    metrics=["views", "engagement", "retention"]
)

# Create content pillar
pillar = client.pillars.create(
    name="Educational Content",
    description="Tutorial and how-to videos",
    color="#3B82F6"
)
```

### JavaScript SDK Example

```javascript
import { CreatorMateClient } from '@creatormate/sdk';

const client = new CreatorMateClient({
  baseUrl: 'http://localhost:8888',
  userId: 'your_user_id'
});

// Login
await client.auth.login({ password: 'your_password' });

// Chat with AI
const chatResponse = await client.agent.chat({
  message: 'What trending topics should I cover?',
  context: { intent: 'content_planning' }
});

// Get quick action suggestions
const suggestions = await client.agent.quickAction({
  actionType: 'generate_ideas',
  parameters: { niche: 'tech', count: 5 }
});
```

### cURL Examples

#### Authentication Flow
```bash
# Login
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "creator123", "password": "secure_password"}'

# Chat with AI (using session cookie)
curl -X POST "http://localhost:8888/api/agent/chat" \
  -H "Content-Type: application/json" \
  -H "Cookie: creatormate_session=your_session_id" \
  -d '{"message": "Analyze my latest video performance"}'

# Get channel analytics
curl -X GET "http://localhost:8888/api/youtube/analytics/channel/UC123?timeframe=7d" \
  -H "Cookie: creatormate_session=your_session_id"
```

## Webhooks

CreatorMate supports webhooks for real-time notifications:

### Webhook Events

| Event | Description |
|-------|-------------|
| `agent.response_completed` | AI agent completed a response |
| `youtube.video_published` | New video detected on channel |
| `analytics.threshold_reached` | Performance metric threshold reached |
| `pillar.video_assigned` | Video assigned to content pillar |
| `session.expired` | User session expired |

### Webhook Payload

```json
{
  "event": "agent.response_completed",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "user_id": "creator123",
    "agent_type": "content_analysis",
    "conversation_id": "conv_456",
    "response_summary": "Video analysis completed"
  },
  "signature": "sha256=signature_hash"
}
```

### Webhook Configuration

```http
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://your-app.com/webhooks/creatormate",
  "events": ["agent.response_completed", "youtube.video_published"],
  "secret": "your_webhook_secret"
}
```

## Health and Monitoring

### Health Check Endpoints

```http
GET /health                    # Basic health check
GET /api/health/system         # Comprehensive system health
GET /api/session/health        # Session system health
```

### System Health Response

```json
{
  "overall_health": 0.95,
  "status": "healthy",
  "model_integrations": {
    "openai": {"status": "healthy", "response_time_ms": 250},
    "google": {"status": "healthy", "response_time_ms": 180}
  },
  "youtube_api": {
    "status": "healthy",
    "quota_remaining": 9500,
    "health_score": 1.0
  },
  "cache_system": {
    "redis_status": "connected",
    "memory_usage": "45%",
    "health_score": 0.9
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Changelog

### v2.0.0 (Current)
- ✅ **Multi-agent architecture** with specialized AI agents
- ✅ **Redis session management** for secure authentication
- ✅ **Enhanced YouTube integration** with OAuth 2.0
- ✅ **Content pillars system** for strategic content organization
- ✅ **Comprehensive API documentation** with OpenAPI/Swagger
- ✅ **Docker containerization** for easy deployment
- ✅ **CI/CD pipeline** with automated testing and security scanning

### v1.0.0 (Legacy)
- Basic AI chat interface
- Simple YouTube analytics
- JWT-based authentication
- Basic content management

## Support

- **Documentation**: https://docs.creatormate.com
- **API Status**: https://status.creatormate.com  
- **Community**: https://community.creatormate.com
- **Support Email**: support@creatormate.com
- **GitHub Issues**: https://github.com/creatormate/api/issues

## Terms of Service

By using the CreatorMate API, you agree to our [Terms of Service](https://creatormate.com/terms) and [Privacy Policy](https://creatormate.com/privacy).

## License

The CreatorMate API documentation is licensed under the [MIT License](https://opensource.org/licenses/MIT).