"""
Unit tests for Boss Agent functionality
"""
import pytest
import json
from unittest.mock import Mock, patch, AsyncMock

from boss_agent import BossAgent, get_boss_agent


class TestBossAgent:
    """Test BossAgent class functionality"""

    def setup_method(self):
        """Set up test instance"""
        self.boss_agent = BossAgent()

    def test_initialization(self):
        """Test BossAgent initialization"""
        assert self.boss_agent is not None
        assert hasattr(self.boss_agent, 'process_user_message')
        assert hasattr(self.boss_agent, 'delegate_to_specialist')
        assert hasattr(self.boss_agent, 'synthesize_response')

    @patch('boss_agent.openai.OpenAI')
    def test_intent_classification(self, mock_openai):
        """Test user intent classification"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"intent": "content_analysis", "confidence": 0.95}'))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = self.boss_agent.classify_intent("How are my videos performing?")
        
        assert result["intent"] == "content_analysis"
        assert result["confidence"] == 0.95

    @patch('boss_agent.openai.OpenAI')
    def test_intent_classification_invalid_json(self, mock_openai):
        """Test intent classification with invalid JSON response"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='invalid json response'))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = self.boss_agent.classify_intent("Test message")
        
        # Should fallback to general intent
        assert result["intent"] == "general"
        assert result["confidence"] < 0.5

    @patch('boss_agent.openai.OpenAI')
    def test_general_response(self, mock_openai):
        """Test general response generation"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="This is a general response"))]
        mock_response.usage = Mock(prompt_tokens=50, completion_tokens=25, total_tokens=75)
        mock_client.chat.completions.create.return_value = mock_response
        
        result = self.boss_agent.generate_general_response(
            "Hello", 
            {"user_id": "test-user"}
        )
        
        assert result["response"] == "This is a general response"
        assert result["token_usage"]["total_tokens"] == 75

    @pytest.mark.asyncio
    async def test_delegate_to_content_analysis(self):
        """Test delegation to content analysis agent"""
        with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
            mock_agent = AsyncMock()
            mock_response = {
                "agent_type": "content_analysis",
                "analysis": {
                    "summary": "Test analysis",
                    "key_insights": [{"insight": "Test insight"}]
                },
                "for_boss_agent_only": True
            }
            mock_agent.analyze_content.return_value = mock_response
            mock_get_agent.return_value = mock_agent
            
            result = await self.boss_agent.delegate_to_specialist(
                "content_analysis", 
                {
                    "query_type": "content_analysis",
                    "context": {"channel_id": "test-channel"},
                    "boss_agent_token": "test-token"
                }
            )
            
            assert result["agent_type"] == "content_analysis"
            assert "summary" in result["analysis"]

    @pytest.mark.asyncio
    async def test_delegate_to_audience_insights(self):
        """Test delegation to audience insights agent"""
        with patch('boss_agent.get_audience_insights_agent') as mock_get_agent:
            mock_agent = AsyncMock()
            mock_response = {
                "agent_type": "audience_insights",
                "analysis": {
                    "summary": "Test audience analysis",
                    "demographics": {"age_range": "25-34"}
                },
                "for_boss_agent_only": True
            }
            mock_agent.analyze_audience.return_value = mock_response
            mock_get_agent.return_value = mock_agent
            
            result = await self.boss_agent.delegate_to_specialist(
                "audience_insights",
                {
                    "query_type": "audience_insights", 
                    "context": {"channel_id": "test-channel"},
                    "boss_agent_token": "test-token"
                }
            )
            
            assert result["agent_type"] == "audience_insights"
            assert "demographics" in result["analysis"]

    def test_invalid_specialist_delegation(self):
        """Test delegation to invalid specialist"""
        with pytest.raises(ValueError, match="Unknown specialist agent"):
            self.boss_agent.delegate_to_specialist(
                "nonexistent_agent",
                {"boss_agent_token": "test-token"}
            )

    @patch('boss_agent.openai.OpenAI')
    def test_synthesize_response_single_agent(self, mock_openai):
        """Test response synthesis from single agent"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Synthesized response"))]
        mock_response.usage = Mock(prompt_tokens=100, completion_tokens=50, total_tokens=150)
        mock_client.chat.completions.create.return_value = mock_response
        
        agent_responses = [{
            "agent_type": "content_analysis",
            "analysis": {
                "summary": "Your videos are performing well",
                "key_insights": [{"insight": "High retention rate"}]
            }
        }]
        
        result = self.boss_agent.synthesize_response(
            "How are my videos doing?",
            agent_responses,
            {"user_id": "test-user"}
        )
        
        assert result["response"] == "Synthesized response"
        assert result["agent_sources"] == ["content_analysis"]

    @patch('boss_agent.openai.OpenAI')
    def test_synthesize_response_multiple_agents(self, mock_openai):
        """Test response synthesis from multiple agents"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Multi-agent synthesized response"))]
        mock_response.usage = Mock(prompt_tokens=200, completion_tokens=100, total_tokens=300)
        mock_client.chat.completions.create.return_value = mock_response
        
        agent_responses = [
            {
                "agent_type": "content_analysis",
                "analysis": {"summary": "Content analysis"}
            },
            {
                "agent_type": "audience_insights", 
                "analysis": {"summary": "Audience analysis"}
            }
        ]
        
        result = self.boss_agent.synthesize_response(
            "Give me a full analysis",
            agent_responses,
            {"user_id": "test-user"}
        )
        
        assert result["response"] == "Multi-agent synthesized response"
        assert len(result["agent_sources"]) == 2
        assert "content_analysis" in result["agent_sources"]
        assert "audience_insights" in result["agent_sources"]

    @pytest.mark.asyncio
    async def test_process_user_message_content_analysis(self):
        """Test processing user message for content analysis"""
        with patch.object(self.boss_agent, 'classify_intent') as mock_classify, \
             patch.object(self.boss_agent, 'delegate_to_specialist') as mock_delegate, \
             patch.object(self.boss_agent, 'synthesize_response') as mock_synthesize:
            
            mock_classify.return_value = {"intent": "content_analysis", "confidence": 0.9}
            mock_delegate.return_value = {
                "agent_type": "content_analysis",
                "analysis": {"summary": "Test analysis"}
            }
            mock_synthesize.return_value = {
                "response": "Final response",
                "agent_sources": ["content_analysis"]
            }
            
            result = await self.boss_agent.process_user_message(
                "How are my videos performing?",
                {"user_id": "test-user", "channel_id": "test-channel"}
            )
            
            assert result["response"] == "Final response"
            assert result["intent"] == "content_analysis"
            assert "content_analysis" in result["agent_sources"]

    @pytest.mark.asyncio
    async def test_process_user_message_general(self):
        """Test processing general user message"""
        with patch.object(self.boss_agent, 'classify_intent') as mock_classify, \
             patch.object(self.boss_agent, 'generate_general_response') as mock_general:
            
            mock_classify.return_value = {"intent": "general", "confidence": 0.3}
            mock_general.return_value = {
                "response": "General response",
                "token_usage": {"total_tokens": 50}
            }
            
            result = await self.boss_agent.process_user_message(
                "Hello there!",
                {"user_id": "test-user"}
            )
            
            assert result["response"] == "General response"
            assert result["intent"] == "general"
            assert result["token_usage"]["total_tokens"] == 50

    @pytest.mark.asyncio
    async def test_process_user_message_multi_agent(self):
        """Test processing message requiring multiple agents"""
        with patch.object(self.boss_agent, 'classify_intent') as mock_classify, \
             patch.object(self.boss_agent, 'delegate_to_specialist') as mock_delegate, \
             patch.object(self.boss_agent, 'synthesize_response') as mock_synthesize:
            
            mock_classify.return_value = {"intent": "comprehensive_analysis", "confidence": 0.95}
            
            # Mock multiple agent responses
            mock_delegate.side_effect = [
                {"agent_type": "content_analysis", "analysis": {"summary": "Content"}},
                {"agent_type": "audience_insights", "analysis": {"summary": "Audience"}},
                {"agent_type": "seo_discoverability", "analysis": {"summary": "SEO"}}
            ]
            
            mock_synthesize.return_value = {
                "response": "Comprehensive analysis response",
                "agent_sources": ["content_analysis", "audience_insights", "seo_discoverability"]
            }
            
            result = await self.boss_agent.process_user_message(
                "Give me a complete analysis of my channel",
                {"user_id": "test-user", "channel_id": "test-channel"}
            )
            
            assert result["response"] == "Comprehensive analysis response"
            assert len(result["agent_sources"]) == 3

    def test_get_boss_agent_singleton(self):
        """Test boss agent singleton pattern"""
        agent1 = get_boss_agent()
        agent2 = get_boss_agent()
        
        assert agent1 is agent2

    @patch('boss_agent.openai.OpenAI')
    def test_error_handling_openai_failure(self, mock_openai):
        """Test error handling when OpenAI API fails"""
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        result = self.boss_agent.classify_intent("Test message")
        
        # Should return fallback response
        assert result["intent"] == "general"
        assert result["confidence"] == 0.0
        assert "error" in result

    @pytest.mark.asyncio
    async def test_error_handling_agent_failure(self):
        """Test error handling when specialist agent fails"""
        with patch('boss_agent.get_content_analysis_agent') as mock_get_agent:
            mock_agent = AsyncMock()
            mock_agent.analyze_content.side_effect = Exception("Agent failed")
            mock_get_agent.return_value = mock_agent
            
            result = await self.boss_agent.delegate_to_specialist(
                "content_analysis",
                {
                    "query_type": "content_analysis",
                    "boss_agent_token": "test-token"
                }
            )
            
            assert "error" in result
            assert result["success"] is False

    def test_token_budget_management(self):
        """Test token budget calculation and management"""
        context = {
            "analysis_depth": "deep",
            "user_tier": "premium"
        }
        
        budget = self.boss_agent.calculate_token_budget(context)
        
        assert "input_tokens" in budget
        assert "output_tokens" in budget
        assert budget["input_tokens"] > 0
        assert budget["output_tokens"] > 0

    def test_context_enrichment(self):
        """Test context enrichment for agent requests"""
        user_context = {
            "user_id": "test-user",
            "channel_id": "test-channel"
        }
        
        enriched = self.boss_agent.enrich_context(user_context)
        
        assert "timestamp" in enriched
        assert "request_id" in enriched
        assert enriched["user_id"] == "test-user"
        assert enriched["channel_id"] == "test-channel"

    @pytest.mark.asyncio
    async def test_parallel_agent_execution(self):
        """Test parallel execution of multiple agents"""
        with patch.object(self.boss_agent, 'delegate_to_specialist') as mock_delegate:
            mock_delegate.side_effect = [
                {"agent_type": "content_analysis", "analysis": {"summary": "Content"}},
                {"agent_type": "audience_insights", "analysis": {"summary": "Audience"}}
            ]
            
            agents = ["content_analysis", "audience_insights"]
            context = {"boss_agent_token": "test-token"}
            
            results = await self.boss_agent.execute_agents_parallel(agents, context)
            
            assert len(results) == 2
            assert results[0]["agent_type"] == "content_analysis"
            assert results[1]["agent_type"] == "audience_insights"


@pytest.mark.unit
class TestBossAgentUtilities:
    """Test utility functions for Boss Agent"""

    def test_intent_mapping(self):
        """Test intent to agent mapping"""
        from boss_agent import INTENT_TO_AGENTS
        
        assert "content_analysis" in INTENT_TO_AGENTS
        assert "audience_insights" in INTENT_TO_AGENTS
        assert "seo_discoverability" in INTENT_TO_AGENTS
        
        # Test comprehensive analysis maps to multiple agents
        comprehensive_agents = INTENT_TO_AGENTS.get("comprehensive_analysis", [])
        assert len(comprehensive_agents) >= 3

    def test_confidence_thresholds(self):
        """Test confidence threshold validation"""
        from boss_agent import CONFIDENCE_THRESHOLDS
        
        assert "high_confidence" in CONFIDENCE_THRESHOLDS
        assert "medium_confidence" in CONFIDENCE_THRESHOLDS
        assert "low_confidence" in CONFIDENCE_THRESHOLDS
        
        assert CONFIDENCE_THRESHOLDS["high_confidence"] > CONFIDENCE_THRESHOLDS["medium_confidence"]
        assert CONFIDENCE_THRESHOLDS["medium_confidence"] > CONFIDENCE_THRESHOLDS["low_confidence"]

    def test_token_budget_defaults(self):
        """Test default token budget configuration"""
        from boss_agent import DEFAULT_TOKEN_BUDGETS
        
        assert "quick" in DEFAULT_TOKEN_BUDGETS
        assert "standard" in DEFAULT_TOKEN_BUDGETS
        assert "deep" in DEFAULT_TOKEN_BUDGETS
        
        # Deep analysis should have more tokens than standard
        deep_budget = DEFAULT_TOKEN_BUDGETS["deep"]
        standard_budget = DEFAULT_TOKEN_BUDGETS["standard"]
        
        assert deep_budget["input_tokens"] > standard_budget["input_tokens"]
        assert deep_budget["output_tokens"] > standard_budget["output_tokens"]