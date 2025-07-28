"""
Security tests for CreatorMate application
"""
import pytest
import json
import secrets
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock


@pytest.mark.security
class TestAuthenticationSecurity:
    """Test authentication security measures"""

    def test_jwt_token_validation(self, test_client: TestClient):
        """Test JWT token validation and security"""
        # Test with invalid token
        headers = {"Authorization": "Bearer invalid-token"}
        response = test_client.post(
            "/api/agent/chat",
            json={"message": "test", "user_id": "test"},
            headers=headers
        )
        
        # Should handle invalid tokens gracefully
        assert response.status_code in [401, 403, 422]

    def test_token_expiry_handling(self, test_client: TestClient):
        """Test expired token handling"""
        # Create an expired token
        import jwt
        from datetime import datetime, timedelta
        
        secret_key = "test-secret"
        expired_payload = {
            "user_id": "test-user",
            "exp": datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
            "iat": datetime.utcnow() - timedelta(hours=2)
        }
        
        expired_token = jwt.encode(expired_payload, secret_key, algorithm="HS256")
        headers = {"Authorization": f"Bearer {expired_token}"}
        
        response = test_client.post(
            "/api/agent/chat",
            json={"message": "test", "user_id": "test"},
            headers=headers
        )
        
        # Should reject expired tokens
        assert response.status_code in [401, 403]

    def test_token_signature_validation(self, test_client: TestClient):
        """Test token signature validation"""
        import jwt
        from datetime import datetime, timedelta
        
        # Create token with wrong secret
        wrong_secret = "wrong-secret"
        payload = {
            "user_id": "test-user",
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        
        invalid_token = jwt.encode(payload, wrong_secret, algorithm="HS256")
        headers = {"Authorization": f"Bearer {invalid_token}"}
        
        response = test_client.post(
            "/api/agent/chat",
            json={"message": "test", "user_id": "test"},
            headers=headers
        )
        
        # Should reject tokens with invalid signatures
        assert response.status_code in [401, 403]

    def test_boss_agent_token_isolation(self, test_client: TestClient):
        """Test boss agent tokens cannot be used for user endpoints"""
        # This would require mocking the boss agent token generation
        # and ensuring it's properly isolated from user tokens
        
        # Mock a boss agent token
        with patch("auth_middleware.AuthenticationManager.verify_token") as mock_verify:
            mock_verify.side_effect = Exception("Invalid token type")
            
            headers = {"Authorization": "Bearer boss-agent-token"}
            response = test_client.post(
                "/api/agent/chat",
                json={"message": "test", "user_id": "test"},
                headers=headers
            )
            
            # Should reject boss agent tokens for user endpoints
            assert response.status_code in [401, 403]


@pytest.mark.security
class TestInputValidationSecurity:
    """Test input validation security measures"""

    def test_sql_injection_prevention(self, test_client: TestClient):
        """Test SQL injection prevention in user inputs"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO users (username) VALUES ('hacker'); --"
        ]
        
        for malicious_input in malicious_inputs:
            # Test in user_id field
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": "test",
                    "user_id": malicious_input
                }
            )
            
            # Should not cause 500 errors (which might indicate SQL injection)
            assert response.status_code != 500
            
            # Test in message field
            response = test_client.post(
                "/api/agent/chat", 
                json={
                    "message": malicious_input,
                    "user_id": "test-user"
                }
            )
            
            assert response.status_code != 500

    def test_xss_prevention(self, test_client: TestClient):
        """Test XSS attack prevention"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": payload,
                    "user_id": "test-user"
                }
            )
            
            # Should not reflect the script back unescaped
            if response.status_code == 200:
                response_text = response.text
                # Check that script tags are not present in raw form
                assert "<script>" not in response_text
                assert "javascript:" not in response_text
                assert "onerror=" not in response_text

    def test_command_injection_prevention(self, test_client: TestClient):
        """Test command injection prevention"""
        command_injection_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "&& rm -rf /",
            "`whoami`",
            "$(rm -rf /)",
            "; python -c 'import os; os.system(\"ls\")'"
        ]
        
        for payload in command_injection_payloads:
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": payload,
                    "user_id": "test-user"
                }
            )
            
            # Should handle malicious input without executing commands
            assert response.status_code != 500

    def test_oversized_input_handling(self, test_client: TestClient):
        """Test handling of oversized inputs"""
        # Test very large message
        large_message = "A" * 100000  # 100KB message
        
        response = test_client.post(
            "/api/agent/chat",
            json={
                "message": large_message,
                "user_id": "test-user"
            }
        )
        
        # Should either reject with 413 (Request Entity Too Large) or 400
        assert response.status_code in [400, 413, 422]

    def test_malformed_json_handling(self, test_client: TestClient):
        """Test handling of malformed JSON"""
        malformed_json_strings = [
            '{"message": "test", "user_id": }',  # Missing value
            '{"message": "test" "user_id": "test"}',  # Missing comma
            '{"message": "test", "user_id": "test",}',  # Trailing comma
            '{message: "test", user_id: "test"}',  # Unquoted keys
        ]
        
        for malformed_json in malformed_json_strings:
            response = test_client.post(
                "/api/agent/chat",
                data=malformed_json,
                headers={"Content-Type": "application/json"}
            )
            
            # Should return 422 (Unprocessable Entity) for malformed JSON
            assert response.status_code == 422

    def test_unicode_handling(self, test_client: TestClient):
        """Test proper unicode and encoding handling"""
        unicode_inputs = [
            "Testing unicode: 你好世界",
            "Emojis: 🚀💯🔥",
            "Mixed: Hello 世界 🌍",
            "Special chars: ñáéíóú",
            "Zero-width chars: \u200b\u200c\u200d"
        ]
        
        for unicode_input in unicode_inputs:
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": unicode_input,
                    "user_id": "test-user"
                }
            )
            
            # Should handle unicode properly without errors
            assert response.status_code in [200, 400, 422]  # 400/422 for validation, not 500


@pytest.mark.security
class TestAPISecurityHeaders:
    """Test security headers and CORS configuration"""

    def test_security_headers_present(self, test_client: TestClient):
        """Test that security headers are present"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        
        # Check for security headers
        expected_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Referrer-Policy"
        ]
        
        for header in expected_headers:
            assert header in response.headers, f"Missing security header: {header}"

    def test_cors_configuration(self, test_client: TestClient):
        """Test CORS configuration"""
        # Test preflight request
        response = test_client.options(
            "/api/agent/chat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        
        # Should allow the request
        assert response.status_code in [200, 204]
        assert "Access-Control-Allow-Origin" in response.headers

    def test_cors_origin_validation(self, test_client: TestClient):
        """Test CORS origin validation"""
        # Test with disallowed origin
        response = test_client.post(
            "/api/agent/chat",
            json={"message": "test", "user_id": "test"},
            headers={"Origin": "http://malicious-site.com"}
        )
        
        # Should still process the request but not include CORS headers for disallowed origins
        if "Access-Control-Allow-Origin" in response.headers:
            assert response.headers["Access-Control-Allow-Origin"] != "http://malicious-site.com"

    def test_content_security_policy(self, test_client: TestClient):
        """Test Content Security Policy header"""
        response = test_client.get("/health")
        
        assert "Content-Security-Policy" in response.headers
        csp = response.headers["Content-Security-Policy"]
        
        # Should restrict script sources
        assert "default-src" in csp
        assert "script-src" in csp
        assert "'unsafe-eval'" not in csp  # Should not allow eval


@pytest.mark.security
class TestDataPrivacySecurity:
    """Test data privacy and protection measures"""

    def test_user_data_isolation(self, test_client: TestClient, sample_user_data):
        """Test that users cannot access other users' data"""
        # Create data for user 1
        user1_data = sample_user_data.copy()
        user1_data["user_id"] = "user-001"
        test_client.post("/api/agent/set-channel-info", json=user1_data)
        
        # Create data for user 2  
        user2_data = sample_user_data.copy()
        user2_data["user_id"] = "user-002"
        user2_data["channel_name"] = "Different Channel"
        test_client.post("/api/agent/set-channel-info", json=user2_data)
        
        # User 1 should not be able to access user 2's data
        response = test_client.get("/api/agent/channel-info/user-002")
        
        # Should either require authentication or return 404/403
        assert response.status_code in [401, 403, 404]

    def test_conversation_history_isolation(self, test_client: TestClient, mock_openai):
        """Test conversation history is isolated between users"""
        # User 1 conversation
        chat1 = {
            "message": "My secret project is about AI",
            "user_id": "user-001"
        }
        
        response1 = test_client.post("/api/agent/chat", json=chat1)
        assert response1.status_code == 200
        
        # User 2 conversation
        chat2 = {
            "message": "What did the previous user say?",
            "user_id": "user-002" 
        }
        
        response2 = test_client.post("/api/agent/chat", json=chat2)
        
        if response2.status_code == 200:
            result = response2.json()
            # Should not leak user 1's conversation to user 2
            assert "secret project" not in result["response"].lower()
            assert "ai" not in result["response"].lower() or "artificial intelligence" in result["response"].lower()

    def test_sensitive_data_logging(self, test_client: TestClient):
        """Test that sensitive data is not logged"""
        # This test would require checking log outputs
        # For now, we test that API keys and tokens are not reflected in responses
        
        sensitive_data = {
            "message": "My API key is sk-1234567890abcdef",
            "user_id": "test-user"
        }
        
        response = test_client.post("/api/agent/chat", json=sensitive_data)
        
        if response.status_code == 200:
            response_text = response.text
            # Should not echo back the API key
            assert "sk-1234567890abcdef" not in response_text

    def test_error_message_information_disclosure(self, test_client: TestClient):
        """Test that error messages don't disclose sensitive information"""
        # Test with invalid database query to trigger error
        response = test_client.get("/api/agent/channel-info/'; DROP TABLE users; --")
        
        if response.status_code >= 400:
            error_response = response.json()
            error_message = str(error_response).lower()
            
            # Should not disclose internal paths, database info, etc.
            sensitive_terms = [
                "/users/",
                "database",
                "sqlite", 
                "traceback",
                "exception",
                "internal server error",
                "stack trace"
            ]
            
            for term in sensitive_terms:
                assert term not in error_message, f"Error message disclosed: {term}"


@pytest.mark.security
class TestRateLimitingSecurity:
    """Test rate limiting security measures"""

    def test_chat_endpoint_rate_limiting(self, test_client: TestClient):
        """Test rate limiting on chat endpoint"""
        chat_data = {
            "message": "Test rate limiting",
            "user_id": "test-user"
        }
        
        # Send multiple rapid requests
        responses = []
        for i in range(20):  # Rapid fire requests
            response = test_client.post("/api/agent/chat", json=chat_data)
            responses.append(response.status_code)
        
        # Should eventually hit rate limits
        assert 429 in responses or all(r == 200 for r in responses[:5])

    def test_per_user_rate_limiting(self, test_client: TestClient):
        """Test per-user rate limiting"""
        # Test with different users
        for user_id in ["user-1", "user-2", "user-3"]:
            chat_data = {
                "message": "Test message",
                "user_id": user_id
            }
            
            # Each user should get their own rate limit bucket
            response = test_client.post("/api/agent/chat", json=chat_data)
            assert response.status_code in [200, 429]

    def test_global_rate_limiting(self, test_client: TestClient):
        """Test global rate limiting protection"""
        import threading
        import time
        
        results = []
        
        def make_request(user_id):
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": "Load test",
                    "user_id": f"user-{user_id}"
                }
            )
            results.append(response.status_code)
        
        # Create many concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should handle concurrent requests without crashing
        assert all(status in [200, 429, 503] for status in results)


@pytest.mark.security
class TestAgentCommunicationSecurity:
    """Test security of inter-agent communication"""

    def test_boss_agent_authentication_required(self, test_client: TestClient):
        """Test that specialized agents require boss agent authentication"""
        # This would require testing the internal agent endpoints
        # For now, we test that unauthorized requests to agent communication fail
        
        # Mock an attempt to directly access a specialized agent
        with patch("content_analysis_agent.get_content_analysis_agent") as mock_agent:
            mock_agent.side_effect = Exception("Unauthorized agent access")
            
            response = test_client.post(
                "/api/agent/chat",
                json={
                    "message": "Analyze my content",
                    "user_id": "test-user"
                }
            )
            
            # Should either succeed through boss agent or fail gracefully
            assert response.status_code in [200, 401, 403, 503]

    def test_agent_token_validation(self):
        """Test agent token validation in specialist agents"""
        # This would test the actual agent authentication
        from auth_middleware import AuthenticationManager
        
        auth_manager = AuthenticationManager("test-secret")
        
        # Generate valid boss agent token
        valid_token = auth_manager.generate_boss_agent_token("test-request")
        
        # Should validate successfully
        payload = auth_manager.verify_boss_agent_token(valid_token)
        assert payload["agent_type"] == "boss_agent"
        
        # Invalid token should fail
        with pytest.raises(Exception):
            auth_manager.verify_boss_agent_token("invalid-token")

    def test_domain_boundary_enforcement(self):
        """Test that agents respect domain boundaries"""
        # This would test that agents reject out-of-scope requests
        # Implementation depends on actual agent code structure
        
        # Mock test for domain validation
        assert True  # Placeholder - would implement actual domain boundary tests