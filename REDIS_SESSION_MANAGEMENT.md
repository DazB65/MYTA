# Redis Session Management System

## Overview

CreatorMate now includes a comprehensive Redis-based session management system that provides secure, scalable session handling with the following features:

- **Secure session storage** with Redis backend
- **Automatic session expiry** and cleanup
- **Session refresh** for long-running sessions
- **Multi-session support** per user with configurable limits
- **IP address validation** for security
- **Comprehensive session management API**
- **Integration with FastAPI middleware**

## Architecture

### Components

1. **RedisSessionManager** (`redis_session_manager.py`)
   - Core session management logic
   - Redis integration and connection handling
   - Session lifecycle management
   - Performance monitoring and statistics

2. **SessionMiddleware** (`session_middleware.py`)
   - FastAPI middleware for request processing
   - Session extraction from cookies/headers
   - Security validation
   - Automatic session refresh

3. **Session Router** (`session_router.py`)
   - REST API endpoints for session management
   - Authentication and authorization
   - Session CRUD operations
   - Statistics and health checks

4. **Session Data Models**
   - `SessionData`: Core session data structure
   - `SessionStatus`: Session state enumeration
   - `RedisSessionConfig`: Configuration management

## Features

### Security Features

- **Secure session ID generation** using cryptographic randomness
- **IP address validation** (configurable)
- **User agent tracking** for suspicious activity detection
- **Session timeout** with automatic cleanup
- **Maximum sessions per user** to prevent abuse
- **HTTP-only cookies** to prevent XSS attacks
- **Secure cookie settings** for production environments

### Session Management

- **Create sessions** with custom metadata and permissions
- **Update session data** including permissions and metadata
- **Retrieve session information** with automatic refresh
- **Revoke individual sessions** or all user sessions
- **List all user sessions** with filtering
- **Session statistics** and health monitoring

### Performance Features

- **Automatic session refresh** to reduce database load
- **Redis TTL** for automatic cleanup
- **Connection pooling** for optimal Redis performance
- **Performance metrics** logging
- **Health check endpoints** for monitoring

## Configuration

### Environment Variables

```bash
# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password

# Session Configuration
SESSION_TIMEOUT_HOURS=8
SESSION_REFRESH_THRESHOLD_HOURS=1
MAX_SESSIONS_PER_USER=10
SESSION_SECRET_KEY=your_secret_key

# Security Settings
SECURE_COOKIES=true
HTTPONLY_COOKIES=true
SAMESITE_POLICY=strict
```

### Session Configuration

The system uses `RedisSessionConfig` for configuration:

```python
config = RedisSessionConfig()
config.session_timeout = timedelta(hours=8)        # Session expiry time
config.refresh_threshold = timedelta(hours=1)      # Auto-refresh threshold
config.max_sessions_per_user = 10                  # Session limit per user
config.secure_cookies = True                       # HTTPS-only cookies
config.httponly_cookies = True                     # Prevent XSS access
```

## API Endpoints

### Authentication Endpoints

- `POST /api/session/login` - Create new session (login)
- `POST /api/session/logout` - Revoke current session (logout)
- `POST /api/session/logout-all` - Revoke all other sessions
- `GET /api/session/current` - Get current session info

### Session Management Endpoints

- `GET /api/session/list` - List all user sessions
- `PUT /api/session/update` - Update current session data
- `DELETE /api/session/revoke/{session_id}` - Revoke specific session
- `GET /api/session/stats` - Get session statistics (admin)
- `GET /api/session/health` - Session system health check

## Usage Examples

### Creating a Session

```python
from session_middleware import create_user_session

session_data = await create_user_session(
    user_id="user123",
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0...",
    permissions=["user", "read"],
    metadata={"device": "mobile", "app_version": "1.0.0"}
)
```

### Using Session Dependencies

```python
from fastapi import Depends
from session_middleware import require_auth, require_admin

@app.get("/protected")
async def protected_endpoint(session: SessionData = Depends(require_auth)):
    return {"user_id": session.user_id, "permissions": session.permissions}

@app.get("/admin-only")
async def admin_endpoint(session: SessionData = Depends(require_admin)):
    return {"message": "Admin access granted"}
```

### Session Middleware Integration

```python
from fastapi import FastAPI
from session_middleware import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware)
```

## Session Data Structure

```python
@dataclass
class SessionData:
    session_id: str                    # Unique session identifier
    user_id: str                       # User identifier
    created_at: datetime               # Session creation time
    last_accessed: datetime            # Last access time
    expires_at: datetime               # Session expiry time
    status: SessionStatus              # Session status (ACTIVE, EXPIRED, REVOKED)
    ip_address: Optional[str]          # Client IP address
    user_agent: Optional[str]          # Client user agent
    permissions: List[str]             # User permissions
    metadata: Dict[str, Any]           # Custom session metadata
```

## Redis Storage

### Key Structure

- Session data: `creatormate:session:{session_id}`
- User sessions: `creatormate:user_sessions:{user_id}` (set of session IDs)
- Session stats: `creatormate:session_stats` (hash of daily statistics)

### Data Storage

Sessions are stored as JSON in Redis with automatic TTL:

```json
{
    "session_id": "abc123...",
    "user_id": "user123",
    "created_at": "2024-01-01T12:00:00Z",
    "last_accessed": "2024-01-01T12:30:00Z",
    "expires_at": "2024-01-01T20:00:00Z",
    "status": "active",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "permissions": ["user", "read"],
    "metadata": {"device": "mobile"}
}
```

## Security Considerations

### Production Deployment

1. **Use HTTPS** for all session-related communication
2. **Set secure cookie flags** (`secure`, `httponly`, `samesite`)
3. **Configure IP validation** for additional security
4. **Monitor session statistics** for unusual activity
5. **Use strong Redis passwords** and network security
6. **Regular session cleanup** to prevent data accumulation

### Session Security

- Session IDs are generated using cryptographic randomness
- Sessions automatically expire after the configured timeout
- IP address validation can detect session hijacking attempts
- User agent changes are logged for monitoring
- Session revocation is immediate and affects all session stores

## Monitoring and Maintenance

### Health Checks

The system includes comprehensive health checks:

```python
# Check Redis connection and performance
health_data = await session_manager.health_check()
# Returns: status, response_time_ms, redis_version, memory_usage, etc.
```

### Session Statistics

Monitor session usage with built-in statistics:

```python
# Get session statistics
stats = await session_manager.get_session_stats()
# Returns: daily_stats, total_active_sessions, redis_info
```

### Cleanup and Maintenance

- Automatic cleanup of expired sessions via Redis TTL
- Manual cleanup function: `cleanup_expired_sessions()`
- Session limit enforcement prevents user session accumulation
- Redis memory usage monitoring and alerts

## Testing

### Code Validation

Run the code validation test to verify implementation:

```bash
python3 test_session_code_validation.py
```

### Integration Testing

With Redis running, test the full integration:

```bash
# Start Redis
redis-server

# Run integration tests
python3 test_redis_session_integration.py
```

### Unit Tests

```bash
# Run unit tests
pytest tests/unit/test_redis_session_manager.py

# Run integration tests  
pytest tests/integration/test_session_integration.py
```

## Docker Integration

The session management system is fully integrated with Docker:

### Development Environment

```bash
# Start with Redis
docker-compose -f docker-compose.dev.yml up

# With admin tools
docker-compose -f docker-compose.dev.yml --profile tools up
```

### Production Environment

```bash
# Production deployment
docker-compose up -d

# With monitoring
docker-compose --profile monitoring up -d
```

## Migration from Existing Auth

To migrate from the existing JWT-based authentication:

1. **Phase 1**: Deploy Redis session system alongside existing auth
2. **Phase 2**: Update frontend to use session cookies instead of JWT tokens
3. **Phase 3**: Migrate existing user sessions to Redis
4. **Phase 4**: Remove legacy JWT authentication code

## Troubleshooting

### Common Issues

1. **Redis Connection Refused**
   - Ensure Redis is running: `redis-server`
   - Check Redis configuration and network access
   - Verify environment variables: `REDIS_URL`, `REDIS_HOST`, `REDIS_PORT`

2. **Session Not Found**
   - Check session expiry time
   - Verify Redis data persistence
   - Check session cleanup processes

3. **Cookie Issues**
   - Verify secure cookie settings for HTTPS
   - Check SameSite policy for cross-origin requests
   - Ensure proper domain and path configuration

4. **Performance Issues**
   - Monitor Redis memory usage
   - Check session cleanup frequency
   - Review session timeout settings
   - Monitor Redis connection pool usage

### Logging

The system provides comprehensive logging:

- Session creation, access, and revocation events
- Security validation failures
- Performance metrics
- Redis connection issues
- Cleanup and maintenance operations

Check logs for detailed information about session system operation and any issues.

## Future Enhancements

- **Distributed session management** for multi-instance deployments
- **Session analytics** and user behavior tracking
- **Advanced security features** like device fingerprinting
- **Session sharing** across multiple applications
- **Real-time session monitoring** dashboard
- **Automated security incident response**