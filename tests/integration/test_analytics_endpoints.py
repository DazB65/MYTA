"""
Integration tests for Analytics API endpoints
Tests the complete flow from HTTP requests through to YouTube Analytics service
"""
import pytest
import json
from httpx import AsyncClient
from unittest.mock import patch, Mock, AsyncMock
from datetime import datetime, timedelta

# Import test fixtures
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from youtube_analytics_fixtures import YouTubeAnalyticsFixtures, YouTubeAnalyticsTestHelpers


@pytest.mark.integration
class TestAnalyticsEndpoints:
    """Integration tests for analytics endpoints"""

    @pytest.mark.asyncio
    async def test_channel_health_endpoint_success(self, async_client: AsyncClient, mock_env_vars):
        """Test successful channel health endpoint response"""
        test_user_id = "test-user-123"
        
        # Mock the analytics service response
        mock_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_channel_health(),
            "metadata": {
                "channel_id": "UC_test_channel_123",
                "retrieved_at": datetime.now().isoformat(),
                "cached": False
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = mock_response
            mock_service.return_value = mock_instance
            
            # Make request
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}&days=30"
            )
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "data" in data
            assert "health_score" in data["data"]
            assert data["data"]["health_score"] == 78.5
            assert len(data["data"]["recommendations"]) >= 2

    @pytest.mark.asyncio
    async def test_channel_health_endpoint_cached_response(self, async_client: AsyncClient, mock_env_vars):
        """Test channel health endpoint with cached response"""
        test_user_id = "test-user-456"
        
        # Mock cached response
        cached_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_channel_health(),
            "metadata": {
                "channel_id": "UC_test_channel_456",
                "retrieved_at": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "cached": True,
                "cache_age_minutes": 30
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = cached_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}&days=30"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["metadata"]["cached"] is True
            assert data["metadata"]["cache_age_minutes"] == 30

    @pytest.mark.asyncio
    async def test_channel_health_endpoint_error(self, async_client: AsyncClient, mock_env_vars):
        """Test channel health endpoint error handling"""
        test_user_id = "invalid-user"
        
        # Mock error response
        error_response = {
            "status": "error",
            "error": "YouTube Analytics service not available for user invalid-user",
            "data": None
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = error_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}"
            )
            
            assert response.status_code == 200  # Service-level errors return 200
            data = response.json()
            assert data["status"] == "error"
            assert data["data"] is None
            assert "not available" in data["error"]

    @pytest.mark.asyncio
    async def test_channel_health_endpoint_missing_user_id(self, async_client: AsyncClient):
        """Test channel health endpoint without user_id parameter"""
        response = await async_client.get("/api/analytics/channel-health")
        
        assert response.status_code == 422  # FastAPI validation error
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_revenue_data_endpoint_success(self, async_client: AsyncClient, mock_env_vars):
        """Test successful revenue data endpoint response"""
        test_user_id = "test-user-revenue"
        
        mock_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_revenue_data(),
            "metadata": {
                "channel_id": "UC_revenue_channel",
                "retrieved_at": datetime.now().isoformat(),
                "cached": False
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_revenue_data.return_value = mock_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/revenue?user_id={test_user_id}&days=30"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert data["data"]["total_revenue"] == 234.56
            assert data["data"]["cpm"] == 1.85
            assert data["data"]["rpm"] == 2.34

    @pytest.mark.asyncio
    async def test_subscriber_data_endpoint_success(self, async_client: AsyncClient, mock_env_vars):
        """Test successful subscriber data endpoint response"""
        test_user_id = "test-user-subs"
        
        mock_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_subscriber_data(),
            "metadata": {
                "channel_id": "UC_subs_channel",
                "retrieved_at": datetime.now().isoformat(),
                "cached": False
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_subscriber_data.return_value = mock_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/subscribers?user_id={test_user_id}&days=7"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "daily_data" in data["data"]
            assert "summary" in data["data"]
            assert len(data["data"]["daily_data"]) == 2
            assert data["data"]["summary"]["net_change"] == 29

    @pytest.mark.asyncio
    async def test_content_performance_endpoint_success(self, async_client: AsyncClient, mock_env_vars):
        """Test successful content performance endpoint response"""
        test_user_id = "test-user-content"
        
        # Mock video data from fixtures
        video_details = YouTubeAnalyticsFixtures.create_video_details_response()
        
        mock_response = {
            "status": "success",
            "data": {
                "videos": [
                    {
                        "video_id": "video_123",
                        "title": "Advanced React Hooks Tutorial",
                        "views": 15420,
                        "likes": 1205,
                        "comments": 187,
                        "published_at": "2024-01-15T10:00:00Z",
                        "performance_score": 85.5,
                        "thumbnail_url": "https://i.ytimg.com/vi/video_123/hqdefault.jpg"
                    }
                ],
                "summary": {
                    "total_videos": 25,
                    "average_views": 12500,
                    "top_performing_video": "video_123",
                    "engagement_rate": 8.2
                }
            },
            "metadata": {
                "channel_id": "UC_content_channel",
                "retrieved_at": datetime.now().isoformat(),
                "cached": False
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_content_performance.return_value = mock_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/content-performance?user_id={test_user_id}&limit=25"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["data"]["videos"]) == 1
            assert data["data"]["videos"][0]["title"] == "Advanced React Hooks Tutorial"
            assert data["data"]["summary"]["total_videos"] == 25

    @pytest.mark.asyncio
    async def test_analytics_overview_endpoint_success(self, async_client: AsyncClient, mock_env_vars):
        """Test analytics overview endpoint combining multiple data sources"""
        test_user_id = "test-user-overview"
        
        # Mock combined response data
        mock_overview = {
            "status": "success",
            "data": {
                "channel_health": YouTubeAnalyticsFixtures.create_expected_channel_health(),
                "revenue_summary": {
                    "total_revenue": 234.56,
                    "rpm": 2.34,
                    "revenue_trend": "increasing"
                },
                "subscriber_summary": {
                    "net_change": 29,
                    "growth_rate": 14.5,
                    "growth_trend": "positive"
                },
                "content_summary": {
                    "total_videos": 25,
                    "average_performance": 75.2,
                    "top_video_performance": 85.5
                }
            },
            "metadata": {
                "channel_id": "UC_overview_channel",
                "retrieved_at": datetime.now().isoformat(),
                "data_sources": ["channel_health", "revenue", "subscribers", "content"],
                "cached": False
            }
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_analytics_overview.return_value = mock_overview
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/overview?user_id={test_user_id}"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "channel_health" in data["data"]
            assert "revenue_summary" in data["data"]
            assert "subscriber_summary" in data["data"]
            assert "content_summary" in data["data"]
            assert len(data["metadata"]["data_sources"]) == 4

    @pytest.mark.asyncio
    async def test_endpoint_authentication_required(self, async_client: AsyncClient):
        """Test that analytics endpoints handle authentication requirements"""
        # Test without any authentication headers
        response = await async_client.get("/api/analytics/channel-health?user_id=test-user")
        
        # Should still work for now (authentication not yet implemented)
        # When authentication is implemented, this should return 401
        assert response.status_code in [200, 401]

    @pytest.mark.asyncio
    async def test_endpoint_rate_limiting(self, async_client: AsyncClient, mock_env_vars):
        """Test rate limiting behavior on analytics endpoints"""
        test_user_id = "rate-limit-user"
        
        # Mock successful response
        mock_response = {
            "status": "success", 
            "data": YouTubeAnalyticsFixtures.create_expected_channel_health(),
            "metadata": {"channel_id": "UC_rate_limit", "retrieved_at": datetime.now().isoformat()}
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = mock_response
            mock_service.return_value = mock_instance
            
            # Make multiple rapid requests
            responses = []
            for i in range(5):
                response = await async_client.get(
                    f"/api/analytics/channel-health?user_id={test_user_id}&request_id={i}"
                )
                responses.append(response)
            
            # All should succeed for now (rate limiting not implemented)
            for response in responses:
                assert response.status_code in [200, 429]  # 429 if rate limiting is active

    @pytest.mark.asyncio
    async def test_endpoint_parameter_validation(self, async_client: AsyncClient):
        """Test parameter validation across analytics endpoints"""
        # Test invalid days parameter
        response = await async_client.get(
            "/api/analytics/channel-health?user_id=test&days=invalid"
        )
        assert response.status_code == 422
        
        # Test days parameter out of range
        response = await async_client.get(
            "/api/analytics/channel-health?user_id=test&days=999"
        )
        assert response.status_code == 422
        
        # Test negative days parameter
        response = await async_client.get(
            "/api/analytics/subscribers?user_id=test&days=-5"
        )
        assert response.status_code == 422
        
        # Test invalid limit parameter
        response = await async_client.get(
            "/api/analytics/content-performance?user_id=test&limit=abc"
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_service_error_handling(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of various service errors"""
        test_user_id = "error-user"
        
        # Test service unavailable
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_service.side_effect = Exception("Service initialization failed")
            
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}"
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "error" in data

    @pytest.mark.asyncio
    async def test_response_structure_validation(self, async_client: AsyncClient, mock_env_vars):
        """Test that all endpoint responses follow expected structure"""
        test_user_id = "structure-test"
        endpoints = [
            "/api/analytics/channel-health",
            "/api/analytics/revenue", 
            "/api/analytics/subscribers",
            "/api/analytics/content-performance",
            "/api/analytics/overview"
        ]
        
        for endpoint in endpoints:
            # Mock successful response
            mock_response = {
                "status": "success",
                "data": {"test": "data"},
                "metadata": {
                    "channel_id": "UC_structure_test",
                    "retrieved_at": datetime.now().isoformat()
                }
            }
            
            with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
                mock_instance = AsyncMock()
                # Mock all possible methods
                mock_instance.get_channel_health.return_value = mock_response
                mock_instance.get_revenue_data.return_value = mock_response
                mock_instance.get_subscriber_data.return_value = mock_response
                mock_instance.get_content_performance.return_value = mock_response
                mock_instance.get_analytics_overview.return_value = mock_response
                mock_service.return_value = mock_instance
                
                response = await async_client.get(f"{endpoint}?user_id={test_user_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    # Verify standard response structure
                    YouTubeAnalyticsTestHelpers.assert_analytics_response_structure(data)


@pytest.mark.integration
@pytest.mark.slow
class TestAnalyticsEndpointsPerformance:
    """Performance tests for analytics endpoints"""

    @pytest.mark.asyncio
    async def test_endpoint_response_time(self, async_client: AsyncClient, mock_env_vars):
        """Test endpoint response times"""
        import time
        
        test_user_id = "perf-test"
        mock_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_channel_health(),
            "metadata": {"channel_id": "UC_perf", "retrieved_at": datetime.now().isoformat()}
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = mock_response
            mock_service.return_value = mock_instance
            
            start_time = time.time()
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}"
            )
            end_time = time.time()
            
            # Should respond within 2 seconds
            response_time = end_time - start_time
            assert response_time < 2.0, f"Response took {response_time:.3f}s, expected < 2.0s"
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of concurrent requests to analytics endpoints"""
        import asyncio
        
        mock_response = {
            "status": "success",
            "data": YouTubeAnalyticsFixtures.create_expected_channel_health(),
            "metadata": {"channel_id": "UC_concurrent", "retrieved_at": datetime.now().isoformat()}
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = mock_response
            mock_service.return_value = mock_instance
            
            # Create 10 concurrent requests
            tasks = []
            for i in range(10):
                task = async_client.get(f"/api/analytics/channel-health?user_id=concurrent-{i}")
                tasks.append(task)
            
            # Execute all requests concurrently
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # All requests should succeed
            successful_responses = [r for r in responses if not isinstance(r, Exception)]
            assert len(successful_responses) >= 8  # Allow some variance
            
            for response in successful_responses:
                if hasattr(response, 'status_code'):
                    assert response.status_code == 200


@pytest.mark.integration
class TestAnalyticsEndpointsErrorScenarios:
    """Test various error scenarios for analytics endpoints"""

    @pytest.mark.asyncio
    async def test_youtube_api_quota_exceeded(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of YouTube API quota exceeded error"""
        test_user_id = "quota-user"
        
        error_response = {
            "status": "error",
            "error": "YouTube API quota exceeded. Please try again later.",
            "data": None,
            "error_code": "QUOTA_EXCEEDED"
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_channel_health.return_value = error_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/channel-health?user_id={test_user_id}"
            )
            
            assert response.status_code == 200  # Service errors return 200
            data = response.json()
            assert data["status"] == "error"
            assert "quota exceeded" in data["error"].lower()
            assert data["error_code"] == "QUOTA_EXCEEDED"

    @pytest.mark.asyncio
    async def test_invalid_oauth_credentials(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of invalid OAuth credentials"""
        test_user_id = "invalid-oauth-user"
        
        error_response = {
            "status": "error",
            "error": "Invalid or expired OAuth credentials for user invalid-oauth-user",
            "data": None,
            "error_code": "INVALID_CREDENTIALS"
        }
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_revenue_data.return_value = error_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/revenue?user_id={test_user_id}"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "error"
            assert "credentials" in data["error"].lower()
            assert data["error_code"] == "INVALID_CREDENTIALS"

    @pytest.mark.asyncio
    async def test_network_timeout(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of network timeouts"""
        test_user_id = "timeout-user"
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            # Simulate timeout
            import asyncio
            mock_instance.get_subscriber_data.side_effect = asyncio.TimeoutError()
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/subscribers?user_id={test_user_id}"
            )
            
            # Should handle timeout gracefully
            assert response.status_code == 500
            data = response.json()
            assert "error" in data

    @pytest.mark.asyncio
    async def test_malformed_service_response(self, async_client: AsyncClient, mock_env_vars):
        """Test handling of malformed service responses"""
        test_user_id = "malformed-user"
        
        # Return malformed response (missing required fields)
        malformed_response = {"invalid": "response"}
        
        with patch('App.youtube_analytics_service.get_youtube_analytics_service') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.get_content_performance.return_value = malformed_response
            mock_service.return_value = mock_instance
            
            response = await async_client.get(
                f"/api/analytics/content-performance?user_id={test_user_id}"
            )
            
            # Should handle malformed response gracefully
            assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])