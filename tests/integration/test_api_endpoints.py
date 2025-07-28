"""
Integration tests for API endpoints
"""
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock


@pytest.mark.integration
class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check_success(self, test_client: TestClient):
        """Test successful health check"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    def test_health_check_with_database_error(self, test_client: TestClient):
        """Test health check with database connectivity issues"""
        with patch("main.check_database_health") as mock_db_check:
            mock_db_check.return_value = False
            
            response = test_client.get("/health")
            
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "unhealthy"
            assert "database" in data["issues"]


@pytest.mark.integration
class TestAgentChatEndpoint:
    """Test agent chat endpoint"""

    def test_chat_success(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test successful chat interaction"""
        chat_data = {
            "message": "What are my top performing videos?",
            "user_id": sample_user_data["user_id"],
            "context": {
                "channel_id": sample_user_data["channel_id"],
                "time_period": "last_30d"
            }
        }
        
        response = test_client.post("/api/agent/chat", json=chat_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "thinking_process" in data
        assert "agent_used" in data
        assert data["success"] is True

    def test_chat_missing_user_id(self, test_client: TestClient):
        """Test chat request with missing user_id"""
        chat_data = {
            "message": "Test message"
            # Missing user_id
        }
        
        response = test_client.post("/api/agent/chat", json=chat_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_chat_empty_message(self, test_client: TestClient):
        """Test chat request with empty message"""
        chat_data = {
            "message": "",
            "user_id": "test-user-123"
        }
        
        response = test_client.post("/api/agent/chat", json=chat_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_chat_with_authentication(self, test_client: TestClient, sample_user_data):
        """Test chat with authentication headers"""
        headers = {
            "Authorization": "Bearer fake-token-for-testing"
        }
        
        chat_data = {
            "message": "Test authenticated message",
            "user_id": sample_user_data["user_id"]
        }
        
        # Mock authentication middleware
        with patch("auth_middleware.AuthenticationManager.verify_token") as mock_verify:
            mock_verify.return_value = {
                "user_id": sample_user_data["user_id"],
                "permissions": ["user"]
            }
            
            response = test_client.post(
                "/api/agent/chat", 
                json=chat_data,
                headers=headers
            )
            
            assert response.status_code == 200

    def test_chat_rate_limiting(self, test_client: TestClient, sample_user_data):
        """Test rate limiting on chat endpoint"""
        chat_data = {
            "message": "Test rate limiting",
            "user_id": sample_user_data["user_id"]
        }
        
        # Send multiple requests rapidly
        responses = []
        for i in range(10):
            response = test_client.post("/api/agent/chat", json=chat_data)
            responses.append(response)
        
        # Check if any requests were rate limited
        status_codes = [r.status_code for r in responses]
        assert 429 in status_codes or all(code == 200 for code in status_codes)


@pytest.mark.integration
class TestChannelInfoEndpoint:
    """Test channel info endpoint"""

    def test_set_channel_info_success(self, test_client: TestClient, sample_user_data):
        """Test successful channel info update"""
        response = test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "message" in data

    def test_set_channel_info_validation_error(self, test_client: TestClient):
        """Test channel info with validation errors"""
        invalid_data = {
            "user_id": "test-user-123",
            "subscriber_count": -100,  # Invalid negative count
            "total_views": "not-a-number"  # Invalid type
        }
        
        response = test_client.post("/api/agent/set-channel-info", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_get_channel_info(self, test_client: TestClient, sample_user_data):
        """Test retrieving channel information"""
        # First set channel info
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Then retrieve it
        response = test_client.get(f"/api/agent/channel-info/{sample_user_data['user_id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == sample_user_data["user_id"]
        assert data["channel_name"] == sample_user_data["channel_name"]

    def test_get_nonexistent_channel_info(self, test_client: TestClient):
        """Test retrieving non-existent channel information"""
        response = test_client.get("/api/agent/channel-info/nonexistent-user")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data


@pytest.mark.integration
class TestQuickActionEndpoint:
    """Test quick action endpoint"""

    def test_generate_script_action(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test script generation quick action"""
        action_data = {
            "action": "generate_script",
            "user_id": sample_user_data["user_id"],
            "parameters": {
                "topic": "How to start a YouTube channel",
                "duration": "10 minutes",
                "style": "educational"
            }
        }
        
        response = test_client.post("/api/agent/quick-action", json=action_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert data["success"] is True

    def test_improve_hooks_action(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test hook improvement quick action"""
        action_data = {
            "action": "improve_hooks",
            "user_id": sample_user_data["user_id"],
            "parameters": {
                "current_hook": "In this video, I'll show you...",
                "video_topic": "Photography tips"
            }
        }
        
        response = test_client.post("/api/agent/quick-action", json=action_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "improved_hooks" in data["result"]

    def test_invalid_quick_action(self, test_client: TestClient, sample_user_data):
        """Test invalid quick action request"""
        action_data = {
            "action": "nonexistent_action",
            "user_id": sample_user_data["user_id"],
            "parameters": {}
        }
        
        response = test_client.post("/api/agent/quick-action", json=action_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data


@pytest.mark.integration
class TestInsightsEndpoint:
    """Test insights endpoint"""

    def test_get_insights_success(self, test_client: TestClient, sample_user_data, mock_openai, mock_youtube_api):
        """Test successful insights retrieval"""
        # First set up user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        response = test_client.get(f"/api/agent/insights/{sample_user_data['user_id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert len(data["insights"]) > 0

    def test_get_insights_no_data(self, test_client: TestClient):
        """Test insights for user with no data"""
        response = test_client.get("/api/agent/insights/nonexistent-user")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data

    def test_generate_insights_success(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test insights generation"""
        # Set up user data first
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        generation_data = {
            "user_id": sample_user_data["user_id"],
            "analysis_depth": "standard",
            "focus_areas": ["content_performance", "audience_growth"]
        }
        
        response = test_client.post("/api/agent/generate-insights", json=generation_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert data["success"] is True

    def test_generate_insights_deep_analysis(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test deep insights generation"""
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        generation_data = {
            "user_id": sample_user_data["user_id"],
            "analysis_depth": "deep",
            "focus_areas": ["competitive_analysis", "monetization_strategy"]
        }
        
        response = test_client.post("/api/agent/generate-insights", json=generation_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "insights" in data
        assert len(data["insights"]) >= 3  # Deep analysis should provide more insights


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling across endpoints"""

    def test_invalid_json_request(self, test_client: TestClient):
        """Test handling of invalid JSON in request body"""
        response = test_client.post(
            "/api/agent/chat",
            data="invalid json data",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

    def test_missing_content_type(self, test_client: TestClient):
        """Test handling of missing content-type header"""
        response = test_client.post(
            "/api/agent/chat",
            data='{"message": "test"}',
        )
        
        assert response.status_code in [400, 422]

    def test_oversized_request(self, test_client: TestClient):
        """Test handling of oversized request bodies"""
        large_message = "x" * 100000  # Very large message
        chat_data = {
            "message": large_message,
            "user_id": "test-user"
        }
        
        response = test_client.post("/api/agent/chat", json=chat_data)
        
        assert response.status_code in [400, 413, 422]

    def test_cors_headers(self, test_client: TestClient):
        """Test CORS headers are properly set"""
        response = test_client.options("/api/agent/chat")
        
        assert response.status_code in [200, 204]
        assert "Access-Control-Allow-Origin" in response.headers

    def test_security_headers(self, test_client: TestClient):
        """Test security headers are properly set"""
        response = test_client.get("/health")
        
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"


@pytest.mark.integration
class TestAgentStatus:
    """Test agent status endpoint"""

    def test_agent_status_all_healthy(self, test_client: TestClient, mock_openai, mock_google_ai):
        """Test agent status when all agents are healthy"""
        response = test_client.get("/api/agent/status")
        
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert data["overall_status"] == "healthy"

    def test_agent_status_with_failures(self, test_client: TestClient):
        """Test agent status with some agent failures"""
        with patch("openai.OpenAI") as mock_openai:
            mock_openai.side_effect = Exception("API connection failed")
            
            response = test_client.get("/api/agent/status")
            
            assert response.status_code == 200
            data = response.json()
            assert data["overall_status"] in ["degraded", "unhealthy"]