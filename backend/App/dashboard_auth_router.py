"""
Dashboard Authentication Router

Secure authentication endpoints for the production dashboard.
Uses environment variables for password configuration.
"""

import os
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt

from .config import get_settings
from .api_models import create_success_response, create_error_response
# from .rate_limiter import limiter  # Temporarily disabled

router = APIRouter(prefix="/api/dashboard", tags=["dashboard-auth"])
security = HTTPBearer(auto_error=False)

# Models
class DashboardLoginRequest(BaseModel):
    password: str

class DashboardAuthResponse(BaseModel):
    token: str
    expires_at: str

# Configuration
settings = get_settings()
TOKEN_EXPIRY_HOURS = 8

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_dashboard_password(password: str) -> bool:
    """Verify dashboard password against environment hash"""
    if not settings.dashboard_password_hash:
        # Fallback for development - hash of 'admin123'
        dev_hash = hash_password('admin123')
        return hash_password(password) == dev_hash

    return hash_password(password) == settings.dashboard_password_hash

def create_dashboard_token() -> tuple[str, datetime]:
    """Create JWT token for dashboard access"""
    now = datetime.utcnow()
    expires_at = now + timedelta(hours=TOKEN_EXPIRY_HOURS)

    payload = {
        'type': 'dashboard_access',
        'iat': int(now.timestamp()),
        'exp': int(expires_at.timestamp()),
        'jti': secrets.token_urlsafe(16)  # Unique token ID
    }

    # Use configured JWT secret or generate one
    jwt_secret = settings.dashboard_jwt_secret or secrets.token_urlsafe(32)
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return token, expires_at

def verify_dashboard_token(token: str) -> bool:
    """Verify dashboard JWT token"""
    try:
        # Use configured JWT secret or generate one
        jwt_secret = settings.dashboard_jwt_secret or secrets.token_urlsafe(32)
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return payload.get('type') == 'dashboard_access'
    except jwt.InvalidTokenError:
        return False

async def get_dashboard_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Dependency to verify dashboard authentication"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    if not verify_dashboard_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return True

@router.post("/auth", response_model=dict)
# @limiter.limit("5/minute")  # Rate limit login attempts - temporarily disabled
async def dashboard_login(password: str = Form(...)):
    """
    Authenticate dashboard access

    - **password**: Dashboard access password
    """
    try:
        if not verify_dashboard_password(password):
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        token, expires_at = create_dashboard_token()

        return create_success_response(
            "Authentication successful",
            {
                "token": token,
                "expires_at": expires_at.isoformat(),
                "type": "dashboard_access"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return create_error_response(
            error="Authentication failed",
            detail=str(e),
            status_code=500
        )

@router.get("/verify", response_model=dict)
async def verify_dashboard_token_endpoint(auth: bool = Depends(get_dashboard_auth)):
    """
    Verify dashboard token validity
    
    Requires valid dashboard token in Authorization header
    """
    return create_success_response(
        "Token is valid",
        {"authenticated": True}
    )

@router.post("/logout", response_model=dict)
async def dashboard_logout(auth: bool = Depends(get_dashboard_auth)):
    """
    Logout from dashboard (token invalidation would require token blacklist)
    
    For now, client should remove token from localStorage
    """
    return create_success_response(
        "Logout successful",
        {"message": "Please remove token from client storage"}
    )

# Platform metrics endpoint
@router.get("/metrics", response_model=dict)
async def get_platform_metrics():
    """Get comprehensive platform metrics for developer dashboard"""
    try:
        from .database import get_database_manager
        from .user_service import UserService
        import sqlite3
        import json

        # Initialize services
        db = get_database_manager()
        user_service = UserService()

        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "users": {},
            "agents": {},
            "system": {},
            "youtube": {},
            "errors": []
        }

        try:
            # Get user metrics
            with sqlite3.connect(db.db_path) as conn:
                cursor = conn.cursor()

                # Total users
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]

                # Active users (logged in last 24h) - check if column exists first
                try:
                    cursor.execute("PRAGMA table_info(users)")
                    columns = [row[1] for row in cursor.fetchall()]
                    if 'last_login' in columns:
                        cursor.execute("""
                            SELECT COUNT(*) FROM users
                            WHERE last_login > datetime('now', '-24 hours')
                        """)
                        active_users_24h = cursor.fetchone()[0]
                    else:
                        active_users_24h = 0
                except:
                    active_users_24h = 0

                # New users (registered last 7 days)
                cursor.execute("""
                    SELECT COUNT(*) FROM users
                    WHERE created_at > datetime('now', '-7 days')
                """)
                new_users_7d = cursor.fetchone()[0]

                # YouTube connected users - check if column exists
                try:
                    if 'youtube_connected' in columns:
                        cursor.execute("SELECT COUNT(*) FROM users WHERE youtube_connected = 1")
                        youtube_connected = cursor.fetchone()[0]
                    else:
                        youtube_connected = 0
                except:
                    youtube_connected = 0

                metrics["users"] = {
                    "total": total_users,
                    "active_24h": active_users_24h,
                    "new_7d": new_users_7d,
                    "youtube_connected": youtube_connected,
                    "youtube_connection_rate": round((youtube_connected / max(total_users, 1)) * 100, 1)
                }

        except Exception as e:
            metrics["errors"].append(f"User metrics error: {str(e)}")
            metrics["users"] = {"total": 0, "active_24h": 0, "new_7d": 0, "youtube_connected": 0}

        try:
            # Get agent performance metrics
            with sqlite3.connect("performance_tracking.db") as perf_conn:
                cursor = perf_conn.cursor()

                # Check if performance tables exist
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agent_performance_metrics'")
                if cursor.fetchone():
                    # Total agent requests (last 24h)
                    cursor.execute("""
                        SELECT COUNT(*) FROM agent_performance_metrics
                        WHERE timestamp > datetime('now', '-24 hours')
                    """)
                    total_requests_24h = cursor.fetchone()[0]

                    # Average response time (last 24h)
                    cursor.execute("""
                        SELECT AVG(total_latency_ms) FROM agent_performance_metrics
                        WHERE timestamp > datetime('now', '-24 hours')
                    """)
                    avg_response_time = cursor.fetchone()[0] or 0

                    # Success rate (last 24h)
                    cursor.execute("""
                        SELECT
                            COUNT(CASE WHEN status = 'success' THEN 1 END) * 100.0 / COUNT(*) as success_rate
                        FROM agent_performance_metrics
                        WHERE timestamp > datetime('now', '-24 hours')
                    """)
                    success_rate = cursor.fetchone()[0] or 100

                    # Agent usage breakdown
                    cursor.execute("""
                        SELECT agent_type, COUNT(*) as requests
                        FROM agent_performance_metrics
                        WHERE timestamp > datetime('now', '-24 hours')
                        GROUP BY agent_type
                    """)
                    agent_usage = dict(cursor.fetchall())

                    metrics["agents"] = {
                        "total_requests_24h": total_requests_24h,
                        "avg_response_time_ms": round(avg_response_time, 2),
                        "success_rate": round(success_rate, 1),
                        "agent_usage": agent_usage,
                        "status": "active" if total_requests_24h > 0 else "idle"
                    }
                else:
                    metrics["agents"] = {
                        "total_requests_24h": 0,
                        "avg_response_time_ms": 0,
                        "success_rate": 100,
                        "agent_usage": {},
                        "status": "no_data"
                    }

        except Exception as e:
            metrics["errors"].append(f"Agent metrics error: {str(e)}")
            metrics["agents"] = {"status": "error", "total_requests_24h": 0}

        # System health
        try:
            import psutil
            import os

            # Get system resources
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            metrics["system"] = {
                "status": "healthy",
                "cpu_usage": round(cpu_percent, 1),
                "memory_usage": round(memory.percent, 1),
                "disk_usage": round(disk.percent, 1),
                "uptime_hours": round((datetime.now().timestamp() - psutil.boot_time()) / 3600, 1)
            }
        except Exception as e:
            metrics["system"] = {
                "status": "unknown",
                "cpu_usage": 0,
                "memory_usage": 0,
                "disk_usage": 0,
                "error": str(e)
            }

        return create_success_response(
            "Platform metrics retrieved successfully",
            metrics
        )

    except Exception as e:
        return create_error_response(
            error="Failed to retrieve platform metrics",
            detail=str(e),
            status_code=500
        )

# Health check endpoint for dashboard
@router.get("/health", response_model=dict)
async def dashboard_health():
    """Dashboard health check"""
    return create_success_response(
        "Dashboard API is healthy",
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "auth_configured": bool(settings.dashboard_password_hash)
        }
    )
