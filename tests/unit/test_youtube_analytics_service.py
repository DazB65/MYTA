"""
Unit tests for YouTube Analytics Service
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timedelta
import json

# Import the service we're testing
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend" / "App"))

from youtube_analytics_service import (
    YouTubeAnalyticsService, 
    ChannelHealthMetrics, 
    RevenueMetrics, 
    AnalyticsMetrics,
    get_youtube_analytics_service
)


class TestYouTubeAnalyticsService:
    """Test YouTube Analytics Service functionality"""

    def setup_method(self):
        """Set up test instance"""
        with patch('youtube_analytics_service.get_settings'), \
             patch('youtube_analytics_service.get_oauth_manager'):
            self.service = YouTubeAnalyticsService()
            self.test_user_id = "test-user-123"
            self.test_channel_id = "UC_test_channel_123"

    @pytest.mark.unit
    def test_initialization(self):
        """Test service initialization"""
        assert self.service is not None
        assert hasattr(self.service, 'get_channel_health')
        assert hasattr(self.service, 'get_revenue_data')
        assert hasattr(self.service, 'get_subscriber_data')
        assert hasattr(self.service, 'get_content_performance')
        assert self.service.cache_duration == 3600
        assert len(self.service.common_metrics) > 0
        assert len(self.service.channel_metrics) > 0

    @pytest.mark.unit
    def test_generate_cache_key(self):
        """Test cache key generation"""
        params = {"days": 30, "type": "health"}
        key = self.service._generate_cache_key(self.test_user_id, "channel_health", params)
        
        assert isinstance(key, str)
        assert len(key) == 64  # SHA-256 hex digest length
        
        # Same inputs should generate same key
        key2 = self.service._generate_cache_key(self.test_user_id, "channel_health", params)
        assert key == key2
        
        # Different inputs should generate different keys
        key3 = self.service._generate_cache_key(self.test_user_id, "revenue", params)
        assert key != key3

    @pytest.mark.unit
    @patch('youtube_analytics_service.sqlite3.connect')
    def test_get_cached_data_hit(self, mock_connect):
        """Test successful cache retrieval"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        cached_data = {"status": "success", "data": {"health_score": 85.0}}
        mock_cursor.fetchone.return_value = (json.dumps(cached_data), datetime.now().isoformat())
        
        result = self.service._get_cached_data("test-cache-key")
        
        assert result == cached_data
        mock_cursor.execute.assert_called_once()

    @pytest.mark.unit
    @patch('youtube_analytics_service.sqlite3.connect')
    def test_get_cached_data_miss(self, mock_connect):
        """Test cache miss"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        result = self.service._get_cached_data("test-cache-key")
        
        assert result is None

    @pytest.mark.unit
    @patch('youtube_analytics_service.sqlite3.connect')
    def test_cache_data(self, mock_connect):
        """Test data caching"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        test_data = {"status": "success", "data": {"views": 1000}}
        
        self.service._cache_data("test-cache-key", test_data)
        
        # Verify table creation and data insertion
        assert mock_cursor.execute.call_count == 2  # CREATE TABLE + INSERT
        assert mock_conn.commit.called

    @pytest.mark.unit
    @patch.object(YouTubeAnalyticsService, '_get_service')
    @patch.object(YouTubeAnalyticsService, '_get_channel_id')
    @patch.object(YouTubeAnalyticsService, '_get_cached_data')
    async def test_get_channel_health_cached(self, mock_cached, mock_channel_id, mock_service):
        """Test channel health retrieval from cache"""
        cached_data = {
            "status": "success",
            "data": ChannelHealthMetrics(health_score=85.0).__dict__
        }
        mock_cached.return_value = cached_data
        
        result = await self.service.get_channel_health(self.test_user_id)
        
        assert result == cached_data
        mock_service.assert_not_called()  # Should not call API if cached

    @pytest.mark.unit
    @patch.object(YouTubeAnalyticsService, '_get_service')
    @patch.object(YouTubeAnalyticsService, '_get_channel_id')
    @patch.object(YouTubeAnalyticsService, '_get_cached_data')
    async def test_get_channel_health_no_service(self, mock_cached, mock_channel_id, mock_service):
        """Test channel health when service unavailable"""
        mock_cached.return_value = None
        mock_service.return_value = None
        mock_channel_id.return_value = None
        
        result = await self.service.get_channel_health(self.test_user_id)
        
        assert result["status"] == "error"
        assert "not available" in result["error"]
        assert result["data"] is None

    @pytest.mark.unit
    @patch.object(YouTubeAnalyticsService, '_get_service')
    @patch.object(YouTubeAnalyticsService, '_get_channel_id')
    @patch.object(YouTubeAnalyticsService, '_get_cached_data')
    @patch.object(YouTubeAnalyticsService, '_cache_data')
    async def test_get_channel_health_success(self, mock_cache, mock_cached, mock_channel_id, mock_service):
        """Test successful channel health retrieval"""
        mock_cached.return_value = None  # No cache
        
        # Mock analytics service
        mock_analytics = Mock()
        mock_service.return_value = mock_analytics
        mock_channel_id.return_value = self.test_channel_id
        
        # Mock API response
        api_response = {
            "rows": [
                ["2024-01-01", 1000, 15000, 200, 150, 5, 10],  # Sample analytics row
                ["2024-01-02", 1200, 18000, 250, 180, 8, 12]
            ]
        }
        mock_analytics.reports().query().execute.return_value = api_response
        
        result = await self.service.get_channel_health(self.test_user_id)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "metadata" in result
        assert result["metadata"]["channel_id"] == self.test_channel_id
        mock_cache.assert_called_once()  # Should cache the result

    @pytest.mark.unit
    def test_process_channel_health_data_empty(self):
        """Test processing empty channel health data"""
        empty_response = {"rows": []}
        
        result = self.service._process_channel_health_data(empty_response)
        
        assert isinstance(result, ChannelHealthMetrics)
        assert result.health_score == 0
        assert result.subscriber_growth_rate == 0
        assert result.view_velocity == 0

    @pytest.mark.unit
    def test_process_channel_health_data_valid(self):
        """Test processing valid channel health data"""
        response = {
            "rows": [
                ["2024-01-01", 1000, 15000, 200, 150, 5, 10, 50000, 0.065],
                ["2024-01-02", 1200, 18000, 250, 180, 8, 12, 52000, 0.071]
            ]
        }
        
        result = self.service._process_channel_health_data(response)
        
        assert isinstance(result, ChannelHealthMetrics)
        assert result.health_score > 0
        assert result.subscriber_growth_rate > 0
        assert result.view_velocity > 0
        assert len(result.recommendations) >= 0

    @pytest.mark.unit
    @patch.object(YouTubeAnalyticsService, '_get_service')
    @patch.object(YouTubeAnalyticsService, '_get_channel_id') 
    @patch.object(YouTubeAnalyticsService, '_get_cached_data')
    async def test_get_revenue_data_error(self, mock_cached, mock_channel_id, mock_service):
        """Test revenue data retrieval error handling"""
        mock_cached.return_value = None
        mock_service.return_value = Mock()
        mock_channel_id.return_value = self.test_channel_id
        
        # Mock API error
        from googleapiclient.errors import HttpError
        mock_resp = Mock()
        mock_resp.status = 403
        mock_service.return_value.reports().query().execute.side_effect = HttpError(mock_resp, b'{"error": "forbidden"}')
        
        result = await self.service.get_revenue_data(self.test_user_id)
        
        assert result["status"] == "error"
        assert "403" in result["error"]

    @pytest.mark.unit
    def test_process_revenue_data_empty(self):
        """Test processing empty revenue data"""
        empty_response = {"rows": []}
        
        result = self.service._process_revenue_data(empty_response)
        
        assert isinstance(result, RevenueMetrics)
        assert result.total_revenue == 0
        assert result.cpm == 0

    @pytest.mark.unit
    def test_process_revenue_data_valid(self):
        """Test processing valid revenue data"""
        response = {
            "rows": [
                ["2024-01-01", 25.50, 1.85, 2.10],
                ["2024-01-02", 32.75, 1.92, 2.25]
            ]
        }
        
        result = self.service._process_revenue_data(response)
        
        assert isinstance(result, RevenueMetrics)
        assert result.total_revenue == 58.25  # Sum of revenue
        assert result.cpm > 0  # Average CPM
        assert result.rpm > 0  # Average RPM

    @pytest.mark.unit
    def test_process_subscriber_data_valid(self):
        """Test processing valid subscriber data"""
        response = {
            "rows": [
                ["2024-01-01", 15, 3],
                ["2024-01-02", 22, 5],
                ["2024-01-03", 18, 2]
            ]
        }
        
        result = self.service._process_subscriber_data(response)
        
        assert "daily_data" in result
        assert "summary" in result
        assert len(result["daily_data"]) == 3
        assert result["summary"]["gained"] == 55  # 15 + 22 + 18
        assert result["summary"]["lost"] == 10   # 3 + 5 + 2
        assert result["summary"]["net_change"] == 45  # 55 - 10
        
        # Check daily data structure
        day_data = result["daily_data"][0]
        assert day_data["date"] == "2024-01-01"
        assert day_data["gained"] == 15
        assert day_data["lost"] == 3
        assert day_data["net_change"] == 12

    @pytest.mark.unit
    async def test_singleton_pattern(self):
        """Test that get_youtube_analytics_service returns singleton"""
        with patch('youtube_analytics_service.get_settings'), \
             patch('youtube_analytics_service.get_oauth_manager'):
            service1 = get_youtube_analytics_service()
            service2 = get_youtube_analytics_service()
            
            assert service1 is service2  # Should be the same instance


class TestAnalyticsDataModels:
    """Test analytics data model classes"""

    @pytest.mark.unit
    def test_channel_health_metrics_initialization(self):
        """Test ChannelHealthMetrics initialization"""
        metrics = ChannelHealthMetrics(
            subscriber_growth_rate=2.5,
            view_velocity=1000.0,
            engagement_rate=3.2,
            health_score=75.5,
            recommendations=["Test recommendation"]
        )
        
        assert metrics.subscriber_growth_rate == 2.5
        assert metrics.view_velocity == 1000.0
        assert metrics.engagement_rate == 3.2
        assert metrics.health_score == 75.5
        assert len(metrics.recommendations) == 1

    @pytest.mark.unit
    def test_channel_health_metrics_defaults(self):
        """Test ChannelHealthMetrics with default values"""
        metrics = ChannelHealthMetrics()
        
        assert metrics.subscriber_growth_rate == 0.0
        assert metrics.view_velocity == 0.0
        assert metrics.engagement_rate == 0.0
        assert metrics.health_score == 0.0
        assert metrics.recommendations == []

    @pytest.mark.unit
    def test_revenue_metrics_initialization(self):
        """Test RevenueMetrics initialization"""
        metrics = RevenueMetrics(
            total_revenue=123.45,
            ad_revenue=98.76,
            cpm=1.85,
            rpm=2.34
        )
        
        assert metrics.total_revenue == 123.45
        assert metrics.ad_revenue == 98.76
        assert metrics.cpm == 1.85
        assert metrics.rpm == 2.34

    @pytest.mark.unit
    def test_analytics_metrics_initialization(self):
        """Test AnalyticsMetrics initialization"""
        metrics = AnalyticsMetrics(
            views=50000,
            watch_time_minutes=8750.5,
            click_through_rate=0.067,
            subscribers_gained=100,
            subscribers_lost=25
        )
        
        assert metrics.views == 50000
        assert metrics.watch_time_minutes == 8750.5
        assert metrics.click_through_rate == 0.067
        assert metrics.subscribers_gained == 100
        assert metrics.subscribers_lost == 25


class TestAnalyticsServiceIntegration:
    """Integration tests for analytics service components"""

    def setup_method(self):
        """Set up integration test environment"""
        with patch('youtube_analytics_service.get_settings'), \
             patch('youtube_analytics_service.get_oauth_manager'):
            self.service = YouTubeAnalyticsService()

    @pytest.mark.integration
    @patch('youtube_analytics_service.sqlite3.connect')
    def test_cache_integration(self, mock_connect):
        """Test complete cache workflow"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Test caching data
        test_data = {"test": "data"}
        cache_key = "test-key"
        
        self.service._cache_data(cache_key, test_data)
        
        # Verify cache operation
        assert mock_cursor.execute.call_count >= 1
        assert mock_conn.commit.called
        
        # Test retrieving cached data
        mock_cursor.fetchone.return_value = (json.dumps(test_data), datetime.now().isoformat())
        
        result = self.service._get_cached_data(cache_key)
        assert result == test_data

    @pytest.mark.integration
    @patch.object(YouTubeAnalyticsService, '_get_service')
    @patch.object(YouTubeAnalyticsService, '_get_youtube_service')
    @patch.object(YouTubeAnalyticsService, '_get_channel_id')
    async def test_content_performance_integration(self, mock_channel_id, mock_youtube, mock_analytics):
        """Test content performance endpoint integration"""
        mock_channel_id.return_value = "UC123"
        
        # Mock YouTube Data API
        mock_youtube_service = Mock()
        mock_youtube.return_value = mock_youtube_service
        
        # Mock search response
        mock_youtube_service.search().list().execute.return_value = {
            "items": [{"id": {"videoId": "video123"}}]
        }
        
        # Mock video details response
        mock_youtube_service.videos().list().execute.return_value = {
            "items": [{
                "id": "video123",
                "snippet": {
                    "title": "Test Video",
                    "publishedAt": "2024-01-01T00:00:00Z",
                    "thumbnails": {"medium": {"url": "test.jpg"}}
                },
                "statistics": {
                    "viewCount": "1000",
                    "likeCount": "100",
                    "commentCount": "10"
                }
            }]
        }
        
        mock_analytics.return_value = Mock()  # Analytics service
        
        result = await self.service.get_content_performance("test-user")
        
        assert result["status"] == "success"
        assert "data" in result
        assert len(result["data"]["videos"]) == 1
        assert result["data"]["videos"][0]["title"] == "Test Video"


# Performance tests
class TestAnalyticsServicePerformance:
    """Performance tests for analytics service"""

    def setup_method(self):
        """Set up performance test environment"""
        with patch('youtube_analytics_service.get_settings'), \
             patch('youtube_analytics_service.get_oauth_manager'):
            self.service = YouTubeAnalyticsService()

    @pytest.mark.performance
    @pytest.mark.slow
    def test_cache_key_generation_performance(self):
        """Test cache key generation performance"""
        import time
        
        start_time = time.time()
        
        # Generate 1000 cache keys
        for i in range(1000):
            params = {"days": i % 365, "type": f"test_{i}"}
            self.service._generate_cache_key(f"user_{i}", "endpoint", params)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in under 1 second
        assert duration < 1.0, f"Cache key generation took {duration:.3f}s, expected < 1.0s"

    @pytest.mark.performance
    def test_data_processing_performance(self):
        """Test data processing performance with large datasets"""
        import time
        
        # Generate large dataset (simulate 365 days of data)
        large_response = {
            "rows": [
                [f"2024-{i//30 + 1:02d}-{i%30 + 1:02d}", 1000 + i, 15000 + i*10, 200 + i, 150 + i, 5 + i//30, 10 + i//20]
                for i in range(365)
            ]
        }
        
        start_time = time.time()
        result = self.service._process_channel_health_data(large_response)
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Should process 365 days of data in under 0.1 seconds
        assert duration < 0.1, f"Data processing took {duration:.3f}s, expected < 0.1s"
        assert isinstance(result, ChannelHealthMetrics)
        assert result.health_score > 0


# Error handling tests
@pytest.mark.unit
class TestAnalyticsServiceErrorHandling:
    """Test error handling scenarios"""

    def setup_method(self):
        """Set up error handling test environment"""
        with patch('youtube_analytics_service.get_settings'), \
             patch('youtube_analytics_service.get_oauth_manager'):
            self.service = YouTubeAnalyticsService()

    @patch.object(YouTubeAnalyticsService, '_get_service')
    async def test_analytics_api_timeout(self, mock_service):
        """Test handling of API timeout"""
        mock_analytics = Mock()
        mock_service.return_value = mock_analytics
        
        # Mock timeout exception
        import asyncio
        mock_analytics.reports().query().execute.side_effect = asyncio.TimeoutError()
        
        result = await self.service.get_channel_health("test-user")
        
        assert result["status"] == "error"
        assert "error" in result

    @patch('youtube_analytics_service.sqlite3.connect')
    def test_cache_database_error(self, mock_connect):
        """Test handling of database errors during caching"""
        mock_connect.side_effect = Exception("Database connection failed")
        
        # Should not raise exception, just log error
        result = self.service._get_cached_data("test-key")
        assert result is None
        
        # Caching should also handle errors gracefully
        self.service._cache_data("test-key", {"test": "data"})  # Should not raise

    def test_invalid_response_data(self):
        """Test handling of invalid API response data"""
        # Test with malformed response
        invalid_response = {"invalid": "structure"}
        
        result = self.service._process_channel_health_data(invalid_response)
        assert isinstance(result, ChannelHealthMetrics)  # Should return default metrics
        
        # Test with None response
        result = self.service._process_channel_health_data(None)
        assert isinstance(result, ChannelHealthMetrics)
        assert result.health_score == 0

    def test_malformed_revenue_data(self):
        """Test handling of malformed revenue data"""
        malformed_response = {
            "rows": [
                ["2024-01-01", "invalid", None, "not_a_number"]
            ]
        }
        
        # Should handle gracefully and return default metrics
        result = self.service._process_revenue_data(malformed_response)
        assert isinstance(result, RevenueMetrics)
        assert result.total_revenue >= 0  # Should be 0 or positive


if __name__ == "__main__":
    pytest.main([__file__, "-v"])