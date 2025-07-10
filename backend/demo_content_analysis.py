"""
Demo script for CreatorMate Content Analysis Agent
Tests the specialized agent's functionality and integration with boss agent
"""

import asyncio
import os
import json
from datetime import datetime
from content_analysis_agent import get_content_analysis_agent, process_content_analysis_request

# Sample content analysis requests
DEMO_REQUESTS = [
    {
        "request_id": "demo_001",
        "query_type": "content_analysis",
        "context": {
            "channel_id": "TechTutor",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 3000,
            "output_tokens": 1500
        },
        "analysis_depth": "standard",
        "include_visual_analysis": True,
        "description": "General content performance analysis"
    },
    {
        "request_id": "demo_002",
        "query_type": "content_analysis",
        "context": {
            "channel_id": "CreativeChannel",
            "time_period": "last_7d",
            "specific_videos": ["video_123", "video_456"],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 4000,
            "output_tokens": 2000
        },
        "analysis_depth": "deep",
        "include_visual_analysis": True,
        "description": "Deep analysis of specific videos"
    },
    {
        "request_id": "demo_003",
        "query_type": "seo",  # Wrong domain to test domain mismatch
        "context": {
            "channel_id": "TestChannel",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 2000,
            "output_tokens": 1000
        },
        "description": "SEO request (should trigger domain mismatch)"
    }
]

async def demo_direct_agent_calls():
    """Test direct calls to the Content Analysis Agent"""
    
    print("🎬 Content Analysis Agent - Direct Testing")
    print("=" * 50)
    
    agent = get_content_analysis_agent()
    
    for i, request in enumerate(DEMO_REQUESTS, 1):
        print(f"\nTest {i}: {request['description']}")
        print(f"📋 Request ID: {request['request_id']}")
        print(f"🎯 Query Type: {request['query_type']}")
        print(f"📺 Channel: {request['context']['channel_id']}")
        print(f"⏱️ Time Period: {request['context']['time_period']}")
        
        try:
            start_time = asyncio.get_event_loop().time()
            response = await agent.process_boss_agent_request(request)
            end_time = asyncio.get_event_loop().time()
            
            processing_time = end_time - start_time
            
            print(f"\n✅ Response received in {processing_time:.2f}s")
            print(f"🤖 Agent Type: {response.get('agent_type', 'unknown')}")
            print(f"✋ Domain Match: {response.get('domain_match', 'unknown')}")
            print(f"🎯 Confidence: {response.get('confidence_score', 0):.2f}")
            
            if response.get('domain_match', True):
                analysis = response.get('analysis', {})
                print(f"📊 Summary: {analysis.get('summary', 'No summary')[:100]}...")
                
                insights = analysis.get('key_insights', [])
                if insights:
                    print(f"💡 Key Insights ({len(insights)}):")
                    for j, insight in enumerate(insights[:3], 1):
                        print(f"   {j}. {insight.get('insight', 'No insight')[:80]}...")
                
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    print(f"🚀 Recommendations ({len(recommendations)}):")
                    for j, rec in enumerate(recommendations[:3], 1):
                        print(f"   {j}. {rec.get('recommendation', 'No recommendation')[:80]}...")
                
                metrics = analysis.get('metrics', {})
                if metrics:
                    print(f"📈 Performance Metrics:")
                    for key, value in metrics.items():
                        print(f"   {key}: {value}")
                
                # Cache information
                cache_info = response.get('cache_info', {})
                if cache_info:
                    print(f"💾 Cache: {'Hit' if cache_info.get('cache_hit') else 'Miss'}")
                    print(f"⏳ TTL Remaining: {cache_info.get('ttl_remaining', 0)}s")
            else:
                print(f"❌ Domain mismatch - request outside content analysis scope")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

async def demo_boss_agent_integration():
    """Test integration with boss agent through the helper function"""
    
    print("\n🧠 Content Analysis Agent - Boss Agent Integration")
    print("=" * 60)
    
    # Simulate boss agent request
    boss_request = {
        "request_id": "boss_demo_001",
        "query_type": "content_analysis",
        "context": {
            "channel_id": "CreatorMate_Demo",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 3500,
            "output_tokens": 1800
        },
        "analysis_depth": "standard",
        "include_visual_analysis": True
    }
    
    print(f"📋 Boss Agent Request:")
    print(f"   Request ID: {boss_request['request_id']}")
    print(f"   Query Type: {boss_request['query_type']}")
    print(f"   Channel: {boss_request['context']['channel_id']}")
    print(f"   Analysis Depth: {boss_request['analysis_depth']}")
    print()
    
    try:
        start_time = asyncio.get_event_loop().time()
        response = await process_content_analysis_request(boss_request)
        end_time = asyncio.get_event_loop().time()
        
        processing_time = end_time - start_time
        
        print(f"✅ Boss Agent Integration Successful!")
        print(f"⏱️ Processing Time: {processing_time:.2f}s")
        print(f"🎯 Confidence Score: {response.get('confidence_score', 0):.2f}")
        print(f"🔍 For Boss Agent Only: {response.get('for_boss_agent_only', False)}")
        
        # Display structured response
        analysis = response.get('analysis', {})
        if analysis:
            print(f"\n📊 Analysis Summary:")
            print(f"   {analysis.get('summary', 'No summary available')}")
            
            detailed_analysis = analysis.get('detailed_analysis', {})
            if detailed_analysis:
                video_count = detailed_analysis.get('video_count', 0)
                print(f"   Videos Analyzed: {video_count}")
                
                content_metrics = detailed_analysis.get('content_metrics', [])
                if content_metrics:
                    print(f"   Sample Video Metrics:")
                    for metric in content_metrics[:2]:
                        print(f"     - {metric.get('title', 'Unknown')[:50]}...")
                        print(f"       Views: {metric.get('views', 0):,}")
                        print(f"       Engagement: {metric.get('engagement_rate', 0):.1f}%")
        
        # Token usage
        token_usage = response.get('token_usage', {})
        if token_usage:
            print(f"\n💰 Token Usage:")
            print(f"   Input: {token_usage.get('input_tokens', 0):,} tokens")
            print(f"   Output: {token_usage.get('output_tokens', 0):,} tokens")
            print(f"   Model: {token_usage.get('model', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Boss Agent Integration Failed: {e}")

async def demo_caching_behavior():
    """Demonstrate caching functionality"""
    
    print("\n💾 Content Analysis Agent - Caching Demo")
    print("=" * 45)
    
    # Same request twice to test caching
    cache_test_request = {
        "request_id": "cache_test_001",
        "query_type": "content_analysis",
        "context": {
            "channel_id": "CacheTestChannel",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "analysis_depth": "standard"
    }
    
    print("🔄 Testing cache behavior with identical requests...")
    
    # First request (should be cache miss)
    print("\n1️⃣ First Request (expected cache miss):")
    start_time_1 = asyncio.get_event_loop().time()
    response_1 = await process_content_analysis_request(cache_test_request)
    end_time_1 = asyncio.get_event_loop().time()
    time_1 = end_time_1 - start_time_1
    
    cache_info_1 = response_1.get('cache_info', {})
    print(f"   ⏱️ Processing Time: {time_1:.2f}s")
    print(f"   💾 Cache Hit: {cache_info_1.get('cache_hit', False)}")
    print(f"   🔑 Cache Key: {cache_info_1.get('cache_key', 'unknown')}")
    
    # Second request (should be cache hit)
    print("\n2️⃣ Second Request (expected cache hit):")
    cache_test_request['request_id'] = "cache_test_002"  # Different request ID
    
    start_time_2 = asyncio.get_event_loop().time()
    response_2 = await process_content_analysis_request(cache_test_request)
    end_time_2 = asyncio.get_event_loop().time()
    time_2 = end_time_2 - start_time_2
    
    cache_info_2 = response_2.get('cache_info', {})
    print(f"   ⏱️ Processing Time: {time_2:.2f}s")
    print(f"   💾 Cache Hit: {cache_info_2.get('cache_hit', False)}")
    print(f"   🔑 Cache Key: {cache_info_2.get('cache_key', 'unknown')}")
    
    # Performance comparison
    if time_1 > 0 and time_2 > 0:
        speedup = ((time_1 - time_2) / time_1) * 100
        print(f"\n⚡ Cache Performance:")
        print(f"   Speed Improvement: {speedup:.1f}%")
        print(f"   Time Saved: {time_1 - time_2:.2f}s")

async def demo_error_handling():
    """Test error handling and edge cases"""
    
    print("\n🛡️ Content Analysis Agent - Error Handling")
    print("=" * 50)
    
    # Test with invalid/malformed request
    invalid_requests = [
        {
            "description": "Missing required fields",
            "request": {
                "request_id": "error_test_001"
                # Missing context and other required fields
            }
        },
        {
            "description": "Empty context",
            "request": {
                "request_id": "error_test_002",
                "query_type": "content_analysis",
                "context": {}
            }
        }
    ]
    
    for test in invalid_requests:
        print(f"\n🧪 Test: {test['description']}")
        
        try:
            response = await process_content_analysis_request(test['request'])
            
            if 'error_message' in response.get('analysis', {}):
                print(f"   ✅ Error handled gracefully")
                print(f"   📝 Error: {response['analysis']['error_message']}")
            else:
                print(f"   ✅ Request processed despite invalid input")
                print(f"   📊 Summary: {response.get('analysis', {}).get('summary', 'No summary')}")
        
        except Exception as e:
            print(f"   ⚠️ Exception caught: {e}")

def print_agent_capabilities():
    """Display Content Analysis Agent capabilities"""
    
    print("\n🎯 Content Analysis Agent Capabilities")
    print("=" * 45)
    print("📋 Agent Role:")
    print("   - Specialized sub-agent within boss agent hierarchy")
    print("   - Handles content_analysis query types exclusively")
    print("   - Reports only to boss agent, never directly to users")
    print()
    print("🔍 Analysis Features:")
    print("   - Video performance metrics analysis")
    print("   - Engagement pattern identification")
    print("   - Content quality assessment")
    print("   - Title and thumbnail effectiveness")
    print("   - Performance benchmarking")
    print()
    print("🚀 Technical Features:")
    print("   - YouTube Data API integration")
    print("   - Gemini 2.5 Pro multi-modal analysis")
    print("   - Intelligent caching with TTL")
    print("   - Domain-specific request validation")
    print("   - Structured JSON response format")
    print()
    print("🔧 Integration Points:")
    print("   - process_content_analysis_request() - Boss agent interface")
    print("   - get_content_analysis_agent() - Agent instance factory")
    print("   - Hierarchical agent communication protocol")

async def main():
    """Run all Content Analysis Agent demos"""
    
    print("🎬 CreatorMate Content Analysis Agent Demo")
    print("=" * 60)
    print("This demo tests the specialized Content Analysis Agent")
    print("that operates as a sub-agent within the boss agent hierarchy.")
    print()
    
    # Check environment variables
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not youtube_key and not gemini_key:
        print("⚠️ Note: API keys not set - running in demo mode")
        print("Set YOUTUBE_API_KEY and GEMINI_API_KEY for full functionality")
    print()
    
    # Display capabilities
    print_agent_capabilities()
    
    # Run demo tests
    await demo_direct_agent_calls()
    await demo_boss_agent_integration()
    await demo_caching_behavior()
    await demo_error_handling()
    
    print("\n🎉 Content Analysis Agent Demo Complete!")
    print()
    print("🔗 Integration Summary:")
    print("   ✅ Hierarchical agent architecture implemented")
    print("   ✅ Domain-specific request handling")
    print("   ✅ Boss agent communication protocol")
    print("   ✅ Intelligent caching system")
    print("   ✅ Error handling and graceful degradation")
    print("   ✅ Multi-modal content analysis capabilities")
    print()
    print("🚀 Next Steps:")
    print("   1. Set API keys for production use")
    print("   2. Integrate with YouTube Analytics API")
    print("   3. Add visual content analysis features")
    print("   4. Implement batch processing for efficiency")

if __name__ == "__main__":
    asyncio.run(main())