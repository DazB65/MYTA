# OAuth 2.0 Implementation for CreatorMate

## Overview

This document describes the complete OAuth 2.0 authorization flow implementation for CreatorMate, enabling users to securely connect their YouTube accounts for enhanced analytics and data access.

## Architecture

### Components

1. **Backend OAuth Manager** (`backend/oauth_manager.py`)
   - Token storage and management
   - OAuth flow orchestration
   - Token refresh mechanisms
   - YouTube API service authentication

2. **OAuth Endpoints** (`backend/oauth_endpoints.py`)
   - RESTful API endpoints for OAuth operations
   - Authorization initiation and callback handling
   - Token management endpoints

3. **Frontend Integration** (`frontend/components/oauth/`)
   - JavaScript OAuth client
   - UI components for connection status
   - User interaction handling

4. **YouTube API Integration** (`backend/youtube_api_integration.py`)
   - Enhanced to support OAuth authentication
   - Fallback to API key for public data
   - Analytics data access for authenticated users

## Features

### ✅ Implemented Features

- **Complete OAuth 2.0 Flow**
  - Authorization URL generation
  - Callback handling with state validation
  - Authorization code exchange for tokens

- **Secure Token Management**
  - SQLite database storage with encryption
  - Automatic token refresh
  - Token revocation support

- **YouTube API Integration**
  - OAuth-authenticated API calls
  - YouTube Analytics access
  - Enhanced data permissions for channel owners

- **Frontend User Experience**
  - Real-time connection status
  - Seamless authentication flow
  - Error handling and user feedback

- **Security Features**
  - State parameter validation
  - Secure token storage
  - JWT-based internal authentication
  - HTTPS-ready implementation

## Setup Instructions

### 1. Google Cloud Console Configuration

1. **Create OAuth 2.0 Credentials:**
   ```
   - Go to Google Cloud Console
   - Navigate to APIs & Services > Credentials
   - Create OAuth 2.0 Client ID
   - Set application type to "Web application"
   - Add authorized redirect URI: http://localhost:8888/auth/callback
   ```

2. **Configure Consent Screen:**
   ```
   - Set application name: "CreatorMate"
   - Add required scopes:
     - https://www.googleapis.com/auth/youtube.readonly
     - https://www.googleapis.com/auth/yt-analytics.readonly
     - https://www.googleapis.com/auth/yt-analytics-monetary.readonly
   ```

### 2. Environment Configuration

Update your `.env` file with OAuth credentials:

```bash
# Google OAuth 2.0 Configuration
GOOGLE_CLIENT_ID=your_actual_google_client_id_here
GOOGLE_CLIENT_SECRET=your_actual_google_client_secret_here
OAUTH_REDIRECT_URI=http://localhost:8888/auth/callback

# YouTube API Key (fallback for public data)
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 3. Install Dependencies

```bash
pip install google-auth-oauthlib google-auth
```

### 4. Database Initialization

The OAuth tokens table is automatically created on first run:

```sql
CREATE TABLE oauth_tokens (
    user_id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    token_type TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    scope TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

## API Endpoints

### OAuth Management

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/auth/status/{user_id}` | GET | Get OAuth authentication status |
| `/auth/initiate` | POST | Initiate OAuth authorization flow |
| `/auth/callback` | GET | Handle OAuth callback from Google |
| `/auth/refresh/{user_id}` | POST | Refresh OAuth token |
| `/auth/revoke/{user_id}` | DELETE | Revoke OAuth token |
| `/auth/health` | GET | Check OAuth system health |

### YouTube API (OAuth-Enhanced)

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/youtube/analytics` | POST | Get channel data (API key or OAuth) |
| `/api/youtube/analytics/authenticated` | POST | Get detailed analytics (OAuth required) |

## Usage Examples

### 1. Initiate OAuth Flow

```javascript
// Frontend JavaScript
const response = await fetch('/auth/initiate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_id: 'user123',
        return_url: window.location.href
    })
});

const data = await response.json();
// Redirect user to data.authorization_url
window.location.href = data.authorization_url;
```

### 2. Check Authentication Status

```javascript
const response = await fetch('/auth/status/user123');
const status = await response.json();

if (status.authenticated) {
    console.log('User is authenticated');
    console.log('Token expires in:', status.expires_in_seconds, 'seconds');
} else {
    console.log('User needs to authenticate');
}
```

### 3. Get Authenticated YouTube Data

```javascript
const response = await fetch('/api/youtube/analytics/authenticated', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        channel_id: 'UC1234567890',
        user_id: 'user123',
        include_videos: true,
        video_count: 10
    })
});

const data = await response.json();
// Access detailed analytics data
console.log('Analytics:', data.analytics_data);
```

### 4. Backend Token Management

```python
from oauth_manager import get_oauth_manager

oauth_manager = get_oauth_manager()

# Get valid token (auto-refreshes if needed)
token = await oauth_manager.get_valid_token('user123')

# Get authenticated YouTube service
service = await oauth_manager.get_youtube_service('user123')

# Get analytics service
analytics = await oauth_manager.get_youtube_service('user123', 'youtubeAnalytics', 'v2')
```

## Security Considerations

### 1. Token Storage
- Tokens stored in SQLite database with restricted file permissions
- Access tokens have limited lifetime (1 hour typical)
- Refresh tokens used for automatic renewal

### 2. State Validation
- Cryptographically secure state parameters
- State expiration (10 minutes)
- Protection against CSRF attacks

### 3. Scope Limitations
- Read-only access to YouTube data
- No permissions to modify channel content
- Minimal required scopes requested

### 4. Error Handling
- Graceful degradation when OAuth unavailable
- Comprehensive error logging
- User-friendly error messages

## Frontend Integration

### OAuth Status Display

The sidebar automatically shows OAuth connection status:

```html
<!-- Connected State -->
<div class="oauth-status connected">
    <span class="status-icon">✓</span>
    <span class="status-text">YouTube Connected</span>
</div>

<!-- Disconnected State -->
<div class="oauth-status disconnected">
    <span class="status-icon">⚠</span>
    <span class="status-text">YouTube Not Connected</span>
</div>
```

### Connection Button

Dynamic button that changes based on authentication state:

```html
<button id="oauth-connect-btn">
    Connect YouTube / Disconnect YouTube / Connecting...
</button>
```

## Testing

### 1. Run Implementation Test

```bash
python simple_oauth_test.py
```

### 2. Test OAuth Health

```bash
curl http://localhost:8888/auth/health
```

### 3. Manual Testing Flow

1. Start server: `uvicorn main:app --reload --host 0.0.0.0 --port 8888`
2. Open frontend: `http://localhost:8888`
3. Click "Connect YouTube" in sidebar
4. Complete Google OAuth flow
5. Verify connection status updates

## Troubleshooting

### Common Issues

1. **"OAuth not configured" Error**
   - Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
   - Verify credentials are not placeholder values

2. **"Redirect URI mismatch" Error**
   - Ensure redirect URI in Google Console matches OAUTH_REDIRECT_URI
   - Check for http vs https differences

3. **"Invalid client" Error**
   - Verify Google OAuth client is properly configured
   - Check client ID and secret are correct

4. **Token Refresh Failures**
   - Ensure refresh token is still valid
   - Re-authenticate if refresh token expired

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features

1. **Multiple Account Support**
   - Support for multiple YouTube accounts per user
   - Account switching interface

2. **Advanced Permissions**
   - Selective scope requests
   - Permission management UI

3. **Enhanced Analytics**
   - Real-time data sync
   - Historical data caching
   - Advanced metrics calculations

4. **Security Improvements**
   - Token encryption at rest
   - Enhanced audit logging
   - Rate limiting implementation

## Conclusion

The OAuth 2.0 implementation provides secure, standards-compliant authentication for YouTube API access. The system supports both public API usage (with API keys) and authenticated access (with OAuth tokens), ensuring maximum functionality while maintaining security best practices.

For production deployment, ensure all security recommendations are followed and OAuth credentials are properly secured.