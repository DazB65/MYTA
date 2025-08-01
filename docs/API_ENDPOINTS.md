# Vidalytics API Endpoints Reference

## Table of Contents

1. [Authentication & Sessions](#authentication--sessions)
2. [Agent System](#agent-system)
3. [YouTube Integration](#youtube-integration)
4. [Content Pillars](#content-pillars)
5. [Analytics](#analytics)
6. [OAuth](#oauth)
7. [Content Cards](#content-cards)
8. [Health & Monitoring](#health--monitoring)

---

## Authentication & Sessions

### Session Management

#### `POST /api/session/login`
Create a new user session (login).

**Tags:** `session`, `auth`

**Request Body:**
```json
{
  "user_id": "string",
  "password": "string",
  "remember_me": false,
  "metadata": {
    "device": "web",
    "app_version": "1.0.0",
    "browser": "Chrome"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "session_id": "abc123def456...",
    "user_id": "creator123",
    "expires_at": "2024-01-01T20:00:00Z",
    "permissions": ["user"]
  }
}
```

**Cookies Set:**
- `Vidalytics_session`: Session ID (HttpOnly, Secure, SameSite=Strict)

---

#### `POST /api/session/logout`
Logout user (revoke current session).

**Tags:** `session`, `auth`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

**Cookies Cleared:**
- `Vidalytics_session`

---

#### `POST /api/session/logout-all`
Logout from all sessions except current.

**Tags:** `session`, `auth`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Logged out from 3 other sessions",
  "data": {
    "revoked_sessions": 3
  }
}
```

---

#### `GET /api/session/current`
Get current session information.

**Tags:** `session`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "Current session retrieved",
  "data": {
    "session_id": "abc123def456...",
    "user_id": "creator123",
    "created_at": "2024-01-01T12:00:00Z",
    "last_accessed": "2024-01-01T12:30:00Z",
    "expires_at": "2024-01-01T20:00:00Z",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0...",
    "permissions": ["user"],
    "metadata": {
      "device": "web",
      "app_version": "1.0.0"
    }
  }
}
```

---

#### `GET /api/session/list`
List all active sessions for current user.

**Tags:** `session`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "User sessions retrieved",
  "data": {
    "sessions": [
      {
        "session_id": "abc123...",
        "created_at": "2024-01-01T12:00:00Z",
        "last_accessed": "2024-01-01T12:30:00Z",
        "expires_at": "2024-01-01T20:00:00Z",
        "ip_address": "192.168.1.100",
        "metadata": {"device": "web"}
      }
    ],
    "total_count": 1
  }
}
```

---

#### `PUT /api/session/update`
Update current session metadata and permissions.

**Tags:** `session`  
**Authentication:** Required

**Request Body:**
```json
{
  "metadata": {
    "device": "mobile",
    "app_version": "1.1.0",
    "push_token": "fcm_token_123"
  },
  "permissions": ["user", "premium"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Session updated successfully"
}
```

---

#### `DELETE /api/session/revoke/{session_id}`
Revoke a specific session (must be owned by current user).

**Tags:** `session`  
**Authentication:** Required

**Path Parameters:**
- `session_id` (string): ID of session to revoke

**Response:**
```json
{
  "success": true,
  "message": "Session revoked successfully"
}
```

---

#### `GET /api/session/stats`
Get session statistics (admin users get detailed stats).

**Tags:** `session`  
**Authentication:** Required

**Response (Regular User):**
```json
{
  "success": true,
  "message": "Session statistics retrieved",
  "data": {
    "user_sessions": 2,
    "current_session_expires_at": "2024-01-01T20:00:00Z"
  }
}
```

**Response (Admin User):**
```json
{
  "success": true,
  "message": "Session statistics retrieved",
  "data": {
    "user_sessions": 2,
    "current_session_expires_at": "2024-01-01T20:00:00Z",
    "daily_stats": {
      "2024-01-01": {
        "created": 10,
        "revoked": 2
      }
    },
    "total_active_sessions": 45,
    "redis_info": {
      "connected": true,
      "memory_usage": "2.5MB"
    }
  }
}
```

---

#### `GET /api/session/health`
Check session system health.

**Tags:** `session`, `health`  
**Rate Limit:** Public health check limit

**Response:**
```json
{
  "success": true,
  "message": "Session system health check completed",
  "data": {
    "status": "healthy",
    "response_time_ms": 12.5,
    "redis_version": "7.0.0",
    "connected_clients": 5,
    "used_memory_human": "2.5MB",
    "total_active_sessions": 45,
    "uptime_seconds": 86400
  }
}
```

---

## Agent System

### Multi-Agent Chat Interface

#### `POST /api/agent/chat`
Interact with the multi-agent system through natural language chat.

**Tags:** `agent`  
**Authentication:** Required  
**Rate Limit:** 100/minute

**Request Body:**
```json
{
  "message": "How can I improve my video thumbnails?",
  "context": {
    "conversation_id": "conv_123",
    "user_intent": "thumbnail_optimization",
    "current_page": "dashboard",
    "video_id": "dQw4w9WgXcQ"
  },
  "preferences": {
    "response_length": "detailed",
    "include_suggestions": true,
    "analysis_depth": "standard"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Response generated successfully",
  "data": {
    "response": "Based on your channel analytics, here are AI-powered suggestions for improving your thumbnails...",
    "agent_type": "boss_agent",
    "delegated_agents": ["content_analysis", "audience_insights"],
    "confidence_score": 0.95,
    "conversation_id": "conv_123",
    "response_metadata": {
      "processing_time_ms": 1250,
      "tokens_used": {
        "input": 150,
        "output": 300
      },
      "cache_hit": false
    },
    "suggestions": [
      {
        "type": "quick_action",
        "title": "Analyze Thumbnail Performance",
        "description": "Get detailed analysis of your current thumbnails",
        "action": "analyze_thumbnails",
        "priority": "high"
      },
      {
        "type": "content_idea",
        "title": "A/B Test Your Thumbnails",
        "description": "Test different thumbnail styles",
        "action": "thumbnail_ab_test",
        "priority": "medium"
      }
    ],
    "related_insights": [
      {
        "type": "performance_metric",
        "title": "CTR Improvement Opportunity",
        "value": "Current CTR: 4.2%, Potential: 6.8%",
        "insight": "Your thumbnails could increase CTR by 2.6% with better contrast"
      }
    ]
  }
}
```

---

#### `POST /api/agent/quick-action`
Execute predefined quick actions for common tasks.

**Tags:** `agent`  
**Authentication:** Required  
**Rate Limit:** 50/minute

**Request Body:**
```json
{
  "action_type": "generate_script",
  "parameters": {
    "topic": "How to optimize YouTube SEO in 2024",
    "duration": "10-15 minutes",
    "style": "educational",
    "target_audience": "beginner",
    "include_sections": ["intro", "main_points", "call_to_action"],
    "tone": "friendly"
  },
  "context": {
    "channel_niche": "education",
    "subscriber_count": 50000,
    "previous_performance": {
      "avg_retention": 0.65,
      "avg_ctr": 0.042
    }
  }
}
```

**Available Action Types:**
- `generate_script`: Create video scripts
- `improve_title`: Optimize video titles
- `analyze_thumbnails`: Thumbnail performance analysis
- `keyword_research`: SEO keyword suggestions
- `generate_ideas`: Content idea generation
- `competitor_analysis`: Analyze competitor strategies
- `audience_insights`: Audience behavior analysis

**Response:**
```json
{
  "success": true,
  "message": "Quick action completed successfully",
  "data": {
    "action_type": "generate_script",
    "result": {
      "script": {
        "title": "YouTube SEO Mastery: Rank Higher in 2024",
        "estimated_duration": "12 minutes",
        "sections": [
          {
            "type": "intro",
            "duration": "30 seconds",
            "content": "Hook: Did you know that 90% of YouTube creators are missing this one SEO trick?...",
            "notes": "Use engaging visuals, keep energy high"
          },
          {
            "type": "main_content",
            "duration": "10 minutes",
            "content": "Let's dive into the 5 essential YouTube SEO strategies...",
            "subsections": [
              {
                "title": "Keyword Research Like a Pro",
                "content": "...",
                "duration": "2 minutes"
              }
            ]
          }
        ]
      },
      "metadata": {
        "word_count": 1500,
        "estimated_engagement_score": 0.78,
        "seo_keywords": ["youtube seo", "video optimization", "ranking factors"],
        "difficulty_level": "beginner-friendly"
      }
    },
    "suggestions": [
      {
        "type": "improvement",
        "suggestion": "Consider adding more specific examples in the keyword research section"
      }
    ],
    "processing_info": {
      "agent_used": "content_analysis",
      "model": "gemini-2.5-pro",
      "processing_time_ms": 3200,
      "confidence_score": 0.92
    }
  }
}
```

---

#### `GET /api/agent/insights/{user_id}`
Get AI-generated insights for a specific user.

**Tags:** `agent`  
**Authentication:** Required

**Path Parameters:**
- `user_id` (string): User identifier

**Query Parameters:**
- `limit` (integer, default: 5): Maximum number of insights to return
- `category` (string, optional): Filter by insight category
- `fresh_only` (boolean, default: false): Only return newly generated insights

**Response:**
```json
{
  "success": true,
  "message": "Insights retrieved successfully",
  "data": {
    "insights": [
      {
        "id": "insight_123",
        "title": "Upload Timing Optimization",
        "category": "performance",
        "priority": "high",
        "summary": "Your videos perform 34% better when uploaded on Tuesday at 2 PM EST",
        "description": "Analysis of your last 30 videos shows a clear pattern...",
        "confidence_score": 0.87,
        "created_at": "2024-01-01T10:00:00Z",
        "actions": [
          {
            "type": "schedule_optimization",
            "title": "Update Upload Schedule",
            "description": "Adjust your content calendar to match optimal timing"
          }
        ],
        "metrics": {
          "improvement_potential": "34%",
          "metric_type": "view_count",
          "baseline": 5000,
          "projected": 6700
        }
      }
    ]
  }
}
```

---

#### `POST /api/agent/generate-insights`
Generate fresh insights for the current user.

**Tags:** `agent`  
**Authentication:** Required  
**Rate Limit:** 10/hour

**Request Body:**
```json
{
  "categories": ["performance", "content", "audience"],
  "analysis_depth": "standard",
  "timeframe": "30d",
  "focus_areas": ["thumbnails", "titles", "timing"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Fresh insights generated successfully",
  "data": {
    "insights_generated": 3,
    "processing_time_ms": 15000,
    "insights": [
      // Same format as GET insights endpoint
    ]
  }
}
```

---

#### `GET /api/agent/status`
Check AI agent system status and availability.

**Tags:** `agent`, `health`  
**Authentication:** Optional

**Response:**
```json
{
  "success": true,
  "message": "Agent system status retrieved",
  "data": {
    "overall_status": "healthy",
    "agents": {
      "boss_agent": {
        "status": "healthy",
        "model": "claude-3.5-sonnet",
        "response_time_ms": 250,
        "availability": 1.0,
        "last_health_check": "2024-01-01T12:00:00Z"
      },
      "content_analysis": {
        "status": "healthy",
        "primary_model": "gemini-2.5-pro",
        "fallback_model": "claude-3.5-sonnet",
        "response_time_ms": 180,
        "availability": 0.98,
        "cache_hit_rate": 0.65
      },
      "audience_insights": {
        "status": "healthy",
        "primary_model": "claude-3.5-sonnet",
        "fallback_model": "claude-3.5-haiku",
        "response_time_ms": 300,
        "availability": 0.99
      }
    },
    "system_metrics": {
      "total_requests_today": 1250,
      "average_response_time_ms": 275,
      "error_rate": 0.02,
      "cache_efficiency": 0.68
    }
  }
}
```

---

## YouTube Integration

### Channel Analytics

#### `GET /api/youtube/analytics/channel/{channel_id}`
Get comprehensive channel analytics data.

**Tags:** `youtube`  
**Authentication:** Required

**Path Parameters:**
- `channel_id` (string): YouTube channel ID

**Query Parameters:**
- `timeframe` (string): Time period (`7d`, `30d`, `90d`, `1y`)
- `metrics` (string): Comma-separated metrics (`views,engagement,retention,revenue`)
- `include_videos` (boolean, default: false): Include video-level data

**Response:**
```json
{
  "success": true,
  "message": "Channel analytics retrieved successfully",
  "data": {
    "channel_info": {
      "channel_id": "UC123456789",
      "title": "Creator Channel",
      "subscriber_count": 50000,
      "total_videos": 150,
      "created_date": "2020-01-01T00:00:00Z"
    },
    "analytics": {
      "timeframe": "30d",
      "summary": {
        "total_views": 125000,
        "total_watch_time_hours": 8500,
        "average_view_duration": "4:30",
        "subscriber_growth": 1250,
        "engagement_rate": 0.065
      },
      "performance_metrics": {
        "views": {
          "current": 125000,
          "previous": 110000,
          "change_percent": 13.6,
          "trend": "increasing"
        },
        "watch_time": {
          "current": 8500,
          "previous": 7200,
          "change_percent": 18.1,
          "trend": "increasing"
        },
        "ctr": {
          "current": 0.042,
          "previous": 0.038,
          "change_percent": 10.5,
          "trend": "improving"
        }
      },
      "top_videos": [
        {
          "video_id": "dQw4w9WgXcQ",
          "title": "Amazing Tutorial",
          "views": 15000,
          "ctr": 0.055,
          "retention": 0.68,
          "published_date": "2024-01-15T10:00:00Z"
        }
      ]
    }
  }
}
```

---

#### `GET /api/youtube/videos/{video_id}`
Get detailed information and analytics for a specific video.

**Tags:** `youtube`  
**Authentication:** Required

**Path Parameters:**
- `video_id` (string): YouTube video ID

**Query Parameters:**
- `include_analytics` (boolean, default: true): Include analytics data
- `include_comments` (boolean, default: false): Include recent comments
- `analytics_period` (string, default: "lifetime"): Analytics time period

**Response:**
```json
{
  "success": true,
  "message": "Video data retrieved successfully",
  "data": {
    "video_info": {
      "video_id": "dQw4w9WgXcQ",
      "title": "Amazing Tutorial: Complete Guide",
      "description": "In this comprehensive tutorial...",
      "published_at": "2024-01-15T10:00:00Z",
      "duration": "PT10M30S",
      "tags": ["tutorial", "education", "howto"],
      "category": "Education",
      "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    },
    "analytics": {
      "views": 15000,
      "likes": 850,
      "dislikes": 12,
      "comments": 95,
      "shares": 45,
      "click_through_rate": 0.055,
      "average_view_duration": "7:15",
      "retention_curve": [
        {"timestamp": 0, "retention": 1.0},
        {"timestamp": 30, "retention": 0.85},
        {"timestamp": 60, "retention": 0.75}
      ],
      "traffic_sources": {
        "youtube_search": 0.35,
        "suggested_videos": 0.28,
        "browse_features": 0.15,
        "external": 0.12,
        "direct": 0.10
      }
    },
    "seo_data": {
      "keywords": ["tutorial", "guide", "education"],
      "search_rankings": [
        {"keyword": "tutorial guide", "position": 15, "search_volume": 10000}
      ],
      "optimization_score": 0.72,
      "suggestions": [
        "Add more specific keywords to description",
        "Improve thumbnail contrast for better CTR"
      ]
    }
  }
}
```

---

#### `GET /api/youtube/search`
Search YouTube videos with advanced filtering.

**Tags:** `youtube`  
**Authentication:** Required

**Query Parameters:**
- `q` (string): Search query
- `channel_id` (string, optional): Limit to specific channel
- `published_after` (string, optional): ISO date filter
- `published_before` (string, optional): ISO date filter
- `duration` (string, optional): `short`, `medium`, `long`
- `order` (string, default: `relevance`): `date`, `rating`, `viewCount`, `title`
- `max_results` (integer, default: 25): Maximum results (max 50)

**Response:**
```json
{
  "success": true,
  "message": "Search completed successfully",
  "data": {
    "total_results": 150000,
    "results_per_page": 25,
    "videos": [
      {
        "video_id": "abc123def456",
        "title": "Advanced Tutorial: Master the Basics",
        "channel_title": "Education Channel",
        "published_at": "2024-01-10T15:30:00Z",
        "duration": "PT15M22S",
        "view_count": 25000,
        "thumbnail_url": "https://img.youtube.com/vi/abc123def456/mqdefault.jpg",
        "description": "Learn advanced techniques in this comprehensive guide..."
      }
    ],
    "search_metadata": {
      "query": "advanced tutorial",
      "search_time_ms": 125,
      "related_keywords": ["tutorial", "guide", "advanced", "education"],
      "trending_topics": ["AI tutorials", "productivity tips"]
    }
  }
}
```

---

### Video Categories and Trends

#### `GET /api/youtube/categories`
Get YouTube video categories for localization.

**Tags:** `youtube`  
**Authentication:** Required

**Query Parameters:**
- `region_code` (string, default: "US"): Country code for localization

**Response:**
```json
{
  "success": true,
  "message": "Categories retrieved successfully",
  "data": {
    "categories": [
      {
        "id": "1",
        "title": "Film & Animation",
        "assignable": true
      },
      {
        "id": "2",
        "title": "Autos & Vehicles",
        "assignable": true
      },
      {
        "id": "10",
        "title": "Music",
        "assignable": true
      }
    ],
    "region_code": "US",
    "last_updated": "2024-01-01T00:00:00Z"
  }
}
```

---

#### `GET /api/youtube/trending`
Get trending videos for analysis and inspiration.

**Tags:** `youtube`  
**Authentication:** Required

**Query Parameters:**
- `region_code` (string, default: "US"): Country code
- `category_id` (string, optional): Filter by category
- `max_results` (integer, default: 25): Maximum results

**Response:**
```json
{
  "success": true,
  "message": "Trending videos retrieved successfully",
  "data": {
    "trending_videos": [
      {
        "video_id": "trending123",
        "title": "Viral Video Title",
        "channel_title": "Popular Channel",
        "published_at": "2024-01-20T12:00:00Z",
        "view_count": 1000000,
        "like_count": 50000,
        "comment_count": 2500,
        "category_id": "22",
        "category_title": "People & Blogs",
        "trending_score": 0.95,
        "growth_rate": 2.5
      }
    ],
    "analysis": {
      "trending_topics": ["AI", "productivity", "tutorials"],
      "trending_formats": ["shorts", "tutorials", "reviews"],
      "average_duration": "PT8M45S",
      "engagement_patterns": {
        "high_ctr_range": [0.08, 0.15],
        "high_retention_range": [0.65, 0.85]
      }
    }
  }
}
```

---

## Content Pillars

### Pillar Management

#### `GET /api/pillars`
List all content pillars for the authenticated user.

**Tags:** `pillars`  
**Authentication:** Required

**Query Parameters:**
- `include_videos` (boolean, default: false): Include assigned videos
- `include_analytics` (boolean, default: false): Include pillar performance metrics
- `sort_by` (string, default: "created_at"): Sort field (`name`, `created_at`, `video_count`)
- `order` (string, default: "desc"): Sort order (`asc`, `desc`)

**Response:**
```json
{
  "success": true,
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
        },
        "videos": [
          {
            "video_id": "dQw4w9WgXcQ",
            "title": "Complete Tutorial Guide",
            "assigned_at": "2024-01-15T14:00:00Z"
          }
        ]
      }
    ],
    "total_count": 5,
    "summary": {
      "total_videos_assigned": 125,
      "unassigned_videos": 8,
      "top_performing_pillar": "Educational Content"
    }
  }
}
```

---

#### `POST /api/pillars`
Create a new content pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Request Body:**
```json
{
  "name": "Tech Reviews",
  "description": "Product reviews, unboxings, and tech comparisons",
  "color": "#10B981",
  "metadata": {
    "target_audience": "tech enthusiasts",
    "content_frequency": "weekly",
    "average_duration": "12-15 minutes"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Pillar created successfully",
  "data": {
    "id": "pillar_456",
    "name": "Tech Reviews",
    "description": "Product reviews, unboxings, and tech comparisons",
    "color": "#10B981",
    "created_at": "2024-01-01T15:00:00Z",
    "video_count": 0,
    "metadata": {
      "target_audience": "tech enthusiasts",
      "content_frequency": "weekly",
      "average_duration": "12-15 minutes"
    }
  }
}
```

---

#### `GET /api/pillars/{pillar_id}`
Get detailed information about a specific pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Path Parameters:**
- `pillar_id` (string): Pillar identifier

**Query Parameters:**
- `include_videos` (boolean, default: true): Include assigned videos
- `include_analytics` (boolean, default: true): Include performance analytics
- `video_limit` (integer, default: 50): Maximum videos to return

**Response:**
```json
{
  "success": true,
  "message": "Pillar retrieved successfully",
  "data": {
    "id": "pillar_123",
    "name": "Educational Content",
    "description": "Tutorials, how-to guides, and educational videos",
    "color": "#3B82F6",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z",
    "video_count": 25,
    "analytics": {
      "timeframe": "30d",
      "total_views": 150000,
      "total_watch_time_hours": 8500,
      "average_ctr": 0.052,
      "average_retention": 0.68,
      "engagement_rate": 0.071,
      "subscriber_growth": 450,
      "revenue": 1250.50,
      "performance_trend": "increasing"
    },
    "videos": [
      {
        "video_id": "dQw4w9WgXcQ",
        "title": "Complete Tutorial Guide",
        "published_at": "2024-01-15T10:00:00Z",
        "assigned_at": "2024-01-15T14:00:00Z",
        "views": 15000,
        "ctr": 0.055,
        "retention": 0.70,
        "performance_score": 0.85
      }
    ],
    "insights": [
      {
        "type": "performance",
        "title": "Strong Retention Performance",
        "description": "This pillar shows 15% higher retention than channel average",
        "confidence": 0.92
      }
    ]
  }
}
```

---

#### `PUT /api/pillars/{pillar_id}`
Update an existing content pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Path Parameters:**
- `pillar_id` (string): Pillar identifier

**Request Body:**
```json
{
  "name": "Advanced Educational Content",
  "description": "In-depth tutorials and advanced educational videos",
  "color": "#6366F1",
  "metadata": {
    "target_audience": "advanced learners",
    "content_frequency": "bi-weekly",
    "average_duration": "20-25 minutes"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Pillar updated successfully",
  "data": {
    "id": "pillar_123",
    "name": "Advanced Educational Content",
    "description": "In-depth tutorials and advanced educational videos",
    "color": "#6366F1",
    "updated_at": "2024-01-20T16:00:00Z",
    "video_count": 25
  }
}
```

---

#### `DELETE /api/pillars/{pillar_id}`
Delete a content pillar (videos will be unassigned).

**Tags:** `pillars`  
**Authentication:** Required

**Path Parameters:**
- `pillar_id` (string): Pillar identifier

**Query Parameters:**
- `force` (boolean, default: false): Force delete even if videos are assigned

**Response:**
```json
{
  "success": true,
  "message": "Pillar deleted successfully",
  "data": {
    "deleted_pillar_id": "pillar_123",
    "unassigned_videos": 25,
    "deleted_at": "2024-01-20T17:00:00Z"
  }
}
```

---

### Video Assignment

#### `POST /api/pillars/{pillar_id}/videos/{video_id}`
Assign a video to a content pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Path Parameters:**
- `pillar_id` (string): Pillar identifier
- `video_id` (string): YouTube video ID

**Request Body (Optional):**
```json
{
  "notes": "Great example of educational content",
  "confidence_score": 0.95,
  "metadata": {
    "assignment_reason": "manual",
    "content_match_score": 0.89
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Video assigned to pillar successfully",
  "data": {
    "pillar_id": "pillar_123",
    "video_id": "dQw4w9WgXcQ",
    "assigned_at": "2024-01-20T18:00:00Z",
    "confidence_score": 0.95,
    "video_info": {
      "title": "Complete Tutorial Guide",
      "published_at": "2024-01-15T10:00:00Z",
      "views": 15000
    }
  }
}
```

---

#### `DELETE /api/pillars/{pillar_id}/videos/{video_id}`
Remove a video from a content pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Path Parameters:**
- `pillar_id` (string): Pillar identifier
- `video_id` (string): YouTube video ID

**Response:**
```json
{
  "success": true,
  "message": "Video removed from pillar successfully",
  "data": {
    "pillar_id": "pillar_123",
    "video_id": "dQw4w9WgXcQ",
    "removed_at": "2024-01-20T19:00:00Z"
  }
}
```

---

#### `GET /api/videos/unassigned`
Get videos that haven't been assigned to any pillar.

**Tags:** `pillars`  
**Authentication:** Required

**Query Parameters:**
- `limit` (integer, default: 25): Maximum videos to return
- `sort_by` (string, default: "published_at"): Sort field
- `order` (string, default: "desc"): Sort order
- `published_after` (string, optional): Filter by publish date

**Response:**
```json
{
  "success": true,
  "message": "Unassigned videos retrieved successfully",
  "data": {
    "videos": [
      {
        "video_id": "unassigned123",
        "title": "Random Video Title",
        "published_at": "2024-01-18T12:00:00Z",
        "views": 8500,
        "ctr": 0.041,
        "retention": 0.62,
        "suggested_pillars": [
          {
            "pillar_id": "pillar_123",
            "pillar_name": "Educational Content",
            "confidence_score": 0.78,
            "reasons": ["similar content topics", "matching audience"]
          }
        ]
      }
    ],
    "total_count": 8,
    "ai_suggestions": {
      "auto_assignment_available": true,
      "high_confidence_matches": 5,
      "review_required": 3
    }
  }
}
```

---

## Analytics

### Dashboard Analytics

#### `GET /api/analytics/dashboard`
Get comprehensive dashboard analytics for the authenticated user.

**Tags:** `analytics`  
**Authentication:** Required

**Query Parameters:**
- `timeframe` (string, default: "30d"): Time period (`7d`, `30d`, `90d`, `1y`)
- `include_predictions` (boolean, default: false): Include AI predictions
- `include_insights` (boolean, default: true): Include AI insights

**Response:**
```json
{
  "success": true,
  "message": "Dashboard analytics retrieved successfully",
  "data": {
    "timeframe": "30d",
    "summary": {
      "total_views": 250000,
      "total_subscribers": 52500,
      "total_videos": 12,
      "total_watch_time_hours": 15000,
      "average_ctr": 0.045,
      "average_retention": 0.65,
      "revenue": 3250.75
    },
    "performance_metrics": {
      "views": {
        "current": 250000,
        "previous": 220000,
        "change_percent": 13.6,
        "trend": "increasing",
        "daily_breakdown": [
          {"date": "2024-01-01", "value": 8500},
          {"date": "2024-01-02", "value": 9200}
        ]
      },
      "subscribers": {
        "current": 52500,
        "previous": 50000,
        "change_percent": 5.0,
        "trend": "steady_growth",
        "growth_rate_per_day": 83.3
      },
      "engagement": {
        "likes": 12500,
        "comments": 850,
        "shares": 320,
        "engagement_rate": 0.054,
        "sentiment_score": 0.78
      }
    },
    "top_content": {
      "best_performing_videos": [
        {
          "video_id": "top123",
          "title": "Viral Tutorial",
          "views": 45000,
          "ctr": 0.082,
          "retention": 0.75,
          "pillar": "Educational Content"
        }
      ],
      "trending_topics": ["AI tutorials", "productivity", "automation"],
      "content_gaps": ["intermediate tutorials", "mobile optimization"]
    },
    "ai_insights": [
      {
        "type": "opportunity",
        "title": "Upload Time Optimization",
        "description": "Videos uploaded on Tuesday perform 25% better",
        "confidence": 0.87,
        "potential_impact": "high"
      }
    ],
    "predictions": {
      "next_month_views": 280000,
      "subscriber_milestone": {
        "target": 60000,
        "estimated_date": "2024-03-15"
      },
      "trending_score": 0.72
    }
  }
}
```

---

#### `GET /api/analytics/performance/{metric_type}`
Get detailed performance analytics for a specific metric.

**Tags:** `analytics`  
**Authentication:** Required

**Path Parameters:**
- `metric_type` (string): Metric type (`views`, `subscribers`, `engagement`, `revenue`, `retention`)

**Query Parameters:**
- `start_date` (string): Start date (ISO format)
- `end_date` (string): End date (ISO format)
- `granularity` (string, default: "daily"): Data granularity (`hourly`, `daily`, `weekly`, `monthly`)
- `breakdown_by` (string, optional): Breakdown dimension (`video`, `pillar`, `traffic_source`)

**Response:**
```json
{
  "success": true,
  "message": "Performance analytics retrieved successfully",
  "data": {
    "metric_type": "views",
    "timeframe": {
      "start_date": "2024-01-01",
      "end_date": "2024-01-31",
      "granularity": "daily"
    },
    "summary": {
      "total": 250000,
      "average_per_period": 8064,
      "peak_value": 15000,
      "peak_date": "2024-01-15",
      "growth_rate": 0.136
    },
    "time_series": [
      {
        "date": "2024-01-01",
        "value": 8500,
        "change_from_previous": 0.05
      },
      {
        "date": "2024-01-02", 
        "value": 9200,
        "change_from_previous": 0.08
      }
    ],
    "breakdown": {
      "by_pillar": [
        {
          "pillar_id": "pillar_123",
          "pillar_name": "Educational Content",
          "value": 125000,
          "percentage": 50.0
        }
      ],
      "by_traffic_source": [
        {
          "source": "youtube_search",
          "value": 87500,
          "percentage": 35.0
        }
      ]
    },
    "insights": [
      {
        "type": "trend",
        "description": "Strong upward trend in the last week",
        "confidence": 0.92
      }
    ]
  }
}
```

---

## OAuth

### YouTube OAuth Flow

#### `GET /api/oauth/youtube/authorize`
Initiate YouTube OAuth authorization flow.

**Tags:** `oauth`  
**Authentication:** Required

**Query Parameters:**
- `redirect_uri` (string, optional): Custom redirect URI
- `state` (string, optional): State parameter for security

**Response:**
```json
{
  "success": true,
  "message": "Authorization URL generated",
  "data": {
    "authorization_url": "https://accounts.google.com/oauth2/auth?client_id=...",
    "state": "secure_random_state",
    "expires_in": 600
  }
}
```

---

#### `POST /api/oauth/youtube/callback`
Handle OAuth callback and exchange code for tokens.

**Tags:** `oauth`  
**Authentication:** Required

**Request Body:**
```json
{
  "code": "oauth_authorization_code",
  "state": "secure_random_state"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OAuth authentication completed successfully",
  "data": {
    "access_token": "ya29.a0AfH6...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "refresh_token": "1//04...",
    "scope": "https://www.googleapis.com/auth/youtube.readonly",
    "channel_info": {
      "channel_id": "UC123456789",
      "title": "Creator Channel",
      "subscriber_count": 50000
    }
  }
}
```

---

#### `GET /api/oauth/youtube/status`
Check YouTube OAuth connection status.

**Tags:** `oauth`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "OAuth status retrieved",
  "data": {
    "connected": true,
    "channel_id": "UC123456789",
    "channel_title": "Creator Channel",
    "scopes": ["youtube.readonly", "youtube.analytics.readonly"],
    "token_expires_at": "2024-01-01T13:00:00Z",
    "last_refresh": "2024-01-01T12:00:00Z",
    "connection_health": "healthy"
  }
}
```

---

#### `DELETE /api/oauth/youtube/disconnect`
Disconnect YouTube OAuth connection.

**Tags:** `oauth`  
**Authentication:** Required

**Response:**
```json
{
  "success": true,
  "message": "YouTube OAuth disconnected successfully",
  "data": {
    "disconnected_at": "2024-01-01T14:00:00Z",
    "revoked_scopes": ["youtube.readonly", "youtube.analytics.readonly"]
  }
}
```

---

## Content Cards

### Content Studio

#### `GET /api/content-cards`
Get content cards for the Content Studio interface.

**Tags:** `content-cards`  
**Authentication:** Required

**Query Parameters:**
- `pillar_id` (string, optional): Filter by pillar
- `status` (string, optional): Filter by status (`draft`, `published`, `scheduled`)
- `limit` (integer, default: 20): Maximum cards to return

**Response:**
```json
{
  "success": true,
  "message": "Content cards retrieved successfully",
  "data": {
    "cards": [
      {
        "id": "card_123",
        "type": "video",
        "title": "Tutorial: Advanced Techniques",
        "status": "published",
        "pillar": {
          "id": "pillar_123",
          "name": "Educational Content",
          "color": "#3B82F6"
        },
        "video_info": {
          "video_id": "dQw4w9WgXcQ",
          "published_at": "2024-01-15T10:00:00Z",
          "duration": "PT10M30S",
          "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
        },
        "performance": {
          "views": 15000,
          "ctr": 0.055,
          "retention": 0.70,
          "engagement_rate": 0.065
        },
        "ai_insights": [
          {
            "type": "optimization",
            "suggestion": "Consider A/B testing a brighter thumbnail",
            "confidence": 0.78
          }
        ]
      }
    ],
    "total_count": 45,
    "filters_applied": ["pillar_id"],
    "summary": {
      "published": 40,
      "draft": 3,
      "scheduled": 2
    }
  }
}
```

---

## Health & Monitoring

### System Health

#### `GET /health`
Basic health check endpoint.

**Tags:** `health`  
**Authentication:** Not required  
**Rate Limit:** 1000/minute

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "service": "Vidalytics Multi-Agent API",
  "version": "2.0.0"
}
```

---

#### `GET /api/health/system`
Comprehensive system health check.

**Tags:** `health`  
**Authentication:** Not required

**Response:**
```json
{
  "overall_health": 0.95,
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "model_integrations": {
    "openai": {
      "status": "healthy",
      "response_time_ms": 250,
      "success_rate": 0.99,
      "quota_remaining": 8500
    },
    "google": {
      "status": "healthy", 
      "response_time_ms": 180,
      "success_rate": 0.98,
      "quota_remaining": 9200
    },
    "overall_health": 0.98
  },
  "youtube_api": {
    "status": "healthy",
    "quota_remaining": 9500,
    "quota_limit": 10000,
    "health_score": 1.0,
    "last_successful_call": "2024-01-01T11:58:00Z"
  },
  "cache_system": {
    "redis_status": "connected",
    "memory_usage": "45%",
    "hit_rate": 0.85,
    "health_score": 0.9,
    "active_connections": 5
  },
  "database": {
    "status": "healthy",
    "connection_pool_usage": 0.15,
    "avg_query_time_ms": 25,
    "health_score": 0.95
  },
  "system_resources": {
    "cpu_usage": 0.25,
    "memory_usage": 0.60,
    "disk_usage": 0.45,
    "health_score": 0.90
  }
}
```

---

This completes the comprehensive API endpoints reference. Each endpoint includes detailed request/response examples, authentication requirements, rate limits, and comprehensive data structures.