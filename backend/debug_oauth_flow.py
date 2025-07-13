#!/usr/bin/env python3
"""
Debug script to trace OAuth data access flow
Tests the exact path when a user asks "what's my best performing video"
"""

import asyncio
import logging
import sys
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import required modules
from boss_agent import get_boss_agent, process_user_message
from oauth_manager import get_oauth_manager
from analytics_service import get_analytics_service
from enhanced_user_context import get_enhanced_context_manager
from realtime_data_pipeline import get_data_pipeline
from ai_services import get_user_context

async def debug_oauth_flow():
    """Debug the OAuth data access flow step by step"""
    
    # Test with a user who has an OAuth token
    test_user_id = "default_user"  # This user has an OAuth token according to our DB check
    test_message = "what's my best performing video"
    
    print("🔍 DEBUGGING OAUTH DATA ACCESS FLOW")
    print("=" * 60)
    print(f"Test User ID: {test_user_id}")
    print(f"Test Message: '{test_message}'")
    print()
    
    # Step 1: Check OAuth status
    print("STEP 1: Checking OAuth Status")
    print("-" * 30)
    try:
        oauth_manager = get_oauth_manager()
        oauth_status = oauth_manager.get_oauth_status(test_user_id)
        print(f"✅ OAuth Status: {oauth_status}")
        
        if not oauth_status.get('authenticated', False):
            print("❌ User is not authenticated!")
            return
        
        # Check if token is valid
        token = await oauth_manager.get_valid_token(test_user_id)
        if token:
            print(f"✅ Valid token found - expires at: {token.expires_at}")
        else:
            print("❌ No valid token found!")
            return
            
    except Exception as e:
        print(f"❌ OAuth status check failed: {e}")
        return
    
    print()
    
    # Step 2: Check user context
    print("STEP 2: Checking User Context")
    print("-" * 30)
    try:
        user_context = get_user_context(test_user_id)
        channel_info = user_context.get('channel_info', {})
        print(f"✅ User context found")
        print(f"   Channel Name: {channel_info.get('name', 'Unknown')}")
        print(f"   Channel ID: {channel_info.get('channel_id', 'Unknown')}")
        print(f"   Total Views: {channel_info.get('total_view_count', 0)}")
        print(f"   Subscriber Count: {channel_info.get('subscriber_count', 0)}")
    except Exception as e:
        print(f"❌ User context check failed: {e}")
        return
    
    print()
    
    # Step 3: Test Analytics Service Direct Access
    print("STEP 3: Testing Analytics Service Direct Access")
    print("-" * 50)
    try:
        analytics_service = get_analytics_service()
        
        # Test getting channel analytics
        print("Testing channel analytics...")
        channel_analytics = await analytics_service.get_channel_analytics(test_user_id, days=30)
        
        if channel_analytics:
            print(f"✅ Channel analytics retrieved successfully")
            print(f"   Views (30 days): {channel_analytics.views}")
            print(f"   Watch time: {channel_analytics.watch_time_hours:.1f} hours")
            print(f"   CTR: {channel_analytics.ctr:.2f}%")
            print(f"   Retention: {channel_analytics.average_view_percentage:.2f}%")
        else:
            print("❌ Failed to get channel analytics")
            
        # Test performance summary
        print("\nTesting performance summary...")
        perf_summary = await analytics_service.get_recent_performance_summary(test_user_id)
        
        if perf_summary:
            print(f"✅ Performance summary retrieved successfully")
            current = perf_summary.get('current_period', {})
            print(f"   Current week views: {current.get('views', 0)}")
            print(f"   Current week CTR: {current.get('ctr', 0):.2f}%")
        else:
            print("❌ Failed to get performance summary")
            
    except Exception as e:
        print(f"❌ Analytics service test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Step 4: Test Enhanced Context Manager
    print("STEP 4: Testing Enhanced Context Manager")
    print("-" * 40)
    try:
        enhanced_context_manager = get_enhanced_context_manager()
        enhanced_context = await enhanced_context_manager.get_enhanced_context(test_user_id)
        
        if enhanced_context:
            print(f"✅ Enhanced context retrieved successfully")
            realtime_data = enhanced_context.get('realtime_data', {})
            if realtime_data:
                print(f"   Has real-time data: YES")
                perf_summary = realtime_data.get('performance_summary', {})
                if perf_summary:
                    current = perf_summary.get('current_period', {})
                    print(f"   Real-time views: {current.get('views', 0)}")
            else:
                print(f"   Has real-time data: NO")
        else:
            print("❌ Failed to get enhanced context")
            
    except Exception as e:
        print(f"❌ Enhanced context test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Step 5: Test Data Pipeline
    print("STEP 5: Testing Data Pipeline")
    print("-" * 30)
    try:
        data_pipeline = get_data_pipeline()
        
        # Register user activity
        await data_pipeline.register_user_activity(test_user_id, "debug_test")
        print(f"✅ Registered user activity")
        
        # Get real-time context
        rt_context = await data_pipeline.get_real_time_context(test_user_id)
        
        if rt_context:
            print(f"✅ Real-time context retrieved successfully")
            key_metrics = rt_context.get('key_metrics', {})
            if key_metrics:
                print(f"   Key metrics available: {list(key_metrics.keys())}")
                print(f"   Current week views: {key_metrics.get('current_week_views', 0)}")
            else:
                print(f"   No key metrics available")
        else:
            print("❌ Failed to get real-time context from pipeline")
            
    except Exception as e:
        print(f"❌ Data pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Step 6: Test Boss Agent Processing
    print("STEP 6: Testing Boss Agent Processing")
    print("-" * 40)
    try:
        # Test the exact flow that happens in the chat endpoint
        boss_response = await process_user_message(test_message, user_context)
        
        if boss_response.get("success", False):
            print(f"✅ Boss agent processed successfully")
            print(f"   Intent: {boss_response.get('intent', 'unknown')}")
            print(f"   Agents used: {boss_response.get('agents_used', [])}")
            print(f"   Confidence: {boss_response.get('confidence', 0):.2f}")
            print(f"   Response length: {len(boss_response.get('response', ''))}")
            print(f"   Real-time data used: {boss_response.get('real_time_data', False)}")
            
            # Show first 200 chars of response
            response_text = boss_response.get('response', '')
            if response_text:
                print(f"   Response preview: {response_text[:200]}...")
            
        else:
            print(f"❌ Boss agent failed")
            print(f"   Error: {boss_response.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Boss agent test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🔍 DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(debug_oauth_flow())