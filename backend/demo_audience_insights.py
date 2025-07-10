"""
Demo script for CreatorMate Audience Insights Agent
Tests the specialized agent's functionality and integration with boss agent
"""

import asyncio
import os
import json
from datetime import datetime
from audience_insights_agent import get_audience_insights_agent, process_audience_insights_request

# Sample audience insights requests
DEMO_REQUESTS = [
    {
        "request_id": "audience_demo_001",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "TechEducator",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 4000,
            "output_tokens": 2000
        },
        "analysis_depth": "standard",
        "include_sentiment_analysis": True,
        "include_demographics": True,
        "include_behavior_analysis": True,
        "description": "Comprehensive audience analysis"
    },
    {
        "request_id": "audience_demo_002",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "CreativeChannel",
            "time_period": "last_7d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 3000,
            "output_tokens": 1500
        },
        "analysis_depth": "quick",
        "include_sentiment_analysis": True,
        "include_demographics": False,
        "include_behavior_analysis": True,
        "description": "Quick sentiment and behavior analysis"
    },
    {
        "request_id": "audience_demo_003",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "GamingChannel",
            "time_period": "last_90d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 5000,
            "output_tokens": 3000
        },
        "analysis_depth": "deep",
        "include_sentiment_analysis": True,
        "include_demographics": True,
        "include_behavior_analysis": True,
        "description": "Deep audience insights with full analysis"
    },
    {
        "request_id": "audience_demo_004",
        "query_type": "content_analysis",  # Wrong domain to test domain mismatch
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
        "description": "Content analysis request (should trigger domain mismatch)"
    }
]

async def demo_direct_agent_calls():
    """Test direct calls to the Audience Insights Agent"""
    
    print("👥 Audience Insights Agent - Direct Testing")
    print("=" * 50)
    
    agent = get_audience_insights_agent()
    
    for i, request in enumerate(DEMO_REQUESTS, 1):
        print(f"\nTest {i}: {request['description']}")
        print(f"📋 Request ID: {request['request_id']}")
        print(f"🎯 Query Type: {request['query_type']}")
        print(f"📺 Channel: {request['context']['channel_id']}")
        print(f"⏱️ Time Period: {request['context']['time_period']}")
        print(f"🔍 Analysis Depth: {request.get('analysis_depth', 'standard')}")
        
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
                
                # Display audience scores
                metrics = analysis.get('metrics', {})
                if metrics:
                    print(f"📈 Audience Health Scores:")
                    for key, value in metrics.items():
                        print(f"   {key.replace('_', ' ').title()}: {value}")
                
                # Display key insights
                insights = analysis.get('key_insights', [])
                if insights:
                    print(f"💡 Key Audience Insights ({len(insights)}):")
                    for j, insight in enumerate(insights[:3], 1):
                        print(f"   {j}. {insight.get('insight', 'No insight')[:80]}...")
                
                # Display recommendations
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    print(f"🚀 Audience Recommendations ({len(recommendations)}):")
                    for j, rec in enumerate(recommendations[:3], 1):
                        print(f"   {j}. {rec.get('recommendation', 'No recommendation')[:80]}...")
                
                # Display detailed analysis highlights
                detailed = analysis.get('detailed_analysis', {})
                if detailed:
                    print(f"🔍 Analysis Details:")
                    
                    # Demographics
                    demographics = detailed.get('demographics', {})
                    if demographics:
                        print(f"   👥 Demographics: {demographics.get('subscriber_count', 0):,} subscribers")
                        if 'age_groups' in demographics:
                            top_age = max(demographics['age_groups'].items(), key=lambda x: x[1])
                            print(f"   🎂 Top Age Group: {top_age[0]} ({top_age[1]}%)")
                    
                    # Behavior patterns
                    behavior = detailed.get('behavior_patterns', {})
                    if behavior:
                        peak_times = behavior.get('peak_activity_times', [])
                        if peak_times:
                            print(f"   ⏰ Peak Activity: {len(peak_times)} optimal time slots identified")
                    
                    # Sentiment
                    sentiment = detailed.get('sentiment_analysis', {})
                    if sentiment and sentiment.get('sentiment_breakdown'):
                        breakdown = sentiment['sentiment_breakdown']
                        print(f"   😊 Sentiment: {breakdown.get('positive', 0):.1f}% positive, "
                              f"{breakdown.get('negative', 0):.1f}% negative")
                
                # Cache information
                cache_info = response.get('cache_info', {})
                if cache_info:
                    print(f"💾 Cache: {'Hit' if cache_info.get('cache_hit') else 'Miss'}")
                    print(f"⏳ TTL Remaining: {cache_info.get('ttl_remaining', 0)}s")
            else:
                print(f"❌ Domain mismatch - request outside audience insights scope")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

async def demo_boss_agent_integration():
    """Test integration with boss agent through the helper function"""
    
    print("\n🧠 Audience Insights Agent - Boss Agent Integration")
    print("=" * 60)
    
    # Simulate boss agent request
    boss_request = {
        "request_id": "boss_audience_001",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "CreatorMate_Audience_Demo",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "token_budget": {
            "input_tokens": 4000,
            "output_tokens": 2000
        },
        "analysis_depth": "standard",
        "include_sentiment_analysis": True,
        "include_demographics": True,
        "include_behavior_analysis": True
    }
    
    print(f"📋 Boss Agent Request:")
    print(f"   Request ID: {boss_request['request_id']}")
    print(f"   Query Type: {boss_request['query_type']}")
    print(f"   Channel: {boss_request['context']['channel_id']}")
    print(f"   Analysis Depth: {boss_request['analysis_depth']}")
    print(f"   Include Sentiment: {boss_request['include_sentiment_analysis']}")
    print(f"   Include Demographics: {boss_request['include_demographics']}")
    print()
    
    try:
        start_time = asyncio.get_event_loop().time()
        response = await process_audience_insights_request(boss_request)
        end_time = asyncio.get_event_loop().time()
        
        processing_time = end_time - start_time
        
        print(f"✅ Boss Agent Integration Successful!")
        print(f"⏱️ Processing Time: {processing_time:.2f}s")
        print(f"🎯 Confidence Score: {response.get('confidence_score', 0):.2f}")
        print(f"🔍 For Boss Agent Only: {response.get('for_boss_agent_only', False)}")
        
        # Display structured response
        analysis = response.get('analysis', {})
        if analysis:
            print(f"\n📊 Audience Analysis Summary:")
            print(f"   {analysis.get('summary', 'No summary available')}")
            
            # Display audience health metrics
            metrics = analysis.get('metrics', {})
            if metrics:
                print(f"\n📈 Audience Health Dashboard:")
                overall_health = metrics.get('overall_audience_health', 0)
                print(f"   Overall Health Score: {overall_health}/10")
                print(f"   Engagement Score: {metrics.get('engagement_score', 0)}/10")
                print(f"   Retention Score: {metrics.get('retention_score', 0)}/10")
                print(f"   Sentiment Score: {metrics.get('sentiment_score', 0)}/10")
                print(f"   Diversity Score: {metrics.get('diversity_score', 0)}/10")
            
            # Display top insights
            insights = analysis.get('key_insights', [])
            if insights:
                print(f"\n💡 Top Audience Insights:")
                for i, insight in enumerate(insights[:3], 1):
                    print(f"   {i}. {insight.get('insight', 'No insight')}")
                    print(f"      Evidence: {insight.get('evidence', 'No evidence')}")
                    print(f"      Impact: {insight.get('impact', 'Unknown')}")
            
            # Display recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                print(f"\n🚀 Audience Growth Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec.get('recommendation', 'No recommendation')}")
                    print(f"      Expected Impact: {rec.get('expected_impact', 'Unknown')}")
        
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
    
    print("\n💾 Audience Insights Agent - Caching Demo")
    print("=" * 45)
    
    # Same request twice to test caching
    cache_test_request = {
        "request_id": "cache_audience_001",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "CacheTestAudienceChannel",
            "time_period": "last_30d",
            "specific_videos": [],
            "competitors": []
        },
        "analysis_depth": "standard",
        "include_sentiment_analysis": True,
        "include_demographics": True,
        "include_behavior_analysis": True
    }
    
    print("🔄 Testing cache behavior with identical requests...")
    
    # First request (should be cache miss)
    print("\n1️⃣ First Request (expected cache miss):")
    start_time_1 = asyncio.get_event_loop().time()
    response_1 = await process_audience_insights_request(cache_test_request)
    end_time_1 = asyncio.get_event_loop().time()
    time_1 = end_time_1 - start_time_1
    
    cache_info_1 = response_1.get('cache_info', {})
    print(f"   ⏱️ Processing Time: {time_1:.2f}s")
    print(f"   💾 Cache Hit: {cache_info_1.get('cache_hit', False)}")
    print(f"   🔑 Cache Key: {cache_info_1.get('cache_key', 'unknown')}")
    
    # Second request (should be cache hit)
    print("\n2️⃣ Second Request (expected cache hit):")
    cache_test_request['request_id'] = "cache_audience_002"  # Different request ID
    
    start_time_2 = asyncio.get_event_loop().time()
    response_2 = await process_audience_insights_request(cache_test_request)
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

async def demo_sentiment_analysis():
    """Demonstrate sentiment analysis capabilities"""
    
    print("\n😊 Audience Insights Agent - Sentiment Analysis Demo")
    print("=" * 55)
    
    sentiment_request = {
        "request_id": "sentiment_demo_001",
        "query_type": "audience_insights",
        "context": {
            "channel_id": "SentimentTestChannel",
            "time_period": "last_7d",
            "specific_videos": [],
            "competitors": []
        },
        "analysis_depth": "deep",
        "include_sentiment_analysis": True,
        "include_demographics": False,
        "include_behavior_analysis": False
    }
    
    print("🔍 Testing sentiment analysis with focus on comment insights...")
    
    try:
        response = await process_audience_insights_request(sentiment_request)
        
        analysis = response.get('analysis', {})
        detailed = analysis.get('detailed_analysis', {})
        sentiment_data = detailed.get('sentiment_analysis', {})
        
        if sentiment_data:
            print(f"\n📊 Sentiment Analysis Results:")
            
            # Sentiment breakdown
            if sentiment_data.get('sentiment_breakdown'):
                breakdown = sentiment_data['sentiment_breakdown']
                print(f"   Positive: {breakdown.get('positive', 0):.1f}%")
                print(f"   Neutral: {breakdown.get('neutral', 0):.1f}%")
                print(f"   Negative: {breakdown.get('negative', 0):.1f}%")
            
            # Key topics
            if sentiment_data.get('key_topics'):
                print(f"\n🏷️ Key Discussion Topics:")
                for topic in sentiment_data['key_topics'][:5]:
                    print(f"   • {topic.get('topic', 'Unknown')}: "
                          f"{topic.get('frequency', 0)} mentions "
                          f"({topic.get('sentiment', 'neutral')} sentiment)")
            
            # Audience insights
            if sentiment_data.get('audience_insights'):
                insights = sentiment_data['audience_insights']
                print(f"\n👥 Audience Community Insights:")
                print(f"   Engagement Level: {insights.get('engagement_level', 'unknown')}")
                print(f"   Expertise Level: {insights.get('expertise_level', 'unknown')}")
                print(f"   Community Health: {insights.get('community_health', 'unknown')}")
            
            # Engagement opportunities
            if sentiment_data.get('engagement_opportunities'):
                print(f"\n🚀 Community Engagement Opportunities:")
                for i, opportunity in enumerate(sentiment_data['engagement_opportunities'][:3], 1):
                    print(f"   {i}. {opportunity}")
        else:
            print("   No sentiment data available in response")
    
    except Exception as e:
        print(f"❌ Sentiment analysis demo failed: {e}")

async def demo_error_handling():
    """Test error handling and edge cases"""
    
    print("\n🛡️ Audience Insights Agent - Error Handling")
    print("=" * 50)
    
    # Test with invalid/malformed request
    invalid_requests = [
        {
            "description": "Missing required fields",
            "request": {
                "request_id": "error_audience_001"
                # Missing context and other required fields
            }
        },
        {
            "description": "Empty context",
            "request": {
                "request_id": "error_audience_002",
                "query_type": "audience_insights",
                "context": {}
            }
        },
        {
            "description": "Invalid analysis depth",
            "request": {
                "request_id": "error_audience_003",
                "query_type": "audience_insights",
                "context": {
                    "channel_id": "ErrorTestChannel",
                    "time_period": "last_30d"
                },
                "analysis_depth": "invalid_depth"
            }
        }
    ]
    
    for test in invalid_requests:
        print(f"\n🧪 Test: {test['description']}")
        
        try:
            response = await process_audience_insights_request(test['request'])
            
            if 'error_message' in response.get('analysis', {}):
                print(f"   ✅ Error handled gracefully")
                print(f"   📝 Error: {response['analysis']['error_message']}")
            else:
                print(f"   ✅ Request processed despite invalid input")
                print(f"   📊 Summary: {response.get('analysis', {}).get('summary', 'No summary')}")
        
        except Exception as e:
            print(f"   ⚠️ Exception caught: {e}")

def print_agent_capabilities():
    """Display Audience Insights Agent capabilities"""
    
    print("\n👥 Audience Insights Agent Capabilities")
    print("=" * 45)
    print("📋 Agent Role:")
    print("   - Specialized sub-agent within boss agent hierarchy")
    print("   - Handles audience_insights query types exclusively")
    print("   - Reports only to boss agent, never directly to users")
    print()
    print("🔍 Analysis Features:")
    print("   - Demographic analysis (age, gender, geography, devices)")
    print("   - Audience behavior patterns and peak activity times")
    print("   - Comment sentiment analysis and topic extraction")
    print("   - Subscriber vs. non-subscriber behavior analysis")
    print("   - Traffic source and discovery pattern analysis")
    print("   - Community engagement and health assessment")
    print()
    print("🤖 AI Capabilities:")
    print("   - Claude 3.5 Sonnet for sentiment analysis")
    print("   - Comment topic extraction and categorization")
    print("   - Audience insight generation and correlation")
    print("   - Personalized engagement strategy recommendations")
    print()
    print("🚀 Technical Features:")
    print("   - YouTube Data API and Analytics API integration")
    print("   - Intelligent caching with audience-specific TTLs")
    print("   - Domain-specific request validation")
    print("   - Progressive analysis depth (quick/standard/deep)")
    print("   - Structured JSON response format")
    print()
    print("🔧 Integration Points:")
    print("   - process_audience_insights_request() - Boss agent interface")
    print("   - get_audience_insights_agent() - Agent instance factory")
    print("   - Hierarchical agent communication protocol")

async def main():
    """Run all Audience Insights Agent demos"""
    
    print("👥 CreatorMate Audience Insights Agent Demo")
    print("=" * 60)
    print("This demo tests the specialized Audience Insights Agent")
    print("that operates as a sub-agent within the boss agent hierarchy.")
    print()
    
    # Check environment variables
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not youtube_key and not openai_key:
        print("⚠️ Note: API keys not set - running in demo mode")
        print("Set YOUTUBE_API_KEY and OPENAI_API_KEY for full functionality")
    print()
    
    # Display capabilities
    print_agent_capabilities()
    
    # Run demo tests
    await demo_direct_agent_calls()
    await demo_boss_agent_integration()
    await demo_caching_behavior()
    await demo_sentiment_analysis()
    await demo_error_handling()
    
    print("\n🎉 Audience Insights Agent Demo Complete!")
    print()
    print("🔗 Integration Summary:")
    print("   ✅ Hierarchical agent architecture implemented")
    print("   ✅ Domain-specific audience analysis handling")
    print("   ✅ Boss agent communication protocol")
    print("   ✅ Intelligent caching system")
    print("   ✅ Sentiment analysis with Claude 3.5 Sonnet")
    print("   ✅ Demographic and behavior analysis")
    print("   ✅ Error handling and graceful degradation")
    print("   ✅ Multi-dimensional audience insights")
    print()
    print("🚀 Next Steps:")
    print("   1. Set API keys for production use")
    print("   2. Integrate with YouTube Analytics API for real demographics")
    print("   3. Add advanced sentiment analysis features")
    print("   4. Implement audience segmentation and personalization")

if __name__ == "__main__":
    asyncio.run(main())