# Vidalytics API Testing Guide

## Overview

This guide provides comprehensive testing instructions for the Vidalytics API, including automated testing, manual testing, performance testing, and integration testing approaches.

## Table of Contents

1. [Quick Start Testing](#quick-start-testing)
2. [Postman Collection](#postman-collection)
3. [Automated Testing](#automated-testing)
4. [Manual Testing](#manual-testing)
5. [Performance Testing](#performance-testing)
6. [Security Testing](#security-testing)
7. [Integration Testing](#integration-testing)
8. [Testing Environments](#testing-environments)
9. [Test Data Management](#test-data-management)
10. [Troubleshooting](#troubleshooting)

## Quick Start Testing

### Prerequisites

1. **Running API Server**
   ```bash
   # Development
   cd backend
   source ../venv/bin/activate
   uvicorn main:app --reload --host 0.0.0.0 --port 8888
   
   # Or with Docker
   docker-compose -f docker-compose.dev.yml up
   ```

2. **Redis Server** (for session management)
   ```bash
   # Via Docker
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   
   # Or local installation
   redis-server
   ```

3. **Environment Variables**
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export GOOGLE_API_KEY="your_google_api_key"
   export YOUTUBE_API_KEY="your_youtube_api_key"
   ```

### Basic Health Check

```bash
# Test basic connectivity
curl -X GET "http://localhost:8888/health" \
  -H "Accept: application/json"

# Expected Response:
# {
#   "status": "healthy",
#   "timestamp": "2024-01-01T12:00:00Z",
#   "service": "Vidalytics Multi-Agent API",
#   "version": "2.0.0"
# }
```

### Authentication Flow Test

```bash
# 1. Create session (login)
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "password": "test_password",
    "metadata": {"device": "test"}
  }' \
  -c cookies.txt

# 2. Test authenticated endpoint
curl -X GET "http://localhost:8888/api/session/current" \
  -H "Accept: application/json" \
  -b cookies.txt

# 3. Logout
curl -X POST "http://localhost:8888/api/session/logout" \
  -H "Accept: application/json" \
  -b cookies.txt
```

## Postman Collection

### Import Collection

1. **Download Collection**
   ```bash
   # Download the official Postman collection
   curl -o Vidalytics_API.postman_collection.json \
     https://raw.githubusercontent.com/Vidalytics/api/main/docs/postman/Vidalytics_API.postman_collection.json
   ```

2. **Import in Postman**
   - Open Postman
   - Click "Import" → "Upload Files"
   - Select the downloaded collection file

3. **Set Environment Variables**
   ```json
   {
     "base_url": "http://localhost:8888",
     "user_id": "test_user",
     "password": "test_password",
     "session_cookie": ""
   }
   ```

### Collection Structure

```
Vidalytics API Collection/
├── Authentication/
│   ├── Login
│   ├── Get Current Session
│   ├── List Sessions
│   ├── Update Session
│   └── Logout
├── Agent System/
│   ├── Chat with AI
│   ├── Quick Actions
│   ├── Get Insights
│   └── Agent Status
├── YouTube Integration/
│   ├── Channel Analytics
│   ├── Video Data
│   ├── Search Videos
│   └── OAuth Flow
├── Content Pillars/
│   ├── List Pillars
│   ├── Create Pillar
│   ├── Get Pillar Details
│   ├── Update Pillar
│   ├── Delete Pillar
│   └── Video Assignment
├── Analytics/
│   ├── Dashboard
│   └── Performance Reports
└── Health Checks/
    ├── Basic Health
    ├── System Health
    └── Session Health
```

### Automated Collection Tests

The Postman collection includes automated tests for each endpoint:

```javascript
// Example test script in Postman
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has success field", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
    pm.expect(jsonData.success).to.be.true;
});

pm.test("Response time is less than 5000ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(5000);
});

// Set session cookie for subsequent requests
if (pm.response.code === 200) {
    const cookies = pm.cookies.toObject();
    if (cookies.Vidalytics_session) {
        pm.environment.set("session_cookie", cookies.Vidalytics_session);
    }
}
```

## Automated Testing

### Unit Tests

```bash
# Run unit tests
cd backend
source ../venv/bin/activate
pytest tests/unit/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_redis_session_manager.py -v

# Run with coverage
pytest tests/unit/ --cov=backend --cov-report=term-missing
```

### Integration Tests

```bash
# Run integration tests (requires Redis)
pytest tests/integration/ -v

# Run session integration tests
pytest tests/integration/test_session_integration.py -v

# Run with real services (requires API keys)
INTEGRATION_TESTS=true pytest tests/integration/ -v
```

### API Tests with pytest

```python
# tests/api/test_session_api.py
import pytest
import httpx
import asyncio

@pytest.fixture
def client():
    return httpx.AsyncClient(base_url="http://localhost:8888")

@pytest.mark.asyncio
async def test_login_flow(client):
    # Test login
    login_response = await client.post("/api/session/login", json={
        "user_id": "test_user",
        "password": "test_password"
    })
    
    assert login_response.status_code == 200
    data = login_response.json()
    assert data["success"] is True
    assert "session_id" in data["data"]
    
    # Extract session cookie
    session_cookie = None
    for cookie in login_response.cookies:
        if cookie.name == "Vidalytics_session":
            session_cookie = cookie.value
            break
    
    assert session_cookie is not None
    
    # Test authenticated endpoint
    current_response = await client.get(
        "/api/session/current",
        cookies={"Vidalytics_session": session_cookie}
    )
    
    assert current_response.status_code == 200
    current_data = current_response.json()
    assert current_data["success"] is True
    assert current_data["data"]["user_id"] == "test_user"

@pytest.mark.asyncio 
async def test_chat_endpoint(client):
    # Login first
    login_response = await client.post("/api/session/login", json={
        "user_id": "test_user",
        "password": "test_password"
    })
    
    session_cookie = login_response.cookies["Vidalytics_session"]
    
    # Test chat
    chat_response = await client.post(
        "/api/agent/chat",
        json={
            "message": "Hello, this is a test message",
            "context": {"intent": "testing"}
        },
        cookies={"Vidalytics_session": session_cookie}
    )
    
    assert chat_response.status_code == 200
    data = chat_response.json()
    assert data["success"] is True
    assert "response" in data["data"]
    assert data["data"]["agent_type"] is not None
```

### Load Testing with pytest-benchmark

```python
# tests/performance/test_api_performance.py
import pytest
import httpx
import asyncio

@pytest.fixture
def authenticated_client():
    client = httpx.AsyncClient(base_url="http://localhost:8888")
    
    # Login and get session
    login_response = client.post("/api/session/login", json={
        "user_id": "test_user",
        "password": "test_password"
    })
    
    session_cookie = login_response.cookies["Vidalytics_session"]
    client.cookies.set("Vidalytics_session", session_cookie)
    
    return client

def test_health_endpoint_performance(benchmark, authenticated_client):
    """Test health endpoint performance"""
    def make_health_request():
        response = authenticated_client.get("/health")
        assert response.status_code == 200
        return response
    
    result = benchmark(make_health_request)
    assert result.status_code == 200

@pytest.mark.asyncio
async def test_chat_endpoint_performance(benchmark, authenticated_client):
    """Test chat endpoint performance"""
    async def make_chat_request():
        response = await authenticated_client.post("/api/agent/chat", json={
            "message": "Quick performance test message"
        })
        assert response.status_code == 200
        return response
    
    result = await benchmark(make_chat_request)
    assert result.status_code == 200
```

## Manual Testing

### Test Scenarios

#### 1. Authentication Workflow

**Scenario: Complete authentication flow**
```bash
# Step 1: Login
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "manual_test_user", "password": "test123"}' \
  -c cookies.txt -v

# Expected: 200 OK, Set-Cookie header with session

# Step 2: Verify session
curl -X GET "http://localhost:8888/api/session/current" \
  -b cookies.txt -v

# Expected: 200 OK, user session data

# Step 3: Update session
curl -X PUT "http://localhost:8888/api/session/update" \
  -H "Content-Type: application/json" \
  -d '{"metadata": {"test": "updated"}}' \
  -b cookies.txt -v

# Expected: 200 OK, session updated

# Step 4: Logout
curl -X POST "http://localhost:8888/api/session/logout" \
  -b cookies.txt -v

# Expected: 200 OK, session terminated

# Step 5: Verify logout
curl -X GET "http://localhost:8888/api/session/current" \
  -b cookies.txt -v

# Expected: 401 Unauthorized
```

#### 2. AI Agent Interaction

**Scenario: Chat with AI agent**
```bash
# Prerequisites: Authenticated session
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "ai_test_user", "password": "test123"}' \
  -c cookies.txt

# Test basic chat
curl -X POST "http://localhost:8888/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I improve my YouTube channel performance?",
    "context": {"intent": "performance_optimization"}
  }' \
  -b cookies.txt -v

# Expected: 200 OK, AI response with suggestions

# Test quick action
curl -X POST "http://localhost:8888/api/agent/quick-action" \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "generate_ideas",
    "parameters": {
      "niche": "education",
      "count": 5,
      "trending_focus": true
    }
  }' \
  -b cookies.txt -v

# Expected: 200 OK, generated content ideas
```

#### 3. Content Pillars Management

**Scenario: Complete pillar lifecycle**
```bash
# Prerequisites: Authenticated session
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "pillar_test_user", "password": "test123"}' \
  -c cookies.txt

# Create pillar
curl -X POST "http://localhost:8888/api/pillars" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Educational Content",
    "description": "Educational videos for testing",
    "color": "#3B82F6"
  }' \
  -b cookies.txt -v

# Expected: 201 Created, pillar data with ID

# List pillars
curl -X GET "http://localhost:8888/api/pillars?include_analytics=true" \
  -b cookies.txt -v

# Expected: 200 OK, array of pillars

# Update pillar (use ID from create response)
curl -X PUT "http://localhost:8888/api/pillars/PILLAR_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Educational Content",
    "description": "Updated description"
  }' \
  -b cookies.txt -v

# Expected: 200 OK, updated pillar data

# Delete pillar
curl -X DELETE "http://localhost:8888/api/pillars/PILLAR_ID" \
  -b cookies.txt -v

# Expected: 200 OK, deletion confirmation
```

### Error Case Testing

#### Authentication Errors

```bash
# Test invalid credentials
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "invalid", "password": "wrong"}' -v

# Expected: 401 Unauthorized

# Test expired/invalid session
curl -X GET "http://localhost:8888/api/session/current" \
  -H "Cookie: Vidalytics_session=invalid_session_id" -v

# Expected: 401 Unauthorized

# Test missing authentication
curl -X GET "http://localhost:8888/api/session/current" -v

# Expected: 401 Unauthorized
```

#### Validation Errors

```bash
# Test missing required fields
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{}' -v

# Expected: 400 Bad Request, validation error

# Test invalid data types
curl -X POST "http://localhost:8888/api/pillars" \
  -H "Content-Type: application/json" \
  -d '{"name": 123, "color": "invalid_color"}' \
  -b cookies.txt -v

# Expected: 400 Bad Request, validation error
```

#### Rate Limiting

```bash
# Test rate limiting (run multiple times quickly)
for i in {1..100}; do
  curl -X GET "http://localhost:8888/health" -w "%{http_code}\n" -o /dev/null -s
done

# Expected: Some 429 Too Many Requests responses
```

## Performance Testing

### Load Testing with Artillery

1. **Install Artillery**
   ```bash
   npm install -g artillery
   ```

2. **Create Test Configuration**
   ```yaml
   # artillery-config.yml
   config:
     target: 'http://localhost:8888'
     phases:
       - duration: 60
         arrivalRate: 10
         name: "Warm up"
       - duration: 120
         arrivalRate: 50
         name: "Ramp up load"
       - duration: 60
         arrivalRate: 100
         name: "Sustained high load"
   
   scenarios:
     - name: "Health check load test"
       weight: 30
       flow:
         - get:
             url: "/health"
     
     - name: "Authentication flow test"
       weight: 40
       flow:
         - post:
             url: "/api/session/login"
             json:
               user_id: "load_test_user_{{ $randomNumber(1, 1000) }}"
               password: "test_password"
             capture:
               - json: "$.data.session_id"
                 as: "session_id"
         - get:
             url: "/api/session/current"
             headers:
               Cookie: "Vidalytics_session={{ session_id }}"
     
     - name: "AI chat test"
       weight: 30
       flow:
         - post:
             url: "/api/session/login"
             json:
               user_id: "chat_test_user_{{ $randomNumber(1, 1000) }}"
               password: "test_password"
             capture:
               - json: "$.data.session_id"
                 as: "session_id"
         - post:
             url: "/api/agent/chat"
             headers:
               Cookie: "Vidalytics_session={{ session_id }}"
             json:
               message: "Performance test message {{ $randomNumber(1, 100) }}"
               context:
                 intent: "performance_testing"
   ```

3. **Run Load Test**
   ```bash
   artillery run artillery-config.yml
   ```

### Stress Testing with Locust

1. **Install Locust**
   ```bash
   pip install locust
   ```

2. **Create Test Script**
   ```python
   # locustfile.py
   from locust import HttpUser, task, between
   import json
   
   class VidalyticsUser(HttpUser):
       wait_time = between(1, 3)
       
       def on_start(self):
           """Login when user starts"""
           response = self.client.post("/api/session/login", json={
               "user_id": f"locust_user_{self.environment.runner.user_count}",
               "password": "test_password"
           })
           
           if response.status_code == 200:
               # Session cookie is automatically handled by requests
               self.session_active = True
           else:
               self.session_active = False
       
       @task(3)
       def health_check(self):
           """Test health endpoint"""
           self.client.get("/health")
       
       @task(2)
       def current_session(self):
           """Test session endpoint"""
           if self.session_active:
               self.client.get("/api/session/current")
       
       @task(1)
       def chat_with_ai(self):
           """Test AI chat endpoint"""
           if self.session_active:
               self.client.post("/api/agent/chat", json={
                   "message": "This is a load test message",
                   "context": {"intent": "load_testing"}
               })
       
       @task(1)
       def list_pillars(self):
           """Test pillars endpoint"""
           if self.session_active:
               self.client.get("/api/pillars")
   ```

3. **Run Stress Test**
   ```bash
   # Start with web UI
   locust -f locustfile.py --host=http://localhost:8888
   
   # Or headless mode
   locust -f locustfile.py --host=http://localhost:8888 --users 100 --spawn-rate 10 --run-time 300s --headless
   ```

### Database Performance Testing

```bash
# Test Redis session performance
redis-cli --latency-history -i 1

# Monitor Redis during load tests
redis-cli monitor

# Check Redis memory usage
redis-cli info memory
```

## Security Testing

### Authentication Security

```bash
# Test session hijacking protection
# 1. Login from one IP
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -d '{"user_id": "security_test", "password": "test123"}' \
  -c cookies.txt

# 2. Try to use session from different IP (if IP validation is enabled)
curl -X GET "http://localhost:8888/api/session/current" \
  -H "X-Forwarded-For: 10.0.0.1" \
  -b cookies.txt

# Expected: Potential 401 if IP validation is strict
```

### Input Validation Testing

```bash
# Test SQL injection attempts
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin\"; DROP TABLE users; --", "password": "test"}' -v

# Test XSS attempts
curl -X POST "http://localhost:8888/api/pillars" \
  -H "Content-Type: application/json" \
  -d '{"name": "<script>alert(\"XSS\")</script>", "description": "test"}' \
  -b cookies.txt -v

# Test command injection
curl -X POST "http://localhost:8888/api/agent/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "; rm -rf / ;"}' \
  -b cookies.txt -v

# All should return appropriate validation errors, not execute malicious code
```

### Rate Limiting Testing

```bash
# Test authentication rate limiting
for i in {1..20}; do
  curl -X POST "http://localhost:8888/api/session/login" \
    -H "Content-Type: application/json" \
    -d '{"user_id": "rate_test", "password": "wrong"}' \
    -w "%{http_code}\n" -o /dev/null -s
done

# Should see 429 responses after rate limit is hit
```

## Integration Testing

### External Service Integration

```bash
# Test YouTube API integration (requires valid API key)
curl -X GET "http://localhost:8888/api/youtube/analytics/channel/UC_test_channel?timeframe=7d" \
  -b cookies.txt -v

# Test OAuth flow (requires browser interaction)
curl -X GET "http://localhost:8888/api/oauth/youtube/authorize" \
  -b cookies.txt -v

# Expected: Authorization URL for OAuth flow
```

### Database Integration Testing

```python
# tests/integration/test_database_integration.py
import pytest
import asyncio
from backend.redis_session_manager import get_session_manager

@pytest.mark.asyncio
async def test_redis_session_persistence():
    """Test session data persistence in Redis"""
    session_manager = get_session_manager()
    
    # Create session
    session = await session_manager.create_session(
        user_id="integration_test_user",
        ip_address="127.0.0.1",
        permissions=["user"],
        metadata={"test": "integration"}
    )
    
    # Verify session exists
    retrieved = await session_manager.get_session(session.session_id)
    assert retrieved is not None
    assert retrieved.user_id == "integration_test_user"
    
    # Update session
    success = await session_manager.update_session(
        session.session_id,
        metadata={"test": "updated"}
    )
    assert success is True
    
    # Verify update
    updated = await session_manager.get_session(session.session_id)
    assert updated.metadata["test"] == "updated"
    
    # Cleanup
    await session_manager.revoke_session(session.session_id)
```

## Testing Environments

### Development Environment

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Run tests against development
export API_BASE_URL="http://localhost:8888"
pytest tests/ -v
```

### Staging Environment

```bash
# Deploy to staging
docker-compose -f docker-compose.yml up -d

# Run comprehensive test suite
export API_BASE_URL="https://staging.Vidalytics.com"
pytest tests/ -v --tb=short
```

### Production Environment

```bash
# Run health checks only in production
export API_BASE_URL="https://api.Vidalytics.com"
pytest tests/health/ -v

# Run smoke tests
pytest tests/smoke/ -v
```

## Test Data Management

### Test User Management

```python
# tests/conftest.py - Shared test fixtures
import pytest
import asyncio
from backend.redis_session_manager import get_session_manager

@pytest.fixture
async def test_user_session():
    """Create test user session"""
    session_manager = get_session_manager()
    
    session = await session_manager.create_session(
        user_id="test_user_" + str(uuid.uuid4())[:8],
        ip_address="127.0.0.1",
        permissions=["user"],
        metadata={"test": True}
    )
    
    yield session
    
    # Cleanup
    await session_manager.revoke_session(session.session_id)

@pytest.fixture
def authenticated_client(test_user_session):
    """HTTP client with authenticated session"""
    client = httpx.AsyncClient(base_url="http://localhost:8888")
    client.cookies.set("Vidalytics_session", test_user_session.session_id)
    return client
```

### Test Data Cleanup

```python
# tests/utils/cleanup.py
import asyncio
from backend.redis_session_manager import get_session_manager

async def cleanup_test_sessions():
    """Clean up test sessions"""
    session_manager = get_session_manager()
    
    # Get all sessions
    redis_keys = session_manager.redis.keys("Vidalytics:session:*")
    
    for key in redis_keys:
        session_data = session_manager.redis.get(key)
        if session_data and "test" in session_data:
            session_id = key.split(":")[-1]
            await session_manager.revoke_session(session_id)

# Run cleanup
if __name__ == "__main__":
    asyncio.run(cleanup_test_sessions())
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused

```bash
# Check if API server is running
curl -I http://localhost:8888/health

# Check if Redis is running
redis-cli ping

# Check Docker containers
docker ps
```

#### 2. Authentication Failures

```bash
# Debug session creation
curl -X POST "http://localhost:8888/api/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "debug_user", "password": "test"}' \
  -v -c cookies.txt

# Check cookies
cat cookies.txt

# Debug session validation
curl -X GET "http://localhost:8888/api/session/current" \
  -b cookies.txt -v
```

#### 3. Rate Limiting Issues

```bash
# Check rate limit headers
curl -I -X GET "http://localhost:8888/health"

# Wait for rate limit reset
sleep 60
```

#### 4. API Key Issues

```bash
# Test with API keys
export OPENAI_API_KEY="your_key"
export GOOGLE_API_KEY="your_key"
export YOUTUBE_API_KEY="your_key"

# Restart API server
uvicorn main:app --reload
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG=true

# Run API server with debug output
uvicorn main:app --reload --log-level debug
```

### Performance Issues

```bash
# Monitor Redis performance
redis-cli --latency

# Check API response times
curl -w "@curl-format.txt" -s -o /dev/null http://localhost:8888/health

# curl-format.txt content:
# time_namelookup:  %{time_namelookup}\n
# time_connect:     %{time_connect}\n
# time_appconnect:  %{time_appconnect}\n
# time_pretransfer: %{time_pretransfer}\n
# time_redirect:    %{time_redirect}\n
# time_starttransfer: %{time_starttransfer}\n
# time_total:       %{time_total}\n
```

## Continuous Integration Testing

### GitHub Actions Workflow

```yaml
# .github/workflows/api-tests.yml
name: API Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        pip install pytest pytest-asyncio pytest-cov httpx
    
    - name: Run unit tests
      run: |
        cd backend
        pytest tests/unit/ -v --cov=. --cov-report=xml
    
    - name: Run integration tests
      run: |
        cd backend
        pytest tests/integration/ -v
      env:
        REDIS_URL: redis://localhost:6379/0
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
```

This comprehensive testing guide covers all aspects of testing the Vidalytics API, from basic health checks to complex load testing scenarios. Use these approaches to ensure your API is robust, secure, and performant.