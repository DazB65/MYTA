# CreatorMate API Documentation

## 📚 Complete Documentation Index

Welcome to the comprehensive documentation for the CreatorMate Multi-Agent API. This documentation covers everything you need to know to integrate with and use the CreatorMate platform.

### 🚀 Getting Started

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API overview, authentication, and usage guide
- **[Quick Start Guide](API_DOCUMENTATION.md#quick-start)** - Get up and running in minutes
- **[Authentication Guide](API_DOCUMENTATION.md#authentication)** - Session management and security

### 📖 Reference Documentation

- **[API Endpoints Reference](API_ENDPOINTS.md)** - Detailed documentation for all endpoints
- **[OpenAPI Specification](openapi.json)** - Machine-readable API specification (JSON)
- **[OpenAPI Specification](openapi.yaml)** - Machine-readable API specification (YAML)
- **[SDK Documentation](SDK_DOCUMENTATION.md)** - Client SDKs for Python, JavaScript, Go, and PHP

### 🧪 Testing & Development

- **[API Testing Guide](API_TESTING.md)** - Comprehensive testing strategies and examples
- **[Postman Collection](API_TESTING.md#postman-collection)** - Pre-built API testing collection
- **[Performance Testing](API_TESTING.md#performance-testing)** - Load and stress testing guides

### 🔧 System Documentation

- **[Redis Session Management](../REDIS_SESSION_MANAGEMENT.md)** - Session system architecture and configuration
- **[Docker Setup](../DOCKER.md)** - Containerization and deployment
- **[CI/CD Pipeline](../CI-CD.md)** - Automated testing and deployment

### 🏗️ Architecture

- **[Multi-Agent System](API_DOCUMENTATION.md#multi-agent-system)** - AI agent architecture and communication
- **[Database Schema](../DATABASE_MIGRATIONS.md)** - Database structure and migrations
- **[Security Model](API_DOCUMENTATION.md#authentication)** - Security architecture and best practices

## 📊 API Overview

### Base URLs

- **Development**: `http://localhost:8888`
- **Production**: `https://api.creatormate.com`

### Authentication

The API uses Redis-based session management with secure HTTP-only cookies or Bearer token authentication.

```bash
# Create a session
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "your_user_id", "password": "your_password"}'

# Use session cookie for subsequent requests
curl -X GET "http://localhost:8888/api/agent/chat" \
  -H "Cookie: creatormate_session=your_session_id"
```

### Core Features

#### 🤖 Multi-Agent System
- **Boss Agent**: Central orchestrator using Claude 3.5 Sonnet
- **Content Analysis**: Video performance analysis using Gemini 2.5 Pro
- **Audience Insights**: Demographics analysis using Claude 3.5 Sonnet
- **SEO & Discoverability**: Search optimization using Claude 3.5 Haiku
- **Competitive Analysis**: Market analysis using Gemini 2.5 Pro
- **Monetization Strategy**: Revenue optimization using Claude 3.5 Haiku

#### 📊 YouTube Integration
- Deep analytics integration with YouTube Data API
- OAuth 2.0 authentication flow
- Real-time video performance monitoring
- Channel metrics and trending analysis

#### 🎯 Content Management
- Strategic content pillar organization
- Video assignment and categorization
- Performance tracking by content type
- AI-powered content recommendations

#### 📈 Analytics & Insights
- Comprehensive dashboard analytics
- Performance trend analysis
- AI-generated insights and recommendations
- Custom reporting and metrics

## 🌟 Key Endpoints

### Authentication
- `POST /api/session/login` - Create session
- `GET /api/session/current` - Get current session
- `POST /api/session/logout` - End session

### AI Agent System
- `POST /api/agent/chat` - Chat with AI agents
- `POST /api/agent/quick-action` - Execute quick actions
- `GET /api/agent/insights/{user_id}` - Get AI insights

### YouTube Integration
- `GET /api/youtube/analytics/channel/{channel_id}` - Channel analytics
- `GET /api/youtube/videos/{video_id}` - Video details
- `GET /api/youtube/search` - Search videos

### Content Pillars
- `GET /api/pillars` - List pillars
- `POST /api/pillars` - Create pillar
- `POST /api/pillars/{pillar_id}/videos/{video_id}` - Assign video

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/performance/{metric_type}` - Performance data

### Health & Monitoring
- `GET /health` - Basic health check
- `GET /api/health/system` - System health
- `GET /api/session/health` - Session system health

## 🛠️ Development Tools

### SDKs Available

- **Python**: `pip install creatormate-sdk`
- **JavaScript/TypeScript**: `npm install @creatormate/sdk`
- **Go**: `go get github.com/creatormate/sdk-go`
- **PHP**: `composer require creatormate/sdk`

### Testing Tools

- **Postman Collection**: Pre-built API testing collection
- **OpenAPI Spec**: Machine-readable API documentation
- **Load Testing**: Artillery and Locust configurations
- **Integration Tests**: Comprehensive test suites

### Development Environment

```bash
# Quick start with Docker
git clone https://github.com/creatormate/api
cd creatormate
docker-compose -f docker-compose.dev.yml up

# Or manual setup
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8888
```

## 📋 Rate Limits

| Tier | Requests/Minute | Burst Limit |
|------|-----------------|-------------|
| Public | 60 | 10 |
| Authenticated | 300 | 50 |
| Premium | 1000 | 100 |
| Admin | 5000 | 500 |

## 🔒 Security

- **Session Management**: Secure Redis-based sessions
- **Cookie Security**: HttpOnly, Secure, SameSite protection
- **Input Validation**: Comprehensive request validation
- **Rate Limiting**: Intelligent rate limiting by user tier
- **CORS**: Configurable cross-origin resource sharing
- **Monitoring**: Security event logging and alerting

## 📞 Support

- **Documentation**: https://docs.creatormate.com
- **API Status**: https://status.creatormate.com
- **Community**: https://community.creatormate.com
- **Support Email**: support@creatormate.com
- **GitHub Issues**: https://github.com/creatormate/api/issues

## 📄 License

The CreatorMate API is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## 🔄 Changelog

### v2.0.0 (Current)
- ✅ **Multi-agent architecture** with specialized AI agents
- ✅ **Redis session management** for secure authentication
- ✅ **Enhanced YouTube integration** with OAuth 2.0
- ✅ **Content pillars system** for strategic content organization
- ✅ **Comprehensive API documentation** with OpenAPI/Swagger
- ✅ **Docker containerization** for easy deployment
- ✅ **CI/CD pipeline** with automated testing and security scanning
- ✅ **Performance optimization** with intelligent caching
- ✅ **Health monitoring** with detailed system metrics

### v1.0.0 (Legacy)
- Basic AI chat interface
- Simple YouTube analytics
- JWT-based authentication
- Basic content management

---

## 🏁 Next Steps

1. **Read the [API Documentation](API_DOCUMENTATION.md)** for a complete overview
2. **Try the [Quick Start Guide](API_DOCUMENTATION.md#quick-start)** to make your first API call
3. **Download our [SDK](SDK_DOCUMENTATION.md)** for your preferred programming language
4. **Import our [Postman Collection](API_TESTING.md#postman-collection)** for easy testing
5. **Join our [Community](https://community.creatormate.com)** for support and discussions

Happy coding! 🚀