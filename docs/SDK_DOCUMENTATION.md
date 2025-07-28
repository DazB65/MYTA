# CreatorMate SDK Documentation

## Overview

The CreatorMate SDK provides easy-to-use client libraries for integrating with the CreatorMate API. Available in multiple programming languages, the SDK handles authentication, rate limiting, error handling, and provides strongly-typed interfaces for all API operations.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Authentication](#authentication)
4. [SDK Methods](#sdk-methods)
5. [Error Handling](#error-handling)
6. [Advanced Usage](#advanced-usage)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Installation

### Python SDK

```bash
pip install creatormate-sdk
```

### JavaScript/TypeScript SDK

```bash
npm install @creatormate/sdk
# or
yarn add @creatormate/sdk
```

### Go SDK

```bash
go get github.com/creatormate/sdk-go
```

### PHP SDK

```bash
composer require creatormate/sdk
```

## Quick Start

### Python

```python
from creatormate_sdk import CreatorMateClient
import asyncio

async def main():
    # Initialize client
    client = CreatorMateClient(
        base_url="http://localhost:8888",  # or https://api.creatormate.com
        user_id="your_user_id"
    )
    
    # Login and create session
    session = await client.auth.login(password="your_password")
    print(f"Logged in as: {session.user_id}")
    
    # Chat with AI agent
    response = await client.agent.chat(
        message="How can I improve my video thumbnails?",
        context={"intent": "thumbnail_optimization"}
    )
    print(f"AI Response: {response.message}")
    
    # Get channel analytics
    analytics = await client.youtube.get_channel_analytics(
        channel_id="UC123456789",
        timeframe="30d",
        metrics=["views", "engagement", "retention"]
    )
    print(f"Total views: {analytics.summary.total_views}")
    
    # Create content pillar
    pillar = await client.pillars.create(
        name="Educational Content",
        description="Tutorial and how-to videos",
        color="#3B82F6"
    )
    print(f"Created pillar: {pillar.name}")

# Run async function
asyncio.run(main())
```

### JavaScript/TypeScript

```typescript
import { CreatorMateClient } from '@creatormate/sdk';

const client = new CreatorMateClient({
  baseUrl: 'http://localhost:8888',
  userId: 'your_user_id'
});

async function main() {
  // Login
  const session = await client.auth.login({
    password: 'your_password'
  });
  console.log(`Logged in as: ${session.userId}`);

  // Chat with AI
  const chatResponse = await client.agent.chat({
    message: 'What trending topics should I cover this week?',
    context: { intent: 'content_planning' }
  });
  console.log(`AI Response: ${chatResponse.message}`);

  // Get analytics
  const analytics = await client.youtube.getChannelAnalytics({
    channelId: 'UC123456789',
    timeframe: '7d',
    includeVideos: true
  });
  console.log(`Total views: ${analytics.summary.totalViews}`);

  // Create pillar
  const pillar = await client.pillars.create({
    name: 'Tech Reviews',
    description: 'Product reviews and tech content',
    color: '#10B981'
  });
  console.log(`Created pillar: ${pillar.name}`);
}

main().catch(console.error);
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    
    "github.com/creatormate/sdk-go"
)

func main() {
    // Initialize client
    client := creatormate.NewClient(&creatormate.Config{
        BaseURL: "http://localhost:8888",
        UserID:  "your_user_id",
    })
    
    ctx := context.Background()
    
    // Login
    session, err := client.Auth.Login(ctx, &creatormate.LoginRequest{
        Password: "your_password",
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Logged in as: %s\n", session.UserID)
    
    // Chat with AI
    chatResp, err := client.Agent.Chat(ctx, &creatormate.ChatRequest{
        Message: "How can I optimize my upload schedule?",
        Context: map[string]interface{}{
            "intent": "scheduling_optimization",
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("AI Response: %s\n", chatResp.Message)
    
    // Get analytics
    analytics, err := client.YouTube.GetChannelAnalytics(ctx, &creatormate.AnalyticsRequest{
        ChannelID: "UC123456789",
        Timeframe: "30d",
        Metrics:   []string{"views", "subscribers", "engagement"},
    })
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Total views: %d\n", analytics.Summary.TotalViews)
}
```

## Authentication

### Session-Based Authentication

The SDK uses session-based authentication with automatic session management:

```python
# Python
client = CreatorMateClient(
    base_url="https://api.creatormate.com",
    user_id="creator123"
)

# Login creates and manages session automatically
session = await client.auth.login(password="secure_password")

# All subsequent requests use the session automatically
# No need to manually handle session tokens
```

```typescript
// TypeScript
const client = new CreatorMateClient({
  baseUrl: 'https://api.creatormate.com',
  userId: 'creator123'
});

// Login and session management is automatic
await client.auth.login({ password: 'secure_password' });

// All API calls now use the authenticated session
```

### Session Management

```python
# Check current session
current_session = await client.auth.get_current_session()
print(f"Session expires at: {current_session.expires_at}")

# List all user sessions
sessions = await client.auth.list_sessions()
print(f"Active sessions: {len(sessions)}")

# Logout from current session
await client.auth.logout()

# Logout from all other sessions
await client.auth.logout_all()

# Update session metadata
await client.auth.update_session(
    metadata={"device": "mobile", "app_version": "2.0.0"}
)
```

### Token Refresh

Session tokens are automatically refreshed by the SDK:

```python
# Automatic refresh is handled internally
# You can also manually check/refresh
if await client.auth.needs_refresh():
    await client.auth.refresh_session()
```

## SDK Methods

### Agent System

#### Chat Interface

```python
# Basic chat
response = await client.agent.chat(
    message="How can I improve my CTR?",
    context={"intent": "performance_optimization"}
)

# Advanced chat with preferences
response = await client.agent.chat(
    message="Analyze my latest video performance",
    context={
        "video_id": "dQw4w9WgXcQ",
        "intent": "video_analysis"
    },
    preferences={
        "response_length": "detailed",
        "include_suggestions": True,
        "analysis_depth": "deep"
    }
)

print(f"Response: {response.message}")
print(f"Confidence: {response.confidence_score}")
print(f"Suggestions: {len(response.suggestions)}")
```

#### Quick Actions

```python
# Generate video script
script = await client.agent.quick_action(
    action_type="generate_script",
    parameters={
        "topic": "YouTube SEO in 2024",
        "duration": "10-15 minutes",
        "style": "educational",
        "target_audience": "beginner"
    }
)

# Analyze thumbnails
analysis = await client.agent.quick_action(
    action_type="analyze_thumbnails",
    parameters={
        "video_ids": ["video1", "video2", "video3"],
        "comparison_type": "performance"
    }
)

# Generate content ideas
ideas = await client.agent.quick_action(
    action_type="generate_ideas",
    parameters={
        "niche": "tech education",
        "count": 10,
        "trending_focus": True
    }
)
```

#### Insights

```python
# Get AI insights
insights = await client.agent.get_insights(
    categories=["performance", "content", "audience"],
    limit=5
)

# Generate fresh insights
new_insights = await client.agent.generate_insights(
    analysis_depth="standard",
    timeframe="30d",
    focus_areas=["thumbnails", "titles", "timing"]
)

for insight in insights:
    print(f"Title: {insight.title}")
    print(f"Priority: {insight.priority}")
    print(f"Confidence: {insight.confidence_score}")
```

### YouTube Integration

#### Channel Analytics

```python
# Get channel analytics
analytics = await client.youtube.get_channel_analytics(
    channel_id="UC123456789",
    timeframe="30d",
    metrics=["views", "engagement", "retention", "revenue"],
    include_videos=True
)

print(f"Total views: {analytics.summary.total_views}")
print(f"Subscriber growth: {analytics.summary.subscriber_growth}")
print(f"Average CTR: {analytics.summary.average_ctr}")
```

#### Video Data

```python
# Get video details
video = await client.youtube.get_video(
    video_id="dQw4w9WgXcQ",
    include_analytics=True,
    include_comments=False
)

print(f"Title: {video.title}")
print(f"Views: {video.analytics.views}")
print(f"CTR: {video.analytics.click_through_rate}")
print(f"Retention: {video.analytics.average_view_duration}")
```

#### Search and Trends

```python
# Search videos
results = await client.youtube.search(
    query="python tutorial",
    max_results=25,
    order="viewCount",
    published_after="2024-01-01"
)

# Get trending videos
trending = await client.youtube.get_trending(
    region_code="US",
    category_id="22",  # People & Blogs
    max_results=50
)

for video in trending.videos:
    print(f"Trending: {video.title} - {video.view_count} views")
```

### Content Pillars

#### Pillar Management

```python
# List all pillars
pillars = await client.pillars.list(
    include_videos=True,
    include_analytics=True
)

# Create new pillar
pillar = await client.pillars.create(
    name="Gaming Content",
    description="Gaming videos, reviews, and tutorials",
    color="#EF4444",
    metadata={
        "target_audience": "gamers",
        "content_frequency": "daily"
    }
)

# Get pillar details
pillar_details = await client.pillars.get(
    pillar_id=pillar.id,
    include_videos=True,
    include_analytics=True
)

# Update pillar
updated_pillar = await client.pillars.update(
    pillar_id=pillar.id,
    name="Advanced Gaming Content",
    description="In-depth gaming analysis and reviews"
)

# Delete pillar
await client.pillars.delete(pillar_id=pillar.id)
```

#### Video Assignment

```python
# Assign video to pillar
assignment = await client.pillars.assign_video(
    pillar_id="pillar_123",
    video_id="dQw4w9WgXcQ",
    notes="Perfect fit for educational content",
    confidence_score=0.95
)

# Remove video from pillar
await client.pillars.remove_video(
    pillar_id="pillar_123",
    video_id="dQw4w9WgXcQ"
)

# Get unassigned videos
unassigned = await client.pillars.get_unassigned_videos(
    limit=25,
    sort_by="published_at"
)

for video in unassigned.videos:
    print(f"Unassigned: {video.title}")
    if video.suggested_pillars:
        best_match = video.suggested_pillars[0]
        print(f"  Suggested: {best_match.pillar_name} ({best_match.confidence_score})")
```

### Analytics

#### Dashboard Analytics

```python
# Get dashboard data
dashboard = await client.analytics.get_dashboard(
    timeframe="30d",
    include_predictions=True,
    include_insights=True
)

print(f"Total views: {dashboard.summary.total_views}")
print(f"Subscriber growth: {dashboard.summary.total_subscribers}")
print(f"Revenue: ${dashboard.summary.revenue}")

# Performance metrics
for metric_name, metric_data in dashboard.performance_metrics.items():
    print(f"{metric_name}: {metric_data.current} ({metric_data.change_percent:+.1f}%)")
```

#### Performance Reports

```python
# Get detailed performance data
performance = await client.analytics.get_performance(
    metric_type="views",
    start_date="2024-01-01",
    end_date="2024-01-31",
    granularity="daily",
    breakdown_by="pillar"
)

print(f"Total {performance.metric_type}: {performance.summary.total}")
print(f"Growth rate: {performance.summary.growth_rate:.2%}")

# Time series data
for point in performance.time_series:
    print(f"{point.date}: {point.value}")

# Breakdown data
for item in performance.breakdown.by_pillar:
    print(f"{item.pillar_name}: {item.value} ({item.percentage:.1f}%)")
```

### OAuth Management

```python
# Check OAuth status
oauth_status = await client.oauth.get_youtube_status()
print(f"Connected: {oauth_status.connected}")
print(f"Channel: {oauth_status.channel_title}")

# Initiate OAuth flow
auth_url = await client.oauth.get_authorization_url(
    redirect_uri="https://your-app.com/callback"
)
print(f"Authorize at: {auth_url}")

# Handle callback (typically in your web application)
await client.oauth.handle_callback(
    code="oauth_code_from_callback",
    state="state_parameter"
)

# Disconnect OAuth
await client.oauth.disconnect_youtube()
```

## Error Handling

### Exception Types

```python
from creatormate_sdk.exceptions import (
    CreatorMateAPIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    NotFoundError,
    ServerError
)

try:
    response = await client.agent.chat(message="Hello")
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Handle re-authentication
    await client.auth.login(password="password")
    
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
    await asyncio.sleep(e.retry_after)
    
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Invalid field: {e.field}")
    
except NotFoundError as e:
    print(f"Resource not found: {e.message}")
    
except ServerError as e:
    print(f"Server error: {e.message}")
    # Implement retry logic
    
except CreatorMateAPIError as e:
    print(f"API error: {e.message} (Code: {e.error_code})")
```

### Retry Logic

```python
import asyncio
from creatormate_sdk.exceptions import RateLimitError, ServerError

async def with_retry(func, max_retries=3, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            return await func()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(e.retry_after)
                continue
            raise
        except ServerError as e:
            if attempt < max_retries - 1:
                delay = backoff_factor ** attempt
                await asyncio.sleep(delay)
                continue
            raise

# Usage
response = await with_retry(
    lambda: client.agent.chat(message="Hello")
)
```

### Global Error Handler

```python
# Set up global error handler
async def handle_api_error(error: CreatorMateAPIError):
    if isinstance(error, AuthenticationError):
        # Redirect to login
        await client.auth.login(password="password")
    elif isinstance(error, RateLimitError):
        # Implement backoff
        await asyncio.sleep(error.retry_after)
    else:
        # Log error for monitoring
        print(f"API Error: {error}")

client.set_error_handler(handle_api_error)
```

## Advanced Usage

### Configuration

```python
from creatormate_sdk import CreatorMateClient, Config

# Advanced configuration
config = Config(
    base_url="https://api.creatormate.com",
    timeout=30,  # Request timeout in seconds
    max_retries=3,  # Automatic retry attempts
    backoff_factor=2,  # Exponential backoff multiplier
    rate_limit_retry=True,  # Automatically retry on rate limit
    verify_ssl=True,  # SSL certificate verification
    user_agent="MyApp/1.0.0",  # Custom user agent
    debug=False  # Enable debug logging
)

client = CreatorMateClient(
    user_id="your_user_id",
    config=config
)
```

### Caching

```python
# Enable response caching
client.enable_caching(
    cache_duration=300,  # 5 minutes
    cache_size=1000,  # Maximum cached responses
    cache_patterns=[
        "/api/youtube/analytics/*",  # Cache analytics data
        "/api/pillars",  # Cache pillar lists
    ]
)

# Cache-specific request
analytics = await client.youtube.get_channel_analytics(
    channel_id="UC123456789",
    timeframe="30d",
    use_cache=True,  # Use cached data if available
    cache_ttl=600  # Custom cache duration
)
```

### Pagination

```python
# Manual pagination
page = 1
all_videos = []

while True:
    response = await client.youtube.search(
        query="tutorial",
        max_results=50,
        page=page
    )
    
    all_videos.extend(response.videos)
    
    if not response.has_next_page:
        break
    
    page += 1

# Automatic pagination
async for video in client.youtube.search_all(
    query="tutorial",
    max_results=1000  # Total limit across all pages
):
    print(f"Video: {video.title}")
```

### Batch Operations

```python
# Batch video analysis
video_ids = ["video1", "video2", "video3", "video4", "video5"]

# Process in batches
batch_size = 3
results = []

for i in range(0, len(video_ids), batch_size):
    batch = video_ids[i:i + batch_size]
    
    # Create batch request
    batch_results = await client.youtube.get_videos_batch(
        video_ids=batch,
        include_analytics=True
    )
    
    results.extend(batch_results)

print(f"Processed {len(results)} videos")
```

### Webhooks

```python
# Configure webhooks
webhook = await client.webhooks.create(
    url="https://your-app.com/webhooks/creatormate",
    events=[
        "agent.response_completed",
        "youtube.video_published",
        "analytics.threshold_reached"
    ],
    secret="your_webhook_secret"
)

# List webhooks
webhooks = await client.webhooks.list()

# Update webhook
await client.webhooks.update(
    webhook_id=webhook.id,
    events=["agent.response_completed"]
)

# Delete webhook
await client.webhooks.delete(webhook_id=webhook.id)
```

## Examples

### Complete YouTube Analytics Dashboard

```python
import asyncio
from creatormate_sdk import CreatorMateClient
from datetime import datetime, timedelta

async def create_analytics_dashboard():
    client = CreatorMateClient(
        base_url="https://api.creatormate.com",
        user_id="creator123"
    )
    
    # Login
    await client.auth.login(password="secure_password")
    
    # Get channel info
    oauth_status = await client.oauth.get_youtube_status()
    if not oauth_status.connected:
        print("Please connect your YouTube account first")
        return
    
    channel_id = oauth_status.channel_id
    
    # Get comprehensive analytics
    analytics = await client.youtube.get_channel_analytics(
        channel_id=channel_id,
        timeframe="30d",
        metrics=["views", "engagement", "retention", "revenue"],
        include_videos=True
    )
    
    # Get dashboard data
    dashboard = await client.analytics.get_dashboard(
        timeframe="30d",
        include_predictions=True,
        include_insights=True
    )
    
    # Get content pillars performance
    pillars = await client.pillars.list(
        include_analytics=True
    )
    
    # Display results
    print("📊 YouTube Analytics Dashboard")
    print("=" * 40)
    
    print(f"📺 Channel: {oauth_status.channel_title}")
    print(f"👥 Subscribers: {analytics.summary.total_subscribers:,}")
    print(f"👀 Views (30d): {analytics.summary.total_views:,}")
    print(f"💰 Revenue (30d): ${analytics.summary.revenue:,.2f}")
    print(f"📈 CTR: {analytics.summary.average_ctr:.2%}")
    print(f"⏱️  Retention: {analytics.summary.average_retention:.1%}")
    
    print("\n🎯 Content Pillars Performance:")
    for pillar in pillars:
        if pillar.analytics:
            print(f"  {pillar.name}: {pillar.analytics.total_views:,} views")
    
    print("\n🔍 AI Insights:")
    for insight in dashboard.ai_insights[:3]:
        print(f"  • {insight.title}")
        print(f"    {insight.description}")
        print(f"    Confidence: {insight.confidence:.0%}")
    
    print("\n📈 Predictions:")
    if dashboard.predictions:
        pred = dashboard.predictions
        print(f"  Next month views: {pred.next_month_views:,}")
        if pred.subscriber_milestone:
            milestone = pred.subscriber_milestone
            print(f"  {milestone.target:,} subscribers by {milestone.estimated_date}")
    
    # Generate content recommendations
    ideas = await client.agent.quick_action(
        action_type="generate_ideas",
        parameters={
            "niche": "youtube_growth",
            "count": 5,
            "trending_focus": True
        }
    )
    
    print("\n💡 Content Ideas:")
    for i, idea in enumerate(ideas.result.ideas[:5], 1):
        print(f"  {i}. {idea.title}")
        print(f"     {idea.description}")

if __name__ == "__main__":
    asyncio.run(create_analytics_dashboard())
```

### AI-Powered Content Optimization

```python
async def optimize_content():
    client = CreatorMateClient(user_id="creator123")
    await client.auth.login(password="secure_password")
    
    # Get recent videos
    unassigned_videos = await client.pillars.get_unassigned_videos(limit=10)
    
    for video in unassigned_videos.videos:
        print(f"\n🎥 Optimizing: {video.title}")
        
        # Analyze video performance
        analysis = await client.agent.quick_action(
            action_type="analyze_video",
            parameters={
                "video_id": video.video_id,
                "analysis_type": "comprehensive"
            }
        )
        
        print(f"Performance Score: {analysis.result.performance_score:.2f}")
        
        # Get optimization suggestions
        optimization = await client.agent.chat(
            message=f"How can I optimize this video: {video.title}",
            context={
                "video_id": video.video_id,
                "intent": "video_optimization"
            }
        )
        
        print("🚀 Optimization Suggestions:")
        for suggestion in optimization.suggestions:
            print(f"  • {suggestion.title}: {suggestion.description}")
        
        # Auto-assign to pillar if confidence is high
        if video.suggested_pillars:
            best_match = video.suggested_pillars[0]
            if best_match.confidence_score > 0.8:
                await client.pillars.assign_video(
                    pillar_id=best_match.pillar_id,
                    video_id=video.video_id,
                    confidence_score=best_match.confidence_score
                )
                print(f"✅ Auto-assigned to: {best_match.pillar_name}")

if __name__ == "__main__":
    asyncio.run(optimize_content())
```

## Troubleshooting

### Common Issues

#### Authentication Problems

```python
# Check session status
try:
    session = await client.auth.get_current_session()
    print(f"Session valid until: {session.expires_at}")
except AuthenticationError:
    print("Session expired, re-authenticating...")
    await client.auth.login(password="password")

# Debug authentication
client.config.debug = True
await client.auth.login(password="password")  # Will show debug info
```

#### Rate Limiting

```python
# Handle rate limits gracefully
from creatormate_sdk.exceptions import RateLimitError

try:
    response = await client.agent.chat(message="Hello")
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
    print(f"Current limit: {e.limit} requests per minute")
    print(f"Remaining: {e.remaining} requests")
    
    # Wait and retry
    await asyncio.sleep(e.retry_after)
    response = await client.agent.chat(message="Hello")
```

#### Connection Issues

```python
# Configure timeouts and retries
config = Config(
    timeout=60,  # Increase timeout for slow connections
    max_retries=5,  # More retry attempts
    backoff_factor=3,  # Longer backoff between retries
    verify_ssl=False  # Only for development with self-signed certs
)

client = CreatorMateClient(user_id="creator123", config=config)

# Test connection
try:
    health = await client.health.check()
    print(f"API Status: {health.status}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Debug Mode

```python
# Enable debug logging
import logging

logging.basicConfig(level=logging.DEBUG)

# Enable SDK debug mode
client.config.debug = True

# All requests/responses will be logged
response = await client.agent.chat(message="Test")
```

### Error Reporting

```python
# Report issues to CreatorMate support
try:
    response = await client.agent.chat(message="Hello")
except CreatorMateAPIError as e:
    # Generate error report
    error_report = client.generate_error_report(e)
    
    print("Error Report:")
    print(f"Request ID: {error_report.request_id}")
    print(f"Timestamp: {error_report.timestamp}")
    print(f"Error Code: {error_report.error_code}")
    print(f"SDK Version: {error_report.sdk_version}")
    
    # Send to support (implement your preferred method)
    # send_to_support(error_report)
```

## Support

- **Documentation**: https://docs.creatormate.com/sdk
- **API Reference**: https://docs.creatormate.com/api
- **GitHub Issues**: 
  - Python: https://github.com/creatormate/sdk-python/issues
  - JavaScript: https://github.com/creatormate/sdk-js/issues
  - Go: https://github.com/creatormate/sdk-go/issues
- **Community**: https://community.creatormate.com
- **Support Email**: sdk-support@creatormate.com

## License

All CreatorMate SDKs are licensed under the [MIT License](https://opensource.org/licenses/MIT).