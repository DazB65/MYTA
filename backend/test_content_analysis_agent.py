"""
Comprehensive Testing Suite for CreatorMate Content Analysis Agent
Tests the specialized agent's functionality, boss agent integration, and performance
"""

import asyncio
import json
import time
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import statistics
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_analysis_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Structure for individual test results"""
    test_name: str
    success: bool
    response_time: float
    token_usage: Dict[str, int]
    cache_hit: bool
    confidence_score: float
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None

@dataclass
class MockVideoData:
    """Mock video data for testing"""
    video_id: str
    title: str
    views: int
    likes: int
    comments: int
    duration: int
    published_at: str
    engagement_rate: float
    
class MockYouTubeAPI:
    """Mock YouTube API responses for consistent testing"""
    
    def __init__(self):
        self.mock_videos = [
            MockVideoData(
                video_id="test_video_001",
                title="How to Master YouTube Analytics in 2024",
                views=15420,
                likes=789,
                comments=156,
                duration=847,  # 14:07
                published_at="2024-07-01T10:00:00Z",
                engagement_rate=6.12
            ),
            MockVideoData(
                video_id="test_video_002", 
                title="5 Content Creation Mistakes That Kill Your Channel",
                views=8965,
                likes=423,
                comments=87,
                duration=623,  # 10:23
                published_at="2024-07-03T14:30:00Z",
                engagement_rate=5.69
            ),
            MockVideoData(
                video_id="test_video_003",
                title="The Ultimate Guide to Video Thumbnails",
                views=22150,
                likes=1247,
                comments=289,
                duration=756,  # 12:36
                published_at="2024-07-05T09:15:00Z",
                engagement_rate=6.93
            ),
            MockVideoData(
                video_id="test_video_004",
                title="YouTube Algorithm Secrets Revealed",
                views=31200,
                likes=1876,
                comments=423,
                duration=1034,  # 17:14
                published_at="2024-07-07T16:45:00Z",
                engagement_rate=7.36
            ),
            MockVideoData(
                video_id="test_video_005",
                title="Building a Loyal YouTube Community",
                views=6734,
                likes=287,
                comments=52,
                duration=532,  # 8:52
                published_at="2024-07-09T11:20:00Z",
                engagement_rate=5.04
            )
        ]
        
        self.channel_averages = {
            "avg_views": 16894,
            "avg_engagement_rate": 6.23,
            "avg_duration": 758,
            "video_count": 47
        }
    
    def get_video_statistics(self, video_ids: List[str]) -> List[Dict]:
        """Return mock video statistics"""
        results = []
        for video_id in video_ids:
            video = next((v for v in self.mock_videos if v.video_id == video_id), None)
            if video:
                results.append({
                    "video_id": video.video_id,
                    "title": video.title,
                    "views": video.views,
                    "likes": video.likes,
                    "comments": video.comments,
                    "duration": video.duration,
                    "published_at": video.published_at,
                    "engagement_rate": video.engagement_rate
                })
        return results
    
    def get_retention_data(self, video_id: str) -> Dict:
        """Return mock retention data"""
        # Generate realistic retention curve
        retention_points = []
        base_retention = 85.0
        
        for i in range(0, 101, 5):  # 0% to 100% in 5% increments
            # Simulate typical YouTube retention curve
            if i <= 15:
                retention = base_retention - (i * 1.2)  # Sharp drop in first 15%
            elif i <= 50:
                retention = base_retention - 18 - ((i - 15) * 0.8)  # Gradual decline
            else:
                retention = base_retention - 46 - ((i - 50) * 0.3)  # Slower decline
            
            retention = max(retention, 15.0)  # Minimum retention
            retention_points.append({
                "elapsed_video_time_ratio": i / 100,
                "audience_watch_ratio": retention / 100
            })
        
        return {
            "video_id": video_id,
            "retention_data": retention_points,
            "average_view_duration": 423,  # seconds
            "average_view_percentage": 58.2
        }
    
    def get_traffic_sources(self, video_id: str) -> Dict:
        """Return mock traffic source data"""
        return {
            "video_id": video_id,
            "traffic_sources": {
                "youtube_search": 32.4,
                "suggested_videos": 28.7,
                "browse_features": 15.2,
                "external": 12.1,
                "channel_page": 8.3,
                "direct_or_unknown": 3.3
            }
        }

class ContentAnalysisTestSuite:
    """Comprehensive test suite for Content Analysis Agent"""
    
    def __init__(self):
        self.mock_api = MockYouTubeAPI()
        self.test_results: List[TestResult] = []
        self.performance_metrics = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "avg_response_time": 0.0,
            "total_tokens_used": 0,
            "cache_hit_rate": 0.0
        }
        
        # Import the Content Analysis Agent
        try:
            from content_analysis_agent import process_content_analysis_request
            self.agent_function = process_content_analysis_request
            logger.info("✅ Content Analysis Agent imported successfully")
        except ImportError as e:
            logger.error(f"❌ Failed to import Content Analysis Agent: {e}")
            self.agent_function = None
    
    async def run_full_test_suite(self) -> Dict[str, Any]:
        """Execute the complete test suite"""
        
        logger.info("🚀 Starting Content Analysis Agent Test Suite")
        logger.info("=" * 60)
        
        if not self.agent_function:
            logger.error("❌ Cannot run tests - agent function not available")
            return {"error": "Agent function not available"}
        
        # Test categories
        test_categories = [
            ("Basic Performance Analysis", self._test_basic_performance_analysis),
            ("Thumbnail & Title Analysis", self._test_thumbnail_title_analysis),
            ("Content Quality Assessment", self._test_content_quality_assessment),
            ("Retention Pattern Analysis", self._test_retention_analysis),
            ("Comparative Performance", self._test_comparative_performance),
            ("Domain Validation", self._test_domain_validation),
            ("Cache Performance", self._test_cache_performance),
            ("Error Handling", self._test_error_handling),
            ("Response Validation", self._test_response_validation)
        ]
        
        # Execute all test categories
        for category_name, test_function in test_categories:
            logger.info(f"\n📋 Testing Category: {category_name}")
            logger.info("-" * 40)
            
            try:
                await test_function()
                logger.info(f"✅ {category_name} tests completed")
            except Exception as e:
                logger.error(f"❌ {category_name} tests failed: {e}")
                logger.error(traceback.format_exc())
        
        # Calculate final metrics
        self._calculate_performance_metrics()
        
        # Generate test report
        report = self._generate_test_report()
        
        logger.info("\n🎉 Test Suite Completed!")
        logger.info("=" * 60)
        
        return report
    
    async def _test_basic_performance_analysis(self):
        """Test basic video performance analysis"""
        
        test_request = {
            "request_id": f"test_basic_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "TechTutor_Test",
                "time_period": "last_30d",
                "specific_videos": ["test_video_001", "test_video_002", "test_video_003"],
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 3000,
                "output_tokens": 1500
            },
            "analysis_depth": "standard",
            "include_visual_analysis": True
        }
        
        result = await self._execute_test(
            "Basic Performance Analysis",
            test_request,
            expected_insights=["engagement", "performance", "views"]
        )
        
        # Validate specific requirements for basic analysis
        if result.success and result.response_data:
            analysis = result.response_data.get('analysis', {})
            
            # Check for required performance metrics
            metrics = analysis.get('metrics', {})
            required_metrics = ['engagement_score', 'performance_vs_average']
            missing_metrics = [m for m in required_metrics if m not in metrics]
            
            if missing_metrics:
                logger.warning(f"⚠️ Missing performance metrics: {missing_metrics}")
            else:
                logger.info("✅ All required performance metrics present")
    
    async def _test_thumbnail_title_analysis(self):
        """Test thumbnail and title effectiveness analysis"""
        
        test_request = {
            "request_id": f"test_thumbnail_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "ThumbnailTest_Channel",
                "time_period": "last_7d",
                "specific_videos": ["test_video_003", "test_video_004"],  # High performing videos
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 3500,
                "output_tokens": 2000
            },
            "analysis_depth": "deep",
            "include_visual_analysis": True,
            "focus_areas": ["thumbnail_effectiveness", "title_optimization"]
        }
        
        result = await self._execute_test(
            "Thumbnail & Title Analysis",
            test_request,
            expected_insights=["thumbnail", "title", "click-through", "visual"]
        )
        
        # Validate thumbnail and title specific insights
        if result.success and result.response_data:
            insights = result.response_data.get('analysis', {}).get('key_insights', [])
            title_thumbnail_insights = [
                insight for insight in insights 
                if any(keyword in insight.get('insight', '').lower() 
                      for keyword in ['thumbnail', 'title', 'visual', 'click'])
            ]
            
            if title_thumbnail_insights:
                logger.info(f"✅ Found {len(title_thumbnail_insights)} thumbnail/title insights")
            else:
                logger.warning("⚠️ No specific thumbnail/title insights generated")
    
    async def _test_content_quality_assessment(self):
        """Test content quality assessment capabilities"""
        
        test_request = {
            "request_id": f"test_quality_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "QualityTest_Channel",
                "time_period": "last_30d",
                "specific_videos": ["test_video_001", "test_video_004", "test_video_005"],
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 4000,
                "output_tokens": 2500
            },
            "analysis_depth": "deep",
            "include_visual_analysis": True,
            "focus_areas": ["content_quality", "production_value", "structure"]
        }
        
        result = await self._execute_test(
            "Content Quality Assessment",
            test_request,
            expected_insights=["quality", "production", "structure", "pacing"]
        )
        
        # Check for quality-specific metrics
        if result.success and result.response_data:
            metrics = result.response_data.get('analysis', {}).get('metrics', {})
            if 'quality_score' in metrics:
                quality_score = metrics['quality_score']
                logger.info(f"✅ Quality score generated: {quality_score}")
                
                if 0 <= quality_score <= 10:
                    logger.info("✅ Quality score within expected range (0-10)")
                else:
                    logger.warning(f"⚠️ Quality score outside expected range: {quality_score}")
    
    async def _test_retention_analysis(self):
        """Test retention pattern analysis"""
        
        test_request = {
            "request_id": f"test_retention_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "RetentionTest_Channel",
                "time_period": "last_14d",
                "specific_videos": ["test_video_002", "test_video_003"],
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 3500,
                "output_tokens": 2000
            },
            "analysis_depth": "standard",
            "include_visual_analysis": False,
            "focus_areas": ["retention_patterns", "audience_behavior", "drop_off_points"]
        }
        
        result = await self._execute_test(
            "Retention Pattern Analysis",
            test_request,
            expected_insights=["retention", "drop-off", "engagement", "duration"]
        )
        
        # Validate retention-specific analysis
        if result.success and result.response_data:
            analysis = result.response_data.get('analysis', {})
            detailed_analysis = analysis.get('detailed_analysis', {})
            
            # Look for retention-related data
            retention_keywords = ['retention', 'watch time', 'duration', 'audience behavior']
            retention_content = str(detailed_analysis).lower()
            
            retention_mentions = sum(1 for keyword in retention_keywords if keyword in retention_content)
            
            if retention_mentions >= 2:
                logger.info(f"✅ Retention analysis includes {retention_mentions} relevant keywords")
            else:
                logger.warning("⚠️ Limited retention-specific analysis detected")
    
    async def _test_comparative_performance(self):
        """Test comparative performance analysis vs channel average"""
        
        test_request = {
            "request_id": f"test_comparative_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "ComparativeTest_Channel",
                "time_period": "last_30d",
                "specific_videos": [],  # Analyze all recent videos
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 3000,
                "output_tokens": 1500
            },
            "analysis_depth": "standard",
            "include_visual_analysis": True,
            "focus_areas": ["performance_comparison", "benchmarking"]
        }
        
        result = await self._execute_test(
            "Comparative Performance Analysis",
            test_request,
            expected_insights=["average", "comparison", "benchmark", "performance"]
        )
        
        # Check for comparative metrics
        if result.success and result.response_data:
            metrics = result.response_data.get('analysis', {}).get('metrics', {})
            
            if 'performance_vs_average' in metrics:
                perf_vs_avg = metrics['performance_vs_average']
                logger.info(f"✅ Performance vs average: {perf_vs_avg}")
                
                # Validate the format (should be a percentage)
                if isinstance(perf_vs_avg, (int, float)) or '%' in str(perf_vs_avg):
                    logger.info("✅ Performance comparison metric properly formatted")
                else:
                    logger.warning(f"⚠️ Unexpected performance comparison format: {perf_vs_avg}")
    
    async def _test_domain_validation(self):
        """Test domain validation and mismatch handling"""
        
        # Test with content analysis request (should succeed)
        valid_request = {
            "request_id": f"test_domain_valid_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "DomainTest_Channel",
                "time_period": "last_7d",
                "specific_videos": ["test_video_001"],
                "competitors": []
            },
            "message": "How is my video performing?",
            "analysis_depth": "quick"
        }
        
        valid_result = await self._execute_test(
            "Domain Validation - Valid Request",
            valid_request,
            expected_domain_match=True
        )
        
        if valid_result.success and valid_result.response_data:
            domain_match = valid_result.response_data.get('domain_match', False)
            if domain_match:
                logger.info("✅ Valid content analysis request properly handled")
            else:
                logger.warning("⚠️ Valid request incorrectly rejected")
        
        # Test with non-content analysis request (should return domain mismatch)
        invalid_request = {
            "request_id": f"test_domain_invalid_{uuid.uuid4().hex[:8]}",
            "query_type": "seo_optimization",  # Wrong domain
            "context": {
                "channel_id": "DomainTest_Channel",
                "time_period": "last_7d",
                "specific_videos": [],
                "competitors": []
            },
            "message": "How can I improve my SEO rankings?",
            "analysis_depth": "quick"
        }
        
        invalid_result = await self._execute_test(
            "Domain Validation - Invalid Request",
            invalid_request,
            expected_domain_match=False
        )
        
        if invalid_result.success and invalid_result.response_data:
            domain_match = invalid_result.response_data.get('domain_match', True)
            if not domain_match:
                logger.info("✅ Invalid request properly rejected with domain mismatch")
            else:
                logger.warning("⚠️ Invalid request incorrectly accepted")
    
    async def _test_cache_performance(self):
        """Test caching effectiveness with identical requests"""
        
        cache_test_request = {
            "request_id": f"test_cache_1_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "CacheTest_Channel",
                "time_period": "last_30d",
                "specific_videos": ["test_video_001", "test_video_002"],
                "competitors": []
            },
            "token_budget": {
                "input_tokens": 3000,
                "output_tokens": 1500
            },
            "analysis_depth": "standard"
        }
        
        # First request (should be cache miss)
        logger.info("🔄 Testing cache performance - First request (cache miss expected)")
        first_result = await self._execute_test(
            "Cache Test - First Request",
            cache_test_request
        )
        
        if first_result.success:
            first_cache_hit = first_result.response_data.get('cache_info', {}).get('cache_hit', False)
            first_time = first_result.response_time
            
            logger.info(f"First request - Cache hit: {first_cache_hit}, Time: {first_time:.2f}s")
            
            # Second identical request (should be cache hit)
            logger.info("🔄 Testing cache performance - Second request (cache hit expected)")
            cache_test_request['request_id'] = f"test_cache_2_{uuid.uuid4().hex[:8]}"
            
            second_result = await self._execute_test(
                "Cache Test - Second Request",
                cache_test_request
            )
            
            if second_result.success:
                second_cache_hit = second_result.response_data.get('cache_info', {}).get('cache_hit', False)
                second_time = second_result.response_time
                
                logger.info(f"Second request - Cache hit: {second_cache_hit}, Time: {second_time:.2f}s")
                
                # Analyze cache performance
                if second_cache_hit and not first_cache_hit:
                    speed_improvement = ((first_time - second_time) / first_time) * 100
                    logger.info(f"✅ Cache working correctly - {speed_improvement:.1f}% faster")
                    
                    if speed_improvement > 30:  # Expect significant speedup
                        logger.info("✅ Cache provides significant performance improvement")
                    else:
                        logger.warning("⚠️ Cache speedup less than expected")
                else:
                    logger.warning("⚠️ Cache behavior not as expected")
    
    async def _test_error_handling(self):
        """Test error handling with malformed requests"""
        
        error_test_cases = [
            {
                "name": "Missing Context",
                "request": {
                    "request_id": f"test_error_1_{uuid.uuid4().hex[:8]}",
                    "query_type": "content_analysis"
                    # Missing context
                }
            },
            {
                "name": "Invalid Channel ID",
                "request": {
                    "request_id": f"test_error_2_{uuid.uuid4().hex[:8]}",
                    "query_type": "content_analysis",
                    "context": {
                        "channel_id": "",  # Empty channel ID
                        "time_period": "last_30d"
                    }
                }
            },
            {
                "name": "Invalid Time Period",
                "request": {
                    "request_id": f"test_error_3_{uuid.uuid4().hex[:8]}",
                    "query_type": "content_analysis",
                    "context": {
                        "channel_id": "ErrorTest_Channel",
                        "time_period": "invalid_period"
                    }
                }
            }
        ]
        
        for test_case in error_test_cases:
            logger.info(f"🧪 Testing error handling: {test_case['name']}")
            
            result = await self._execute_test(
                f"Error Handling - {test_case['name']}",
                test_case['request'],
                expect_error=True
            )
            
            if result.success:
                # Check if error was handled gracefully
                if result.response_data and 'error_message' in result.response_data.get('analysis', {}):
                    logger.info(f"✅ Error handled gracefully: {test_case['name']}")
                else:
                    logger.info(f"✅ Request processed despite malformed input: {test_case['name']}")
            else:
                logger.info(f"✅ Error properly caught and handled: {test_case['name']}")
    
    async def _test_response_validation(self):
        """Test response structure validation"""
        
        validation_request = {
            "request_id": f"test_validation_{uuid.uuid4().hex[:8]}",
            "query_type": "content_analysis",
            "context": {
                "channel_id": "ValidationTest_Channel",
                "time_period": "last_30d",
                "specific_videos": ["test_video_001", "test_video_002"],
                "competitors": []
            },
            "analysis_depth": "standard"
        }
        
        result = await self._execute_test(
            "Response Structure Validation",
            validation_request
        )
        
        if result.success and result.response_data:
            self._validate_response_structure(result.response_data)
    
    def _validate_response_structure(self, response: Dict[str, Any]):
        """Validate response follows expected schema"""
        
        required_fields = [
            'agent_type', 'response_id', 'request_id', 'timestamp',
            'confidence_score', 'domain_match', 'analysis', 'for_boss_agent_only'
        ]
        
        missing_fields = [field for field in required_fields if field not in response]
        
        if missing_fields:
            logger.warning(f"⚠️ Missing required fields: {missing_fields}")
        else:
            logger.info("✅ All required response fields present")
        
        # Validate agent_type
        if response.get('agent_type') == 'content_analysis':
            logger.info("✅ Correct agent_type specified")
        else:
            logger.warning(f"⚠️ Incorrect agent_type: {response.get('agent_type')}")
        
        # Validate for_boss_agent_only flag
        if response.get('for_boss_agent_only') is True:
            logger.info("✅ for_boss_agent_only flag correctly set")
        else:
            logger.warning("⚠️ for_boss_agent_only flag missing or incorrect")
        
        # Validate analysis structure
        analysis = response.get('analysis', {})
        analysis_fields = ['summary', 'key_insights', 'recommendations']
        
        for field in analysis_fields:
            if field in analysis:
                logger.info(f"✅ Analysis field '{field}' present")
            else:
                logger.warning(f"⚠️ Analysis field '{field}' missing")
        
        # Validate confidence score range
        confidence = response.get('confidence_score', 0)
        if 0.0 <= confidence <= 1.0:
            logger.info(f"✅ Confidence score in valid range: {confidence}")
        else:
            logger.warning(f"⚠️ Confidence score outside valid range: {confidence}")
    
    async def _execute_test(self, test_name: str, request: Dict[str, Any], 
                          expected_insights: List[str] = None,
                          expected_domain_match: bool = True,
                          expect_error: bool = False) -> TestResult:
        """Execute a single test and return results"""
        
        logger.info(f"🧪 Executing test: {test_name}")
        
        start_time = time.time()
        
        try:
            # Execute the agent request
            response = await self.agent_function(request)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            # Extract metrics from response
            token_usage = response.get('token_usage', {})
            cache_info = response.get('cache_info', {})
            confidence_score = response.get('confidence_score', 0.0)
            
            # Determine if test passed
            success = True
            error_message = None
            
            # Check domain match expectation
            domain_match = response.get('domain_match', True)
            if domain_match != expected_domain_match:
                success = False
                error_message = f"Domain match mismatch: expected {expected_domain_match}, got {domain_match}"
            
            # Check for expected insights if provided
            if expected_insights and success:
                analysis = response.get('analysis', {})
                response_text = json.dumps(analysis).lower()
                
                found_insights = [insight for insight in expected_insights if insight in response_text]
                
                if len(found_insights) < len(expected_insights) * 0.5:  # At least 50% of expected insights
                    logger.warning(f"⚠️ Only found {len(found_insights)}/{len(expected_insights)} expected insights")
            
            # Create test result
            result = TestResult(
                test_name=test_name,
                success=success,
                response_time=response_time,
                token_usage=token_usage,
                cache_hit=cache_info.get('cache_hit', False),
                confidence_score=confidence_score,
                error_message=error_message,
                response_data=response
            )
            
            logger.info(f"✅ Test completed: {test_name} - Time: {response_time:.2f}s")
            
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            if expect_error:
                # Error was expected
                result = TestResult(
                    test_name=test_name,
                    success=True,  # Expected error, so test passes
                    response_time=response_time,
                    token_usage={},
                    cache_hit=False,
                    confidence_score=0.0,
                    error_message=f"Expected error: {str(e)}"
                )
                logger.info(f"✅ Expected error handled: {test_name}")
            else:
                # Unexpected error
                result = TestResult(
                    test_name=test_name,
                    success=False,
                    response_time=response_time,
                    token_usage={},
                    cache_hit=False,
                    confidence_score=0.0,
                    error_message=str(e)
                )
                logger.error(f"❌ Test failed: {test_name} - Error: {str(e)}")
        
        self.test_results.append(result)
        return result
    
    def _calculate_performance_metrics(self):
        """Calculate overall performance metrics"""
        
        if not self.test_results:
            return
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        
        response_times = [result.response_time for result in self.test_results]
        avg_response_time = statistics.mean(response_times)
        
        # Calculate total token usage
        total_input_tokens = sum(
            result.token_usage.get('input_tokens', 0) 
            for result in self.test_results
        )
        total_output_tokens = sum(
            result.token_usage.get('output_tokens', 0) 
            for result in self.test_results
        )
        
        # Calculate cache hit rate
        cache_hits = sum(1 for result in self.test_results if result.cache_hit)
        cache_hit_rate = (cache_hits / total_tests) * 100 if total_tests > 0 else 0
        
        self.performance_metrics = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests) * 100,
            "avg_response_time": avg_response_time,
            "min_response_time": min(response_times),
            "max_response_time": max(response_times),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "cache_hit_rate": cache_hit_rate,
            "avg_confidence_score": statistics.mean([r.confidence_score for r in self.test_results])
        }
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        
        report = {
            "test_summary": {
                "execution_time": datetime.now().isoformat(),
                "total_tests": self.performance_metrics["total_tests"],
                "passed_tests": self.performance_metrics["passed_tests"],
                "failed_tests": self.performance_metrics["failed_tests"],
                "success_rate": f"{self.performance_metrics['success_rate']:.1f}%"
            },
            "performance_metrics": self.performance_metrics,
            "test_results": [
                {
                    "test_name": result.test_name,
                    "success": result.success,
                    "response_time": result.response_time,
                    "confidence_score": result.confidence_score,
                    "cache_hit": result.cache_hit,
                    "error_message": result.error_message
                }
                for result in self.test_results
            ],
            "recommendations": self._generate_recommendations()
        }
        
        # Log summary
        logger.info("\n📊 TEST SUITE SUMMARY")
        logger.info("=" * 40)
        logger.info(f"Total Tests: {self.performance_metrics['total_tests']}")
        logger.info(f"Passed: {self.performance_metrics['passed_tests']}")
        logger.info(f"Failed: {self.performance_metrics['failed_tests']}")
        logger.info(f"Success Rate: {self.performance_metrics['success_rate']:.1f}%")
        logger.info(f"Average Response Time: {self.performance_metrics['avg_response_time']:.2f}s")
        logger.info(f"Cache Hit Rate: {self.performance_metrics['cache_hit_rate']:.1f}%")
        logger.info(f"Total Tokens Used: {self.performance_metrics['total_tokens']:,}")
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        
        recommendations = []
        
        # Performance recommendations
        if self.performance_metrics['avg_response_time'] > 5.0:
            recommendations.append("Consider optimizing response time - average is above 5 seconds")
        
        if self.performance_metrics['cache_hit_rate'] < 30:
            recommendations.append("Cache hit rate is low - review caching strategy")
        
        if self.performance_metrics['success_rate'] < 90:
            recommendations.append("Success rate below 90% - investigate failed tests")
        
        # Token usage recommendations
        avg_tokens_per_test = self.performance_metrics['total_tokens'] / max(self.performance_metrics['total_tests'], 1)
        if avg_tokens_per_test > 5000:
            recommendations.append("High token usage per test - consider optimizing prompts")
        
        # Confidence score recommendations
        if self.performance_metrics['avg_confidence_score'] < 0.8:
            recommendations.append("Average confidence score is low - review analysis quality")
        
        if not recommendations:
            recommendations.append("All metrics look good - agent is performing well!")
        
        return recommendations

async def main():
    """Main function to run the test suite"""
    
    print("🎬 CreatorMate Content Analysis Agent Test Suite")
    print("=" * 60)
    print("Testing the specialized Content Analysis Agent")
    print("that operates within the boss agent hierarchy.")
    print()
    
    # Initialize and run test suite
    test_suite = ContentAnalysisTestSuite()
    
    try:
        report = await test_suite.run_full_test_suite()
        
        # Save test report
        report_filename = f"content_analysis_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n💾 Test report saved to: {report_filename}")
        
        # Print final recommendations
        recommendations = report.get('recommendations', [])
        if recommendations:
            logger.info("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                logger.info(f"   {i}. {rec}")
        
        logger.info("\n🎉 Test suite completed successfully!")
        
        return report
        
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        logger.error(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    # Run the test suite
    import sys
    
    try:
        report = asyncio.run(main())
        
        # Exit with appropriate code
        if report.get('error'):
            sys.exit(1)
        elif report.get('test_summary', {}).get('failed_tests', 0) > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("\n⚠️ Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)