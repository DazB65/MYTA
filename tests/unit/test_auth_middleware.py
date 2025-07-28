"""
Unit tests for authentication middleware
"""
import pytest
import jwt
import secrets
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from auth_middleware import AuthenticationManager, AuthError


class TestAuthenticationManager:
    """Test AuthenticationManager functionality"""

    def setup_method(self):
        """Set up test instance"""
        self.secret_key = secrets.token_urlsafe(32)
        self.auth_manager = AuthenticationManager(self.secret_key)

    def test_initialization(self):
        """Test AuthenticationManager initialization"""
        assert self.auth_manager.secret_key == self.secret_key
        assert self.auth_manager.algorithm == "HS256"
        assert self.auth_manager.token_expiry_hours == 4

    def test_generate_auth_token(self):
        """Test JWT token generation"""
        user_id = "test-user-123"
        session_id = "test-session-456"
        
        token = self.auth_manager.generate_auth_token(user_id, session_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token to verify contents
        decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        assert decoded["user_id"] == user_id
        assert decoded["session_id"] == session_id
        assert decoded["permissions"] == ["user"]
        assert "exp" in decoded
        assert "iat" in decoded

    def test_generate_boss_agent_token(self):
        """Test boss agent token generation"""
        request_id = "test-request-123"
        
        token = self.auth_manager.generate_boss_agent_token(request_id)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token to verify contents
        decoded = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        assert decoded["request_id"] == request_id
        assert decoded["agent_type"] == "boss_agent"
        assert decoded["permissions"] == ["agent_communication"]
        assert "exp" in decoded
        assert "iat" in decoded

    def test_verify_token_valid(self):
        """Test valid token verification"""
        user_id = "test-user-123"
        session_id = "test-session-456"
        
        token = self.auth_manager.generate_auth_token(user_id, session_id)
        payload = self.auth_manager.verify_token(token)
        
        assert payload["user_id"] == user_id
        assert payload["session_id"] == session_id
        assert payload["permissions"] == ["user"]

    def test_verify_token_expired(self):
        """Test expired token verification"""
        # Create token with past expiry
        past_time = datetime.utcnow() - timedelta(hours=1)
        payload = {
            "user_id": "test-user",
            "session_id": "test-session", 
            "permissions": ["user"],
            "exp": past_time,
            "iat": past_time - timedelta(hours=1)
        }
        
        expired_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        with pytest.raises(AuthError, match="Token has expired"):
            self.auth_manager.verify_token(expired_token)

    def test_verify_token_invalid_signature(self):
        """Test token with invalid signature"""
        wrong_secret = secrets.token_urlsafe(32)
        wrong_auth_manager = AuthenticationManager(wrong_secret)
        
        # Generate token with one secret
        token = self.auth_manager.generate_auth_token("user", "session")
        
        # Try to verify with different secret
        with pytest.raises(AuthError, match="Invalid token signature"):
            wrong_auth_manager.verify_token(token)

    def test_verify_token_malformed(self):
        """Test malformed token verification"""
        malformed_token = "not.a.valid.jwt.token"
        
        with pytest.raises(AuthError, match="Invalid token format"):
            self.auth_manager.verify_token(malformed_token)

    def test_verify_token_missing_claims(self):
        """Test token with missing required claims"""
        # Create token without required claims
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
            # Missing user_id, permissions, etc.
        }
        
        invalid_token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        
        with pytest.raises(AuthError, match="Missing required claims"):
            self.auth_manager.verify_token(invalid_token)

    def test_verify_boss_agent_token_valid(self):
        """Test valid boss agent token verification"""
        request_id = "test-request-123"
        
        token = self.auth_manager.generate_boss_agent_token(request_id)
        payload = self.auth_manager.verify_boss_agent_token(token)
        
        assert payload["request_id"] == request_id
        assert payload["agent_type"] == "boss_agent"
        assert payload["permissions"] == ["agent_communication"]

    def test_verify_boss_agent_token_wrong_type(self):
        """Test user token used for boss agent verification"""
        user_token = self.auth_manager.generate_auth_token("user", "session")
        
        with pytest.raises(AuthError, match="Invalid agent token"):
            self.auth_manager.verify_boss_agent_token(user_token)

    def test_has_permission_valid(self):
        """Test permission checking with valid permissions"""
        payload = {
            "user_id": "test-user",
            "permissions": ["user", "admin"]
        }
        
        assert self.auth_manager.has_permission(payload, "user") is True
        assert self.auth_manager.has_permission(payload, "admin") is True
        assert self.auth_manager.has_permission(payload, "super_admin") is False

    def test_has_permission_missing_permissions(self):
        """Test permission checking with missing permissions claim"""
        payload = {
            "user_id": "test-user"
            # Missing permissions
        }
        
        assert self.auth_manager.has_permission(payload, "user") is False

    def test_get_user_from_token(self):
        """Test extracting user info from token"""
        user_id = "test-user-123"
        session_id = "test-session-456"
        
        token = self.auth_manager.generate_auth_token(user_id, session_id)
        user_info = self.auth_manager.get_user_from_token(token)
        
        assert user_info["user_id"] == user_id
        assert user_info["session_id"] == session_id
        assert user_info["permissions"] == ["user"]

    def test_refresh_token(self):
        """Test token refresh functionality"""
        user_id = "test-user-123"
        session_id = "test-session-456"
        
        original_token = self.auth_manager.generate_auth_token(user_id, session_id)
        refreshed_token = self.auth_manager.refresh_token(original_token)
        
        # Tokens should be different
        assert original_token != refreshed_token
        
        # But should contain same user info
        original_payload = self.auth_manager.verify_token(original_token)
        refreshed_payload = self.auth_manager.verify_token(refreshed_token)
        
        assert original_payload["user_id"] == refreshed_payload["user_id"]
        assert original_payload["session_id"] == refreshed_payload["session_id"]
        assert original_payload["permissions"] == refreshed_payload["permissions"]
        
        # Refreshed token should have later expiry
        assert refreshed_payload["exp"] > original_payload["exp"]

    def test_blacklist_token(self):
        """Test token blacklisting"""
        token = self.auth_manager.generate_auth_token("user", "session")
        
        # Token should be valid initially
        payload = self.auth_manager.verify_token(token)
        assert payload is not None
        
        # Blacklist the token
        self.auth_manager.blacklist_token(token)
        
        # Token should now be invalid
        with pytest.raises(AuthError, match="Token has been revoked"):
            self.auth_manager.verify_token(token)

    def test_cleanup_expired_tokens(self):
        """Test cleanup of expired tokens from blacklist"""
        # Create and blacklist a token
        token = self.auth_manager.generate_auth_token("user", "session")
        self.auth_manager.blacklist_token(token)
        
        assert len(self.auth_manager.blacklisted_tokens) == 1
        
        # Mock expired token (simulate passage of time)
        with patch("jwt.decode") as mock_decode:
            mock_decode.side_effect = jwt.ExpiredSignatureError()
            self.auth_manager.cleanup_expired_tokens()
        
        # Expired token should be removed from blacklist
        assert len(self.auth_manager.blacklisted_tokens) == 0

    def test_custom_token_expiry(self):
        """Test custom token expiry time"""
        custom_auth_manager = AuthenticationManager(
            self.secret_key,
            token_expiry_hours=8
        )
        
        token = custom_auth_manager.generate_auth_token("user", "session")
        payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        
        # Check expiry is approximately 8 hours from now
        exp_time = datetime.fromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + timedelta(hours=8)
        
        # Allow 1 minute tolerance
        assert abs((exp_time - expected_exp).total_seconds()) < 60


class TestAuthError:
    """Test AuthError exception class"""

    def test_auth_error_creation(self):
        """Test AuthError exception creation"""
        error = AuthError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, Exception)

    def test_auth_error_with_details(self):
        """Test AuthError with additional details"""
        details = {"error_code": "INVALID_TOKEN", "user_id": "test"}
        error = AuthError("Test error", details)
        
        assert str(error) == "Test error"
        assert error.details == details


@pytest.mark.unit 
class TestAuthMiddlewareIntegration:
    """Test authentication middleware integration scenarios"""

    def setup_method(self):
        """Set up test environment"""
        self.secret_key = secrets.token_urlsafe(32)
        self.auth_manager = AuthenticationManager(self.secret_key)

    def test_full_authentication_flow(self):
        """Test complete authentication flow"""
        user_id = "test-user-123"
        session_id = "test-session-456"
        
        # 1. Generate token
        token = self.auth_manager.generate_auth_token(user_id, session_id)
        assert token is not None
        
        # 2. Verify token
        payload = self.auth_manager.verify_token(token)
        assert payload["user_id"] == user_id
        
        # 3. Check permissions
        assert self.auth_manager.has_permission(payload, "user") is True
        
        # 4. Get user info
        user_info = self.auth_manager.get_user_from_token(token)
        assert user_info["user_id"] == user_id
        
        # 5. Refresh token
        new_token = self.auth_manager.refresh_token(token)
        assert new_token != token
        
        # 6. Blacklist original token
        self.auth_manager.blacklist_token(token)
        
        # 7. Original token should be invalid
        with pytest.raises(AuthError):
            self.auth_manager.verify_token(token)
        
        # 8. New token should still work
        new_payload = self.auth_manager.verify_token(new_token)
        assert new_payload["user_id"] == user_id

    def test_boss_agent_authentication_flow(self):
        """Test boss agent authentication flow"""
        request_id = "test-request-123"
        
        # 1. Generate boss agent token
        token = self.auth_manager.generate_boss_agent_token(request_id)
        assert token is not None
        
        # 2. Verify boss agent token
        payload = self.auth_manager.verify_boss_agent_token(token)
        assert payload["request_id"] == request_id
        assert payload["agent_type"] == "boss_agent"
        
        # 3. Check agent permissions
        assert self.auth_manager.has_permission(payload, "agent_communication") is True
        assert self.auth_manager.has_permission(payload, "user") is False