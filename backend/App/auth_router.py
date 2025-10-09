"""
Secure Authentication Router for Vidalytics
Implements user registration, login, logout, and password management
"""

import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address

from .auth_models import (
    UserRegistration, UserLogin, UserResponse, PasswordReset,
    PasswordResetConfirm, ChangePassword
)
from .supabase_user_service import supabase_user_service as user_service
from .auth_middleware import auth_middleware, get_current_user, AuthToken
from .rate_limiter import limiter, get_rate_limit
from .enhanced_jwt import enhanced_jwt_service
from .email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer(auto_error=False)

# Simple test endpoint without middleware complexity
@router.post("/test-register", response_model=dict)
async def test_register_user(registration: UserRegistration):
    """
    Simple test registration endpoint without complex middleware
    """
    try:
        logger.info(f"Test registration attempt for: {registration.email}")

        # Create user account directly
        user = user_service.create_user(registration)

        logger.info(f"Test user created successfully: {user.email}")

        return {
            "status": "success",
            "message": "Test user registered successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }

    except ValueError as e:
        logger.warning(f"Test registration failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        logger.error(f"Test registration error: {e}")
        return {
            "status": "error",
            "message": f"Registration failed: {str(e)}"
        }

@router.post("/register", response_model=dict)
@limiter.limit("5/minute")  # Strict rate limiting for registration
async def register_user(
    request: Request,
    registration: UserRegistration
):
    """
    Register a new user account

    - **email**: Valid email address
    - **password**: Strong password (8+ chars, uppercase, lowercase, digit, special char)
    - **name**: User's full name
    - **confirm_password**: Must match password
    """
    try:
        # Create user account with security context
        user = user_service.create_user(
            registration,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

        # Generate verification token and code
        verification_token = secrets.token_urlsafe(32)
        verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])

        # Update user with verification token
        await user_service.update_user(
            user.id,
            {
                'verification_token': verification_token,
                'verification_code': verification_code
            }
        )

        # Send verification email
        try:
            await send_verification_email(
                user_email=user.email,
                user_name=user.name,
                verification_token=verification_token,
                verification_code=verification_code
            )
            logger.info(f"Verification email sent to: {user.email}")
        except Exception as email_error:
            logger.error(f"Failed to send verification email: {email_error}")
            # Continue with registration even if email fails

        # Generate authentication token
        session_id = f"session_{user.id}_{datetime.utcnow().timestamp()}"
        token = auth_middleware.generate_auth_token(
            user_id=user.id,
            session_id=session_id,
            permissions=['read', 'write']
        )

        # Log registration
        logger.info(f"User registered: {user.email} from {request.client.host}")

        return {
            "status": "success",
            "message": "User registered successfully. Please check your email to verify your account.",
            "user": user.to_response(),
            "token": token,
            "expires_in": 28800,  # 8 hours in seconds
            "requires_verification": True
        }

    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=dict)
@limiter.limit("10/minute")  # Rate limiting for login attempts
async def login_user(
    request: Request,
    response: Response,
    login: UserLogin
):
    """
    Authenticate user and create session
    
    - **email**: User's email address
    - **password**: User's password
    - **remember_me**: Extend session duration if true
    """
    try:
        # Authenticate user with security context
        user = user_service.authenticate_user(
            login,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is verified (optional - can be enabled later)
        # if not user.is_verified:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Please verify your email address"
        #     )
        
        # Generate session tokens
        session_id = f"session_{user.id}_{datetime.utcnow().timestamp()}"
        access_token = auth_middleware.generate_auth_token(
            user_id=user.id,
            session_id=session_id,
            permissions=['read', 'write']
        )

        # Generate refresh token
        refresh_token = enhanced_jwt_service.create_refresh_token(
            user_id=user.id,
            session_id=session_id
        )

        # Set secure httpOnly cookies
        max_age = 86400 * 30 if login.remember_me else 28800  # 30 days or 8 hours
        response.set_cookie(
            key="auth_token",
            value=access_token,
            max_age=28800,  # Access token: 8 hours
            httponly=True,
            secure=True,  # HTTPS only in production
            samesite="strict"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=max_age,  # Refresh token: 8 hours or 30 days
            httponly=True,
            secure=True,
            samesite="strict"
        )
        
        # Log successful login
        logger.info(f"User logged in: {user.email} from {request.client.host}")
        
        logger.info(f"User logged in successfully: {user.email}")
        
        return {
            "status": "success",
            "message": "Login successful",
            "user": user.to_response(),
            "token": access_token,
            "expires_in": 28800  # Access token expiry
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/logout")
async def logout_user(
    request: Request,
    response: Response,
    current_user: AuthToken = Depends(get_current_user)
):
    """
    Logout user and invalidate session
    """
    try:
        # Get token from request
        token = None
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = request.cookies.get("auth_token")
        
        # Blacklist the token
        if token:
            auth_middleware.blacklist_token(token)
        
        # Clear cookies
        response.delete_cookie(
            key="auth_token",
            httponly=True,
            secure=True,
            samesite="strict"
        )
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=True,
            samesite="strict"
        )
        
        # Log logout
        logger.info(f"User logged out: {current_user.user_id} from {request.client.host}")
        
        logger.info(f"User logged out: {current_user.user_id}")
        
        return {
            "status": "success",
            "message": "Logged out successfully"
        }
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: AuthToken = Depends(get_current_user)
):
    """
    Get current user information
    """
    try:
        user = user_service.get_user_by_id(current_user.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user.to_response()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

@router.post("/change-password")
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    password_change: ChangePassword,
    current_user: AuthToken = Depends(get_current_user)
):
    """
    Change user password
    """
    try:
        user = user_service.get_user_by_id(current_user.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not user.verify_password(password_change.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.update_password(password_change.new_password)
        user_service.update_user(user)
        
        # Log password change
        logger.info(f"Password changed for user: {user.email} from {request.client.host}")
        
        logger.info(f"Password changed for user: {user.email}")
        
        return {
            "status": "success",
            "message": "Password changed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Change password error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

@router.post("/verify-token")
async def verify_token(
    current_user: AuthToken = Depends(get_current_user)
):
    """
    Verify if current token is valid
    """
    return {
        "status": "success",
        "message": "Token is valid",
        "user_id": current_user.user_id,
        "expires_at": current_user.expires_at.isoformat()
    }

@router.post("/refresh")
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    response: Response
):
    """
    Refresh access token using refresh token
    """
    try:
        # Get refresh token from cookie
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not found"
            )

        # Refresh tokens
        result = enhanced_jwt_service.refresh_access_token(refresh_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        new_access_token, new_refresh_token = result

        # Set new cookies
        response.set_cookie(
            key="auth_token",
            value=new_access_token,
            max_age=28800,  # 8 hours
            httponly=True,
            secure=True,
            samesite="strict"
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            max_age=86400 * 30,  # 30 days
            httponly=True,
            secure=True,
            samesite="strict"
        )

        logger.info("Tokens refreshed successfully")

        return {
            "status": "success",
            "message": "Tokens refreshed successfully",
            "expires_in": 28800
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


# ============================================================================
# EMAIL VERIFICATION ENDPOINTS
# ============================================================================

@router.post("/send-verification-email")
@limiter.limit("3/hour")  # Limit verification email requests
async def resend_verification_email(
    request: Request,
    current_user: AuthToken = Depends(get_current_user)
):
    """
    Resend verification email to user
    """
    try:
        # Get user from database
        user = await user_service.get_user_by_id(current_user.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Check if already verified
        if user.get('is_verified'):
            return {
                "status": "success",
                "message": "Email already verified"
            }

        # Generate new verification token and code
        verification_token = secrets.token_urlsafe(32)
        verification_code = ''.join([str(secrets.randbelow(10)) for _ in range(6)])

        # Update user with new token
        await user_service.update_user(
            user['id'],
            {
                'verification_token': verification_token,
                'verification_code': verification_code
            }
        )

        # Send verification email
        email_sent = await send_verification_email(
            user_email=user['email'],
            user_name=user['name'],
            verification_token=verification_token,
            verification_code=verification_code
        )

        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email"
            )

        logger.info(f"Verification email sent to: {user['email']}")

        return {
            "status": "success",
            "message": "Verification email sent successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Send verification email error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )


@router.post("/verify-email")
@limiter.limit("10/hour")
async def verify_email(
    request: Request,
    token: str = None,
    code: str = None
):
    """
    Verify user email with token or code

    - **token**: Verification token from email link
    - **code**: 6-digit verification code
    """
    try:
        if not token and not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either token or code is required"
            )

        # Find user by verification token or code
        if token:
            user = await user_service.get_user_by_verification_token(token)
        else:
            user = await user_service.get_user_by_verification_code(code)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token/code"
            )

        # Check if already verified
        if user.get('is_verified'):
            return {
                "status": "success",
                "message": "Email already verified"
            }

        # Mark user as verified
        await user_service.update_user(
            user['id'],
            {
                'is_verified': True,
                'verification_token': None,
                'verification_code': None
            }
        )

        # Send welcome email
        await send_welcome_email(
            user_email=user['email'],
            user_name=user['name']
        )

        logger.info(f"Email verified for user: {user['email']}")

        return {
            "status": "success",
            "message": "Email verified successfully",
            "user": {
                "id": user['id'],
                "email": user['email'],
                "name": user['name'],
                "is_verified": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed"
        )


# ============================================================================
# PASSWORD RESET ENDPOINTS
# ============================================================================

@router.post("/request-password-reset")
@limiter.limit("3/hour")  # Limit password reset requests
async def request_password_reset(
    request: Request,
    password_reset: PasswordReset
):
    """
    Request password reset email

    - **email**: User's email address
    """
    try:
        # Get user by email
        user = await user_service.get_user_by_email(password_reset.email)

        # Always return success to prevent email enumeration
        # But only send email if user exists
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            reset_token_expires = datetime.utcnow() + timedelta(hours=1)

            # Update user with reset token
            await user_service.update_user(
                user['id'],
                {
                    'reset_token': reset_token,
                    'reset_token_expires': reset_token_expires.isoformat()
                }
            )

            # Send password reset email
            email_sent = await send_password_reset_email(
                user_email=user['email'],
                user_name=user['name'],
                reset_token=reset_token
            )

            if email_sent:
                logger.info(f"Password reset email sent to: {user['email']}")
            else:
                logger.error(f"Failed to send password reset email to: {user['email']}")

        # Always return success message
        return {
            "status": "success",
            "message": "If an account exists with that email, a password reset link has been sent"
        }

    except Exception as e:
        logger.error(f"Password reset request error: {e}")
        # Still return success to prevent email enumeration
        return {
            "status": "success",
            "message": "If an account exists with that email, a password reset link has been sent"
        }


@router.post("/reset-password")
@limiter.limit("5/hour")
async def reset_password(
    request: Request,
    reset_data: PasswordResetConfirm
):
    """
    Reset password with token

    - **token**: Reset token from email
    - **new_password**: New password
    - **confirm_password**: Confirm new password
    """
    try:
        # Validate passwords match
        if reset_data.new_password != reset_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        # Find user by reset token
        user = await user_service.get_user_by_reset_token(reset_data.token)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Check if token is expired
        if user.get('reset_token_expires'):
            expires_at = datetime.fromisoformat(user['reset_token_expires'])
            if datetime.utcnow() > expires_at:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Reset token has expired"
                )

        # Update password and clear reset token
        from .auth_models import hash_password
        new_password_hash = hash_password(reset_data.new_password)

        await user_service.update_user(
            user['id'],
            {
                'password_hash': new_password_hash,
                'reset_token': None,
                'reset_token_expires': None
            }
        )

        logger.info(f"Password reset successful for user: {user['email']}")

        return {
            "status": "success",
            "message": "Password reset successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed"
        )
