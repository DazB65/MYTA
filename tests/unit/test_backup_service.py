"""
Unit tests for backup service
"""
import pytest
import tempfile
import os
import shutil
import time
import threading
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from backup_service import (
    BackupService,
    BackupSchedule,
    BackupAlert,
    BackupFrequency,
    BackupMonitor,
    BackupHealthChecker,
    get_backup_service
)


class TestBackupSchedule:
    """Test backup schedule configuration"""
    
    def test_backup_schedule_creation(self):
        """Test creating backup schedule"""
        schedule = BackupSchedule(
            frequency=BackupFrequency.DAILY,
            time="02:00",
            enabled=True,
            compression=True,
            max_backups=10
        )
        
        assert schedule.frequency == BackupFrequency.DAILY
        assert schedule.time == "02:00"
        assert schedule.enabled is True
        assert schedule.compression is True
        assert schedule.max_backups == 10
    
    def test_backup_schedule_defaults(self):
        """Test backup schedule with default values"""
        schedule = BackupSchedule(
            frequency=BackupFrequency.WEEKLY,
            time="03:00"
        )
        
        assert schedule.enabled is True
        assert schedule.compression is True
        assert schedule.max_backups == 10
        assert schedule.cleanup_enabled is True


class TestBackupAlert:
    """Test backup alert configuration"""
    
    def test_backup_alert_creation(self):
        """Test creating backup alert configuration"""
        alert = BackupAlert(
            email_enabled=True,
            email_recipients=["admin@example.com"],
            webhook_url="https://example.com/webhook",
            alert_on_failure=True,
            alert_on_success=False
        )
        
        assert alert.email_enabled is True
        assert alert.email_recipients == ["admin@example.com"]
        assert alert.webhook_url == "https://example.com/webhook"
        assert alert.alert_on_failure is True
        assert alert.alert_on_success is False
    
    def test_backup_alert_defaults(self):
        """Test backup alert with default values"""
        alert = BackupAlert()
        
        assert alert.email_enabled is False
        assert alert.email_recipients is None
        assert alert.webhook_url is None
        assert alert.alert_on_failure is True
        assert alert.alert_on_success is False
        assert alert.alert_on_cleanup is False


class TestBackupMonitor:
    """Test backup monitoring functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.alert_config = BackupAlert(
            email_enabled=True,
            alert_on_failure=True,
            alert_on_success=True,
            alert_on_cleanup=True
        )
        self.monitor = BackupMonitor(self.alert_config)
    
    @patch('backup_service.BackupMonitor._send_alert')
    def test_send_backup_success_alert(self, mock_send_alert):
        """Test sending backup success alert"""
        from migration_manager import BackupInfo
        
        backup_info = BackupInfo(
            backup_id="test_backup_001",
            filename="test_backup.db",
            file_path="/path/to/backup.db",
            size_bytes=1024*1024,
            created_at=datetime.now(),
            database_version="001",
            backup_type="manual",
            compression=True,
            integrity_hash="abc123",
            metadata={}
        )
        
        self.monitor.send_backup_success_alert(backup_info)
        
        mock_send_alert.assert_called_once()
        args = mock_send_alert.call_args[0]
        assert "Backup completed successfully" in args[0]
        assert "test_backup_001" in args[1]
    
    @patch('backup_service.BackupMonitor._send_alert')
    def test_send_backup_failure_alert(self, mock_send_alert):
        """Test sending backup failure alert"""
        error_message = "Database connection failed"
        
        self.monitor.send_backup_failure_alert(error_message, "scheduled")
        
        mock_send_alert.assert_called_once()
        args = mock_send_alert.call_args[0]
        assert "Backup failed" in args[0]
        assert error_message in args[1]
        assert "scheduled" in args[1]
    
    @patch('backup_service.BackupMonitor._send_alert')
    def test_send_cleanup_alert(self, mock_send_alert):
        """Test sending cleanup alert"""
        deleted_count = 5
        total_size_freed = 10 * 1024 * 1024  # 10 MB
        
        self.monitor.send_cleanup_alert(deleted_count, total_size_freed)
        
        mock_send_alert.assert_called_once()
        args = mock_send_alert.call_args[0]
        assert "Backup cleanup completed" in args[0]
        assert str(deleted_count) in args[1]
    
    def test_no_alert_when_disabled(self):
        """Test that alerts are not sent when disabled"""
        alert_config = BackupAlert(alert_on_success=False)
        monitor = BackupMonitor(alert_config)
        
        with patch('backup_service.BackupMonitor._send_alert') as mock_send_alert:
            from migration_manager import BackupInfo
            backup_info = BackupInfo(
                backup_id="test", filename="test.db", file_path="/test",
                size_bytes=1024, created_at=datetime.now(), database_version="001",
                backup_type="manual", compression=False, integrity_hash="abc",
                metadata={}
            )
            
            monitor.send_backup_success_alert(backup_info)
            mock_send_alert.assert_not_called()


class TestBackupService:
    """Test backup service functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        
        # Create a test database
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER)")
            conn.commit()
        
        self.schedule_config = BackupSchedule(
            frequency=BackupFrequency.DAILY,
            time="02:00",
            enabled=True,
            max_backups=5
        )
        
        self.alert_config = BackupAlert()
        
        self.service = BackupService(
            db_path=self.db_path,
            schedule_config=self.schedule_config,
            alert_config=self.alert_config
        )
    
    def teardown_method(self):
        """Clean up test environment"""
        if hasattr(self, 'service') and self.service._running:
            self.service.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_service_initialization(self):
        """Test service initialization"""
        assert self.service.db_path == self.db_path
        assert self.service.schedule_config == self.schedule_config
        assert self.service.alert_config == self.alert_config
        assert self.service._running is False
    
    def test_create_manual_backup(self):
        """Test creating manual backup"""
        backup_id = self.service.create_manual_backup({"test": "metadata"})
        
        assert backup_id is not None
        assert backup_id.startswith("backup_")
        
        # Verify backup exists
        backup_info = self.service.migration_manager.get_backup_info(backup_id)
        assert backup_info is not None
        assert backup_info.backup_type == "manual"
        assert backup_info.metadata["test"] == "metadata"
    
    def test_service_start_stop(self):
        """Test starting and stopping service"""
        assert self.service._running is False
        
        self.service.start()
        assert self.service._running is True
        assert self.service._scheduler_thread is not None
        
        self.service.stop()
        assert self.service._running is False
    
    def test_service_status(self):
        """Test getting service status"""
        status = self.service.get_service_status()
        
        assert "running" in status
        assert "schedule" in status
        assert "alerts" in status
        assert "last_check" in status
        
        assert status["running"] is False
        assert status["schedule"]["frequency"] == "daily"
        assert status["schedule"]["time"] == "02:00"
    
    def test_update_schedule(self):
        """Test updating backup schedule"""
        new_schedule = BackupSchedule(
            frequency=BackupFrequency.WEEKLY,
            time="03:00",
            max_backups=10
        )
        
        self.service.update_schedule(new_schedule)
        
        assert self.service.schedule_config == new_schedule
        status = self.service.get_service_status()
        assert status["schedule"]["frequency"] == "weekly"
        assert status["schedule"]["time"] == "03:00"
    
    def test_update_alerts(self):
        """Test updating alert configuration"""
        new_alerts = BackupAlert(
            email_enabled=True,
            alert_on_success=True
        )
        
        self.service.update_alerts(new_alerts)
        
        assert self.service.alert_config == new_alerts
        status = self.service.get_service_status()
        assert status["alerts"]["email_enabled"] is True
    
    @patch('schedule.every')
    def test_schedule_setup_daily(self, mock_schedule):
        """Test setting up daily schedule"""
        mock_every = Mock()
        mock_schedule.return_value = mock_every
        mock_every.day = Mock()
        mock_every.day.at = Mock()
        
        schedule_config = BackupSchedule(
            frequency=BackupFrequency.DAILY,
            time="02:00",
            enabled=True
        )
        
        service = BackupService(
            db_path=self.db_path,
            schedule_config=schedule_config,
            alert_config=self.alert_config
        )
        
        mock_every.day.at.assert_called_with("02:00")
    
    @patch('schedule.every')
    def test_schedule_setup_hourly(self, mock_schedule):
        """Test setting up hourly schedule"""
        mock_every = Mock()
        mock_schedule.return_value = mock_every
        mock_every.hour = Mock()
        mock_every.hour.at = Mock()
        
        schedule_config = BackupSchedule(
            frequency=BackupFrequency.HOURLY,
            time="30",  # 30 minutes past the hour
            enabled=True
        )
        
        service = BackupService(
            db_path=self.db_path,
            schedule_config=schedule_config,
            alert_config=self.alert_config
        )
        
        mock_every.hour.at.assert_called_with(":30")
    
    def test_cleanup_old_backups(self):
        """Test cleanup of old automatic backups"""
        # Create multiple automatic backups
        for i in range(7):
            self.service.migration_manager.create_backup(
                backup_type="automatic",
                compression=False
            )
        
        # Should have 7 backups
        backups = self.service.migration_manager.list_backups()
        automatic_backups = [b for b in backups if b.backup_type == "automatic"]
        assert len(automatic_backups) == 7
        
        # Test cleanup (service is configured to keep max 5)
        self.service._cleanup_old_backups()
        
        # Should now have 5 backups
        backups = self.service.migration_manager.list_backups()
        automatic_backups = [b for b in backups if b.backup_type == "automatic"]
        assert len(automatic_backups) == 5


class TestBackupHealthChecker:
    """Test backup health checking functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        
        # Create a test database
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER)")
            conn.commit()
        
        self.health_checker = BackupHealthChecker(self.db_path)
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_run_health_check(self):
        """Test running comprehensive health check"""
        report = self.health_checker.run_health_check()
        
        assert "timestamp" in report
        assert "overall_status" in report
        assert "checks" in report
        
        # Should have various health checks
        expected_checks = [
            "database_accessible",
            "backup_directory", 
            "recent_backups",
            "backup_integrity",
            "storage_space",
            "migration_status"
        ]
        
        for check in expected_checks:
            assert check in report["checks"]
    
    def test_database_access_check(self):
        """Test database access check"""
        result = self.health_checker._check_database_access()
        
        assert result["status"] is True
        assert "Database is accessible" in result["message"]
        assert "details" in result
    
    def test_backup_directory_check(self):
        """Test backup directory check"""
        result = self.health_checker._check_backup_directory()
        
        assert result["status"] is True
        assert "Backup directory is accessible" in result["message"]
        assert "path" in result["details"]
    
    def test_recent_backups_check_no_backups(self):
        """Test recent backups check when no backups exist"""
        result = self.health_checker._check_recent_backups()
        
        assert result["status"] is False
        assert "No backups found" in result["message"]
        assert result["details"]["backup_count"] == 0
    
    def test_recent_backups_check_with_backups(self):
        """Test recent backups check with existing backups"""
        # Create a backup
        self.health_checker.migration_manager.create_backup(backup_type="test")
        
        result = self.health_checker._check_recent_backups()
        
        assert result["status"] is True
        assert result["details"]["backup_count"] == 1
        assert "hours_since_last" in result["details"]
    
    def test_storage_space_check(self):
        """Test storage space check"""
        result = self.health_checker._check_storage_space()
        
        assert "status" in result
        assert "message" in result
        assert "details" in result
        assert "free_space_mb" in result["details"]
        assert "total_space_mb" in result["details"]
        assert "used_percent" in result["details"]
    
    def test_migration_status_check(self):
        """Test migration status check"""
        result = self.health_checker._check_migration_status()
        
        assert "status" in result
        assert "message" in result
        assert "details" in result
        assert "current_version" in result["details"]
        assert "pending_count" in result["details"]


class TestGlobalBackupService:
    """Test global backup service function"""
    
    def test_get_backup_service_singleton(self):
        """Test backup service singleton behavior"""
        service1 = get_backup_service("test1.db")
        service2 = get_backup_service("test1.db")
        
        # Should return same instance for same path
        assert service1 is service2
    
    def test_get_backup_service_with_config(self):
        """Test backup service with custom configuration"""
        schedule_config = BackupSchedule(
            frequency=BackupFrequency.WEEKLY,
            time="04:00"
        )
        
        alert_config = BackupAlert(
            email_enabled=True,
            alert_on_success=True
        )
        
        service = get_backup_service(
            db_path="test.db",
            schedule_config=schedule_config,
            alert_config=alert_config
        )
        
        assert service.schedule_config.frequency == BackupFrequency.WEEKLY
        assert service.schedule_config.time == "04:00"
        assert service.alert_config.email_enabled is True


@pytest.mark.unit
class TestBackupServiceIntegration:
    """Integration tests for backup service"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        
        # Create test database
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER, data TEXT)")
            cursor.execute("INSERT INTO test VALUES (1, 'test data')")
            conn.commit()
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_complete_backup_workflow(self):
        """Test complete backup workflow"""
        schedule_config = BackupSchedule(
            frequency=BackupFrequency.DAILY,
            time="02:00",
            max_backups=3,
            cleanup_enabled=True
        )
        
        alert_config = BackupAlert(
            alert_on_failure=True,
            alert_on_success=False
        )
        
        service = BackupService(
            db_path=self.db_path,
            schedule_config=schedule_config,
            alert_config=alert_config
        )
        
        try:
            # Create manual backup
            backup_id = service.create_manual_backup()
            assert backup_id is not None
            
            # Verify backup exists and is valid
            backup_info = service.migration_manager.get_backup_info(backup_id)
            assert backup_info is not None
            assert os.path.exists(backup_info.file_path)
            
            # Verify backup integrity
            is_valid = service.migration_manager.verify_backup_integrity(backup_id)
            assert is_valid is True
            
            # Get service status
            status = service.get_service_status()
            assert status["running"] is False
            assert status["schedule"]["max_backups"] == 3
            
            # Run health check
            health_checker = BackupHealthChecker(self.db_path)
            health_report = health_checker.run_health_check()
            assert health_report["overall_status"] in ["healthy", "degraded"]
            
        finally:
            if service._running:
                service.stop()