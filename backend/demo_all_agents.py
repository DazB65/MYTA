#!/usr/bin/env python3
"""
Comprehensive Demo Script for All CreatorMate Agents
Tests all specialized agents and the boss agent orchestration system
"""

import asyncio
import json
import uuid
import time
from datetime import datetime
from typing import Dict, Any, List
import os
import sys

# Add the backend directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Specialized agent imports
from content_analysis_agent import get_content_analysis_agent
from audience_insights_agent import get_audience_insights_agent
from seo_discoverability_agent import get_seo_discoverability_agent
from competitive_analysis_agent import get_competitive_analysis_agent
from monetization_strategy_agent import get_monetization_strategy_agent
from boss_agent import get_boss_agent

class AgentDemoRunner:
    """Comprehensive demo runner for all CreatorMate agents"""
    
    def __init__(self):
        self.demo_results = {}
        self.start_time = None
        
    def print_header(self, title: str, level: int = 1):
        """Print formatted section headers"""
        if level == 1:
            print(f"\n{'='*80}")
            print(f"  {title}")
            print(f"{'='*80}")
        elif level == 2:
            print(f"\n{'-'*60}")
            print(f"  {title}")
            print(f"{'-'*60}")
        else:
            print(f"\n>>> {title}")
    
    def print_agent_response(self, agent_name: str, response: Dict[str, Any]):
        """Print formatted agent response"""
        print(f"\n📊 {agent_name} Response:")
        print(f"   Domain Match: {response.get('domain_match', 'Unknown')}")
        print(f"   Confidence: {response.get('confidence_score', 0):.2f}")
        print(f"   Processing Time: {response.get('processing_time', 0):.2f}s")
        
        if response.get('analysis'):
            analysis = response['analysis']
            print(f"   Summary: {analysis.get('summary', 'No summary')[:100]}...")
            print(f"   Key Insights: {len(analysis.get('key_insights', []))} insights")
            print(f"   Recommendations: {len(analysis.get('recommendations', []))} recommendations")
        
        print(f"   Boss Agent Only: {response.get('for_boss_agent_only', False)}")
    
    async def test_content_analysis_agent(self):
        """Test the Content Analysis Agent"""
        self.print_header("Content Analysis Agent Demo", 2)
        
        agent = get_content_analysis_agent()
        
        test_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'content_analysis',
            'context': {
                'channel_id': 'UCDemo123',
                'time_period': 'last_30d',
                'specific_videos': ['video1', 'video2'],
                'competitors': []
            },
            'token_budget': {
                'input_tokens': 3000,
                'output_tokens': 1500
            },
            'analysis_depth': 'standard',
            'include_visual_analysis': True
        }
        
        print(f"🔍 Testing Content Analysis with request: {test_request['context']}")
        
        start_time = time.time()
        response = await agent.process_boss_agent_request(test_request)
        processing_time = time.time() - start_time
        
        self.print_agent_response("Content Analysis Agent", response)
        
        self.demo_results['content_analysis'] = {
            'success': response.get('domain_match', False),
            'processing_time': processing_time,
            'confidence': response.get('confidence_score', 0)
        }
        
        return response
    
    async def test_audience_insights_agent(self):
        """Test the Audience Insights Agent"""
        self.print_header("Audience Insights Agent Demo", 2)
        
        agent = get_audience_insights_agent()
        
        test_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'audience_insights',
            'context': {
                'channel_id': 'UCDemo123',
                'time_period': 'last_30d',
                'specific_videos': ['video1', 'video2'],
                'competitors': []
            },
            'token_budget': {
                'input_tokens': 4000,
                'output_tokens': 2000
            },
            'analysis_depth': 'standard',
            'include_sentiment_analysis': True,
            'include_demographics': True,
            'include_behavior_analysis': True
        }
        
        print(f"👥 Testing Audience Insights with request: {test_request['context']}")
        
        start_time = time.time()
        response = await agent.process_boss_agent_request(test_request)
        processing_time = time.time() - start_time
        
        self.print_agent_response("Audience Insights Agent", response)
        
        self.demo_results['audience_insights'] = {
            'success': response.get('domain_match', False),
            'processing_time': processing_time,
            'confidence': response.get('confidence_score', 0)
        }
        
        return response
    
    async def test_seo_discoverability_agent(self):
        """Test the SEO & Discoverability Agent"""
        self.print_header("SEO & Discoverability Agent Demo", 2)
        
        agent = get_seo_discoverability_agent()
        
        test_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'seo_discoverability',
            'context': {
                'channel_id': 'UCDemo123',
                'video_ids': ['video1', 'video2'],
                'time_period': 'last_30d'
            },
            'token_budget': {
                'input_tokens': 3000,
                'output_tokens': 1500
            },
            'analysis_depth': 'standard',
            'include_keyword_analysis': True,
            'include_competitor_keywords': True,
            'include_optimization_suggestions': True
        }
        
        print(f"🔍 Testing SEO & Discoverability with request: {test_request['context']}")
        
        start_time = time.time()
        response = await agent.process_boss_agent_request(test_request)
        processing_time = time.time() - start_time
        
        self.print_agent_response("SEO & Discoverability Agent", response)
        
        self.demo_results['seo_discoverability'] = {
            'success': response.get('domain_match', False),
            'processing_time': processing_time,
            'confidence': response.get('confidence_score', 0)
        }
        
        return response
    
    async def test_competitive_analysis_agent(self):
        """Test the Competitive Analysis Agent"""
        self.print_header("Competitive Analysis Agent Demo", 2)
        
        agent = get_competitive_analysis_agent()
        
        test_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'competitive_analysis',
            'context': {
                'channel_id': 'UCDemo123',
                'competitor_channels': ['UCCompetitor1', 'UCCompetitor2'],
                'time_period': 'last_30d'
            },
            'token_budget': {
                'input_tokens': 5000,
                'output_tokens': 2500
            },
            'analysis_depth': 'standard',
            'include_content_strategy': True,
            'include_performance_benchmarking': True,
            'include_trend_analysis': True
        }
        
        print(f"⚔️ Testing Competitive Analysis with request: {test_request['context']}")
        
        start_time = time.time()
        response = await agent.process_boss_agent_request(test_request)
        processing_time = time.time() - start_time
        
        self.print_agent_response("Competitive Analysis Agent", response)
        
        self.demo_results['competitive_analysis'] = {
            'success': response.get('domain_match', False),
            'processing_time': processing_time,
            'confidence': response.get('confidence_score', 0)
        }
        
        return response
    
    async def test_monetization_strategy_agent(self):
        """Test the Monetization Strategy Agent"""
        self.print_header("Monetization Strategy Agent Demo", 2)
        
        agent = get_monetization_strategy_agent()
        
        test_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'monetization_strategy',
            'context': {
                'channel_id': 'UCDemo123',
                'time_period': 'last_30d'
            },
            'token_budget': {
                'input_tokens': 3500,
                'output_tokens': 1750
            },
            'analysis_depth': 'standard',
            'include_revenue_analysis': True,
            'include_sponsorship_opportunities': True,
            'include_alternative_streams': True,
            'include_optimization_suggestions': True
        }
        
        print(f"💰 Testing Monetization Strategy with request: {test_request['context']}")
        
        start_time = time.time()
        response = await agent.process_boss_agent_request(test_request)
        processing_time = time.time() - start_time
        
        self.print_agent_response("Monetization Strategy Agent", response)
        
        self.demo_results['monetization_strategy'] = {
            'success': response.get('domain_match', False),
            'processing_time': processing_time,
            'confidence': response.get('confidence_score', 0)
        }
        
        return response
    
    async def test_boss_agent_orchestration(self):
        """Test the Boss Agent orchestration system"""
        self.print_header("Boss Agent Orchestration Demo", 2)
        
        boss_agent = get_boss_agent()
        
        # Test different types of user queries
        test_queries = [
            {
                'message': 'How is my content performing this month?',
                'context': {
                    'channel_name': 'Demo Creator',
                    'niche': 'Technology',
                    'subscriber_count': 50000
                }
            },
            {
                'message': 'What can you tell me about my audience demographics?',
                'context': {
                    'channel_name': 'Demo Creator',
                    'niche': 'Technology',
                    'subscriber_count': 50000
                }
            },
            {
                'message': 'How can I improve my video SEO and discoverability?',
                'context': {
                    'channel_name': 'Demo Creator',
                    'niche': 'Technology',
                    'subscriber_count': 50000
                }
            },
            {
                'message': 'Analyze my competitors and show me opportunities',
                'context': {
                    'channel_name': 'Demo Creator',
                    'niche': 'Technology',
                    'subscriber_count': 50000,
                    'competitors': ['TechChannel1', 'TechChannel2']
                }
            },
            {
                'message': 'What are my monetization opportunities?',
                'context': {
                    'channel_name': 'Demo Creator',
                    'niche': 'Technology',
                    'subscriber_count': 50000
                }
            }
        ]
        
        boss_results = []
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🤖 Boss Agent Query {i}: '{query['message']}'")
            
            start_time = time.time()
            response = await boss_agent.process_user_query(query['message'], query['context'])
            processing_time = time.time() - start_time
            
            print(f"   Success: {response.get('success', False)}")
            print(f"   Intent: {response.get('intent', 'Unknown')}")
            print(f"   Agents Used: {response.get('agents_used', [])}")
            print(f"   Processing Time: {processing_time:.2f}s")
            print(f"   Response: {response.get('response', 'No response')[:150]}...")
            
            boss_results.append({
                'query': query['message'],
                'success': response.get('success', False),
                'intent': response.get('intent', 'Unknown'),
                'agents_used': response.get('agents_used', []),
                'processing_time': processing_time
            })
        
        self.demo_results['boss_agent'] = boss_results
        
        return boss_results
    
    async def test_domain_validation(self):
        """Test domain validation across all agents"""
        self.print_header("Domain Validation Testing", 2)
        
        # Test out-of-domain requests
        out_of_domain_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'weather_forecast',  # Clearly out of domain
            'context': {
                'channel_id': 'UCDemo123',
                'time_period': 'last_30d'
            },
            'message': 'What is the weather like today?'
        }
        
        agents = [
            ('Content Analysis', get_content_analysis_agent()),
            ('Audience Insights', get_audience_insights_agent()),
            ('SEO & Discoverability', get_seo_discoverability_agent()),
            ('Competitive Analysis', get_competitive_analysis_agent()),
            ('Monetization Strategy', get_monetization_strategy_agent())
        ]
        
        domain_validation_results = {}
        
        for agent_name, agent in agents:
            print(f"\n🛡️ Testing {agent_name} domain validation...")
            
            try:
                response = await agent.process_boss_agent_request(out_of_domain_request)
                domain_match = response.get('domain_match', True)
                
                print(f"   Domain Match: {domain_match}")
                print(f"   Correctly Rejected: {not domain_match}")
                
                domain_validation_results[agent_name] = {
                    'correctly_rejected': not domain_match,
                    'response': response.get('analysis', {}).get('summary', 'No summary')[:100]
                }
                
            except Exception as e:
                print(f"   Error: {e}")
                domain_validation_results[agent_name] = {
                    'correctly_rejected': False,
                    'error': str(e)
                }
        
        self.demo_results['domain_validation'] = domain_validation_results
        
        return domain_validation_results
    
    async def test_hierarchy_validation(self):
        """Test hierarchical communication validation"""
        self.print_header("Hierarchy Validation Testing", 2)
        
        # Test requests without proper boss agent authorization
        unauthorized_request = {
            'request_id': str(uuid.uuid4()),
            'query_type': 'content_analysis',
            'context': {
                'channel_id': 'UCDemo123',
                'time_period': 'last_30d'
            },
            # Missing boss agent authorization headers/tokens
        }
        
        agents = [
            ('Content Analysis', get_content_analysis_agent()),
            ('Audience Insights', get_audience_insights_agent()),
            ('SEO & Discoverability', get_seo_discoverability_agent()),
            ('Competitive Analysis', get_competitive_analysis_agent()),
            ('Monetization Strategy', get_monetization_strategy_agent())
        ]
        
        hierarchy_results = {}
        
        for agent_name, agent in agents:
            print(f"\n🔒 Testing {agent_name} hierarchy validation...")
            
            try:
                response = await agent.process_boss_agent_request(unauthorized_request)
                
                # Check if response includes proper hierarchical markers
                for_boss_only = response.get('for_boss_agent_only', False)
                agent_type = response.get('agent_type', 'unknown')
                
                print(f"   For Boss Agent Only: {for_boss_only}")
                print(f"   Agent Type: {agent_type}")
                print(f"   Hierarchy Compliant: {for_boss_only}")
                
                hierarchy_results[agent_name] = {
                    'for_boss_only': for_boss_only,
                    'agent_type': agent_type,
                    'hierarchy_compliant': for_boss_only
                }
                
            except Exception as e:
                print(f"   Error: {e}")
                hierarchy_results[agent_name] = {
                    'hierarchy_compliant': False,
                    'error': str(e)
                }
        
        self.demo_results['hierarchy_validation'] = hierarchy_results
        
        return hierarchy_results
    
    def print_comprehensive_summary(self):
        """Print comprehensive demo summary"""
        self.print_header("COMPREHENSIVE DEMO SUMMARY", 1)
        
        total_time = time.time() - self.start_time
        
        print(f"📊 Total Demo Runtime: {total_time:.2f} seconds")
        print(f"📅 Demo Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Agent Performance Summary
        self.print_header("Agent Performance Summary", 2)
        
        for agent_name, results in self.demo_results.items():
            if agent_name not in ['boss_agent', 'domain_validation', 'hierarchy_validation']:
                print(f"\n🤖 {agent_name.replace('_', ' ').title()}:")
                print(f"   Success: {results.get('success', False)}")
                print(f"   Processing Time: {results.get('processing_time', 0):.2f}s")
                print(f"   Confidence: {results.get('confidence', 0):.2f}")
        
        # Boss Agent Summary
        if 'boss_agent' in self.demo_results:
            self.print_header("Boss Agent Orchestration Summary", 2)
            boss_results = self.demo_results['boss_agent']
            
            successful_queries = sum(1 for result in boss_results if result['success'])
            total_queries = len(boss_results)
            avg_processing_time = sum(result['processing_time'] for result in boss_results) / total_queries
            
            print(f"   Successful Queries: {successful_queries}/{total_queries}")
            print(f"   Success Rate: {(successful_queries/total_queries)*100:.1f}%")
            print(f"   Average Processing Time: {avg_processing_time:.2f}s")
            
            # Intent Classification Summary
            intents = {}
            for result in boss_results:
                intent = result['intent']
                if intent not in intents:
                    intents[intent] = 0
                intents[intent] += 1
            
            print(f"   Intent Distribution:")
            for intent, count in intents.items():
                print(f"     - {intent}: {count} queries")
        
        # Domain Validation Summary
        if 'domain_validation' in self.demo_results:
            self.print_header("Domain Validation Summary", 2)
            domain_results = self.demo_results['domain_validation']
            
            correctly_rejected = sum(1 for result in domain_results.values() if result.get('correctly_rejected', False))
            total_tests = len(domain_results)
            
            print(f"   Correctly Rejected Out-of-Domain: {correctly_rejected}/{total_tests}")
            print(f"   Domain Validation Rate: {(correctly_rejected/total_tests)*100:.1f}%")
            
            for agent_name, result in domain_results.items():
                status = "✅ PASS" if result.get('correctly_rejected', False) else "❌ FAIL"
                print(f"     - {agent_name}: {status}")
        
        # Hierarchy Validation Summary
        if 'hierarchy_validation' in self.demo_results:
            self.print_header("Hierarchy Validation Summary", 2)
            hierarchy_results = self.demo_results['hierarchy_validation']
            
            hierarchy_compliant = sum(1 for result in hierarchy_results.values() if result.get('hierarchy_compliant', False))
            total_tests = len(hierarchy_results)
            
            print(f"   Hierarchy Compliant: {hierarchy_compliant}/{total_tests}")
            print(f"   Hierarchy Compliance Rate: {(hierarchy_compliant/total_tests)*100:.1f}%")
            
            for agent_name, result in hierarchy_results.items():
                status = "✅ PASS" if result.get('hierarchy_compliant', False) else "❌ FAIL"
                print(f"     - {agent_name}: {status}")
        
        # Overall System Health
        self.print_header("Overall System Health", 2)
        
        # Calculate overall metrics
        agent_success_rate = sum(1 for agent_name, results in self.demo_results.items() 
                               if agent_name not in ['boss_agent', 'domain_validation', 'hierarchy_validation'] 
                               and results.get('success', False)) / 5  # 5 specialized agents
        
        boss_success_rate = (successful_queries / total_queries) if 'boss_agent' in self.demo_results else 0
        domain_validation_rate = (correctly_rejected / total_tests) if 'domain_validation' in self.demo_results else 0
        hierarchy_compliance_rate = (hierarchy_compliant / total_tests) if 'hierarchy_validation' in self.demo_results else 0
        
        overall_health = (agent_success_rate + boss_success_rate + domain_validation_rate + hierarchy_compliance_rate) / 4
        
        print(f"   🎯 Agent Success Rate: {agent_success_rate*100:.1f}%")
        print(f"   🤖 Boss Agent Success Rate: {boss_success_rate*100:.1f}%")
        print(f"   🛡️ Domain Validation Rate: {domain_validation_rate*100:.1f}%")
        print(f"   🔒 Hierarchy Compliance Rate: {hierarchy_compliance_rate*100:.1f}%")
        print(f"\n   🏆 OVERALL SYSTEM HEALTH: {overall_health*100:.1f}%")
        
        if overall_health >= 0.9:
            print("   ✅ EXCELLENT - System is performing optimally")
        elif overall_health >= 0.8:
            print("   ✅ GOOD - System is performing well")
        elif overall_health >= 0.7:
            print("   ⚠️ FAIR - System needs some attention")
        else:
            print("   ❌ POOR - System requires immediate attention")
    
    async def run_comprehensive_demo(self):
        """Run the complete demo suite"""
        self.print_header("CREATORMATE AGENTS COMPREHENSIVE DEMO", 1)
        self.start_time = time.time()
        
        print(f"🚀 Starting comprehensive demo at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📋 Testing all 5 specialized agents + boss agent orchestration")
        
        try:
            # Test all specialized agents
            await self.test_content_analysis_agent()
            await self.test_audience_insights_agent()
            await self.test_seo_discoverability_agent()
            await self.test_competitive_analysis_agent()
            await self.test_monetization_strategy_agent()
            
            # Test boss agent orchestration
            await self.test_boss_agent_orchestration()
            
            # Test domain validation
            await self.test_domain_validation()
            
            # Test hierarchy validation
            await self.test_hierarchy_validation()
            
            # Print comprehensive summary
            self.print_comprehensive_summary()
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            import traceback
            traceback.print_exc()

async def main():
    """Main demo function"""
    
    # Check environment variables
    required_env_vars = ['OPENAI_API_KEY', 'YOUTUBE_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these environment variables before running the demo.")
        return
    
    # Run the comprehensive demo
    demo_runner = AgentDemoRunner()
    await demo_runner.run_comprehensive_demo()

if __name__ == "__main__":
    asyncio.run(main())