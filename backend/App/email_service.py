"""
Email Service for MYTA
Handles sending team invitations, notifications, and other email communications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from datetime import datetime

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .team_models import TeamInvitation
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.BUSINESS)

# Try to import Resend, but don't fail if not installed
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend package not installed. Install with: pip install resend")


class EmailService:
    """Service for sending emails"""

    def __init__(self):
        # Email provider configuration
        self.use_resend = os.getenv("USE_RESEND", "true").lower() == "true"
        self.resend_api_key = os.getenv("RESEND_API_KEY", "")

        # SMTP configuration (fallback)
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")

        # Email settings
        self.from_email = os.getenv("FROM_EMAIL", "noreply@myta.app")
        self.from_name = os.getenv("FROM_NAME", "MYTA Team")
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")

        # Initialize Resend if configured
        if self.use_resend and self.resend_api_key and RESEND_AVAILABLE:
            resend.api_key = self.resend_api_key
            logger.info("Email service initialized with Resend")
        elif self.use_resend and not RESEND_AVAILABLE:
            logger.warning("Resend requested but not available, falling back to SMTP")
            self.use_resend = False
        else:
            logger.info("Email service initialized with SMTP")

        # Setup Jinja2 for email templates
        template_dir = os.path.join(os.path.dirname(__file__), "email_templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email using Resend or SMTP"""
        try:
            # Use Resend if configured
            if self.use_resend and self.resend_api_key and RESEND_AVAILABLE:
                return await self._send_with_resend(to_email, subject, html_content, text_content)
            else:
                return await self._send_with_smtp(to_email, subject, html_content, text_content)

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def _send_with_resend(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email using Resend API"""
        try:
            params = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }

            if text_content:
                params["text"] = text_content

            # Resend SDK is synchronous, so we run it in a thread pool
            import asyncio
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: resend.Emails.send(params))

            logger.info(f"Email sent successfully via Resend to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email via Resend to {to_email}: {e}")
            return False

    async def _send_with_smtp(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            # Add text content
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)

            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Send email
            if self.smtp_username and self.smtp_password:
                # Use authenticated SMTP
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_host,
                    port=self.smtp_port,
                    start_tls=True,
                    username=self.smtp_username,
                    password=self.smtp_password,
                )
            else:
                # For development - just log the email
                logger.info(f"EMAIL (DEV MODE): To: {to_email}, Subject: {subject}")
                logger.info(f"HTML Content: {html_content[:200]}...")
                return True

            logger.info(f"Email sent successfully via SMTP to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email via SMTP to {to_email}: {e}")
            return False
    
    async def send_team_invitation(self, invitation: TeamInvitation, team_name: str) -> bool:
        """Send team invitation email"""
        try:
            # Prepare template data
            template_data = {
                "invitation": invitation,
                "team_name": team_name,
                "invited_by_name": invitation.invited_by_name,
                "invited_by_email": invitation.invited_by_email,
                "role": invitation.role.value.title(),
                "accept_url": f"{self.base_url}/invite/accept?token={invitation.token}",
                "decline_url": f"{self.base_url}/invite/decline?token={invitation.token}",
                "expires_at": invitation.expires_at.strftime("%B %d, %Y at %I:%M %p UTC"),
                "current_year": datetime.now().year
            }
            
            # Render email templates
            html_template = self.jinja_env.get_template("team_invitation.html")
            text_template = self.jinja_env.get_template("team_invitation.txt")
            
            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)
            
            # Send email
            subject = f"You're invited to join {team_name} on MYTA"
            
            return await self.send_email(
                to_email=invitation.email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send team invitation: {e}")
            return False
    
    async def send_invitation_accepted_notification(
        self, 
        team_owner_email: str, 
        team_name: str, 
        new_member_name: str,
        new_member_email: str
    ) -> bool:
        """Notify team owner when invitation is accepted"""
        try:
            template_data = {
                "team_name": team_name,
                "new_member_name": new_member_name,
                "new_member_email": new_member_email,
                "dashboard_url": f"{self.base_url}/dashboard",
                "team_settings_url": f"{self.base_url}/settings?tab=team",
                "current_year": datetime.now().year
            }
            
            html_template = self.jinja_env.get_template("invitation_accepted.html")
            text_template = self.jinja_env.get_template("invitation_accepted.txt")
            
            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)
            
            subject = f"{new_member_name} joined your team on MYTA"
            
            return await self.send_email(
                to_email=team_owner_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send invitation accepted notification: {e}")
            return False
    
    async def send_welcome_to_team_email(
        self,
        new_member_email: str,
        new_member_name: str,
        team_name: str,
        role: str
    ) -> bool:
        """Send welcome email to new team member"""
        try:
            template_data = {
                "member_name": new_member_name,
                "team_name": team_name,
                "role": role.title(),
                "dashboard_url": f"{self.base_url}/dashboard",
                "getting_started_url": f"{self.base_url}/help/getting-started",
                "current_year": datetime.now().year
            }
            
            html_template = self.jinja_env.get_template("welcome_to_team.html")
            text_template = self.jinja_env.get_template("welcome_to_team.txt")
            
            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)
            
            subject = f"Welcome to {team_name} on MYTA!"
            
            return await self.send_email(
                to_email=new_member_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False
    
    async def send_member_removed_notification(
        self,
        removed_member_email: str,
        removed_member_name: str,
        team_name: str
    ) -> bool:
        """Notify member when they're removed from team"""
        try:
            template_data = {
                "member_name": removed_member_name,
                "team_name": team_name,
                "support_email": "support@myta.app",
                "current_year": datetime.now().year
            }

            html_template = self.jinja_env.get_template("member_removed.html")
            text_template = self.jinja_env.get_template("member_removed.txt")

            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)

            subject = f"You've been removed from {team_name} on MYTA"

            return await self.send_email(
                to_email=removed_member_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error(f"Failed to send member removed notification: {e}")
            return False

    # Authentication Email Methods

    async def send_verification_email(
        self,
        user_email: str,
        user_name: str,
        verification_token: str,
        verification_code: str
    ) -> bool:
        """Send email verification email to new user"""
        try:
            template_data = {
                "user_name": user_name,
                "verification_url": f"{self.base_url}/verify-email?token={verification_token}",
                "verification_code": verification_code,
                "current_year": datetime.now().year
            }

            html_template = self.jinja_env.get_template("email_verification.html")
            text_template = self.jinja_env.get_template("email_verification.txt")

            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)

            subject = "Verify your MYTA account"

            return await self.send_email(
                to_email=user_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            return False

    async def send_password_reset_email(
        self,
        user_email: str,
        user_name: str,
        reset_token: str
    ) -> bool:
        """Send password reset email"""
        try:
            template_data = {
                "user_name": user_name,
                "reset_url": f"{self.base_url}/reset-password?token={reset_token}",
                "current_year": datetime.now().year
            }

            html_template = self.jinja_env.get_template("password_reset.html")
            text_template = self.jinja_env.get_template("password_reset.txt")

            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)

            subject = "Reset your MYTA password"

            return await self.send_email(
                to_email=user_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")
            return False

    async def send_welcome_email(
        self,
        user_email: str,
        user_name: str
    ) -> bool:
        """Send welcome email to newly verified user"""
        try:
            template_data = {
                "user_name": user_name,
                "dashboard_url": f"{self.base_url}/dashboard",
                "help_url": f"{self.base_url}/help",
                "current_year": datetime.now().year
            }

            html_template = self.jinja_env.get_template("welcome.html")
            text_template = self.jinja_env.get_template("welcome.txt")

            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)

            subject = "Welcome to MYTA! 🎬"

            return await self.send_email(
                to_email=user_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False

    async def send_email_change_confirmation(
        self,
        new_email: str,
        user_name: str,
        old_email: str,
        confirmation_token: str
    ) -> bool:
        """Send email change confirmation to new email address"""
        try:
            template_data = {
                "user_name": user_name,
                "old_email": old_email,
                "new_email": new_email,
                "confirmation_url": f"{self.base_url}/confirm-email-change?token={confirmation_token}",
                "current_year": datetime.now().year
            }

            html_template = self.jinja_env.get_template("email_change_confirmation.html")
            text_template = self.jinja_env.get_template("email_change_confirmation.txt")

            html_content = html_template.render(**template_data)
            text_content = text_template.render(**template_data)

            subject = "Confirm your new email address - MYTA"

            return await self.send_email(
                to_email=new_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )

        except Exception as e:
            logger.error(f"Failed to send email change confirmation: {e}")
            return False


# Global email service instance
email_service = EmailService()


# Utility functions for common email operations
async def send_team_invitation_email(invitation: TeamInvitation, team_name: str) -> bool:
    """Convenience function to send team invitation"""
    return await email_service.send_team_invitation(invitation, team_name)


async def notify_invitation_accepted(
    team_owner_email: str, 
    team_name: str, 
    new_member_name: str,
    new_member_email: str
) -> bool:
    """Convenience function to notify team owner of accepted invitation"""
    return await email_service.send_invitation_accepted_notification(
        team_owner_email, team_name, new_member_name, new_member_email
    )


async def send_welcome_email(
    new_member_email: str,
    new_member_name: str,
    team_name: str,
    role: str
) -> bool:
    """Convenience function to send welcome email"""
    return await email_service.send_welcome_to_team_email(
        new_member_email, new_member_name, team_name, role
    )


async def notify_member_removed(
    removed_member_email: str,
    removed_member_name: str,
    team_name: str
) -> bool:
    """Convenience function to notify removed member"""
    return await email_service.send_member_removed_notification(
        removed_member_email, removed_member_name, team_name
    )


# Authentication email convenience functions
async def send_verification_email(
    user_email: str,
    user_name: str,
    verification_token: str,
    verification_code: str
) -> bool:
    """Convenience function to send verification email"""
    return await email_service.send_verification_email(
        user_email, user_name, verification_token, verification_code
    )


async def send_password_reset_email(
    user_email: str,
    user_name: str,
    reset_token: str
) -> bool:
    """Convenience function to send password reset email"""
    return await email_service.send_password_reset_email(
        user_email, user_name, reset_token
    )


async def send_welcome_email(
    user_email: str,
    user_name: str
) -> bool:
    """Convenience function to send welcome email"""
    return await email_service.send_welcome_email(user_email, user_name)


async def send_email_change_confirmation(
    new_email: str,
    user_name: str,
    old_email: str,
    confirmation_token: str
) -> bool:
    """Convenience function to send email change confirmation"""
    return await email_service.send_email_change_confirmation(
        new_email, user_name, old_email, confirmation_token
    )
