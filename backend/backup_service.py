"""
Automated Database Backup Service for Vidalytics
Handles scheduled backups, monitoring, and maintenance
"""

import os
import schedule
import threading
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

from migration_manager import get_migration_manager, BackupInfo

logger = logging.getLogger(__name__)


class BackupFrequency(Enum):
    """Backup frequency options"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class BackupSchedule:
    """Backup schedule configuration"""
    frequency: BackupFrequency
    time: str  # Format: "HH:MM" for daily/weekly/monthly, or "MM" for hourly
    enabled: bool = True
    compression: bool = True
    max_backups: int = 10
    cleanup_enabled: bool = True


@dataclass
class BackupAlert:
    """Backup alert configuration"""
    email_enabled: bool = False
    email_recipients: List[str] = None
    webhook_url: Optional[str] = None
    alert_on_failure: bool = True
    alert_on_success: bool = False
    alert_on_cleanup: bool = False


class BackupMonitor:
    """Monitor backup health and send alerts"""
    
    def __init__(self, alert_config: BackupAlert):
        self.alert_config = alert_config
    
    def send_backup_success_alert(self, backup_info: BackupInfo):
        """Send alert for successful backup"""
        if not self.alert_config.alert_on_success:
            return
        
        subject = f"Vidalytics: Backup completed successfully - {backup_info.backup_id}"
        message = self._format_success_message(backup_info)
        self._send_alert(subject, message)
    
    def send_backup_failure_alert(self, error_message: str, backup_type: str = "scheduled"):
        """Send alert for backup failure"""
        if not self.alert_config.alert_on_failure:
            return
        
        subject = f"Vidalytics: Backup failed - {backup_type}"
        message = self._format_failure_message(error_message, backup_type)
        self._send_alert(subject, message)
    
    def send_cleanup_alert(self, deleted_count: int, total_size_freed: int):
        """Send alert for backup cleanup"""
        if not self.alert_config.alert_on_cleanup:
            return
        
        subject = f"Vidalytics: Backup cleanup completed - {deleted_count} backups removed"
        message = self._format_cleanup_message(deleted_count, total_size_freed)
        self._send_alert(subject, message)
    
    def _format_success_message(self, backup_info: BackupInfo) -> str:
        """Format success alert message"""
        return f"""
Backup completed successfully!

Backup ID: {backup_info.backup_id}
Type: {backup_info.backup_type}
Size: {backup_info.size_bytes / (1024*1024):.2f} MB
Database Version: {backup_info.database_version}
Compression: {'Yes' if backup_info.compression else 'No'}
Created: {backup_info.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Location: {backup_info.file_path}

The database has been successfully backed up and is ready for recovery if needed.
"""
    
    def _format_failure_message(self, error_message: str, backup_type: str) -> str:
        """Format failure alert message"""
        return f"""
Backup failed!

Backup Type: {backup_type}
Error: {error_message}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check the Vidalytics logs for more details and resolve the issue.
This backup failure may affect data recovery capabilities.
"""
    
    def _format_cleanup_message(self, deleted_count: int, total_size_freed: int) -> str:
        """Format cleanup alert message"""
        return f"""
Backup cleanup completed.

Backups removed: {deleted_count}
Space freed: {total_size_freed / (1024*1024):.2f} MB
Cleanup time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Old backups have been automatically cleaned up to maintain storage efficiency.
"""
    
    def _send_alert(self, subject: str, message: str):
        """Send alert via configured channels"""
        try:
            # Send email alert
            if self.alert_config.email_enabled and self.alert_config.email_recipients:
                self._send_email_alert(subject, message)
            
            # Send webhook alert
            if self.alert_config.webhook_url:
                self._send_webhook_alert(subject, message)
        
        except Exception as e:
            logger.error(f"Error sending backup alert: {e}")
    
    def _send_email_alert(self, subject: str, message: str):
        """Send email alert"""
        try:
            # This would require email configuration
            # For now, just log the alert
            logger.info(f"EMAIL ALERT: {subject}\n{message}")
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")
    
    def _send_webhook_alert(self, subject: str, message: str):
        """Send webhook alert"""
        try:
            import requests
            payload = {
                "subject": subject,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "service": "Vidalytics Backup Service"
            }
            
            response = requests.post(
                self.alert_config.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            logger.info("Webhook alert sent successfully")
            
        except Exception as e:
            logger.error(f"Error sending webhook alert: {e}")


class BackupService:
    """Automated backup service with scheduling and monitoring"""
    
    def __init__(
        self,
        db_path: str,
        schedule_config: BackupSchedule,
        alert_config: BackupAlert = None
    ):
        self.db_path = db_path
        self.schedule_config = schedule_config
        self.alert_config = alert_config or BackupAlert()
        
        self.migration_manager = get_migration_manager(db_path)
        self.monitor = BackupMonitor(self.alert_config)
        
        self._running = False
        self._scheduler_thread = None
        self._setup_schedule()
    
    def start(self):
        """Start the backup service"""
        if self._running:
            logger.warning("Backup service is already running")
            return
        
        self._running = True
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        
        logger.info("Backup service started")
        logger.info(f"Schedule: {self.schedule_config.frequency.value} at {self.schedule_config.time}")
    
    def stop(self):
        """Stop the backup service"""
        if not self._running:
            return
        
        self._running = False
        schedule.clear()
        
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._scheduler_thread.join(timeout=5)
        
        logger.info("Backup service stopped")
    
    def create_manual_backup(self, metadata: Dict = None) -> Optional[str]:
        """Create a manual backup"""
        try:
            logger.info("Creating manual backup...")
            
            backup_id = self.migration_manager.create_backup(
                backup_type="manual",
                compression=self.schedule_config.compression,
                metadata=metadata or {}
            )
            
            if backup_id:
                backup_info = self.migration_manager.get_backup_info(backup_id)
                self.monitor.send_backup_success_alert(backup_info)
                logger.info(f"Manual backup created successfully: {backup_id}")
            else:
                self.monitor.send_backup_failure_alert("Manual backup creation failed", "manual")
            
            return backup_id
            
        except Exception as e:
            error_msg = f"Error creating manual backup: {e}"
            logger.error(error_msg)
            self.monitor.send_backup_failure_alert(error_msg, "manual")
            return None
    
    def _setup_schedule(self):
        """Set up backup schedule based on configuration"""
        if not self.schedule_config.enabled:
            return
        
        frequency = self.schedule_config.frequency
        time_str = self.schedule_config.time
        
        if frequency == BackupFrequency.HOURLY:
            # For hourly, time_str should be minutes (e.g., "30" for 30 minutes past the hour)
            schedule.every().hour.at(f":{time_str}").do(self._create_scheduled_backup)
        
        elif frequency == BackupFrequency.DAILY:
            # For daily, time_str should be "HH:MM"
            schedule.every().day.at(time_str).do(self._create_scheduled_backup)
        
        elif frequency == BackupFrequency.WEEKLY:
            # For weekly, assume Sunday at specified time
            schedule.every().sunday.at(time_str).do(self._create_scheduled_backup)
        
        elif frequency == BackupFrequency.MONTHLY:
            # For monthly, run on the 1st of each month
            schedule.every().day.at(time_str).do(self._check_monthly_backup)
        
        logger.info(f"Backup schedule configured: {frequency.value} at {time_str}")
    
    def _run_scheduler(self):
        """Run the backup scheduler"""
        logger.info("Backup scheduler started")
        
        while self._running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Error in backup scheduler: {e}")
                time.sleep(60)
        
        logger.info("Backup scheduler stopped")
    
    def _create_scheduled_backup(self):
        """Create a scheduled backup"""
        try:
            logger.info("Creating scheduled backup...")
            
            backup_id = self.migration_manager.create_backup(
                backup_type="automatic",
                compression=self.schedule_config.compression,
                metadata={
                    "schedule_frequency": self.schedule_config.frequency.value,
                    "schedule_time": self.schedule_config.time
                }
            )
            
            if backup_id:
                backup_info = self.migration_manager.get_backup_info(backup_id)
                self.monitor.send_backup_success_alert(backup_info)
                logger.info(f"Scheduled backup created successfully: {backup_id}")
                
                # Cleanup old backups if enabled
                if self.schedule_config.cleanup_enabled:
                    self._cleanup_old_backups()
            else:
                self.monitor.send_backup_failure_alert("Scheduled backup creation failed", "automatic")
            
        except Exception as e:
            error_msg = f"Error creating scheduled backup: {e}"
            logger.error(error_msg)
            self.monitor.send_backup_failure_alert(error_msg, "automatic")
    
    def _check_monthly_backup(self):
        """Check if monthly backup is needed"""
        today = datetime.now()
        if today.day == 1:  # First day of the month
            self._create_scheduled_backup()
    
    def _cleanup_old_backups(self):
        """Clean up old backups based on configuration"""
        try:
            # Get current backups
            backups = self.migration_manager.list_backups()
            automatic_backups = [b for b in backups if b.backup_type == "automatic"]
            
            if len(automatic_backups) <= self.schedule_config.max_backups:
                return
            
            # Sort by creation date (oldest first)
            automatic_backups.sort(key=lambda b: b.created_at)
            
            # Calculate how many to delete
            to_delete = len(automatic_backups) - self.schedule_config.max_backups
            backups_to_delete = automatic_backups[:to_delete]
            
            total_size_freed = 0
            deleted_count = 0
            
            for backup in backups_to_delete:
                if self.migration_manager.delete_backup(backup.backup_id):
                    total_size_freed += backup.size_bytes
                    deleted_count += 1
            
            if deleted_count > 0:
                self.monitor.send_cleanup_alert(deleted_count, total_size_freed)
                logger.info(f"Cleaned up {deleted_count} old automatic backups, freed {total_size_freed / (1024*1024):.2f} MB")
            
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")
    
    def get_service_status(self) -> Dict:
        """Get backup service status"""
        return {
            "running": self._running,
            "schedule": {
                "frequency": self.schedule_config.frequency.value,
                "time": self.schedule_config.time,
                "enabled": self.schedule_config.enabled,
                "compression": self.schedule_config.compression,
                "max_backups": self.schedule_config.max_backups,
                "cleanup_enabled": self.schedule_config.cleanup_enabled
            },
            "alerts": {
                "email_enabled": self.alert_config.email_enabled,
                "webhook_enabled": bool(self.alert_config.webhook_url),
                "alert_on_failure": self.alert_config.alert_on_failure,
                "alert_on_success": self.alert_config.alert_on_success
            },
            "last_check": datetime.now().isoformat()
        }
    
    def update_schedule(self, new_schedule: BackupSchedule):
        """Update backup schedule"""
        self.schedule_config = new_schedule
        
        # Clear existing schedule and set up new one
        schedule.clear()
        self._setup_schedule()
        
        logger.info(f"Backup schedule updated: {new_schedule.frequency.value} at {new_schedule.time}")
    
    def update_alerts(self, new_alert_config: BackupAlert):
        """Update alert configuration"""
        self.alert_config = new_alert_config
        self.monitor = BackupMonitor(new_alert_config)
        logger.info("Backup alert configuration updated")


class BackupHealthChecker:
    """Check backup system health and integrity"""
    
    def __init__(self, db_path: str):
        self.migration_manager = get_migration_manager(db_path)
    
    def run_health_check(self) -> Dict:
        """Run comprehensive backup health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {}
        }
        
        try:
            # Check 1: Database accessibility
            health_report["checks"]["database_accessible"] = self._check_database_access()
            
            # Check 2: Backup directory
            health_report["checks"]["backup_directory"] = self._check_backup_directory()
            
            # Check 3: Recent backups
            health_report["checks"]["recent_backups"] = self._check_recent_backups()
            
            # Check 4: Backup integrity
            health_report["checks"]["backup_integrity"] = self._check_backup_integrity()
            
            # Check 5: Storage space
            health_report["checks"]["storage_space"] = self._check_storage_space()
            
            # Check 6: Migration status
            health_report["checks"]["migration_status"] = self._check_migration_status()
            
            # Determine overall status
            failed_checks = [
                check for check, result in health_report["checks"].items()
                if not result.get("status", False)
            ]
            
            if failed_checks:
                health_report["overall_status"] = "degraded" if len(failed_checks) < 3 else "unhealthy"
                health_report["failed_checks"] = failed_checks
            
            return health_report
            
        except Exception as e:
            logger.error(f"Error running backup health check: {e}")
            health_report["overall_status"] = "error"
            health_report["error"] = str(e)
            return health_report
    
    def _check_database_access(self) -> Dict:
        """Check if database is accessible"""
        try:
            stats = self.migration_manager.get_database_stats()
            return {
                "status": True,
                "message": "Database is accessible",
                "details": {
                    "size_mb": stats.get("database_size_mb", 0),
                    "tables": stats.get("total_tables", 0)
                }
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Database access failed: {e}",
                "details": {}
            }
    
    def _check_backup_directory(self) -> Dict:
        """Check backup directory status"""
        try:
            backup_dir = self.migration_manager.backups_dir
            
            if not os.path.exists(backup_dir):
                return {
                    "status": False,
                    "message": "Backup directory does not exist",
                    "details": {"path": backup_dir}
                }
            
            if not os.access(backup_dir, os.W_OK):
                return {
                    "status": False,
                    "message": "Backup directory is not writable",
                    "details": {"path": backup_dir}
                }
            
            return {
                "status": True,
                "message": "Backup directory is accessible",
                "details": {"path": backup_dir}
            }
            
        except Exception as e:
            return {
                "status": False,
                "message": f"Backup directory check failed: {e}",
                "details": {}
            }
    
    def _check_recent_backups(self) -> Dict:
        """Check for recent backups"""
        try:
            backups = self.migration_manager.list_backups()
            
            if not backups:
                return {
                    "status": False,
                    "message": "No backups found",
                    "details": {"backup_count": 0}
                }
            
            latest_backup = backups[0]  # Backups are sorted by creation date desc
            hours_since_last = (datetime.now() - latest_backup.created_at).total_seconds() / 3600
            
            # Warning if no backup in last 48 hours
            if hours_since_last > 48:
                return {
                    "status": False,
                    "message": f"Latest backup is {hours_since_last:.1f} hours old",
                    "details": {
                        "backup_count": len(backups),
                        "latest_backup": latest_backup.backup_id,
                        "hours_since_last": hours_since_last
                    }
                }
            
            return {
                "status": True,
                "message": f"Latest backup is {hours_since_last:.1f} hours old",
                "details": {
                    "backup_count": len(backups),
                    "latest_backup": latest_backup.backup_id,
                    "hours_since_last": hours_since_last
                }
            }
            
        except Exception as e:
            return {
                "status": False,
                "message": f"Recent backup check failed: {e}",
                "details": {}
            }
    
    def _check_backup_integrity(self) -> Dict:
        """Check integrity of recent backups"""
        try:
            backups = self.migration_manager.list_backups()
            
            if not backups:
                return {
                    "status": True,
                    "message": "No backups to check",
                    "details": {}
                }
            
            # Check integrity of the 3 most recent backups
            recent_backups = backups[:3]
            integrity_results = []
            
            for backup in recent_backups:
                is_valid = self.migration_manager.verify_backup_integrity(backup.backup_id)
                integrity_results.append({
                    "backup_id": backup.backup_id,
                    "valid": is_valid
                })
            
            failed_backups = [r for r in integrity_results if not r["valid"]]
            
            if failed_backups:
                return {
                    "status": False,
                    "message": f"{len(failed_backups)} backups failed integrity check",
                    "details": {
                        "checked": len(integrity_results),
                        "failed": len(failed_backups),
                        "results": integrity_results
                    }
                }
            
            return {
                "status": True,
                "message": f"All {len(integrity_results)} recent backups passed integrity check",
                "details": {
                    "checked": len(integrity_results),
                    "results": integrity_results
                }
            }
            
        except Exception as e:
            return {
                "status": False,
                "message": f"Backup integrity check failed: {e}",
                "details": {}
            }
    
    def _check_storage_space(self) -> Dict:
        """Check available storage space"""
        try:
            backup_dir = self.migration_manager.backups_dir
            
            # Get disk usage
            statvfs = os.statvfs(backup_dir)
            total_space = statvfs.f_frsize * statvfs.f_blocks
            free_space = statvfs.f_frsize * statvfs.f_available
            used_space = total_space - free_space
            
            free_space_mb = free_space / (1024 * 1024)
            total_space_mb = total_space / (1024 * 1024)
            used_percent = (used_space / total_space) * 100
            
            # Warning if less than 1GB free or more than 90% used
            if free_space_mb < 1024 or used_percent > 90:
                return {
                    "status": False,
                    "message": f"Low disk space: {free_space_mb:.1f} MB free ({used_percent:.1f}% used)",
                    "details": {
                        "free_space_mb": round(free_space_mb, 1),
                        "total_space_mb": round(total_space_mb, 1),
                        "used_percent": round(used_percent, 1)
                    }
                }
            
            return {
                "status": True,
                "message": f"Sufficient disk space: {free_space_mb:.1f} MB free",
                "details": {
                    "free_space_mb": round(free_space_mb, 1),
                    "total_space_mb": round(total_space_mb, 1),
                    "used_percent": round(used_percent, 1)
                }
            }
            
        except Exception as e:
            return {
                "status": False,
                "message": f"Storage space check failed: {e}",
                "details": {}
            }
    
    def _check_migration_status(self) -> Dict:
        """Check database migration status"""
        try:
            current_version = self.migration_manager.get_current_version()
            pending_migrations = self.migration_manager.get_pending_migrations()
            
            if pending_migrations:
                return {
                    "status": False,
                    "message": f"{len(pending_migrations)} pending migrations",
                    "details": {
                        "current_version": current_version,
                        "pending_count": len(pending_migrations),
                        "pending_versions": [m.version for m in pending_migrations]
                    }
                }
            
            return {
                "status": True,
                "message": f"Database is up to date (version {current_version})",
                "details": {
                    "current_version": current_version,
                    "pending_count": 0
                }
            }
            
        except Exception as e:
            return {
                "status": False,
                "message": f"Migration status check failed: {e}",
                "details": {}
            }


# Global backup service instance
_backup_service: Optional[BackupService] = None


def get_backup_service(
    db_path: str = "Vidalytics.db",
    schedule_config: BackupSchedule = None,
    alert_config: BackupAlert = None
) -> BackupService:
    """Get or create global backup service instance"""
    global _backup_service
    
    if _backup_service is None:
        # Default configuration
        default_schedule = BackupSchedule(
            frequency=BackupFrequency.DAILY,
            time="02:00",  # 2 AM daily
            enabled=True,
            compression=True,
            max_backups=7,  # Keep 7 daily backups
            cleanup_enabled=True
        )
        
        default_alerts = BackupAlert(
            email_enabled=False,
            alert_on_failure=True,
            alert_on_success=False
        )
        
        _backup_service = BackupService(
            db_path=db_path,
            schedule_config=schedule_config or default_schedule,
            alert_config=alert_config or default_alerts
        )
    
    return _backup_service