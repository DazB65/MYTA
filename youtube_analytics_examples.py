# YouTube Analytics API Data Examples for CreatorMate
# This file shows the rich data we can now access with OAuth

from datetime import datetime, timedelta
from typing import Dict, List, Any

# Example 1: Enhanced Video Performance Data
enhanced_video_data = {
    "video_id": "abc123",
    "title": "THE RUM REBELLION - Liquor Feuded Coup",
    "published_at": "2025-04-14T00:00:00Z",
    
    # Basic metrics (what we had before)
    "views": 358,
    "likes": 16,
    "comments": 2,
    
    # NEW: YouTube Analytics API data
    "analytics": {
        # Watch time metrics
        "estimated_minutes_watched": 1247,
        "average_view_duration": 209,  # seconds
        "average_view_percentage": 0.78,  # 78% retention
        
        # Performance metrics
        "impressions": 4521,
        "impression_click_through_rate": 0.079,  # 7.9% CTR
        "card_click_rate": 0.023,
        "end_screen_click_rate": 0.045,
        
        # Revenue data (if monetized)
        "estimated_revenue": 2.47,  # USD
        "estimated_ad_revenue": 2.47,
        "estimated_red_revenue": 0.0,
        "cpm": 1.85,  # Cost per mille
        "playback_based_cpm": 2.12,
        
        # Traffic sources
        "traffic_sources": {
            "youtube_search": 0.32,
            "suggested_videos": 0.28,
            "external": 0.15,
            "browse_features": 0.12,
            "direct_or_unknown": 0.08,
            "playlist": 0.05
        },
        
        # Audience retention curve (every 10 seconds)
        "retention_curve": [
            {"time": 0, "retention": 1.0},
            {"time": 10, "retention": 0.92},
            {"time": 20, "retention": 0.87},
            {"time": 30, "retention": 0.82},
            {"time": 40, "retention": 0.78},
            # ... continues for full video duration
        ],
        
        # Demographics
        "demographics": {
            "age_groups": {
                "13-17": 0.05,
                "18-24": 0.23,
                "25-34": 0.35,
                "35-44": 0.24,
                "45-54": 0.09,
                "55-64": 0.03,
                "65+": 0.01
            },
            "gender": {
                "male": 0.68,
                "female": 0.32
            }
        },
        
        # Geographic data
        "geography": {
            "countries": {
                "US": 0.42,
                "AU": 0.31,
                "CA": 0.12,
                "GB": 0.08,
                "NZ": 0.04,
                "other": 0.03
            }
        },
        
        # Device types
        "devices": {
            "mobile": 0.58,
            "desktop": 0.27,
            "tablet": 0.12,
            "tv": 0.03
        }
    }
}

# Example 2: Channel-Level Analytics
channel_analytics = {
    "channel_id": "UC123abc",
    "time_period": "last_28_days",
    
    # Overall performance
    "metrics": {
        "views": 12547,
        "estimated_minutes_watched": 45231,
        "subscribers_gained": 89,
        "subscribers_lost": 12,
        "estimated_revenue": 67.89,
        "impressions": 156789,
        "impression_ctr": 0.081
    },
    
    # Top performing videos
    "top_videos": [
        {
            "video_id": "xyz789",
            "title": "THE RUM REBELLION - Liquor Feuded Coup",
            "views": 358,
            "watch_time_minutes": 1247,
            "ctr": 0.079,
            "revenue": 2.47
        }
        # ... more videos
    ],
    
    # Audience insights
    "audience_insights": {
        "subscriber_vs_non_subscriber": {
            "subscribers": 0.34,
            "non_subscribers": 0.66
        },
        "new_vs_returning": {
            "new_viewers": 0.72,
            "returning_viewers": 0.28
        },
        "peak_viewing_times": {
            "monday": [19, 20, 21],  # hours
            "tuesday": [19, 20],
            "wednesday": [19, 20, 21],
            "thursday": [19, 20],
            "friday": [19, 20, 21, 22],
            "saturday": [14, 15, 19, 20],
            "sunday": [15, 16, 19, 20]
        }
    },
    
    # Content performance by category
    "content_analysis": {
        "by_topic": {
            "Australian History": {
                "videos": 12,
                "avg_views": 287,
                "avg_retention": 0.76,
                "avg_ctr": 0.074
            },
            "Educational": {
                "videos": 8,
                "avg_views": 156,
                "avg_retention": 0.82,
                "avg_ctr": 0.069
            }
        }
    }
}

# Example 3: Real-time Analytics Query Structure
def get_youtube_analytics(youtube_service, channel_id: str, start_date: str, end_date: str):
    """
    Example of how we'd query YouTube Analytics API
    """
    
    # Video-level analytics query
    video_analytics_request = youtube_service.reports().query(
        ids=f'channel=={channel_id}',
        startDate=start_date,
        endDate=end_date,
        metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,estimatedRevenue,impressions,impressionClickThroughRate',
        dimensions='video',
        maxResults=50,
        sort='-views'
    )
    
    # Audience retention query
    retention_request = youtube_service.reports().query(
        ids=f'channel=={channel_id}',
        startDate=start_date,
        endDate=end_date,
        metrics='audienceWatchRatio,relativeRetentionPerformance',
        dimensions='elapsedVideoTimeRatio',
        filters=f'video=={video_id}'
    )
    
    # Demographics query
    demographics_request = youtube_service.reports().query(
        ids=f'channel=={channel_id}',
        startDate=start_date,
        endDate=end_date,
        metrics='viewerPercentage',
        dimensions='ageGroup,gender',
        maxResults=25
    )
    
    return {
        'video_analytics': video_analytics_request,
        'retention': retention_request,
        'demographics': demographics_request
    }

# Example 4: Enhanced UI Data Structure
enhanced_video_display = {
    "video_id": "abc123",
    "title": "THE RUM REBELLION - Liquor Feuded Coup",
    "thumbnail": "https://...",
    "duration": "4:47",
    "published": "14/4/2025",
    "category": "People & Blogs",
    
    # Enhanced metrics for UI
    "performance": {
        "views": 358,
        "likes": 16,
        "comments": 2,
        "watch_time": "20.8 hours",  # 1247 minutes formatted
        "retention": "78%",
        "ctr": "7.9%",
        "revenue": "$2.47"
    },
    
    # Performance indicators
    "indicators": {
        "performance_vs_channel_avg": 1.24,  # 24% above average
        "retention_grade": "A",  # Based on retention curve
        "ctr_grade": "B+",
        "trending_score": 0.67
    },
    
    # Quick insights
    "insights": [
        "Strong retention at 78% - above channel average",
        "CTR could improve - test new thumbnails",
        "Peak traffic from YouTube search - good SEO"
    ],
    
    # Action items
    "recommendations": [
        {
            "type": "thumbnail",
            "action": "Test alternative thumbnail designs",
            "reason": "CTR below benchmark for this topic"
        },
        {
            "type": "promotion",
            "action": "Create follow-up video",
            "reason": "High retention suggests audience wants more"
        }
    ]
}