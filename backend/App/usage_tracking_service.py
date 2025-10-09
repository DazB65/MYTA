"""
Usage Tracking Service for MYTA
Handles tracking, limiting, and monitoring of subscription usage
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple, Any
from uuid import UUID
import sqlite3
import json
from fastapi import HTTPException, status

try:
    from .logging_config import get_logger, LogCategory
except ImportError:
    # Fallback for when running from backend directory
    from logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.BUSINESS)

class UsageType:
    """Constants for different usage types"""
    AI_CONVERSATIONS = "ai_conversations"
    VIDEO_ANALYSIS = "video_analysis"
    RESEARCH_PROJECTS = "research_projects"
    GOALS = "goals"
    TASKS = "tasks"
    TEAM_MEMBERS = "team_members"
    CONTENT_PILLARS = "content_pillars"

class UsageTrackingService:
    """Service for tracking and enforcing subscription usage limits"""

    def __init__(self):
        self.logger = logger
        self.db_path = "Vidalytics.db"

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    async def track_usage(
        self,
        user_id: UUID,
        usage_type: str,
        amount: int = 1,
        cost_estimate: float = 0.0,
        metadata: Dict[str, Any] = None,
        team_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """Track usage for a user or team"""
        try:
            conn = self.get_connection()

            # Get current billing period
            period = self._get_current_billing_period()

            # Insert usage record
            cursor = conn.execute(
                """
                INSERT INTO usage_tracking (
                    user_id, team_id, usage_type, amount, cost_estimate,
                    metadata, period_start, period_end
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (str(user_id), str(team_id) if team_id else None, usage_type, amount, cost_estimate,
                 json.dumps(metadata or {}), period['period_start'], period['period_end'])
            )
            usage_id = cursor.lastrowid

            # Update usage summary
            self._update_usage_summary(conn, user_id, team_id, usage_type, amount, cost_estimate, period)

            conn.commit()

            # Check if usage exceeds limits
            usage_status = self._check_usage_limits(conn, user_id, team_id, usage_type, period)

            # Create alerts if necessary
            if usage_status['percentage_used'] >= 80:
                self._create_usage_alert(conn, user_id, team_id, usage_type, usage_status)
                conn.commit()

            conn.close()

            self.logger.info(f"Tracked usage: {usage_type} for user {user_id}, amount: {amount}")

            return {
                "usage_id": usage_id,
                "current_usage": usage_status['current_usage'],
                "limit": usage_status['limit'],
                "percentage_used": usage_status['percentage_used'],
                "remaining": usage_status['remaining']
            }

        except Exception as e:
            self.logger.error(f"Error tracking usage: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to track usage"
            )
    
    async def check_usage_limit(
        self,
        user_id: UUID,
        usage_type: str,
        team_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """Check if user/team can perform an action based on usage limits"""
        try:
            conn = self.get_connection()
            period = self._get_current_billing_period()
            usage_status = self._check_usage_limits(conn, user_id, team_id, usage_type, period)
            conn.close()

            return {
                "can_use": usage_status['remaining'] > 0 or usage_status['limit'] == -1,
                "current_usage": usage_status['current_usage'],
                "limit": usage_status['limit'],
                "percentage_used": usage_status['percentage_used'],
                "remaining": usage_status['remaining']
            }

        except Exception as e:
            self.logger.error(f"Error checking usage limit: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to check usage limit"
            )
    
    async def get_usage_summary(
        self,
        user_id: UUID,
        team_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """Get comprehensive usage summary for user/team"""
        try:
            conn = self.get_connection()
            period = self._get_current_billing_period()

            # Get user's subscription plan
            plan_id = self._get_user_plan(conn, user_id)

            # Get usage summaries for current period
            cursor = conn.execute(
                """
                SELECT usage_type, total_amount, total_cost
                FROM usage_summaries
                WHERE user_id = ?
                AND (? IS NULL OR team_id = ?)
                AND period_start = ? AND period_end = ?
                """,
                (str(user_id), str(team_id) if team_id else None, str(team_id) if team_id else None,
                 period['period_start'], period['period_end'])
            )
            summaries = cursor.fetchall()

            # Get limits for user's plan
            cursor = conn.execute(
                """
                SELECT usage_type, limit_amount
                FROM usage_limits
                WHERE plan_id = ?
                """,
                (plan_id,)
            )
            limits = cursor.fetchall()

            conn.close()

            # Combine usage and limits
            usage_data = {}
            limits_dict = {limit[0]: limit[1] for limit in limits}

            for summary in summaries:
                usage_type = summary[0]
                limit = limits_dict.get(usage_type, 0)
                current_usage = summary[1]

                usage_data[usage_type] = {
                    "current_usage": current_usage,
                    "limit": limit,
                    "cost": float(summary[2]),
                    "percentage_used": (current_usage / limit * 100) if limit > 0 else 0,
                    "remaining": max(0, limit - current_usage) if limit > 0 else -1
                }

            # Add zero usage for types not yet used
            for usage_type, limit in limits_dict.items():
                if usage_type not in usage_data:
                    usage_data[usage_type] = {
                        "current_usage": 0,
                        "limit": limit,
                        "cost": 0.0,
                        "percentage_used": 0,
                        "remaining": limit if limit > 0 else -1
                    }

            return {
                "period_start": period['period_start'],
                "period_end": period['period_end'],
                "plan_id": plan_id,
                "usage": usage_data,
                "total_cost": sum(data['cost'] for data in usage_data.values())
            }

        except Exception as e:
            self.logger.error(f"Error getting usage summary: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get usage summary"
            )
    
    async def get_usage_alerts(
        self,
        user_id: UUID,
        team_id: Optional[UUID] = None,
        unread_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get usage alerts for user/team"""
        try:
            conn = self.get_connection()

            query = """
                SELECT id, usage_type, alert_type, current_usage, usage_limit,
                       percentage_used, message, is_read, created_at
                FROM usage_alerts
                WHERE user_id = ?
                AND (? IS NULL OR team_id = ?)
            """
            params = [str(user_id), str(team_id) if team_id else None, str(team_id) if team_id else None]

            if unread_only:
                query += " AND is_read = 0"

            query += " ORDER BY created_at DESC LIMIT 50"

            cursor = conn.execute(query, params)
            alerts = cursor.fetchall()
            conn.close()

            return [
                {
                    "id": str(alert[0]),
                    "usage_type": alert[1],
                    "alert_type": alert[2],
                    "current_usage": alert[3],
                    "usage_limit": alert[4],
                    "percentage_used": float(alert[5]),
                    "message": alert[6],
                    "is_read": bool(alert[7]),
                    "created_at": alert[8]
                }
                for alert in alerts
            ]

        except Exception as e:
            self.logger.error(f"Error getting usage alerts: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get usage alerts"
            )
    
    async def mark_alert_read(self, alert_id: str, user_id: UUID) -> bool:
        """Mark a usage alert as read"""
        try:
            conn = self.get_connection()

            cursor = conn.execute(
                """
                UPDATE usage_alerts
                SET is_read = 1
                WHERE id = ? AND user_id = ?
                """,
                (alert_id, str(user_id))
            )

            conn.commit()
            success = cursor.rowcount > 0
            conn.close()

            return success

        except Exception as e:
            self.logger.error(f"Error marking alert as read: {e}")
            return False
    
    # Private helper methods

    def _get_current_billing_period(self) -> Dict[str, str]:
        """Get current billing period"""
        # For now, use calendar month. In production, use actual billing cycle
        today = date.today()
        period_start = today.replace(day=1)

        # Get last day of month
        if today.month == 12:
            period_end = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            period_end = date(today.year, today.month + 1, 1) - timedelta(days=1)

        return {
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat()
        }
    
    def _get_user_plan(self, conn, user_id: UUID) -> str:
        """Get user's current subscription plan"""
        # TODO: Implement actual subscription lookup
        # For now, return mock data based on user_id for testing
        return "solo_pro"  # or "solo", "teams"

    def _update_usage_summary(self, conn, user_id: UUID, team_id: Optional[UUID],
                             usage_type: str, amount: int, cost_estimate: float, period: Dict[str, str]):
        """Update usage summary for the current period"""
        try:
            # Check if summary exists
            cursor = conn.execute(
                """
                SELECT total_amount, total_cost FROM usage_summaries
                WHERE user_id = ? AND (team_id = ? OR (team_id IS NULL AND ? IS NULL))
                AND usage_type = ? AND period_start = ? AND period_end = ?
                """,
                (str(user_id), str(team_id) if team_id else None, str(team_id) if team_id else None,
                 usage_type, period['period_start'], period['period_end'])
            )

            existing = cursor.fetchone()

            if existing:
                # Update existing summary
                new_amount = existing[0] + amount
                new_cost = existing[1] + cost_estimate
                conn.execute(
                    """
                    UPDATE usage_summaries
                    SET total_amount = ?, total_cost = ?, last_updated = datetime('now')
                    WHERE user_id = ? AND (team_id = ? OR (team_id IS NULL AND ? IS NULL))
                    AND usage_type = ? AND period_start = ? AND period_end = ?
                    """,
                    (new_amount, new_cost, str(user_id), str(team_id) if team_id else None,
                     str(team_id) if team_id else None, usage_type, period['period_start'], period['period_end'])
                )
            else:
                # Insert new summary
                conn.execute(
                    """
                    INSERT INTO usage_summaries (
                        user_id, team_id, usage_type, total_amount, total_cost,
                        period_start, period_end, last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
                    """,
                    (str(user_id), str(team_id) if team_id else None, usage_type, amount, cost_estimate,
                     period['period_start'], period['period_end'])
                )
        except Exception as e:
            self.logger.error(f"Error updating usage summary: {e}")

    def _check_usage_limits(self, conn, user_id: UUID, team_id: Optional[UUID],
                           usage_type: str, period: Dict[str, str]) -> Dict[str, Any]:
        """Check current usage against limits"""
        plan_id = self._get_user_plan(conn, user_id)

        # Get current usage
        cursor = conn.execute(
            """
            SELECT COALESCE(total_amount, 0)
            FROM usage_summaries
            WHERE user_id = ? AND (team_id = ? OR (team_id IS NULL AND ? IS NULL))
            AND usage_type = ? AND period_start = ? AND period_end = ?
            """,
            (str(user_id), str(team_id) if team_id else None, str(team_id) if team_id else None,
             usage_type, period['period_start'], period['period_end'])
        )

        result = cursor.fetchone()
        current_usage = result[0] if result else 0

        # Get limit
        cursor = conn.execute(
            """
            SELECT limit_amount FROM usage_limits
            WHERE plan_id = ? AND usage_type = ?
            """,
            (plan_id, usage_type)
        )

        limit_result = cursor.fetchone()
        limit = limit_result[0] if limit_result else 0

        # Calculate metrics
        if limit == -1:  # Unlimited
            percentage_used = 0
            remaining = -1
        else:
            percentage_used = (current_usage / limit * 100) if limit > 0 else 100
            remaining = max(0, limit - current_usage)

        return {
            "current_usage": current_usage,
            "limit": limit,
            "percentage_used": percentage_used,
            "remaining": remaining
        }

    def _create_usage_alert(self, conn, user_id: UUID, team_id: Optional[UUID],
                           usage_type: str, usage_status: Dict[str, Any]):
        """Create usage alert when approaching limits"""
        percentage = usage_status['percentage_used']

        if percentage >= 100:
            alert_type = "limit_reached"
            message = f"You've reached your {usage_type.replace('_', ' ')} limit for this billing period."
        elif percentage >= 90:
            alert_type = "warning"
            message = f"You've used {percentage:.0f}% of your {usage_type.replace('_', ' ')} limit."
        else:
            alert_type = "warning"
            message = f"You've used {percentage:.0f}% of your {usage_type.replace('_', ' ')} limit."

        # Check if similar alert already exists (within last 24 hours)
        cursor = conn.execute(
            """
            SELECT id FROM usage_alerts
            WHERE user_id = ? AND usage_type = ? AND alert_type = ?
            AND datetime(created_at) > datetime('now', '-24 hours')
            """,
            (str(user_id), usage_type, alert_type)
        )

        existing = cursor.fetchone()

        if not existing:
            conn.execute(
                """
                INSERT INTO usage_alerts (
                    user_id, team_id, usage_type, alert_type, current_usage,
                    usage_limit, percentage_used, message
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (str(user_id), str(team_id) if team_id else None, usage_type, alert_type,
                 usage_status['current_usage'], usage_status['limit'], percentage, message)
            )
    
    async def _check_usage_limits(
        self, 
        conn, 
        user_id: UUID, 
        team_id: Optional[UUID], 
        usage_type: str
    ) -> Dict[str, Any]:
        """Check current usage against limits"""
        period = await self._get_current_billing_period(conn)
        plan_id = await self._get_user_plan(conn, user_id)
        
        # Get current usage
        current_usage = await conn.fetchval(
            """
            SELECT COALESCE(total_amount, 0)
            FROM usage_summaries
            WHERE user_id = $1 
            AND ($2::UUID IS NULL OR team_id = $2)
            AND usage_type = $3
            AND period_start = $4 AND period_end = $5
            """,
            user_id, team_id, usage_type, period['period_start'], period['period_end']
        ) or 0
        
        # Get limit
        limit = await conn.fetchval(
            """
            SELECT limit_amount
            FROM usage_limits
            WHERE plan_id = $1 AND usage_type = $2
            """,
            plan_id, usage_type
        ) or 0
        
        # Calculate metrics
        if limit == -1:  # Unlimited
            percentage_used = 0
            remaining = -1
        else:
            percentage_used = (current_usage / limit * 100) if limit > 0 else 100
            remaining = max(0, limit - current_usage)
        
        return {
            "current_usage": current_usage,
            "limit": limit,
            "percentage_used": percentage_used,
            "remaining": remaining
        }
    
    async def _create_usage_alert(
        self,
        conn,
        user_id: UUID,
        team_id: Optional[UUID],
        usage_type: str,
        usage_status: Dict[str, Any]
    ):
        """Create usage alert when approaching limits"""
        percentage = usage_status['percentage_used']
        
        if percentage >= 100:
            alert_type = "limit_reached"
            message = f"You've reached your {usage_type.replace('_', ' ')} limit for this billing period."
        elif percentage >= 90:
            alert_type = "warning"
            message = f"You've used {percentage:.0f}% of your {usage_type.replace('_', ' ')} limit."
        else:
            alert_type = "warning"
            message = f"You've used {percentage:.0f}% of your {usage_type.replace('_', ' ')} limit."
        
        # Check if similar alert already exists
        existing = await conn.fetchval(
            """
            SELECT id FROM usage_alerts
            WHERE user_id = $1 AND usage_type = $2 AND alert_type = $3
            AND created_at > NOW() - INTERVAL '24 hours'
            """,
            user_id, usage_type, alert_type
        )
        
        if not existing:
            await conn.execute(
                """
                INSERT INTO usage_alerts (
                    user_id, team_id, usage_type, alert_type, current_usage,
                    usage_limit, percentage_used, message
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                user_id, team_id, usage_type, alert_type,
                usage_status['current_usage'], usage_status['limit'],
                percentage, message
            )

# Global service instance
usage_tracking_service = UsageTrackingService()

def get_usage_tracking_service() -> UsageTrackingService:
    """Get the global usage tracking service instance"""
    return usage_tracking_service
