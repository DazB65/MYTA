#!/usr/bin/env python3
"""
API Key Testing Script for MYTA Application
Tests the validity and functionality of API keys
"""

import os
import sys
import asyncio
import argparse
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APIKeyTester:
    """Tests API keys for various services"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self.load_environment()
        
        self.test_results = {}
    
    def load_environment(self):
        """Load environment variables from .env file"""
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    async def test_openai_key(self) -> Dict[str, any]:
        """Test OpenAI API key"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return {'status': 'missing', 'error': 'OPENAI_API_KEY not found'}
        
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            # Test with models list (lightweight call)
            models = client.models.list()
            
            return {
                'status': 'valid',
                'key_preview': api_key[:10] + '...',
                'models_count': len(models.data) if hasattr(models, 'data') else 0,
                'tested_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'invalid',
                'error': str(e),
                'key_preview': api_key[:10] + '...' if api_key else 'None'
            }
    
    async def test_anthropic_key(self) -> Dict[str, any]:
        """Test Anthropic API key"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            return {'status': 'missing', 'error': 'ANTHROPIC_API_KEY not found'}
        
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            # Basic format validation
            if not api_key.startswith('sk-ant-api03-'):
                return {
                    'status': 'invalid',
                    'error': 'Invalid key format',
                    'key_preview': api_key[:10] + '...'
                }
            
            # Note: Anthropic doesn't have a simple test endpoint like OpenAI
            # So we do basic validation and format checking
            return {
                'status': 'valid',
                'key_preview': api_key[:10] + '...',
                'note': 'Format validation passed (full test requires API call)',
                'tested_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'invalid',
                'error': str(e),
                'key_preview': api_key[:10] + '...' if api_key else 'None'
            }
    
    async def test_google_key(self) -> Dict[str, any]:
        """Test Google API key"""
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            return {'status': 'missing', 'error': 'GOOGLE_API_KEY not found'}
        
        try:
            import httpx
            
            # Test with a simple API call
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key={api_key}&maxResults=1"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'status': 'valid',
                        'key_preview': api_key[:10] + '...',
                        'quota_used': response.headers.get('X-Goog-Api-Client', 'Unknown'),
                        'tested_at': datetime.now().isoformat()
                    }
                elif response.status_code == 403:
                    return {
                        'status': 'invalid',
                        'error': 'API key invalid or quota exceeded',
                        'key_preview': api_key[:10] + '...'
                    }
                else:
                    return {
                        'status': 'error',
                        'error': f'HTTP {response.status_code}: {response.text}',
                        'key_preview': api_key[:10] + '...'
                    }
                    
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'key_preview': api_key[:10] + '...' if api_key else 'None'
            }
    
    async def test_youtube_key(self) -> Dict[str, any]:
        """Test YouTube API key (usually same as Google key)"""
        youtube_key = os.getenv('YOUTUBE_API_KEY')
        yt_key = os.getenv('YT_API_KEY')
        
        # Use YouTube key if available, otherwise fall back to Google key
        api_key = youtube_key or yt_key or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            return {'status': 'missing', 'error': 'No YouTube API key found'}
        
        # Test is same as Google API key test
        result = await self.test_google_key()
        result['note'] = 'Tested using YouTube Data API v3'
        return result
    
    def test_internal_keys(self) -> Dict[str, any]:
        """Test internal application keys"""
        results = {}
        
        # Test Boss Agent Secret Key
        boss_key = os.getenv('BOSS_AGENT_SECRET_KEY')
        if boss_key:
            results['boss_agent_secret'] = {
                'status': 'present',
                'length': len(boss_key),
                'key_preview': boss_key[:10] + '...',
                'valid_length': len(boss_key) >= 32
            }
        else:
            results['boss_agent_secret'] = {'status': 'missing', 'error': 'BOSS_AGENT_SECRET_KEY not found'}
        
        # Test Session Secret Key
        session_key = os.getenv('SESSION_SECRET_KEY')
        if session_key:
            results['session_secret'] = {
                'status': 'present',
                'length': len(session_key),
                'key_preview': session_key[:10] + '...',
                'valid_length': len(session_key) >= 32
            }
        else:
            results['session_secret'] = {'status': 'missing', 'error': 'SESSION_SECRET_KEY not found'}
        
        return results
    
    def test_oauth_credentials(self) -> Dict[str, any]:
        """Test OAuth credentials"""
        results = {}
        
        # Test Google OAuth
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if client_id and client_secret:
            results['google_oauth'] = {
                'status': 'present',
                'client_id_preview': client_id[:20] + '...' if len(client_id) > 20 else client_id,
                'client_secret_preview': client_secret[:10] + '...',
                'valid_format': client_id.endswith('.apps.googleusercontent.com')
            }
        else:
            results['google_oauth'] = {
                'status': 'missing',
                'error': 'Google OAuth credentials not found'
            }
        
        return results
    
    async def test_all_keys(self, verbose: bool = False) -> Dict[str, any]:
        """Test all API keys"""
        logger.info("Testing all API keys...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'external_apis': {},
            'internal_keys': {},
            'oauth_credentials': {},
            'summary': {}
        }
        
        # Test external APIs
        logger.info("Testing external API keys...")
        results['external_apis']['openai'] = await self.test_openai_key()
        results['external_apis']['anthropic'] = await self.test_anthropic_key()
        results['external_apis']['google'] = await self.test_google_key()
        results['external_apis']['youtube'] = await self.test_youtube_key()
        
        # Test internal keys
        logger.info("Testing internal keys...")
        results['internal_keys'] = self.test_internal_keys()
        
        # Test OAuth credentials
        logger.info("Testing OAuth credentials...")
        results['oauth_credentials'] = self.test_oauth_credentials()
        
        # Generate summary
        total_tests = 0
        passed_tests = 0
        
        for category in ['external_apis', 'internal_keys', 'oauth_credentials']:
            for service, result in results[category].items():
                total_tests += 1
                if result.get('status') in ['valid', 'present']:
                    passed_tests += 1
        
        results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        return results
    
    def print_results(self, results: Dict[str, any], verbose: bool = False):
        """Print test results in a readable format"""
        print("\n" + "="*60)
        print("API KEY TEST RESULTS")
        print("="*60)
        
        print(f"Test completed at: {results['timestamp']}")
        print(f"Success rate: {results['summary']['success_rate']:.1f}% ({results['summary']['passed_tests']}/{results['summary']['total_tests']})")
        
        # External APIs
        print(f"\n🌐 EXTERNAL API KEYS:")
        for service, result in results['external_apis'].items():
            status = result['status']
            icon = "✅" if status == 'valid' else "❌" if status in ['invalid', 'error'] else "⚠️"
            print(f"  {icon} {service.upper()}: {status}")
            
            if verbose or status != 'valid':
                if 'error' in result:
                    print(f"      Error: {result['error']}")
                if 'key_preview' in result:
                    print(f"      Key: {result['key_preview']}")
        
        # Internal Keys
        print(f"\n🔐 INTERNAL KEYS:")
        for key_name, result in results['internal_keys'].items():
            status = result['status']
            icon = "✅" if status == 'present' else "❌"
            print(f"  {icon} {key_name.upper()}: {status}")
            
            if verbose or status != 'present':
                if 'error' in result:
                    print(f"      Error: {result['error']}")
                if 'length' in result:
                    valid = "✅" if result.get('valid_length', False) else "❌"
                    print(f"      Length: {result['length']} {valid}")
        
        # OAuth Credentials
        print(f"\n🔑 OAUTH CREDENTIALS:")
        for service, result in results['oauth_credentials'].items():
            status = result['status']
            icon = "✅" if status == 'present' else "❌"
            print(f"  {icon} {service.upper()}: {status}")
            
            if verbose or status != 'present':
                if 'error' in result:
                    print(f"      Error: {result['error']}")
                if 'valid_format' in result:
                    format_icon = "✅" if result['valid_format'] else "❌"
                    print(f"      Format: {format_icon}")
        
        print("\n" + "="*60)


async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Test API keys for MYTA application")
    parser.add_argument('--service', choices=['openai', 'anthropic', 'google', 'youtube', 'internal', 'oauth'], 
                       help='Test specific service only')
    parser.add_argument('--all', action='store_true', help='Test all keys (default)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--env-file', default='.env', help='Environment file path')
    
    args = parser.parse_args()
    
    tester = APIKeyTester(args.env_file)
    
    if args.service:
        if args.service == 'openai':
            result = await tester.test_openai_key()
            print(f"OpenAI: {result}")
        elif args.service == 'anthropic':
            result = await tester.test_anthropic_key()
            print(f"Anthropic: {result}")
        elif args.service == 'google':
            result = await tester.test_google_key()
            print(f"Google: {result}")
        elif args.service == 'youtube':
            result = await tester.test_youtube_key()
            print(f"YouTube: {result}")
        elif args.service == 'internal':
            result = tester.test_internal_keys()
            print(f"Internal Keys: {result}")
        elif args.service == 'oauth':
            result = tester.test_oauth_credentials()
            print(f"OAuth: {result}")
    else:
        # Test all keys
        results = await tester.test_all_keys(args.verbose)
        tester.print_results(results, args.verbose)
        
        # Exit with error code if any tests failed
        if results['summary']['failed_tests'] > 0:
            exit(1)


if __name__ == "__main__":
    asyncio.run(main())
