# YouTube Analytics API Documentation

## Overview

The YouTube Analytics API provides comprehensive analytics data for YouTube channels, including channel health, revenue data, subscriber analytics, and content performance metrics.

## Authentication

All analytics endpoints require:
- Valid JWT token in the Authorization header
- YouTube OAuth connection for the user
- Channel owner permissions

```bash
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### 1. Channel Health Analytics

Get comprehensive channel health metrics including subscriber growth, engagement rates, and performance recommendations.

**Endpoint:** `GET /api/analytics/channel-health/{user_id}`

**Parameters:**
- `user_id` (path): User identifier
- `days` (query, optional): Number of days to analyze (default: 30, max: 365)

**Example Request:**
```bash
curl -X GET "http://localhost:8888/api/analytics/channel-health/user123?days=30" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "subscriber_growth_rate": 2.5,
    "view_velocity": 1250.0,
    "engagement_rate": 4.2,
    "upload_consistency": 85.0,
    "audience_retention": 68.5,
    "click_through_rate": 0.078,
    "health_score": 78.5,
    "recommendations": [
      "Focus on subscriber acquisition strategies",
      "Improve thumbnail and title optimization"
    ]
  },
  "metadata": {
    "channel_id": "UC...",
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-01-31"
    },
    "retrieved_at": "2024-01-31T12:00:00"
  }
}
```

### 2. Revenue Analytics

Get detailed revenue analytics including ad revenue, CPM, and monetization metrics.

**Endpoint:** `GET /api/analytics/revenue/{user_id}`

**Parameters:**
- `user_id` (path): User identifier
- `days` (query, optional): Number of days to analyze (default: 30)

**Example Request:**
```bash
curl -X GET "http://localhost:8888/api/analytics/revenue/user123?days=7" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "total_revenue": 123.45,
    "ad_revenue": 98.76,
    "youtube_premium_revenue": 15.50,
    "super_chat_revenue": 9.19,
    "channel_memberships_revenue": 0.0,
    "merchandise_revenue": 0.0,
    "estimated_partner_revenue": 98.76,
    "rpm": 2.47,
    "cpm": 1.85
  },
  "metadata": {
    "channel_id": "UC...",
    "date_range": {
      "start": "2024-01-25",
      "end": "2024-01-31"
    },
    "retrieved_at": "2024-01-31T12:00:00"
  }
}
```

### 3. Subscriber Analytics

Get subscriber growth analytics with daily breakdown and growth trends.

**Endpoint:** `GET /api/analytics/subscribers/{user_id}`

**Parameters:**
- `user_id` (path): User identifier  
- `days` (query, optional): Number of days to analyze (default: 30)

**Example Request:**
```bash
curl -X GET "http://localhost:8888/api/analytics/subscribers/user123?days=14" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "daily_data": [
      {
        "date": "2024-01-17",
        "gained": 15,
        "lost": 3,
        "net_change": 12
      },
      {
        "date": "2024-01-18", 
        "gained": 22,
        "lost": 1,
        "net_change": 21
      }
    ],
    "summary": {
      "net_change": 156,
      "gained": 234,
      "lost": 78,
      "growth_rate": 11.14
    }
  },
  "metadata": {
    "channel_id": "UC...",
    "date_range": {
      "start": "2024-01-17",
      "end": "2024-01-31"
    },
    "retrieved_at": "2024-01-31T12:00:00"
  }
}
```

### 4. Content Performance Analytics

Get performance analytics for recent videos including views, engagement, and rankings.

**Endpoint:** `GET /api/analytics/content-performance/{user_id}`

**Parameters:**
- `user_id` (path): User identifier
- `days` (query, optional): Number of days to analyze (default: 30)

**Example Request:**
```bash
curl -X GET "http://localhost:8888/api/analytics/content-performance/user123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "videos": [
      {
        "video_id": "dQw4w9WgXcQ",
        "title": "Amazing Tutorial Video",
        "published_at": "2024-01-20T10:00:00Z",
        "views": 15420,
        "likes": 892,
        "comments": 156,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
      }
    ],
    "summary": {
      "total_videos": 5,
      "total_views": 45250,
      "average_views": 9050.0,
      "total_engagement": 2845
    }
  },
  "metadata": {
    "channel_id": "UC...",
    "retrieved_at": "2024-01-31T12:00:00"
  }
}
```

### 5. Analytics Status

Check if YouTube Analytics is available for a user and get endpoint information.

**Endpoint:** `GET /api/analytics/status/{user_id}`

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "youtube_connected": true,
    "analytics_available": true,
    "channel_id": "UC...",
    "endpoints": {
      "channel_health": "/api/analytics/channel-health/user123",
      "revenue": "/api/analytics/revenue/user123", 
      "subscribers": "/api/analytics/subscribers/user123",
      "content_performance": "/api/analytics/content-performance/user123"
    },
    "available_parameters": {
      "days": "Number of days to analyze (default: 30, max: 365)"
    }
  }
}
```

### 6. Analytics Overview

Get a comprehensive overview combining all analytics data in a single request.

**Endpoint:** `GET /api/analytics/overview/{user_id}`

**Parameters:**
- `user_id` (path): User identifier
- `days` (query, optional): Number of days to analyze (default: 30)

**Example Response:**
```json
{
  "status": "success",
  "data": {
    "summary": {
      "period": "Last 30 days",
      "generated_at": "2024-01-31T12:00:00"
    },
    "channel_health": { /* Channel health data */ },
    "revenue": { /* Revenue data */ },
    "subscribers": { /* Subscriber data */ },
    "content_performance": { /* Content performance data */ }
  }
}
```

## Error Handling

### Common Error Responses

**401 Unauthorized - No YouTube Connection:**
```json
{
  "detail": "YouTube Analytics access not available. Please connect your YouTube account."
}
```

**403 Forbidden - Access Denied:**
```json
{
  "detail": "Access denied: Cannot access another user's analytics"
}
```

**500 Internal Server Error - API Error:**
```json
{
  "detail": "YouTube Analytics API error: 403"
}
```

### Error Status Codes

- `200` - Success
- `401` - Unauthorized (no valid token or YouTube connection)
- `403` - Forbidden (accessing another user's data)
- `404` - Not Found (invalid user ID)
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error

## Rate Limiting

- **Default Rate Limit:** 60 requests per minute per user
- **Burst Allowance:** 10 additional requests
- **Headers:** Rate limit info included in response headers

## Caching

- **Cache Duration:** 1 hour
- **Cache Key:** Based on user ID, endpoint, and parameters
- **Cache Storage:** SQLite database table `analytics_cache`

## Data Models

### ChannelHealthMetrics
```typescript
interface ChannelHealthMetrics {
  subscriber_growth_rate: number;
  view_velocity: number;
  engagement_rate: number;
  upload_consistency: number;
  audience_retention: number;
  click_through_rate: number;
  health_score: number; // 0-100
  recommendations: string[];
}
```

### RevenueMetrics
```typescript
interface RevenueMetrics {
  total_revenue: number;
  ad_revenue: number;
  youtube_premium_revenue: number;
  super_chat_revenue: number;
  channel_memberships_revenue: number;
  merchandise_revenue: number;
  estimated_partner_revenue: number;
  rpm: number; // Revenue per mille
  cpm: number; // Cost per mille
}
```

## Integration Examples

### JavaScript/Frontend
```javascript
// Get channel health with error handling
async function getChannelHealth(userId, days = 30) {
  try {
    const response = await fetch(`/api/analytics/channel-health/${userId}?days=${days}`, {
      headers: {
        'Authorization': `Bearer ${getJwtToken()}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching channel health:', error);
    throw error;
  }
}

// Get analytics overview
async function getAnalyticsOverview(userId) {
  const response = await fetch(`/api/analytics/overview/${userId}`, {
    headers: { 'Authorization': `Bearer ${getJwtToken()}` }
  });
  return response.json();
}
```

### Python Client
```python
import requests
import json

class YouTubeAnalyticsClient:
    def __init__(self, base_url, jwt_token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
    
    def get_channel_health(self, user_id, days=30):
        url = f"{self.base_url}/api/analytics/channel-health/{user_id}"
        params = {'days': days}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_overview(self, user_id, days=30):
        url = f"{self.base_url}/api/analytics/overview/{user_id}"
        params = {'days': days}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
```

## Setup Requirements

1. **YouTube OAuth Setup:**
   - Configure Google OAuth credentials
   - Enable YouTube Data API v3
   - Enable YouTube Analytics API
   - Set up proper OAuth scopes

2. **Database Setup:**
   - OAuth tokens table with channel_id field
   - Analytics cache table for performance

3. **Environment Variables:**
   ```bash
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   YOUTUBE_API_KEY=your_api_key
   ```

4. **OAuth Scopes Required:**
   ```
   https://www.googleapis.com/auth/youtube.readonly
   https://www.googleapis.com/auth/yt-analytics.readonly
   ```

## Testing

Run the test suite to verify functionality:

```bash
cd backend/App
python test_youtube_analytics.py
```

This will test all endpoints and data models without requiring real YouTube data.