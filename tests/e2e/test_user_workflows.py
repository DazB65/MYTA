"""
End-to-End Tests for Critical User Workflows
Tests complete user journeys from frontend to backend with enhanced error handling
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
import threading
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from exceptions import ValidationError, AuthenticationError, ExternalAPIError
from auth_middleware import create_session_token


@pytest.mark.e2e
class TestOnboardingWorkflow:
    """Test complete user onboarding workflow"""

    def test_complete_onboarding_flow(self, test_client: TestClient, mock_youtube_api, mock_openai):
        """Test complete user onboarding from start to finish"""
        user_id = "new-user-123"
        
        # Step 1: Health check - ensure system is ready
        health_response = test_client.get("/health")
        assert health_response.status_code == 200
        
        # Step 2: Set channel information
        channel_data = {
            "user_id": user_id,
            "channel_name": "New Creator Channel",
            "channel_id": "new-channel-id",
            "subscriber_count": 50,
            "total_views": 1000,
            "video_count": 5,
            "niche": "Gaming",
            "goals": ["Growth", "Engagement"],
            "content_type": "Entertainment"
        }
        
        channel_response = test_client.post("/api/agent/set-channel-info", json=channel_data)
        assert channel_response.status_code == 200
        assert channel_response.json()["success"] is True
        
        # Step 3: Verify channel info was stored
        get_channel_response = test_client.get(f"/api/agent/channel-info/{user_id}")
        assert get_channel_response.status_code == 200
        stored_data = get_channel_response.json()
        assert stored_data["channel_name"] == "New Creator Channel"
        assert stored_data["niche"] == "Gaming"
        
        # Step 4: First chat interaction - general welcome
        first_chat_data = {
            "message": "Hello! I'm new to CreatorMate.",
            "user_id": user_id
        }
        
        first_chat_response = test_client.post("/api/agent/chat", json=first_chat_data)
        assert first_chat_response.status_code == 200
        chat_result = first_chat_response.json()
        assert chat_result["success"] is True
        assert "welcome" in chat_result["response"].lower() or "hello" in chat_result["response"].lower()
        
        # Step 5: Generate initial insights
        insights_data = {
            "user_id": user_id,
            "analysis_depth": "quick",
            "focus_areas": ["content_performance", "growth_opportunities"]
        }
        
        insights_response = test_client.post("/api/agent/generate-insights", json=insights_data)
        assert insights_response.status_code == 200
        insights_result = insights_response.json()
        assert insights_result["success"] is True
        assert len(insights_result["insights"]) >= 2
        
        # Step 6: First quick action - generate script
        quick_action_data = {
            "action": "generate_script",
            "user_id": user_id,
            "parameters": {
                "topic": "Gaming tips for beginners",
                "duration": "5 minutes",
                "style": "casual"
            }
        }
        
        quick_action_response = test_client.post("/api/agent/quick-action", json=quick_action_data)
        assert quick_action_response.status_code == 200
        action_result = quick_action_response.json()
        assert action_result["success"] is True
        assert "script" in action_result["result"]


@pytest.mark.e2e
class TestContentAnalysisWorkflow:
    """Test complete content analysis workflow"""

    def test_comprehensive_content_analysis(self, test_client: TestClient, sample_user_data, mock_openai, mock_google_ai, mock_youtube_api):
        """Test comprehensive content analysis workflow"""
        user_id = sample_user_data["user_id"]
        
        # Setup: Ensure user data exists
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Step 1: Request content analysis
        content_analysis_chat = {
            "message": "Analyze my video performance for the last month",
            "user_id": user_id,
            "context": {
                "channel_id": sample_user_data["channel_id"],
                "time_period": "last_30d"
            }
        }
        
        analysis_response = test_client.post("/api/agent/chat", json=content_analysis_chat)
        assert analysis_response.status_code == 200
        analysis_result = analysis_response.json()
        
        assert analysis_result["success"] is True
        assert "content_analysis" in analysis_result.get("agent_used", "")
        assert "performance" in analysis_result["response"].lower()
        
        # Step 2: Ask for specific metrics
        metrics_chat = {
            "message": "What are my top performing videos and why?",
            "user_id": user_id,
            "context": {
                "channel_id": sample_user_data["channel_id"]
            }
        }
        
        metrics_response = test_client.post("/api/agent/chat", json=metrics_chat)
        assert metrics_response.status_code == 200
        metrics_result = metrics_response.json()
        
        assert metrics_result["success"] is True
        assert "top" in metrics_result["response"].lower()
        
        # Step 3: Request improvement suggestions
        improvement_chat = {
            "message": "How can I improve my video hooks and retention?",
            "user_id": user_id
        }
        
        improvement_response = test_client.post("/api/agent/chat", json=improvement_chat)
        assert improvement_response.status_code == 200
        improvement_result = improvement_response.json()
        
        assert improvement_result["success"] is True
        assert any(word in improvement_result["response"].lower() 
                  for word in ["hook", "retention", "engagement", "improve"])
        
        # Step 4: Use quick action to improve hooks
        hook_improvement_data = {
            "action": "improve_hooks",
            "user_id": user_id,
            "parameters": {
                "current_hook": "Welcome back to my channel, today we're going to...",
                "video_topic": "Gaming tutorial"
            }
        }
        
        hook_response = test_client.post("/api/agent/quick-action", json=hook_improvement_data)
        assert hook_response.status_code == 200
        hook_result = hook_response.json()
        
        assert hook_result["success"] is True
        assert "improved_hooks" in hook_result["result"]


@pytest.mark.e2e
class TestMultiAgentWorkflow:
    """Test workflows requiring multiple agents"""

    def test_comprehensive_channel_analysis(self, test_client: TestClient, sample_user_data, mock_openai, mock_google_ai, mock_youtube_api):
        """Test comprehensive analysis requiring multiple agents"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Request comprehensive analysis
        comprehensive_chat = {
            "message": "Give me a complete analysis of my channel including content performance, audience insights, SEO opportunities, and monetization strategies",
            "user_id": user_id,
            "context": {
                "channel_id": sample_user_data["channel_id"],
                "analysis_depth": "deep"
            }
        }
        
        response = test_client.post("/api/agent/chat", json=comprehensive_chat)
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        
        # Should involve multiple agents
        assert "agent_sources" in result
        agent_sources = result.get("agent_sources", [])
        assert len(agent_sources) >= 3  # At least 3 different agents
        
        # Should contain comprehensive analysis
        response_text = result["response"].lower()
        assert any(word in response_text for word in ["content", "performance", "video"])
        assert any(word in response_text for word in ["audience", "demographic", "viewer"])
        assert any(word in response_text for word in ["seo", "search", "discovery"])
        assert any(word in response_text for word in ["monetization", "revenue", "earning"])

    def test_competitive_analysis_workflow(self, test_client: TestClient, sample_user_data, mock_openai, mock_google_ai):
        """Test competitive analysis workflow"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Request competitive analysis
        competitive_chat = {
            "message": "How do I compare to other creators in my niche? What can I learn from top performers?",
            "user_id": user_id,
            "context": {
                "channel_id": sample_user_data["channel_id"],
                "niche": sample_user_data["niche"],
                "competitors": ["competitor1", "competitor2"]
            }
        }
        
        response = test_client.post("/api/agent/chat", json=competitive_chat)
        assert response.status_code == 200
        result = response.json()
        
        assert result["success"] is True
        response_text = result["response"].lower()
        assert any(word in response_text for word in ["competitor", "compare", "benchmark"])
        assert any(word in response_text for word in ["learn", "improve", "opportunity"])


@pytest.mark.e2e
class TestErrorRecoveryWorkflow:
    """Test error recovery in complete workflows"""

    def test_api_failure_recovery(self, test_client: TestClient, sample_user_data):
        """Test system behavior when external APIs fail"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Simulate OpenAI API failure
        with patch("openai.OpenAI") as mock_openai:
            mock_openai.side_effect = Exception("OpenAI API unavailable")
            
            chat_data = {
                "message": "Analyze my content performance",
                "user_id": user_id
            }
            
            response = test_client.post("/api/agent/chat", json=chat_data)
            
            # Should handle gracefully
            assert response.status_code in [200, 503]
            
            if response.status_code == 200:
                result = response.json()
                # Should indicate service issues or provide fallback
                assert "error" in result or "unavailable" in result.get("response", "").lower()

    def test_partial_agent_failure_recovery(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test recovery when some agents fail but others succeed"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Mock partial failure - content analysis fails, but boss agent succeeds
        with patch("boss_agent.get_content_analysis_agent") as mock_content_agent:
            mock_content_agent.side_effect = Exception("Content analysis agent failed")
            
            chat_data = {
                "message": "Analyze my video performance",
                "user_id": user_id
            }
            
            response = test_client.post("/api/agent/chat", json=chat_data)
            assert response.status_code == 200
            result = response.json()
            
            # Should still provide some response, even if degraded
            assert result["success"] is True
            assert len(result["response"]) > 0


@pytest.mark.e2e
class TestDataPersistenceWorkflow:
    """Test data persistence across sessions"""

    def test_conversation_history_persistence(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test conversation history is maintained across requests"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # First conversation
        first_chat = {
            "message": "What's my subscriber count?",
            "user_id": user_id
        }
        
        first_response = test_client.post("/api/agent/chat", json=first_chat)
        assert first_response.status_code == 200
        
        # Second conversation referencing first
        second_chat = {
            "message": "How can I increase that number?",
            "user_id": user_id
        }
        
        second_response = test_client.post("/api/agent/chat", json=second_chat)
        assert second_response.status_code == 200
        second_result = second_response.json()
        
        assert second_result["success"] is True
        # Should understand context from previous conversation
        response_text = second_result["response"].lower()
        assert any(word in response_text for word in ["subscriber", "grow", "increase"])

    def test_insights_caching(self, test_client: TestClient, sample_user_data, mock_openai):
        """Test insights are cached and retrieved properly"""
        user_id = sample_user_data["user_id"]
        
        # Setup user data
        test_client.post("/api/agent/set-channel-info", json=sample_user_data)
        
        # Generate insights
        insights_data = {
            "user_id": user_id,
            "analysis_depth": "standard",
            "focus_areas": ["content_performance"]
        }
        
        first_insights_response = test_client.post("/api/agent/generate-insights", json=insights_data)
        assert first_insights_response.status_code == 200
        first_result = first_insights_response.json()
        
        # Retrieve cached insights
        cached_insights_response = test_client.get(f"/api/agent/insights/{user_id}")
        assert cached_insights_response.status_code == 200
        cached_result = cached_insights_response.json()
        
        # Should have insights available
        assert len(cached_result["insights"]) > 0


@pytest.mark.e2e
@pytest.mark.slow
class TestLoadWorkflow:
    """Test system behavior under load"""

    def test_concurrent_users(self, test_client: TestClient, mock_openai):
        """Test system handles multiple concurrent users"""
        import threading
        import time
        
        results = []
        
        def user_workflow(user_id):
            """Simulate a user workflow"""
            try:
                # Set channel info
                channel_data = {
                    "user_id": f"user-{user_id}",
                    "channel_name": f"Channel {user_id}",
                    "channel_id": f"channel-{user_id}",
                    "subscriber_count": 100 * user_id,
                    "niche": "Technology"
                }
                
                channel_response = test_client.post("/api/agent/set-channel-info", json=channel_data)
                
                # Chat interaction
                chat_data = {
                    "message": "How are my videos performing?",
                    "user_id": f"user-{user_id}"
                }
                
                chat_response = test_client.post("/api/agent/chat", json=chat_data)
                
                results.append({
                    "user_id": user_id,
                    "channel_success": channel_response.status_code == 200,
                    "chat_success": chat_response.status_code == 200
                })
                
            except Exception as e:
                results.append({
                    "user_id": user_id,
                    "error": str(e),
                    "channel_success": False,
                    "chat_success": False
                })
        
        # Create multiple threads for concurrent users
        threads = []
        for i in range(5):  # 5 concurrent users
            thread = threading.Thread(target=user_workflow, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        assert len(results) == 5
        successful_users = sum(1 for r in results if r.get("channel_success") and r.get("chat_success"))
        
        # At least 80% should succeed under load
        assert successful_users >= 4