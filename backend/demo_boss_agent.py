"""
Demo script for CreatorMate Boss Agent System
Shows how the orchestration system works with different query types
"""

import asyncio
import os
from boss_agent import process_user_message
from agent_cache import get_agent_cache

# Sample user context for demonstration
SAMPLE_USER_CONTEXT = {
    "channel_info": {
        "name": "TechTutor",
        "niche": "Educational Technology",
        "subscriber_count": 25000,
        "avg_view_count": 8500,
        "content_type": "Tutorial",
        "ctr": 4.2,
        "retention": 65,
        "upload_frequency": "3 times per week",
        "video_length": "10-15 minutes",
        "monetization_status": "Enabled",
        "primary_goal": "Reach 100K subscribers",
        "notes": "Focus on beginner-friendly content"
    },
    "conversation_history": []
}

# Sample queries to demonstrate different agent types
DEMO_QUERIES = [
    {
        "message": "How are my recent videos performing? I want to understand what's working and what isn't.",
        "expected_intent": "content_analysis",
        "description": "Content performance analysis query"
    },
    {
        "message": "Who is my audience and when are they most active? I need insights about my viewers.",
        "expected_intent": "audience",
        "description": "Audience insights query"
    },
    {
        "message": "My videos aren't showing up in search. How can I optimize for better discoverability?",
        "expected_intent": "seo",
        "description": "SEO optimization query"
    },
    {
        "message": "How do I compare against other tech education channels? What are my competitors doing?",
        "expected_intent": "competition",
        "description": "Competitive analysis query"
    },
    {
        "message": "I want to increase my revenue. What monetization opportunities am I missing?",
        "expected_intent": "monetization",
        "description": "Monetization optimization query"
    },
    {
        "message": "Hello! What can you help me with today?",
        "expected_intent": "general",
        "description": "General greeting query"
    }
]

async def demo_boss_agent():
    """Demonstrate the boss agent system with various query types"""
    
    print("🤖 CreatorMate Boss Agent System Demo")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key to run the demo")
        return
    
    print(f"📊 Demo Channel: {SAMPLE_USER_CONTEXT['channel_info']['name']}")
    print(f"🎯 Niche: {SAMPLE_USER_CONTEXT['channel_info']['niche']}")
    print(f"👥 Subscribers: {SAMPLE_USER_CONTEXT['channel_info']['subscriber_count']:,}")
    print(f"📈 Goal: {SAMPLE_USER_CONTEXT['channel_info']['primary_goal']}")
    print()
    
    cache = get_agent_cache()
    
    for i, query in enumerate(DEMO_QUERIES, 1):
        print(f"Query {i}: {query['description']}")
        print(f"💬 User: \"{query['message']}\"")
        print(f"🎯 Expected Intent: {query['expected_intent']}")
        print()
        
        try:
            # Process the query through boss agent
            start_time = asyncio.get_event_loop().time()
            response = await process_user_message(query["message"], SAMPLE_USER_CONTEXT)
            end_time = asyncio.get_event_loop().time()
            
            processing_time = end_time - start_time
            
            if response.get("success", False):
                print(f"✅ Success! Intent: {response.get('intent', 'unknown')}")
                print(f"🔧 Agents Used: {', '.join(response.get('agents_used', []))}")
                print(f"⏱️ Processing Time: {processing_time:.2f}s")
                print(f"🎯 Confidence: {response.get('confidence', 0):.2f}")
                print()
                print(f"🤖 CreatorMate Response:")
                print(f"   {response['response'][:200]}...")
                
                if response.get('recommendations'):
                    print()
                    print("💡 Top Recommendations:")
                    for j, rec in enumerate(response['recommendations'][:3], 1):
                        print(f"   {j}. {rec}")
                
            else:
                print(f"❌ Failed: {response.get('error', 'Unknown error')}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        print()
        print("-" * 50)
        print()
    
    # Show cache statistics
    print("📊 Cache Performance Statistics:")
    stats = cache.get_stats()
    print(f"   Cache Size: {stats['cache_size']} entries")
    print(f"   Hit Rate: {stats['hit_rate']}%")
    print(f"   Total Requests: {stats['total_requests']}")
    print(f"   Cache Hits: {stats['total_hits']}")
    print(f"   Cache Misses: {stats['total_misses']}")
    print()
    
    # Demonstrate cache functionality
    print("🔄 Testing Cache Functionality...")
    print("Re-running first query to demonstrate caching...")
    
    start_time = asyncio.get_event_loop().time()
    cached_response = await process_user_message(DEMO_QUERIES[0]["message"], SAMPLE_USER_CONTEXT)
    end_time = asyncio.get_event_loop().time()
    
    cached_processing_time = end_time - start_time
    
    print(f"⚡ Cached Response Time: {cached_processing_time:.2f}s")
    print(f"📈 Speed Improvement: {((processing_time - cached_processing_time) / processing_time * 100):.1f}% faster")
    
    # Final cache stats
    final_stats = cache.get_stats()
    print()
    print("📊 Final Cache Statistics:")
    print(f"   Hit Rate: {final_stats['hit_rate']}%")
    print(f"   Total Hits: {final_stats['total_hits']}")
    print(f"   Total Misses: {final_stats['total_misses']}")

async def demo_parallel_processing():
    """Demonstrate parallel agent processing capabilities"""
    
    print("\n🔀 Parallel Processing Demo")
    print("=" * 30)
    
    # Query that should trigger multiple agents
    complex_query = "I need a complete analysis of my channel performance, including content, audience, SEO, and competition insights"
    
    print(f"💬 Complex Query: \"{complex_query}\"")
    print()
    
    try:
        start_time = asyncio.get_event_loop().time()
        response = await process_user_message(complex_query, SAMPLE_USER_CONTEXT)
        end_time = asyncio.get_event_loop().time()
        
        if response.get("success", False):
            print(f"✅ Multi-Agent Response Completed")
            print(f"🔧 Agents Activated: {', '.join(response.get('agents_used', []))}")
            print(f"⏱️ Total Processing Time: {end_time - start_time:.2f}s")
            print(f"🎯 Overall Confidence: {response.get('confidence', 0):.2f}")
            print()
            print("🤖 Synthesized Response:")
            print(f"   {response['response'][:300]}...")
            
        else:
            print(f"❌ Failed: {response.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error in parallel processing demo: {e}")

if __name__ == "__main__":
    print("Starting CreatorMate Boss Agent Demo...")
    print("Make sure your OPENAI_API_KEY environment variable is set!")
    print()
    
    # Run the demo
    asyncio.run(demo_boss_agent())
    
    # Run parallel processing demo
    asyncio.run(demo_parallel_processing())
    
    print("\n🎉 Demo completed! The boss agent system is ready for production use.")
    print("\nTo integrate with your frontend:")
    print("1. Use the /api/agent/chat endpoint for regular chat")
    print("2. Use the /api/agent/analytics endpoint for advanced analytics")
    print("3. Monitor cache performance with /api/agent/cache/stats")
    print("4. Clear cache when needed with /api/agent/cache/clear")