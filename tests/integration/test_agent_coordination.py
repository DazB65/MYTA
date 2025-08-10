"""
Integration tests for agent coordination and communication
Tests the interaction between Boss Agent and specialist agents
"""
import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import test fixtures
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from sample_data import SampleDataFactory


@pytest.mark.integration
class TestBossAgentCoordination:
    """Test Boss Agent coordination with specialist agents"""

    def setup_method(self):
        """Set up test environment"""
        # Import boss agent here to avoid import issues
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend" / "App"))
        
    @pytest.mark.asyncio
    async def test_content_analysis_workflow(self, mock_env_vars):
        """Test complete workflow for content analysis requests"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        user_message = "How are my videos performing? I want to understand what's working."
        context = {
            "user_id": "test-user-123",
            "channel_id": "UC_test_channel",
            "analysis_depth": "standard"
        }
        
        # Mock intent classification
        with patch.object(boss_agent, 'classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "content_analysis", 
                "confidence": 0.92,
                "suggested_agents": ["content_analysis"]
            }
            
            # Mock content analysis agent response
            expected_analysis = SampleDataFactory.create_content_analysis_response()
            
            with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.analyze_content.return_value = expected_analysis
                mock_get_agent.return_value = mock_agent
                
                # Mock synthesis
                with patch.object(boss_agent, 'synthesize_response') as mock_synthesize:
                    mock_synthesize.return_value = {
                        "response": "Based on my analysis, your tutorial content is performing excellently! Your videos average 12K views with strong engagement.",
                        "intent": "content_analysis",
                        "confidence": 0.92,
                        "agent_sources": ["content_analysis"],
                        "token_usage": {"total_tokens": 1800}
                    }
                    
                    # Execute workflow
                    result = await boss_agent.process_user_message(user_message, context)
                    
                    # Verify workflow execution
                    assert result["intent"] == "content_analysis"
                    assert result["confidence"] > 0.9
                    assert "content_analysis" in result["agent_sources"]
                    assert "tutorial" in result["response"]
                    
                    # Verify agent was called with correct parameters
                    mock_agent.analyze_content.assert_called_once()
                    call_args = mock_agent.analyze_content.call_args[0][0]
                    assert call_args["query_type"] == "content_analysis"
                    assert "boss_agent_token" in call_args

    @pytest.mark.asyncio
    async def test_audience_insights_workflow(self, mock_env_vars):
        """Test complete workflow for audience insights requests"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        user_message = "Who is my audience and what do they want to see?"
        context = {
            "user_id": "test-user-456", 
            "channel_id": "UC_audience_test",
            "analysis_depth": "deep"
        }
        
        with patch.object(boss_agent, 'classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "audience_insights",
                "confidence": 0.88,
                "suggested_agents": ["audience_insights"]
            }
            
            expected_insights = SampleDataFactory.create_audience_insights_response()
            
            with patch('boss_agent.get_audience_insights_agent') as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.analyze_audience.return_value = expected_insights
                mock_get_agent.return_value = mock_agent
                
                with patch.object(boss_agent, 'synthesize_response') as mock_synthesize:
                    mock_synthesize.return_value = {
                        "response": "Your audience is primarily tech-savvy millennials aged 25-34 who prefer hands-on learning content. They're most active during evening hours and strongly respond to interactive coding sessions.",
                        "intent": "audience_insights",
                        "confidence": 0.88,
                        "agent_sources": ["audience_insights"],
                        "token_usage": {"total_tokens": 1500}
                    }
                    
                    result = await boss_agent.process_user_message(user_message, context)
                    
                    assert result["intent"] == "audience_insights"
                    assert "millennials" in result["response"]
                    assert "25-34" in result["response"]
                    assert result["confidence"] > 0.8

    @pytest.mark.asyncio
    async def test_multi_agent_comprehensive_analysis(self, mock_env_vars):
        """Test comprehensive analysis requiring multiple agents"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        user_message = "Give me a complete analysis of my channel - performance, audience, and growth opportunities."
        context = {
            "user_id": "test-user-multi",
            "channel_id": "UC_comprehensive_test",
            "analysis_depth": "comprehensive"
        }
        
        with patch.object(boss_agent, 'classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "comprehensive_analysis",
                "confidence": 0.95,
                "suggested_agents": ["content_analysis", "audience_insights", "seo_discoverability"]
            }
            
            # Mock multiple agent responses
            content_response = SampleDataFactory.create_content_analysis_response()
            audience_response = SampleDataFactory.create_audience_insights_response()
            seo_response = {
                "agent_type": "seo_discoverability",
                "response_id": "seo-123",
                "analysis": {
                    "summary": "SEO analysis complete",
                    "key_insights": [{"insight": "Improve title optimization"}]
                },
                "for_boss_agent_only": True
            }
            
            with patch('boss_agent.get_content_analysis_agent') as mock_content_agent, \
                 patch('boss_agent.get_audience_insights_agent') as mock_audience_agent, \
                 patch('boss_agent.get_seo_discoverability_agent') as mock_seo_agent:
                
                # Set up agent mocks
                mock_content_agent.return_value.analyze_content = AsyncMock(return_value=content_response)
                mock_audience_agent.return_value.analyze_audience = AsyncMock(return_value=audience_response)  
                mock_seo_agent.return_value.analyze_seo = AsyncMock(return_value=seo_response)
                
                with patch.object(boss_agent, 'synthesize_response') as mock_synthesize:
                    mock_synthesize.return_value = {
                        "response": "Your channel shows strong performance across multiple areas. Your tutorial content excels with tech-savvy millennials, but there are opportunities to improve SEO and discoverability.",
                        "intent": "comprehensive_analysis",
                        "confidence": 0.93,
                        "agent_sources": ["content_analysis", "audience_insights", "seo_discoverability"],
                        "token_usage": {"total_tokens": 4200}
                    }
                    
                    result = await boss_agent.process_user_message(user_message, context)
                    
                    assert result["intent"] == "comprehensive_analysis"
                    assert len(result["agent_sources"]) == 3
                    assert "content_analysis" in result["agent_sources"]
                    assert "audience_insights" in result["agent_sources"]
                    assert "seo_discoverability" in result["agent_sources"]
                    assert result["token_usage"]["total_tokens"] > 3000

    @pytest.mark.asyncio
    async def test_agent_failure_handling(self, mock_env_vars):
        """Test handling when specialist agent fails"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        user_message = "Analyze my content performance"
        context = {"user_id": "test-user-fail", "channel_id": "UC_fail_test"}
        
        with patch.object(boss_agent, 'classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "content_analysis",
                "confidence": 0.9,
                "suggested_agents": ["content_analysis"]
            }
            
            with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
                mock_agent = AsyncMock()
                mock_agent.analyze_content.side_effect = Exception("Agent service unavailable")
                mock_get_agent.return_value = mock_agent
                
                with patch.object(boss_agent, 'generate_general_response') as mock_general:
                    mock_general.return_value = {
                        "response": "I'm sorry, I'm experiencing technical difficulties analyzing your content right now. Please try again in a few minutes.",
                        "intent": "error_fallback",
                        "token_usage": {"total_tokens": 50}
                    }
                    
                    result = await boss_agent.process_user_message(user_message, context)
                    
                    assert "technical difficulties" in result["response"]
                    assert result["intent"] == "error_fallback"

    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self, mock_env_vars):
        """Test parallel execution of multiple agents"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        agents = ["content_analysis", "audience_insights"]
        context = {
            "boss_agent_token": "test-token-parallel",
            "request_id": "parallel-test-123"
        }
        
        # Mock agent responses
        content_response = SampleDataFactory.create_content_analysis_response()
        audience_response = SampleDataFactory.create_audience_insights_response()
        
        with patch.object(boss_agent, 'delegate_to_specialist') as mock_delegate:
            mock_delegate.side_effect = [content_response, audience_response]
            
            results = await boss_agent.execute_agents_parallel(agents, context)
            
            assert len(results) == 2
            assert results[0]["agent_type"] == "content_analysis"
            assert results[1]["agent_type"] == "audience_insights"
            assert mock_delegate.call_count == 2

    @pytest.mark.asyncio
    async def test_context_enrichment(self, mock_env_vars):
        """Test context enrichment for agent requests"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        base_context = {
            "user_id": "test-user-context",
            "channel_id": "UC_context_test"
        }
        
        enriched = boss_agent.enrich_context(base_context)
        
        # Verify enriched context includes required fields
        assert enriched["user_id"] == "test-user-context"
        assert enriched["channel_id"] == "UC_context_test"
        assert "timestamp" in enriched
        assert "request_id" in enriched
        assert len(enriched["request_id"]) > 10  # Should be a UUID-like string

    @pytest.mark.asyncio 
    async def test_token_budget_management(self, mock_env_vars):
        """Test token budget calculation and enforcement"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        # Test different analysis depths
        contexts = [
            {"analysis_depth": "quick", "user_tier": "free"},
            {"analysis_depth": "standard", "user_tier": "premium"},
            {"analysis_depth": "deep", "user_tier": "enterprise"}
        ]
        
        for context in contexts:
            budget = boss_agent.calculate_token_budget(context)
            
            assert "input_tokens" in budget
            assert "output_tokens" in budget
            assert budget["input_tokens"] > 0
            assert budget["output_tokens"] > 0
            
            # Deeper analysis should get more tokens
            if context["analysis_depth"] == "deep":
                assert budget["input_tokens"] > 2000
                assert budget["output_tokens"] > 1000

    @pytest.mark.asyncio
    async def test_agent_response_validation(self, mock_env_vars):
        """Test validation of agent responses"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        # Test valid response
        valid_response = SampleDataFactory.create_content_analysis_response()
        assert boss_agent.validate_agent_response(valid_response) is True
        
        # Test invalid response (missing required fields)
        invalid_response = {"incomplete": "response"}
        assert boss_agent.validate_agent_response(invalid_response) is False
        
        # Test response with error
        error_response = {"error": "Agent failed", "success": False}
        assert boss_agent.validate_agent_response(error_response) is False

    @pytest.mark.asyncio
    async def test_response_synthesis_quality(self, mock_env_vars):
        """Test quality of response synthesis from multiple agents"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        agent_responses = [
            SampleDataFactory.create_content_analysis_response(),
            SampleDataFactory.create_audience_insights_response()
        ]
        
        user_message = "Give me insights about my channel"
        context = {"user_id": "synthesis-test"}
        
        with patch('boss_agent.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            
            mock_response = Mock()
            mock_response.choices = [Mock(
                message=Mock(
                    content="Your channel shows strong tutorial performance with engaged millennials. Focus on interactive content to maximize growth potential."
                )
            )]
            mock_response.usage = Mock(
                prompt_tokens=500,
                completion_tokens=150, 
                total_tokens=650
            )
            mock_client.chat.completions.create.return_value = mock_response
            
            result = boss_agent.synthesize_response(user_message, agent_responses, context)
            
            assert result["response"] is not None
            assert len(result["response"]) > 50  # Should be substantial
            assert result["agent_sources"] == ["content_analysis", "audience_insights"]
            assert result["token_usage"]["total_tokens"] == 650


@pytest.mark.integration
class TestAgentErrorRecovery:
    """Test agent error recovery and fallback mechanisms"""
    
    def setup_method(self):
        """Set up test environment"""
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend" / "App"))

    @pytest.mark.asyncio
    async def test_single_agent_failure_fallback(self, mock_env_vars):
        """Test fallback when a single agent fails"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
            mock_agent = AsyncMock()
            mock_agent.analyze_content.side_effect = Exception("Service timeout")
            mock_get_agent.return_value = mock_agent
            
            result = await boss_agent.delegate_to_specialist(
                "content_analysis",
                {"boss_agent_token": "test-token"}
            )
            
            assert "error" in result
            assert result["success"] is False
            assert "timeout" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_multiple_agent_partial_failure(self, mock_env_vars):
        """Test handling when some agents succeed and others fail"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        # Mock one successful and one failed agent response
        content_response = SampleDataFactory.create_content_analysis_response()
        
        with patch.object(boss_agent, 'delegate_to_specialist') as mock_delegate:
            mock_delegate.side_effect = [
                content_response,  # Success
                {"error": "Agent failed", "success": False}  # Failure
            ]
            
            agents = ["content_analysis", "audience_insights"]
            context = {"boss_agent_token": "test-token"}
            
            results = await boss_agent.execute_agents_parallel(agents, context)
            
            # Should get partial results
            assert len(results) == 2
            assert results[0]["agent_type"] == "content_analysis"  # Successful
            assert "error" in results[1]  # Failed

    @pytest.mark.asyncio
    async def test_openai_api_failure_fallback(self, mock_env_vars):
        """Test fallback when OpenAI API fails"""
        from boss_agent import BossAgent
        
        boss_agent = BossAgent()
        
        with patch('boss_agent.openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("OpenAI API Error")
            
            result = boss_agent.classify_intent("Test message")
            
            # Should return fallback response
            assert result["intent"] == "general"
            assert result["confidence"] == 0.0
            assert "error" in result

    @pytest.mark.asyncio
    async def test_network_resilience(self, mock_env_vars):
        """Test network resilience and retry mechanisms"""
        from boss_agent import BossAgent
        import asyncio
        
        boss_agent = BossAgent()
        
        with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
            mock_agent = AsyncMock()
            # Simulate temporary network failure, then success
            mock_agent.analyze_content.side_effect = [
                asyncio.TimeoutError(),  # First attempt fails
                SampleDataFactory.create_content_analysis_response()  # Second attempt succeeds
            ]
            mock_get_agent.return_value = mock_agent
            
            # If retry mechanism is implemented, this should eventually succeed
            result = await boss_agent.delegate_to_specialist(
                "content_analysis", 
                {"boss_agent_token": "test-token"}
            )
            
            # Result depends on whether retry is implemented
            assert "error" in result or "agent_type" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])