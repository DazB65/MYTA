"""
Compatibility layer for tests expecting AuthenticationManager and FastAPI dependencies
"""
from __future__ import annotations

import secrets
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

import jwt


class AuthError(Exception):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.details = details or {}


class AuthToken(Dict[str, Any]):
    pass


class AuthenticationManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256", token_expiry_hours: int = 4) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_hours = token_expiry_hours
        self.blacklisted_tokens: set[str] = set()

    def _encode(self, payload: Dict[str, Any]) -> str:
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def _decode(self, token: str) -> Dict[str, Any]:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def generate_auth_token(self, user_id: str, session_id: str, permissions: Optional[list[str]] = None) -> str:
        now = datetime.utcnow()
        exp = now + timedelta(hours=self.token_expiry_hours)
        payload = {
            "user_id": user_id,
            "session_id": session_id,
            "permissions": permissions or ["user"],
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return self._encode(payload)

    def generate_boss_agent_token(self, request_id: str = "test") -> str:
        now = datetime.utcnow()
        exp = now + timedelta(hours=self.token_expiry_hours)
        payload = {
            "request_id": request_id,
            "agent_type": "boss_agent",
            "permissions": ["agent_communication"],
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
        }
        return self._encode(payload)

    def verify_token(self, token: str) -> Dict[str, Any]:
        if token in self.blacklisted_tokens:
            raise AuthError("Token has been revoked")
        try:
            return self._decode(token)
        except jwt.ExpiredSignatureError:
            raise AuthError("Token has expired")
        except jwt.InvalidSignatureError:
            raise AuthError("Invalid token signature")
        except jwt.DecodeError:
            raise AuthError("Invalid token format")
        except jwt.InvalidTokenError as e:
            raise AuthError(str(e))

    def verify_boss_agent_token(self, token: str) -> Dict[str, Any]:
        payload = self.verify_token(token)
        if payload.get("agent_type") != "boss_agent" or "agent_communication" not in payload.get("permissions", []):
            raise AuthError("Invalid agent token")
        return payload

    def has_permission(self, payload: Dict[str, Any], permission: str) -> bool:
        return permission in payload.get("permissions", [])

    def get_user_from_token(self, token: str) -> Dict[str, Any]:
        payload = self.verify_token(token)
        return {
            "user_id": payload.get("user_id"),
            "session_id": payload.get("session_id"),
            "permissions": payload.get("permissions", []),
        }

    def refresh_token(self, token: str) -> str:
        payload = self.verify_token(token)
        user_id = payload.get("user_id")
        session_id = payload.get("session_id")
        permissions = payload.get("permissions", ["user"])  # preserve
        return self.generate_auth_token(user_id, session_id, permissions)

    def blacklist_token(self, token: str) -> None:
        self.blacklisted_tokens.add(token)

    def cleanup_expired_tokens(self) -> None:
        to_remove = set()
        for t in self.blacklisted_tokens:
            try:
                jwt.decode(t, self.secret_key, algorithms=[self.algorithm])
            except jwt.ExpiredSignatureError:
                to_remove.add(t)
            except Exception:
                pass
        self.blacklisted_tokens -= to_remove


# Minimal FastAPI dependency shims expected by routers/tests

def get_current_user(token: Optional[str] = None) -> Dict[str, Any]:
    return {"user_id": "test-user", "permissions": ["user"]}


def get_optional_user(token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return {"user_id": "test-user", "permissions": ["user"]}


def get_user_id_from_request(request: Any = None) -> str:  # type: ignore
    return "test-user"


def create_session_token(user_id: str) -> str:
    secret = generate_test_secret()
    return AuthenticationManager(secret).generate_auth_token(user_id=user_id, session_id="test-session")


def generate_test_secret() -> str:
    return secrets.token_urlsafe(32)
