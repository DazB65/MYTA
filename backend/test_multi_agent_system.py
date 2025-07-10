#!/usr/bin/env python3
"""
Comprehensive Testing Script for CreatorMate Multi-Agent System
Tests all components of the hierarchical agent architecture
"""

import asyncio
import json
import time
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys
import os
import httpx
from dataclasses import dataclass

# Add the backend directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('multi_agent_test.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Represents the result of a test"""
    test_name: str
    success: bool
    duration: float
    details: Dict[str, Any]
    error_message: Optional[str] = None

class CreatorMateSystemTester:
    """Comprehensive tester for the CreatorMate multi-agent system"""
    
    def __init__(self, base_url: str = "http://localhost:8888"):
        self.base_url = base_url
        self.test_results: List[TestResult] = []
        self.start_time = datetime.now()
        
        # Test data - using MrBeast as a well-known channel for testing
        self.test_channel_data = {
            "channel_id": "UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast
            "channel_name": "MrBeast",
            "user_id": "test_user_001"
        }
        
        # Test queries for different agent types
        self.test_queries = {
            "content_analysis": "How are my recent videos performing? I want to analyze hooks and retention.",
            "audience_insights": "Tell me about my audience demographics and engagement patterns.",
            "seo_optimization": "How can I improve my video discoverability and SEO?",
            "competitive_analysis": "Analyze my competitors and show me opportunities.",
            "monetization": "What are my best monetization opportunities right now?",
            "general": "Give me an overall assessment of my channel performance."
        }
        
        # Expected model assignments from CLAUDE.md
        self.expected_models = {
            "boss_agent": "claude-3-5-sonnet-20241022",
            "content_analysis": "gemini-2.0-flash-exp", 
            "audience_insights": "claude-3-5-sonnet-20241022",
            "seo_discoverability": "claude-3-5-haiku-20241022",
            "competitive_analysis": "gemini-2.0-flash-exp",
            "monetization_strategy": "claude-3-5-haiku-20241022"
        }
    
    def log_test_start(self, test_name: str):
        """Log the start of a test"""
        logger.info(f"\n{'='*80}")
        logger.info(f"🧪 STARTING TEST: {test_name}")
        logger.info(f"{'='*80}")
    
    def log_test_result(self, result: TestResult):
        """Log the result of a test"""
        status_emoji = "✅" if result.success else "❌"
        logger.info(f"{status_emoji} TEST COMPLETED: {result.test_name}")
        logger.info(f"   Duration: {result.duration:.2f}s")
        logger.info(f"   Success: {result.success}")
        if result.error_message:
            logger.error(f"   Error: {result.error_message}")
        logger.info(f"   Details: {json.dumps(result.details, indent=2)}")
        
        self.test_results.append(result)
    
    async def test_system_startup(self) -> TestResult:
        """Test that the system starts up correctly"""
        self.log_test_start("System Startup and Health Check")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # Test system health endpoint
                response = await client.get(f"{self.base_url}/api/system/health")
                
                if response.status_code == 200:
                    health_data = response.json()
                    
                    success = health_data.get("overall_health", 0) >= 70
                    
                    result = TestResult(
                        test_name="System Startup",
                        success=success,
                        duration=time.time() - start_time,
                        details={
                            "overall_health": health_data.get("overall_health"),
                            "status": health_data.get("status"),
                            "model_integrations": health_data.get("model_integrations"),
                            "youtube_api": health_data.get("youtube_api"),
                            "cache_system": health_data.get("cache_system")
                        }
                    )
                else:
                    result = TestResult(
                        test_name="System Startup",
                        success=False,
                        duration=time.time() - start_time,
                        details={"status_code": response.status_code},
                        error_message=f"Health check failed with status {response.status_code}"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="System Startup",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_model_integrations(self) -> TestResult:
        """Test all model integrations"""
        self.log_test_start("Model Integration Testing")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # Get model status
                response = await client.get(f"{self.base_url}/api/models/status")
                
                if response.status_code == 200:
                    model_data = response.json()
                    
                    # Test each available integration
                    test_results = {}
                    for provider in model_data.get("active_integrations", []):
                        try:
                            test_response = await client.post(f"{self.base_url}/api/models/test/{provider}")
                            if test_response.status_code == 200:
                                test_data = test_response.json()
                                test_results[provider] = {
                                    "success": test_data.get("success", False),
                                    "model": test_data.get("model"),
                                    "response_preview": test_data.get("response_preview"),
                                    "tokens_used": test_data.get("tokens_used"),
                                    "processing_time": test_data.get("processing_time")
                                }
                            else:
                                test_results[provider] = {"success": False, "error": f"Status {test_response.status_code}"}
                        except Exception as e:
                            test_results[provider] = {"success": False, "error": str(e)}
                    
                    # Determine overall success
                    successful_tests = sum(1 for result in test_results.values() if result.get("success"))
                    total_tests = len(test_results)
                    success = successful_tests > 0  # At least one model working
                    
                    result = TestResult(
                        test_name="Model Integrations",
                        success=success,
                        duration=time.time() - start_time,
                        details={
                            "model_status": model_data,
                            "test_results": test_results,
                            "successful_integrations": successful_tests,
                            "total_integrations": total_tests
                        }
                    )
                else:
                    result = TestResult(
                        test_name="Model Integrations",
                        success=False,
                        duration=time.time() - start_time,
                        details={"status_code": response.status_code},
                        error_message=f"Model status endpoint failed with status {response.status_code}"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="Model Integrations",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_boss_agent(self) -> TestResult:
        """Test the Boss Agent orchestration"""
        self.log_test_start("Boss Agent Orchestration")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # Test general query that should involve multiple agents
                test_payload = {
                    "message": self.test_queries["general"],
                    "user_id": self.test_channel_data["user_id"]
                }
                
                response = await client.post(
                    f"{self.base_url}/api/agent/chat",
                    json=test_payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    chat_data = response.json()
                    
                    # Check for successful response
                    has_response = bool(chat_data.get("response"))
                    response_length = len(chat_data.get("response", ""))
                    
                    success = has_response and response_length > 50  # Meaningful response
                    
                    result = TestResult(
                        test_name="Boss Agent",
                        success=success,
                        duration=time.time() - start_time,
                        details={
                            "response_received": has_response,
                            "response_length": response_length,
                            "response_preview": chat_data.get("response", "")[:200] + "...",
                            "status": chat_data.get("status")
                        }
                    )
                else:
                    result = TestResult(
                        test_name="Boss Agent",
                        success=False,
                        duration=time.time() - start_time,
                        details={"status_code": response.status_code},
                        error_message=f"Boss agent endpoint failed with status {response.status_code}"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="Boss Agent",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_specialized_agents(self) -> TestResult:
        """Test all specialized agents through the Boss Agent"""
        self.log_test_start("Specialized Agents Testing")
        start_time = time.time()
        
        agent_results = {}
        
        try:
            async with httpx.AsyncClient() as client:
                # Test each agent type with specific queries
                for agent_type, query in self.test_queries.items():
                    if agent_type == "general":  # Skip general query
                        continue
                    
                    logger.info(f"🤖 Testing {agent_type} agent...")
                    
                    try:
                        test_payload = {
                            "message": query,
                            "user_id": self.test_channel_data["user_id"]
                        }
                        
                        agent_start = time.time()
                        response = await client.post(
                            f"{self.base_url}/api/agent/chat",
                            json=test_payload,
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            chat_data = response.json()
                            has_response = bool(chat_data.get("response"))
                            response_length = len(chat_data.get("response", ""))
                            
                            agent_results[agent_type] = {
                                "success": has_response and response_length > 50,
                                "response_length": response_length,
                                "processing_time": time.time() - agent_start,
                                "response_preview": chat_data.get("response", "")[:150] + "..."
                            }
                        else:
                            agent_results[agent_type] = {
                                "success": False,
                                "error": f"Status {response.status_code}",
                                "processing_time": time.time() - agent_start
                            }
                    
                    except Exception as e:
                        agent_results[agent_type] = {
                            "success": False,
                            "error": str(e),
                            "processing_time": time.time() - agent_start
                        }
                
                # Determine overall success
                successful_agents = sum(1 for result in agent_results.values() if result.get("success"))
                total_agents = len(agent_results)
                success = successful_agents >= (total_agents * 0.6)  # At least 60% success rate
                
                result = TestResult(
                    test_name="Specialized Agents",
                    success=success,
                    duration=time.time() - start_time,
                    details={
                        "agent_results": agent_results,
                        "successful_agents": successful_agents,
                        "total_agents": total_agents,
                        "success_rate": (successful_agents / total_agents * 100) if total_agents > 0 else 0
                    }
                )
        
        except Exception as e:
            result = TestResult(
                test_name="Specialized Agents",
                success=False,
                duration=time.time() - start_time,
                details={"agent_results": agent_results},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_caching_system(self) -> TestResult:
        """Test the caching system performance"""
        self.log_test_start("Caching System Performance")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # Get initial cache stats
                stats_response = await client.get(f"{self.base_url}/api/agent/cache/stats")
                
                if stats_response.status_code == 200:
                    initial_stats = stats_response.json().get("cache_stats", {})
                    
                    # Make the same request twice to test caching
                    test_payload = {
                        "message": self.test_queries["content_analysis"],
                        "user_id": self.test_channel_data["user_id"]
                    }
                    
                    # First request
                    first_start = time.time()
                    first_response = await client.post(
                        f"{self.base_url}/api/agent/chat",
                        json=test_payload,
                        timeout=30.0
                    )
                    first_duration = time.time() - first_start
                    
                    # Wait a moment
                    await asyncio.sleep(1)
                    
                    # Second request (should be faster due to caching)
                    second_start = time.time()
                    second_response = await client.post(
                        f"{self.base_url}/api/agent/chat",
                        json=test_payload,
                        timeout=30.0
                    )
                    second_duration = time.time() - second_start
                    
                    # Get updated cache stats
                    final_stats_response = await client.get(f"{self.base_url}/api/agent/cache/stats")
                    final_stats = final_stats_response.json().get("cache_stats", {}) if final_stats_response.status_code == 200 else {}
                    
                    # Analyze caching effectiveness
                    cache_improvement = (first_duration - second_duration) / first_duration * 100 if first_duration > 0 else 0
                    both_successful = (first_response.status_code == 200 and second_response.status_code == 200)
                    
                    success = both_successful and cache_improvement > -50  # Allow some variance
                    
                    result = TestResult(
                        test_name="Caching System",
                        success=success,
                        duration=time.time() - start_time,
                        details={
                            "initial_cache_stats": initial_stats,
                            "final_cache_stats": final_stats,
                            "first_request_time": first_duration,
                            "second_request_time": second_duration,
                            "cache_improvement_percent": cache_improvement,
                            "both_requests_successful": both_successful
                        }
                    )
                else:
                    result = TestResult(
                        test_name="Caching System",
                        success=False,
                        duration=time.time() - start_time,
                        details={"status_code": stats_response.status_code},
                        error_message="Could not access cache stats endpoint"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="Caching System",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_youtube_integration(self) -> TestResult:
        """Test YouTube API integration"""
        self.log_test_start("YouTube API Integration")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                # Test YouTube quota endpoint
                quota_response = await client.get(f"{self.base_url}/api/youtube/quota")
                
                if quota_response.status_code == 200:
                    quota_data = quota_response.json()
                    
                    # Test YouTube analytics endpoint with our test channel
                    analytics_payload = {
                        "channel_id": self.test_channel_data["channel_id"],
                        "user_id": self.test_channel_data["user_id"],
                        "analysis_type": "comprehensive",
                        "include_videos": True,
                        "video_count": 5
                    }
                    
                    analytics_response = await client.post(
                        f"{self.base_url}/api/youtube/analytics",
                        json=analytics_payload,
                        timeout=30.0
                    )
                    
                    if analytics_response.status_code == 200:
                        analytics_data = analytics_response.json()
                        channel_data = analytics_data.get("channel_data", {})
                        
                        success = bool(channel_data.get("basic_info", {}).get("channel_id"))
                        
                        result = TestResult(
                            test_name="YouTube Integration",
                            success=success,
                            duration=time.time() - start_time,
                            details={
                                "quota_status": quota_data.get("quota_status"),
                                "analytics_available": success,
                                "channel_info": channel_data.get("basic_info", {}),
                                "recent_videos_count": len(channel_data.get("recent_videos", []))
                            }
                        )
                    else:
                        result = TestResult(
                            test_name="YouTube Integration",
                            success=False,
                            duration=time.time() - start_time,
                            details={
                                "quota_status": quota_data.get("quota_status"),
                                "analytics_status_code": analytics_response.status_code
                            },
                            error_message=f"Analytics endpoint failed with status {analytics_response.status_code}"
                        )
                else:
                    result = TestResult(
                        test_name="YouTube Integration",
                        success=False,
                        duration=time.time() - start_time,
                        details={"quota_status_code": quota_response.status_code},
                        error_message=f"Quota endpoint failed with status {quota_response.status_code}"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="YouTube Integration",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_authentication_system(self) -> TestResult:
        """Test the JWT authentication system"""
        self.log_test_start("Authentication System")
        start_time = time.time()
        
        try:
            # Import auth system components
            from boss_agent_auth import get_boss_agent_authenticator
            
            authenticator = get_boss_agent_authenticator()
            
            # Test token generation
            test_request_id = str(uuid.uuid4())
            token = authenticator.generate_boss_agent_token(test_request_id)
            
            # Test token validation
            validation_result = authenticator.validate_boss_agent_token(token, test_request_id)
            
            # Test with invalid token
            invalid_validation = authenticator.validate_boss_agent_token("invalid_token", test_request_id)
            
            success = (
                validation_result.is_valid and 
                not invalid_validation.is_valid and
                validation_result.request_id == test_request_id
            )
            
            result = TestResult(
                test_name="Authentication System",
                success=success,
                duration=time.time() - start_time,
                details={
                    "token_generated": bool(token),
                    "valid_token_accepted": validation_result.is_valid,
                    "invalid_token_rejected": not invalid_validation.is_valid,
                    "request_id_match": validation_result.request_id == test_request_id,
                    "agent_id": validation_result.agent_id,
                    "permissions": validation_result.permissions
                }
            )
        
        except Exception as e:
            result = TestResult(
                test_name="Authentication System",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    async def test_agent_status_endpoint(self) -> TestResult:
        """Test the agent status endpoint"""
        self.log_test_start("Agent Status Endpoint")
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/agent/status")
                
                if response.status_code == 200:
                    status_data = response.json()
                    
                    required_fields = ["status", "version", "architecture", "agents", "timestamp"]
                    has_required_fields = all(field in status_data for field in required_fields)
                    
                    expected_agents = ["boss_agent", "content_analysis", "audience_insights", 
                                     "seo_discoverability", "competitive_analysis", "monetization_strategy"]
                    has_expected_agents = all(agent in status_data.get("agents", []) for agent in expected_agents)
                    
                    is_online = status_data.get("status") in ["online", "initializing"]
                    correct_architecture = status_data.get("architecture") == "hierarchical_multi_agent"
                    
                    success = has_required_fields and has_expected_agents and is_online and correct_architecture
                    
                    result = TestResult(
                        test_name="Agent Status Endpoint",
                        success=success,
                        duration=time.time() - start_time,
                        details={
                            "status": status_data.get("status"),
                            "version": status_data.get("version"),
                            "architecture": status_data.get("architecture"),
                            "agents_count": len(status_data.get("agents", [])),
                            "system_health": status_data.get("system_health", {}),
                            "has_required_fields": has_required_fields,
                            "has_expected_agents": has_expected_agents
                        }
                    )
                else:
                    result = TestResult(
                        test_name="Agent Status Endpoint",
                        success=False,
                        duration=time.time() - start_time,
                        details={"status_code": response.status_code},
                        error_message=f"Status endpoint failed with status {response.status_code}"
                    )
        
        except Exception as e:
            result = TestResult(
                test_name="Agent Status Endpoint",
                success=False,
                duration=time.time() - start_time,
                details={},
                error_message=str(e)
            )
        
        self.log_test_result(result)
        return result
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        successful_tests = sum(1 for result in self.test_results if result.success)
        total_tests = len(self.test_results)
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Categorize results
        passed_tests = [result for result in self.test_results if result.success]
        failed_tests = [result for result in self.test_results if not result.success]
        
        report = {
            "test_session": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "total_duration": total_duration,
                "test_environment": {
                    "base_url": self.base_url,
                    "test_channel": self.test_channel_data
                }
            },
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": len(failed_tests),
                "success_rate": success_rate,
                "overall_status": "PASS" if success_rate >= 70 else "FAIL"
            },
            "test_results": {
                "passed": [{"name": r.test_name, "duration": r.duration} for r in passed_tests],
                "failed": [{"name": r.test_name, "duration": r.duration, "error": r.error_message} for r in failed_tests]
            },
            "detailed_results": [
                {
                    "test_name": result.test_name,
                    "success": result.success,
                    "duration": result.duration,
                    "details": result.details,
                    "error_message": result.error_message
                }
                for result in self.test_results
            ]
        }
        
        return report
    
    def print_test_summary(self):
        """Print a formatted test summary"""
        report = self.generate_test_report()
        
        print("\n" + "="*80)
        print("🧪 CREATORMATE MULTI-AGENT SYSTEM TEST SUMMARY")
        print("="*80)
        
        summary = report["summary"]
        print(f"📊 Test Results: {summary['successful_tests']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
        print(f"⏱️  Total Duration: {report['test_session']['total_duration']:.2f} seconds")
        print(f"🎯 Overall Status: {summary['overall_status']}")
        
        if report["test_results"]["passed"]:
            print(f"\n✅ Passed Tests ({len(report['test_results']['passed'])}):")
            for test in report["test_results"]["passed"]:
                print(f"   • {test['name']} ({test['duration']:.2f}s)")
        
        if report["test_results"]["failed"]:
            print(f"\n❌ Failed Tests ({len(report['test_results']['failed'])}):")
            for test in report["test_results"]["failed"]:
                print(f"   • {test['name']} ({test['duration']:.2f}s)")
                if test["error"]:
                    print(f"     Error: {test['error']}")
        
        print("\n" + "="*80)
        
        # Save detailed report
        report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Detailed report saved to: {report_filename}")
        print("📄 Test logs saved to: multi_agent_test.log")
    
    async def run_all_tests(self):
        """Run all tests in sequence"""
        logger.info("🚀 Starting CreatorMate Multi-Agent System Comprehensive Test Suite")
        logger.info(f"📍 Base URL: {self.base_url}")
        logger.info(f"🧪 Test Channel: {self.test_channel_data['channel_name']} ({self.test_channel_data['channel_id']})")
        
        # Define test sequence
        tests = [
            self.test_system_startup,
            self.test_agent_status_endpoint,
            self.test_authentication_system,
            self.test_model_integrations,
            self.test_caching_system,
            self.test_youtube_integration,
            self.test_boss_agent,
            self.test_specialized_agents
        ]
        
        # Run each test
        for test_func in tests:
            try:
                await test_func()
                # Small delay between tests
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Test function {test_func.__name__} failed with exception: {e}")
                # Create a failed test result
                result = TestResult(
                    test_name=test_func.__name__,
                    success=False,
                    duration=0,
                    details={},
                    error_message=str(e)
                )
                self.test_results.append(result)
        
        # Generate and print summary
        self.print_test_summary()

async def main():
    """Main test function"""
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8888/health")
            if response.status_code != 200:
                print("❌ CreatorMate server is not running or not healthy!")
                print("Please start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8888")
                return
    except Exception as e:
        print("❌ Cannot connect to CreatorMate server!")
        print("Please start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8888")
        print(f"Error: {e}")
        return
    
    # Run comprehensive tests
    tester = CreatorMateSystemTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())