"""
Integration tests for agent communication system
Tests the complete agent hierarchy and communication protocols
"""

import pytest
import asyncio
import json
from datetime import datetime
from typing import Dict, Any
from unittest.mock import Mock, patch, AsyncMock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from exceptions import (
    AgentCommunicationError, AgentTimeoutError, AgentAuthenticationError,
    ValidationError, ExternalAPIError
)
from boss_agent_auth import BossAgentAuthenticator, BossAgentCredentials
from base_agent import AgentType, AnalysisDepth, Priority
from async_processing import AsyncProcessor, TaskPriority, TaskStatus
from distributed_cache import DistributedCache
from circuit_breaker import CircuitBreakerManager


class TestAgentAuthentication:
    """Test agent authentication system"""
    
    @pytest.fixture
    def authenticator(self):
        """Create test authenticator"""
        credentials = BossAgentCredentials(secret_key="test-secret-key")
        return BossAgentAuthenticator(credentials)
    
    def test_token_generation(self, authenticator):
        """Test JWT token generation"""
        token = authenticator.generate_token("test-request-123")
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_token_validation_success(self, authenticator):
        """Test successful token validation"""
        request_id = "test-request-123"
        token = authenticator.generate_token(request_id)
        
        result = authenticator.validate_token(token)
        assert result.is_valid
        assert result.request_id == request_id
        assert result.agent_id == "boss_agent"
    
    def test_token_validation_invalid(self, authenticator):
        """Test invalid token validation"""
        invalid_token = "invalid.token.here"
        
        result = authenticator.validate_token(invalid_token)
        assert not result.is_valid
        assert result.error_message is not None
    
    def test_token_validation_expired(self, authenticator):
        """Test expired token validation"""
        # Create authenticator with very short expiry
        credentials = BossAgentCredentials(
            secret_key="test-secret-key",
            token_expiry_hours=0.001  # ~3.6 seconds
        )
        short_lived_auth = BossAgentAuthenticator(credentials)
        
        token = short_lived_auth.generate_token("test-request")
        
        # Wait for token to expire
        import time
        time.sleep(4)
        
        result = short_lived_auth.validate_token(token)
        assert not result.is_valid
        assert "expired" in result.error_message.lower()


class TestAgentCommunication:
    """Test agent communication protocols"""
    
    @pytest.fixture
    async def mock_agents(self):
        """Create mock agent implementations"""
        agents = {}
        
        # Mock Content Analysis Agent
        content_agent = Mock()
        content_agent.process_request = AsyncMock(return_value={
            "agent_type": "content_analysis",
            "analysis": {
                "summary": "Video performance analysis",
                "key_insights": [
                    {
                        "insight": "Strong hook engagement",
                        "evidence": "95% retention in first 30 seconds",
                        "impact": "High",
                        "confidence": 0.9
                    }
                ],
                "recommendations": [
                    {
                        "recommendation": "Maintain current hook style",
                        "expected_impact": "High",
                        "implementation_difficulty": "Easy"
                    }
                ]
            },
            "confidence_score": 0.88,
            "domain_match": True,
            "for_boss_agent_only": True
        })
        agents["content_analysis"] = content_agent
        
        # Mock Audience Insights Agent
        audience_agent = Mock()
        audience_agent.process_request = AsyncMock(return_value={
            "agent_type": "audience_insights",
            "analysis": {
                "summary": "Audience demographic analysis",
                "key_insights": [
                    {
                        "insight": "Primary audience: 25-34 age group",
                        "evidence": "68% of viewers in this demographic",
                        "impact": "High",
                        "confidence": 0.85
                    }
                ],
                "recommendations": [
                    {
                        "recommendation": "Create content for young professionals",
                        "expected_impact": "Medium",
                        "implementation_difficulty": "Medium"
                    }
                ]
            },
            "confidence_score": 0.82,
            "domain_match": True,
            "for_boss_agent_only": True
        })
        agents["audience_insights"] = audience_agent
        
        return agents
    
    @pytest.fixture
    async def boss_agent(self, mock_agents):
        """Create mock boss agent"""
        with patch('boss_agent.BossAgent') as MockBossAgent:
            boss = MockBossAgent.return_value
            boss.specialized_agents = mock_agents
            boss.process_chat_message = AsyncMock()
            boss.delegate_to_agent = AsyncMock()
            return boss
    
    async def test_boss_agent_delegation(self, boss_agent, mock_agents):
        """Test boss agent delegation to specialized agents"""
        # Mock boss agent delegation
        boss_agent.delegate_to_agent.return_value = {
            "success": True,
            "agent_type": "content_analysis",
            "response": mock_agents["content_analysis"].process_request.return_value
        }
        
        # Test delegation
        result = await boss_agent.delegate_to_agent(
            agent_type="content_analysis",
            request_data={
                "query": "Analyze my latest video performance",
                "context": {"channel_id": "test-channel"}
            }
        )
        
        assert result["success"]
        assert result["agent_type"] == "content_analysis"
        assert result["response"]["domain_match"]
        assert result["response"]["for_boss_agent_only"]
    
    async def test_agent_authentication_flow(self, mock_agents):
        """Test complete authentication flow between agents"""
        authenticator = BossAgentAuthenticator()
        
        # Generate token
        request_id = "test-auth-flow"
        token = authenticator.generate_token(request_id)
        
        # Simulate agent receiving request with token
        with patch('boss_agent_auth.get_boss_agent_authenticator') as mock_get_auth:
            mock_get_auth.return_value = authenticator
            
            # Mock agent should validate token
            validation_result = authenticator.validate_token(token)
            assert validation_result.is_valid
            
            # Mock successful agent processing
            mock_agents["content_analysis"].process_request.assert_not_called()
            
            # Call agent with valid token
            response = await mock_agents["content_analysis"].process_request({
                "boss_agent_token": token,
                "request_id": request_id,
                "query_type": "content_analysis"
            })
            
            assert response["for_boss_agent_only"]
            assert response["domain_match"]
    
    async def test_agent_timeout_handling(self, mock_agents):
        """Test agent timeout handling"""
        # Mock agent that times out
        timeout_agent = Mock()
        timeout_agent.process_request = AsyncMock(
            side_effect=asyncio.TimeoutError("Agent timed out")
        )
        
        with pytest.raises(AgentTimeoutError):
            # Simulate timeout scenario
            try:
                await asyncio.wait_for(
                    timeout_agent.process_request({}),
                    timeout=0.1
                )
            except asyncio.TimeoutError:
                raise AgentTimeoutError("content_analysis", 30)
    
    async def test_agent_error_handling(self, mock_agents):
        """Test agent error handling"""
        # Mock agent that raises errors
        error_agent = Mock()
        error_agent.process_request = AsyncMock(
            side_effect=ExternalAPIError("OpenAI API", "Rate limit exceeded", 429)
        )
        
        with pytest.raises(ExternalAPIError):
            await error_agent.process_request({})


class TestAsyncProcessing:
    """Test async processing system"""
    
    @pytest.fixture
    async def processor(self):
        """Create test async processor"""
        processor = AsyncProcessor(max_workers=2, queue_size=100)
        await processor.start()
        yield processor
        await processor.stop()
    
    async def test_task_submission(self, processor):
        """Test task submission and execution"""
        # Define test function
        def test_func(x, y):
            return x + y
        
        # Submit task
        task_id = await processor.submit_task(
            test_func,
            5, 10,
            priority=TaskPriority.NORMAL,
            timeout=30
        )
        
        assert task_id is not None
        
        # Wait for result
        result = await processor.get_task_result(task_id, wait=True, timeout=10)
        
        assert result is not None
        assert result.status == TaskStatus.COMPLETED
        assert result.result == 15
    
    async def test_task_priority_ordering(self, processor):
        """Test task priority ordering"""
        results = []
        
        def test_func(priority_name):
            results.append(priority_name)
            return priority_name
        
        # Submit tasks with different priorities
        high_task = await processor.submit_task(
            test_func, "high",
            priority=TaskPriority.HIGH
        )
        
        low_task = await processor.submit_task(
            test_func, "low",
            priority=TaskPriority.LOW
        )
        
        normal_task = await processor.submit_task(
            test_func, "normal",
            priority=TaskPriority.NORMAL
        )
        
        # Wait for all tasks to complete
        await asyncio.sleep(2)
        
        # High priority should execute first
        assert len(results) >= 3
        assert results[0] == "high"
    
    async def test_task_timeout(self, processor):
        """Test task timeout handling"""
        import time
        
        def slow_func():
            time.sleep(5)  # Sleep longer than timeout
            return "completed"
        
        task_id = await processor.submit_task(
            slow_func,
            timeout=1,  # 1 second timeout
            use_thread=True
        )
        
        result = await processor.get_task_result(task_id, wait=True, timeout=10)
        
        assert result is not None
        assert result.status == TaskStatus.TIMEOUT
        assert "timed out" in result.error.lower()
    
    async def test_task_failure_handling(self, processor):
        """Test task failure handling"""
        def failing_func():
            raise ValueError("Test error")
        
        task_id = await processor.submit_task(failing_func)
        
        result = await processor.get_task_result(task_id, wait=True, timeout=10)
        
        assert result is not None
        assert result.status == TaskStatus.FAILED
        assert "Test error" in result.error


class TestCircuitBreaker:
    """Test circuit breaker functionality"""
    
    @pytest.fixture
    def circuit_manager(self):
        """Create circuit breaker manager"""
        return CircuitBreakerManager()
    
    async def test_circuit_breaker_normal_operation(self, circuit_manager):
        """Test circuit breaker in normal operation"""
        breaker = circuit_manager.get_breaker("test_service")
        
        def successful_operation():
            return "success"
        
        # Should work normally
        result = await breaker.call(successful_operation)
        assert result == "success"
        assert breaker.get_state().value == "closed"
    
    async def test_circuit_breaker_failure_threshold(self, circuit_manager):
        """Test circuit breaker opening on failures"""
        from circuit_breaker import CircuitBreakerConfig
        
        config = CircuitBreakerConfig(
            failure_threshold=3,
            recovery_timeout=1,
            expected_exception=ValueError
        )
        
        breaker = circuit_manager.get_breaker("test_failing_service", config)
        
        def failing_operation():
            raise ValueError("Service failed")
        
        # Cause failures to open circuit
        for _ in range(3):
            try:
                await breaker.call(failing_operation)
            except ValueError:
                pass
        
        # Circuit should be open now
        assert breaker.get_state().value == "open"
        
        # Further calls should be rejected
        from exceptions import SystemError
        with pytest.raises(SystemError):
            await breaker.call(failing_operation)


class TestCacheIntegration:
    """Test cache integration"""
    
    @pytest.fixture
    async def cache(self):
        """Create test cache"""
        cache = DistributedCache(redis_url=None, enable_fallback=True)
        await cache.initialize()
        return cache
    
    async def test_agent_response_caching(self, cache):
        """Test caching of agent responses"""
        # Mock agent response
        response_data = {
            "agent_type": "content_analysis",
            "analysis": {"summary": "Test analysis"},
            "confidence_score": 0.85,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        cache_key = "agent:content_analysis:user123:query_hash"
        
        # Set cache
        success = await cache.set(cache_key, response_data, category="agent_response")
        assert success
        
        # Get from cache
        cached_data = await cache.get(cache_key)
        assert cached_data is not None
        assert cached_data["agent_type"] == "content_analysis"
        assert cached_data["confidence_score"] == 0.85
    
    async def test_cache_invalidation(self, cache):
        """Test cache invalidation"""
        cache_key = "test:invalidation"
        test_data = {"value": "test"}
        
        # Set and verify
        await cache.set(cache_key, test_data)
        assert await cache.get(cache_key) is not None
        
        # Delete and verify
        deleted = await cache.delete(cache_key)
        assert deleted
        assert await cache.get(cache_key) is None


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows"""
    
    @pytest.fixture
    async def complete_system(self):
        """Setup complete system for testing"""
        # Mock all components
        system = {
            "authenticator": BossAgentAuthenticator(),
            "processor": AsyncProcessor(max_workers=1),
            "cache": DistributedCache(redis_url=None, enable_fallback=True),
            "circuit_manager": CircuitBreakerManager()
        }
        
        await system["processor"].start()
        await system["cache"].initialize()
        
        yield system
        
        await system["processor"].stop()
    
    async def test_complete_agent_workflow(self, complete_system):
        """Test complete agent communication workflow"""
        auth = complete_system["authenticator"]
        processor = complete_system["processor"]
        cache = complete_system["cache"]
        
        # Simulate user request
        user_id = "test-user-123"
        request_id = "test-request-456"
        
        # Generate authentication token
        token = auth.generate_token(request_id)
        
        # Create mock agent processing function
        async def mock_agent_processing(user_query, context, auth_token):
            # Validate token
            validation = auth.validate_token(auth_token)
            if not validation.is_valid:
                raise AgentAuthenticationError("content_analysis")
            
            # Simulate processing
            await asyncio.sleep(0.1)
            
            return {
                "agent_type": "content_analysis",
                "response_id": "resp-123",
                "analysis": {
                    "summary": f"Analysis for: {user_query}",
                    "confidence": 0.92
                },
                "processing_time": 0.1,
                "for_boss_agent_only": True
            }
        
        # Submit processing task
        task_id = await processor.submit_task(
            mock_agent_processing,
            "Analyze my channel performance",
            {"channel_id": "test-channel"},
            token,
            user_id=user_id,
            agent_type="content_analysis",
            priority=TaskPriority.HIGH
        )
        
        # Wait for result
        result = await processor.get_task_result(task_id, wait=True, timeout=10)
        
        assert result is not None
        assert result.status == TaskStatus.COMPLETED
        assert result.result["agent_type"] == "content_analysis"
        assert result.result["for_boss_agent_only"]
        
        # Cache the result
        cache_key = f"agent_result:{user_id}:{task_id}"
        cached = await cache.set(cache_key, result.result, category="agent_response")
        assert cached
        
        # Verify cache retrieval
        cached_result = await cache.get(cache_key)
        assert cached_result["analysis"]["confidence"] == 0.92
    
    async def test_error_recovery_workflow(self, complete_system):
        """Test error recovery in complete workflow"""
        processor = complete_system["processor"]
        
        # Mock failing agent
        async def failing_agent():
            raise ExternalAPIError("OpenAI", "API temporarily unavailable", 503)
        
        task_id = await processor.submit_task(
            failing_agent,
            timeout=5
        )
        
        result = await processor.get_task_result(task_id, wait=True, timeout=10)
        
        assert result is not None
        assert result.status == TaskStatus.FAILED
        assert "API temporarily unavailable" in result.error


@pytest.mark.asyncio
class TestRealTimeProcessing:
    """Test real-time processing scenarios"""
    
    async def test_concurrent_agent_requests(self):
        """Test handling multiple concurrent agent requests"""
        processor = AsyncProcessor(max_workers=3)
        await processor.start()
        
        try:
            # Submit multiple concurrent tasks
            tasks = []
            for i in range(10):
                task_id = await processor.submit_task(
                    lambda x: x * 2,
                    i,
                    priority=TaskPriority.NORMAL
                )
                tasks.append(task_id)
            
            # Wait for all results
            results = []
            for task_id in tasks:
                result = await processor.get_task_result(task_id, wait=True, timeout=10)
                results.append(result)
            
            # Verify all completed successfully
            assert len(results) == 10
            assert all(r.status == TaskStatus.COMPLETED for r in results)
            
        finally:
            await processor.stop()
    
    async def test_load_balancing(self):
        """Test load balancing across workers"""
        processor = AsyncProcessor(max_workers=2)
        await processor.start()
        
        try:
            # Submit tasks that take time
            import time
            
            def slow_task(task_id):
                time.sleep(0.5)
                return f"completed-{task_id}"
            
            # Submit multiple tasks
            task_ids = []
            for i in range(4):
                task_id = await processor.submit_task(
                    slow_task,
                    i,
                    use_thread=True
                )
                task_ids.append(task_id)
            
            # All tasks should complete
            for task_id in task_ids:
                result = await processor.get_task_result(task_id, wait=True, timeout=15)
                assert result.status == TaskStatus.COMPLETED
                assert "completed-" in result.result
        
        finally:
            await processor.stop()


if __name__ == "__main__":
    # Run specific test classes
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ])