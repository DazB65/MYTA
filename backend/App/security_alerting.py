"""
Security Alerting System for MYTA Application
Monitors security events and sends alerts for critical incidents
"""

import os
import json
import logging
import asyncio
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass, asdict
import httpx

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of security alerts"""
    AUTHENTICATION_FAILURE = "auth_failure"
    RATE_LIMIT_EXCEEDED = "rate_limit"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    API_KEY_ISSUE = "api_key_issue"
    SYSTEM_ERROR = "system_error"
    SECURITY_SCAN_FAILURE = "security_scan_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    DATA_BREACH_ATTEMPT = "data_breach_attempt"


@dataclass
class SecurityAlert:
    """Security alert data structure"""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    description: str
    timestamp: datetime
    source: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        data = asdict(self)
        data['alert_type'] = self.alert_type.value
        data['severity'] = self.severity.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


class SecurityAlerting:
    """Main security alerting system"""
    
    def __init__(self):
        self.alert_thresholds = {
            AlertType.AUTHENTICATION_FAILURE: {
                'count': 5,
                'window_minutes': 15,
                'severity': AlertSeverity.HIGH
            },
            AlertType.RATE_LIMIT_EXCEEDED: {
                'count': 10,
                'window_minutes': 5,
                'severity': AlertSeverity.MEDIUM
            },
            AlertType.SUSPICIOUS_ACTIVITY: {
                'count': 3,
                'window_minutes': 10,
                'severity': AlertSeverity.HIGH
            },
            AlertType.API_KEY_ISSUE: {
                'count': 1,
                'window_minutes': 1,
                'severity': AlertSeverity.CRITICAL
            }
        }
        
        self.recent_alerts = []
        self.alert_cooldown = {}  # Prevent spam
        
        # Configuration
        self.email_enabled = os.getenv('SECURITY_ALERTS_EMAIL_ENABLED', 'false').lower() == 'true'
        self.slack_enabled = os.getenv('SECURITY_ALERTS_SLACK_ENABLED', 'false').lower() == 'true'
        self.webhook_enabled = os.getenv('SECURITY_ALERTS_WEBHOOK_ENABLED', 'false').lower() == 'true'
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.alert_email_from = os.getenv('ALERT_EMAIL_FROM', 'security@myta.com')
        self.alert_email_to = os.getenv('ALERT_EMAIL_TO', 'admin@myta.com').split(',')
        
        # Slack configuration
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
        
        # Generic webhook configuration
        self.webhook_url = os.getenv('SECURITY_WEBHOOK_URL', '')
    
    def generate_alert_id(self) -> str:
        """Generate unique alert ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    async def create_alert(
        self,
        alert_type: AlertType,
        title: str,
        description: str,
        severity: AlertSeverity = None,
        source: str = "system",
        user_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        request_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> SecurityAlert:
        """Create a new security alert"""
        
        # Use default severity if not provided
        if severity is None:
            severity = self.alert_thresholds.get(alert_type, {}).get('severity', AlertSeverity.MEDIUM)
        
        alert = SecurityAlert(
            alert_id=self.generate_alert_id(),
            alert_type=alert_type,
            severity=severity,
            title=title,
            description=description,
            timestamp=datetime.now(),
            source=source,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
            metadata=metadata or {}
        )
        
        # Check if we should send this alert (avoid spam)
        if self._should_send_alert(alert):
            await self._send_alert(alert)
            self._record_alert(alert)
        
        return alert
    
    def _should_send_alert(self, alert: SecurityAlert) -> bool:
        """Check if alert should be sent based on thresholds and cooldown"""
        alert_key = f"{alert.alert_type.value}_{alert.ip_address or 'unknown'}"
        
        # Check cooldown
        if alert_key in self.alert_cooldown:
            last_sent = self.alert_cooldown[alert_key]
            cooldown_minutes = 30  # 30 minute cooldown for same alert type from same IP
            if datetime.now() - last_sent < timedelta(minutes=cooldown_minutes):
                logger.debug(f"Alert {alert_key} in cooldown period")
                return False
        
        # Check thresholds for certain alert types
        threshold_config = self.alert_thresholds.get(alert.alert_type)
        if threshold_config:
            count_threshold = threshold_config['count']
            window_minutes = threshold_config['window_minutes']
            
            # Count recent similar alerts
            cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
            similar_alerts = [
                a for a in self.recent_alerts
                if (a.alert_type == alert.alert_type and
                    a.timestamp > cutoff_time and
                    a.ip_address == alert.ip_address)
            ]
            
            if len(similar_alerts) < count_threshold - 1:  # -1 because current alert will be added
                logger.debug(f"Alert threshold not met: {len(similar_alerts) + 1}/{count_threshold}")
                return False
        
        return True
    
    def _record_alert(self, alert: SecurityAlert):
        """Record alert for threshold tracking"""
        self.recent_alerts.append(alert)
        
        # Clean up old alerts (keep last 1000 or last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.recent_alerts = [
            a for a in self.recent_alerts[-1000:]
            if a.timestamp > cutoff_time
        ]
        
        # Update cooldown
        alert_key = f"{alert.alert_type.value}_{alert.ip_address or 'unknown'}"
        self.alert_cooldown[alert_key] = datetime.now()
    
    async def _send_alert(self, alert: SecurityAlert):
        """Send alert through configured channels"""
        logger.info(f"Sending security alert: {alert.title} (Severity: {alert.severity.value})")
        
        # Send to all configured channels
        tasks = []
        
        if self.email_enabled:
            tasks.append(self._send_email_alert(alert))
        
        if self.slack_enabled:
            tasks.append(self._send_slack_alert(alert))
        
        if self.webhook_enabled:
            tasks.append(self._send_webhook_alert(alert))
        
        # Execute all notifications concurrently
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Log any failures
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Alert notification failed: {result}")
    
    async def _send_email_alert(self, alert: SecurityAlert):
        """Send alert via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.alert_email_from
            msg['To'] = ', '.join(self.alert_email_to)
            msg['Subject'] = f"🚨 MYTA Security Alert: {alert.title}"
            
            # Create email body
            body = self._format_email_body(alert)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_username and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            logger.info(f"Email alert sent for {alert.alert_id}")
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            raise
    
    async def _send_slack_alert(self, alert: SecurityAlert):
        """Send alert to Slack"""
        try:
            if not self.slack_webhook_url:
                logger.warning("Slack webhook URL not configured")
                return
            
            # Format Slack message
            color = {
                AlertSeverity.LOW: "#36a64f",
                AlertSeverity.MEDIUM: "#ff9500",
                AlertSeverity.HIGH: "#ff0000",
                AlertSeverity.CRITICAL: "#8B0000"
            }.get(alert.severity, "#808080")
            
            payload = {
                "attachments": [{
                    "color": color,
                    "title": f"🚨 Security Alert: {alert.title}",
                    "text": alert.description,
                    "fields": [
                        {"title": "Severity", "value": alert.severity.value.upper(), "short": True},
                        {"title": "Type", "value": alert.alert_type.value, "short": True},
                        {"title": "Source", "value": alert.source, "short": True},
                        {"title": "Time", "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), "short": True}
                    ],
                    "footer": f"Alert ID: {alert.alert_id}",
                    "ts": int(alert.timestamp.timestamp())
                }]
            }
            
            if alert.ip_address:
                payload["attachments"][0]["fields"].append({
                    "title": "IP Address", "value": alert.ip_address, "short": True
                })
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.slack_webhook_url, json=payload)
                response.raise_for_status()
            
            logger.info(f"Slack alert sent for {alert.alert_id}")
            
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            raise
    
    async def _send_webhook_alert(self, alert: SecurityAlert):
        """Send alert to generic webhook"""
        try:
            if not self.webhook_url:
                logger.warning("Webhook URL not configured")
                return
            
            payload = alert.to_dict()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
            
            logger.info(f"Webhook alert sent for {alert.alert_id}")
            
        except Exception as e:
            logger.error(f"Failed to send webhook alert: {e}")
            raise
    
    def _format_email_body(self, alert: SecurityAlert) -> str:
        """Format email body for alert"""
        severity_color = {
            AlertSeverity.LOW: "#28a745",
            AlertSeverity.MEDIUM: "#ffc107",
            AlertSeverity.HIGH: "#fd7e14",
            AlertSeverity.CRITICAL: "#dc3545"
        }.get(alert.severity, "#6c757d")
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <div style="border-left: 4px solid {severity_color}; padding-left: 20px;">
                <h2 style="color: {severity_color};">🚨 MYTA Security Alert</h2>
                <h3>{alert.title}</h3>
                <p><strong>Description:</strong> {alert.description}</p>
                
                <table style="border-collapse: collapse; width: 100%; margin-top: 20px;">
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Alert ID</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.alert_id}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Severity</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6; color: {severity_color};">
                            <strong>{alert.severity.value.upper()}</strong>
                        </td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Type</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.alert_type.value}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Source</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.source}</td>
                    </tr>
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Timestamp</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")}</td>
                    </tr>
        """
        
        if alert.ip_address:
            body += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>IP Address</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.ip_address}</td>
                    </tr>
            """
        
        if alert.user_id:
            body += f"""
                    <tr style="background-color: #f8f9fa;">
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>User ID</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.user_id}</td>
                    </tr>
            """
        
        if alert.request_id:
            body += f"""
                    <tr>
                        <td style="padding: 8px; border: 1px solid #dee2e6;"><strong>Request ID</strong></td>
                        <td style="padding: 8px; border: 1px solid #dee2e6;">{alert.request_id}</td>
                    </tr>
            """
        
        body += """
                </table>
                
                <div style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
                    <h4>Recommended Actions:</h4>
                    <ul>
                        <li>Review the security logs for additional context</li>
                        <li>Check if this is part of a larger attack pattern</li>
                        <li>Consider blocking the IP address if malicious activity is confirmed</li>
                        <li>Update security policies if necessary</li>
                    </ul>
                </div>
                
                <p style="margin-top: 20px; font-size: 12px; color: #6c757d;">
                    This is an automated security alert from the MYTA application monitoring system.
                </p>
            </div>
        </body>
        </html>
        """
        
        return body


# Global instance
security_alerting = SecurityAlerting()


# Convenience functions for common alerts
async def alert_authentication_failure(user_id: str = None, ip_address: str = None, 
                                     user_agent: str = None, request_id: str = None):
    """Alert for authentication failures"""
    await security_alerting.create_alert(
        alert_type=AlertType.AUTHENTICATION_FAILURE,
        title="Authentication Failure Detected",
        description=f"Failed authentication attempt from IP {ip_address or 'unknown'}",
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        request_id=request_id
    )


async def alert_rate_limit_exceeded(ip_address: str = None, endpoint: str = None, 
                                  request_id: str = None):
    """Alert for rate limit exceeded"""
    await security_alerting.create_alert(
        alert_type=AlertType.RATE_LIMIT_EXCEEDED,
        title="Rate Limit Exceeded",
        description=f"Rate limit exceeded for endpoint {endpoint or 'unknown'} from IP {ip_address or 'unknown'}",
        ip_address=ip_address,
        request_id=request_id,
        metadata={"endpoint": endpoint}
    )


async def alert_suspicious_activity(description: str, ip_address: str = None, 
                                  user_id: str = None, request_id: str = None, 
                                  metadata: Dict[str, Any] = None):
    """Alert for suspicious activity"""
    await security_alerting.create_alert(
        alert_type=AlertType.SUSPICIOUS_ACTIVITY,
        title="Suspicious Activity Detected",
        description=description,
        severity=AlertSeverity.HIGH,
        user_id=user_id,
        ip_address=ip_address,
        request_id=request_id,
        metadata=metadata
    )


async def alert_api_key_issue(description: str, severity: AlertSeverity = AlertSeverity.CRITICAL):
    """Alert for API key issues"""
    await security_alerting.create_alert(
        alert_type=AlertType.API_KEY_ISSUE,
        title="API Key Security Issue",
        description=description,
        severity=severity,
        source="api_key_monitor"
    )
