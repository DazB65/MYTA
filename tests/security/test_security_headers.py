"""
Security Headers Testing for MYTA Application
Tests that all required security headers are properly configured
"""

import pytest
import httpx
import asyncio
from typing import Dict, List, Optional
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from fastapi.testclient import TestClient


class SecurityHeadersTest:
    """Test suite for security headers validation"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.required_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Content-Security-Policy': None,  # Will validate content
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': None,  # Will validate content
        }
        
        self.production_headers = {
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            'Cross-Origin-Embedder-Policy': 'require-corp',
            'Cross-Origin-Opener-Policy': 'same-origin',
            'Cross-Origin-Resource-Policy': 'same-origin'
        }
    
    async def test_security_headers_endpoint(self, endpoint: str = "/health") -> Dict[str, any]:
        """Test security headers for a specific endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}")
                return {
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'missing_headers': [],
                    'invalid_headers': [],
                    'passed': True,
                    'errors': []
                }
            except Exception as e:
                return {
                    'endpoint': endpoint,
                    'status_code': 0,
                    'headers': {},
                    'missing_headers': list(self.required_headers.keys()),
                    'invalid_headers': [],
                    'passed': False,
                    'errors': [f"Connection error: {str(e)}"]
                }
    
    def validate_headers(self, headers: Dict[str, str], is_production: bool = False) -> Dict[str, any]:
        """Validate security headers against requirements"""
        missing_headers = []
        invalid_headers = []
        errors = []
        
        # Check required headers
        for header_name, expected_value in self.required_headers.items():
            if header_name not in headers:
                missing_headers.append(header_name)
                errors.append(f"Missing required header: {header_name}")
            elif expected_value and headers[header_name] != expected_value:
                invalid_headers.append({
                    'header': header_name,
                    'expected': expected_value,
                    'actual': headers[header_name]
                })
                errors.append(f"Invalid {header_name}: expected '{expected_value}', got '{headers[header_name]}'")
        
        # Validate CSP header content
        if 'Content-Security-Policy' in headers:
            csp_errors = self._validate_csp(headers['Content-Security-Policy'])
            errors.extend(csp_errors)
        
        # Check production-specific headers
        if is_production:
            for header_name, expected_value in self.production_headers.items():
                if header_name not in headers:
                    missing_headers.append(header_name)
                    errors.append(f"Missing production header: {header_name}")
                elif expected_value and headers[header_name] != expected_value:
                    invalid_headers.append({
                        'header': header_name,
                        'expected': expected_value,
                        'actual': headers[header_name]
                    })
        
        return {
            'missing_headers': missing_headers,
            'invalid_headers': invalid_headers,
            'errors': errors,
            'passed': len(missing_headers) == 0 and len(invalid_headers) == 0
        }
    
    def _validate_csp(self, csp_header: str) -> List[str]:
        """Validate Content Security Policy header"""
        errors = []
        required_directives = [
            'default-src',
            'script-src',
            'style-src',
            'img-src',
            'connect-src',
            'font-src',
            'object-src',
            'media-src',
            'frame-src'
        ]
        
        # Parse CSP directives
        directives = {}
        for directive in csp_header.split(';'):
            directive = directive.strip()
            if directive:
                parts = directive.split(' ', 1)
                if len(parts) >= 1:
                    directives[parts[0]] = parts[1] if len(parts) > 1 else ''
        
        # Check for required directives
        for required in required_directives:
            if required not in directives:
                errors.append(f"CSP missing required directive: {required}")
        
        # Check for unsafe directives
        unsafe_patterns = ["'unsafe-inline'", "'unsafe-eval'", "data:", "javascript:"]
        for directive, value in directives.items():
            for unsafe in unsafe_patterns:
                if unsafe in value:
                    errors.append(f"CSP contains unsafe directive in {directive}: {unsafe}")
        
        return errors
    
    async def run_comprehensive_test(self, endpoints: List[str] = None) -> Dict[str, any]:
        """Run comprehensive security headers test"""
        if endpoints is None:
            endpoints = ["/health", "/api/health", "/", "/api/csrf-token"]
        
        results = []
        overall_passed = True
        
        for endpoint in endpoints:
            result = await self.test_security_headers_endpoint(endpoint)
            
            # Validate headers
            is_production = os.getenv('ENVIRONMENT', 'development') == 'production'
            validation = self.validate_headers(result['headers'], is_production)
            
            result.update(validation)
            results.append(result)
            
            if not result['passed']:
                overall_passed = False
        
        return {
            'overall_passed': overall_passed,
            'total_endpoints': len(endpoints),
            'passed_endpoints': sum(1 for r in results if r['passed']),
            'failed_endpoints': sum(1 for r in results if not r['passed']),
            'results': results,
            'summary': self._generate_summary(results)
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict[str, any]:
        """Generate test summary"""
        all_missing = set()
        all_invalid = set()
        all_errors = []
        
        for result in results:
            all_missing.update(result.get('missing_headers', []))
            all_invalid.update(h['header'] for h in result.get('invalid_headers', []))
            all_errors.extend(result.get('errors', []))
        
        return {
            'unique_missing_headers': list(all_missing),
            'unique_invalid_headers': list(all_invalid),
            'total_errors': len(all_errors),
            'unique_errors': list(set(all_errors))
        }


# Pytest test functions
@pytest.fixture
def security_tester():
    """Fixture to provide SecurityHeadersTest instance"""
    return SecurityHeadersTest()


@pytest.mark.asyncio
async def test_health_endpoint_security_headers(security_tester):
    """Test security headers on health endpoint"""
    result = await security_tester.test_security_headers_endpoint("/health")
    
    assert result['status_code'] == 200, f"Health endpoint returned {result['status_code']}"
    
    validation = security_tester.validate_headers(result['headers'])
    
    if not validation['passed']:
        pytest.fail(f"Security headers validation failed: {validation['errors']}")


@pytest.mark.asyncio
async def test_api_endpoints_security_headers(security_tester):
    """Test security headers on API endpoints"""
    endpoints = ["/api/health", "/api/csrf-token"]
    
    for endpoint in endpoints:
        result = await security_tester.test_security_headers_endpoint(endpoint)
        validation = security_tester.validate_headers(result['headers'])
        
        if not validation['passed']:
            pytest.fail(f"Security headers validation failed for {endpoint}: {validation['errors']}")


@pytest.mark.asyncio
async def test_comprehensive_security_headers():
    """Run comprehensive security headers test"""
    tester = SecurityHeadersTest()
    result = await tester.run_comprehensive_test()
    
    print(f"\n=== Security Headers Test Summary ===")
    print(f"Total endpoints tested: {result['total_endpoints']}")
    print(f"Passed: {result['passed_endpoints']}")
    print(f"Failed: {result['failed_endpoints']}")
    
    if not result['overall_passed']:
        print(f"\nErrors found:")
        for error in result['summary']['unique_errors']:
            print(f"  - {error}")
        
        pytest.fail(f"Security headers test failed. See summary above.")
    
    print("✅ All security headers tests passed!")


if __name__ == "__main__":
    # Run standalone test
    async def main():
        tester = SecurityHeadersTest()
        result = await tester.run_comprehensive_test()
        
        print("=== Security Headers Test Results ===")
        print(f"Overall passed: {result['overall_passed']}")
        print(f"Endpoints tested: {result['total_endpoints']}")
        print(f"Passed: {result['passed_endpoints']}")
        print(f"Failed: {result['failed_endpoints']}")
        
        if not result['overall_passed']:
            print("\nDetailed Results:")
            for endpoint_result in result['results']:
                if not endpoint_result['passed']:
                    print(f"\n❌ {endpoint_result['endpoint']}:")
                    for error in endpoint_result['errors']:
                        print(f"  - {error}")
                else:
                    print(f"✅ {endpoint_result['endpoint']}: PASSED")
        
        return result['overall_passed']
    
    # Run the test
    passed = asyncio.run(main())
    exit(0 if passed else 1)
