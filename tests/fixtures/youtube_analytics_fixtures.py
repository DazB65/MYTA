"""
YouTube Analytics specific test fixtures and mock data
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any
import random


class YouTubeAnalyticsFixtures:
    """Fixtures for YouTube Analytics testing"""
    
    @staticmethod
    def create_analytics_api_response(days: int = 30) -> Dict[str, Any]:
        """Create realistic YouTube Analytics API response"""
        rows = []
        base_date = datetime.now().date() - timedelta(days=days)
        
        for i in range(days):
            current_date = base_date + timedelta(days=i)
            
            # Simulate realistic daily metrics with some variance
            views = random.randint(800, 2500)
            watch_time = views * random.uniform(3.5, 8.5)  # Minutes
            avg_duration = random.uniform(180, 420)  # 3-7 minutes
            subs_gained = random.randint(5, 50)
            subs_lost = random.randint(1, 15)
            impressions = views * random.randint(15, 35)
            ctr = random.uniform(0.04, 0.12)
            
            row = [
                current_date.isoformat(),
                views,
                watch_time,
                avg_duration,
                subs_gained,
                subs_lost,
                impressions,
                ctr
            ]
            rows.append(row)
        
        return {
            "kind": "youtubeAnalytics#resultTable",
            "columnHeaders": [
                {"name": "day", "columnType": "DIMENSION", "dataType": "STRING"},
                {"name": "views", "columnType": "METRIC", "dataType": "INTEGER"},
                {"name": "estimatedMinutesWatched", "columnType": "METRIC", "dataType": "FLOAT"},
                {"name": "averageViewDuration", "columnType": "METRIC", "dataType": "FLOAT"},
                {"name": "subscribersGained", "columnType": "METRIC", "dataType": "INTEGER"},
                {"name": "subscribersLost", "columnType": "METRIC", "dataType": "INTEGER"},
                {"name": "impressions", "columnType": "METRIC", "dataType": "INTEGER"},
                {"name": "impressionClickThroughRate", "columnType": "METRIC", "dataType": "FLOAT"}
            ],
            "rows": rows
        }
    
    @staticmethod
    def create_revenue_api_response(days: int = 30) -> Dict[str, Any]:
        """Create realistic revenue analytics response"""
        rows = []
        base_date = datetime.now().date() - timedelta(days=days)
        
        for i in range(days):
            current_date = base_date + timedelta(days=i)
            
            # Simulate daily revenue (some days may be $0)
            daily_revenue = random.uniform(0, 25) if random.random() > 0.3 else 0
            cpm = random.uniform(1.2, 3.8) if daily_revenue > 0 else 0
            playback_cpm = cpm * random.uniform(1.1, 1.4) if daily_revenue > 0 else 0
            
            row = [
                current_date.isoformat(),
                round(daily_revenue, 2),
                round(cpm, 2),
                round(playback_cpm, 2)
            ]
            rows.append(row)
        
        return {
            "kind": "youtubeAnalytics#resultTable", 
            "columnHeaders": [
                {"name": "day", "columnType": "DIMENSION", "dataType": "STRING"},
                {"name": "estimatedRevenue", "columnType": "METRIC", "dataType": "FLOAT"},
                {"name": "cpm", "columnType": "METRIC", "dataType": "FLOAT"},
                {"name": "playbackBasedCpm", "columnType": "METRIC", "dataType": "FLOAT"}
            ],
            "rows": rows
        }
    
    @staticmethod
    def create_subscriber_api_response(days: int = 30) -> Dict[str, Any]:
        """Create realistic subscriber analytics response"""
        rows = []
        base_date = datetime.now().date() - timedelta(days=days)
        
        for i in range(days):
            current_date = base_date + timedelta(days=i)
            
            # Simulate daily subscriber changes
            gained = random.randint(2, 75)
            lost = random.randint(1, 25)
            
            row = [
                current_date.isoformat(),
                gained,
                lost
            ]
            rows.append(row)
        
        return {
            "kind": "youtubeAnalytics#resultTable",
            "columnHeaders": [
                {"name": "day", "columnType": "DIMENSION", "dataType": "STRING"},
                {"name": "subscribersGained", "columnType": "METRIC", "dataType": "INTEGER"},
                {"name": "subscribersLost", "columnType": "METRIC", "dataType": "INTEGER"}
            ],
            "rows": rows
        }
    
    @staticmethod
    def create_video_search_response() -> Dict[str, Any]:
        """Create YouTube Data API search response"""
        return {
            "kind": "youtube#searchListResponse",
            "nextPageToken": "CAUQAA",
            "regionCode": "US",
            "pageInfo": {
                "totalResults": 25,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#searchResult",
                    "etag": "test-etag-1",
                    "id": {
                        "kind": "youtube#video",
                        "videoId": "video_123"
                    }
                },
                {
                    "kind": "youtube#searchResult", 
                    "etag": "test-etag-2",
                    "id": {
                        "kind": "youtube#video",
                        "videoId": "video_456"
                    }
                },
                {
                    "kind": "youtube#searchResult",
                    "etag": "test-etag-3", 
                    "id": {
                        "kind": "youtube#video",
                        "videoId": "video_789"
                    }
                }
            ]
        }
    
    @staticmethod
    def create_video_details_response() -> Dict[str, Any]:
        """Create YouTube Data API video details response"""
        return {
            "kind": "youtube#videoListResponse",
            "etag": "test-etag",
            "items": [
                {
                    "kind": "youtube#video",
                    "etag": "video-etag-1",
                    "id": "video_123",
                    "snippet": {
                        "publishedAt": "2024-01-15T10:00:00Z",
                        "channelId": "UC_test_channel_123",
                        "title": "Advanced React Hooks Tutorial",
                        "description": "Learn advanced React hooks patterns including useCallback, useMemo, and custom hooks.",
                        "thumbnails": {
                            "default": {
                                "url": "https://i.ytimg.com/vi/video_123/default.jpg",
                                "width": 120,
                                "height": 90
                            },
                            "medium": {
                                "url": "https://i.ytimg.com/vi/video_123/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            },
                            "high": {
                                "url": "https://i.ytimg.com/vi/video_123/hqdefault.jpg",
                                "width": 480,
                                "height": 360
                            }
                        },
                        "channelTitle": "Tech Tutorial Pro",
                        "tags": [
                            "react",
                            "hooks",
                            "javascript",
                            "tutorial",
                            "web development"
                        ],
                        "categoryId": "28"
                    },
                    "statistics": {
                        "viewCount": "15420",
                        "likeCount": "1205",
                        "commentCount": "187"
                    }
                },
                {
                    "kind": "youtube#video",
                    "etag": "video-etag-2",
                    "id": "video_456",
                    "snippet": {
                        "publishedAt": "2024-01-12T14:30:00Z",
                        "channelId": "UC_test_channel_123",
                        "title": "Building REST APIs with Node.js",
                        "description": "Complete guide to building scalable REST APIs using Node.js and Express.",
                        "thumbnails": {
                            "medium": {
                                "url": "https://i.ytimg.com/vi/video_456/mqdefault.jpg",
                                "width": 320,
                                "height": 180
                            }
                        },
                        "channelTitle": "Tech Tutorial Pro",
                        "tags": [
                            "nodejs",
                            "api",
                            "backend",
                            "tutorial"
                        ],
                        "categoryId": "28"
                    },
                    "statistics": {
                        "viewCount": "8760",
                        "likeCount": "654",
                        "commentCount": "98"
                    }
                }
            ]
        }
    
    @staticmethod
    def create_channel_details_response() -> Dict[str, Any]:
        """Create YouTube Data API channel details response"""
        return {
            "kind": "youtube#channelListResponse",
            "etag": "test-channel-etag",
            "pageInfo": {
                "totalResults": 1,
                "resultsPerPage": 1
            },
            "items": [
                {
                    "kind": "youtube#channel",
                    "etag": "channel-item-etag",
                    "id": "UC_test_channel_123",
                    "snippet": {
                        "title": "Tech Tutorial Pro",
                        "description": "Professional programming tutorials and tech insights for developers of all levels.",
                        "customUrl": "@TechTutorialPro",
                        "publishedAt": "2020-03-15T09:00:00Z",
                        "thumbnails": {
                            "default": {
                                "url": "https://yt3.ggpht.com/channel_default.jpg"
                            },
                            "medium": {
                                "url": "https://yt3.ggpht.com/channel_medium.jpg"
                            },
                            "high": {
                                "url": "https://yt3.ggpht.com/channel_high.jpg"
                            }
                        },
                        "country": "US"
                    },
                    "statistics": {
                        "viewCount": "1250000",
                        "subscriberCount": "12500",
                        "videoCount": "175"
                    }
                }
            ]
        }
    
    @staticmethod
    def create_error_responses() -> Dict[str, Dict[str, Any]]:
        """Create various API error responses"""
        return {
            "quota_exceeded": {
                "error": {
                    "code": 403,
                    "message": "The request cannot be completed because you have exceeded your quota.",
                    "errors": [
                        {
                            "domain": "youtube.quota",
                            "reason": "quotaExceeded",
                            "message": "The request cannot be completed because you have exceeded your quota."
                        }
                    ]
                }
            },
            "invalid_credentials": {
                "error": {
                    "code": 401,
                    "message": "Request is missing required authentication credential.",
                    "errors": [
                        {
                            "domain": "global",
                            "reason": "required",
                            "message": "Login Required",
                            "locationType": "header",
                            "location": "Authorization"
                        }
                    ]
                }
            },
            "forbidden": {
                "error": {
                    "code": 403,
                    "message": "Forbidden",
                    "errors": [
                        {
                            "domain": "youtube.common",
                            "reason": "forbidden",
                            "message": "Forbidden"
                        }
                    ]
                }
            },
            "not_found": {
                "error": {
                    "code": 404,
                    "message": "The requested channel was not found.",
                    "errors": [
                        {
                            "domain": "youtube.channel",
                            "reason": "channelNotFound",
                            "message": "The requested channel was not found."
                        }
                    ]
                }
            },
            "server_error": {
                "error": {
                    "code": 500,
                    "message": "Internal error encountered.",
                    "errors": [
                        {
                            "domain": "global",
                            "reason": "backendError",
                            "message": "Internal error encountered."
                        }
                    ]
                }
            }
        }
    
    @staticmethod
    def create_mock_oauth_credentials():
        """Create mock OAuth credentials for testing"""
        from unittest.mock import Mock
        
        mock_credentials = Mock()
        mock_credentials.valid = True
        mock_credentials.expired = False
        mock_credentials.token = "mock-access-token"
        mock_credentials.refresh_token = "mock-refresh-token"
        mock_credentials.client_id = "mock-client-id"
        mock_credentials.client_secret = "mock-client-secret"
        
        return mock_credentials
    
    @staticmethod
    def create_expected_channel_health() -> Dict[str, Any]:
        """Create expected channel health metrics for testing"""
        return {
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
        }
    
    @staticmethod
    def create_expected_revenue_data() -> Dict[str, Any]:
        """Create expected revenue data for testing"""
        return {
            "total_revenue": 234.56,
            "ad_revenue": 198.43,
            "youtube_premium_revenue": 25.67,
            "super_chat_revenue": 10.46,
            "channel_memberships_revenue": 0.0,
            "merchandise_revenue": 0.0,
            "estimated_partner_revenue": 198.43,
            "rpm": 2.34,
            "cpm": 1.85
        }
    
    @staticmethod
    def create_expected_subscriber_data() -> Dict[str, Any]:
        """Create expected subscriber data for testing"""
        return {
            "daily_data": [
                {
                    "date": "2024-01-01",
                    "gained": 15,
                    "lost": 3,
                    "net_change": 12
                },
                {
                    "date": "2024-01-02",
                    "gained": 22,
                    "lost": 5,
                    "net_change": 17
                }
            ],
            "summary": {
                "net_change": 29,
                "gained": 37,
                "lost": 8,
                "growth_rate": 14.5
            }
        }
    
    @staticmethod
    def create_cache_scenarios() -> Dict[str, Dict[str, Any]]:
        """Create different cache scenarios for testing"""
        return {
            "fresh_cache": {
                "data": {"health_score": 85.0, "cached": True},
                "timestamp": datetime.now(),
                "should_return": True
            },
            "expired_cache": {
                "data": {"health_score": 80.0, "cached": True},
                "timestamp": datetime.now() - timedelta(hours=2),
                "should_return": False
            },
            "no_cache": {
                "data": None,
                "timestamp": None,
                "should_return": False
            }
        }
    
    @staticmethod
    def create_performance_test_data(size: str = "medium") -> Dict[str, Any]:
        """Create data for performance testing"""
        sizes = {
            "small": {"days": 7, "videos": 5},
            "medium": {"days": 30, "videos": 20}, 
            "large": {"days": 365, "videos": 100}
        }
        
        config = sizes.get(size, sizes["medium"])
        
        return {
            "analytics_response": YouTubeAnalyticsFixtures.create_analytics_api_response(config["days"]),
            "revenue_response": YouTubeAnalyticsFixtures.create_revenue_api_response(config["days"]),
            "subscriber_response": YouTubeAnalyticsFixtures.create_subscriber_api_response(config["days"]),
            "expected_processing_time": {
                "small": 0.05,    # 50ms
                "medium": 0.1,    # 100ms  
                "large": 0.5      # 500ms
            }[size]
        }


class YouTubeAnalyticsTestHelpers:
    """Helper methods for YouTube Analytics testing"""
    
    @staticmethod
    def assert_analytics_response_structure(response: Dict[str, Any]):
        """Assert that analytics response has correct structure"""
        assert "status" in response
        assert response["status"] in ["success", "error"]
        
        if response["status"] == "success":
            assert "data" in response
            assert "metadata" in response
            assert "channel_id" in response["metadata"]
            assert "retrieved_at" in response["metadata"]
        else:
            assert "error" in response
            assert response["data"] is None
    
    @staticmethod
    def assert_channel_health_data(data: Dict[str, Any]):
        """Assert channel health data structure"""
        required_fields = [
            "subscriber_growth_rate",
            "view_velocity", 
            "engagement_rate",
            "health_score",
            "recommendations"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Assert data types
        assert isinstance(data["health_score"], (int, float))
        assert 0 <= data["health_score"] <= 100
        assert isinstance(data["recommendations"], list)
    
    @staticmethod
    def assert_revenue_data(data: Dict[str, Any]):
        """Assert revenue data structure"""
        required_fields = [
            "total_revenue",
            "ad_revenue",
            "cpm",
            "rpm"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
            assert isinstance(data[field], (int, float))
            assert data[field] >= 0  # Revenue should be non-negative
    
    @staticmethod
    def assert_subscriber_data(data: Dict[str, Any]):
        """Assert subscriber data structure"""
        assert "daily_data" in data
        assert "summary" in data
        assert isinstance(data["daily_data"], list)
        assert isinstance(data["summary"], dict)
        
        # Check daily data structure
        if data["daily_data"]:
            day = data["daily_data"][0]
            assert "date" in day
            assert "gained" in day
            assert "lost" in day 
            assert "net_change" in day
        
        # Check summary structure
        summary = data["summary"]
        required_summary_fields = ["net_change", "gained", "lost", "growth_rate"]
        for field in required_summary_fields:
            assert field in summary, f"Missing summary field: {field}"
    
    @staticmethod
    def create_test_database_data() -> Dict[str, List[Dict[str, Any]]]:
        """Create test data for database operations"""
        return {
            "oauth_tokens": [
                {
                    "user_id": "test-user-123",
                    "access_token": "mock-access-token",
                    "refresh_token": "mock-refresh-token", 
                    "channel_id": "UC_test_channel_123",
                    "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
                }
            ],
            "analytics_cache": [
                {
                    "cache_key": "test-cache-key",
                    "data": '{"health_score": 85.0}',
                    "created_at": datetime.now().isoformat()
                }
            ]
        }


# Export convenience instances
youtube_fixtures = YouTubeAnalyticsFixtures()
test_helpers = YouTubeAnalyticsTestHelpers()