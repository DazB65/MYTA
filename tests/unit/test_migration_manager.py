"""
Unit tests for database migration manager
"""
import pytest
import tempfile
import os
import shutil
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from migration_manager import (
    DatabaseMigrationManager, 
    MigrationScript, 
    MigrationInfo, 
    BackupInfo,
    get_migration_manager
)


class TestMigrationScript:
    """Test base migration script functionality"""
    
    def test_migration_script_creation(self):
        """Test creating a migration script"""
        migration = MockMigration()
        
        assert migration.version == "001"
        assert migration.name == "Test Migration"
        assert migration.description == "Test migration description"
    
    def test_migration_script_validation_default(self):
        """Test default validation returns True"""
        migration = MockMigration()
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                assert migration.validate(cursor) is True
        finally:
            os.unlink(db_path)


class TestDatabaseMigrationManager:
    """Test database migration manager"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.migrations_dir = os.path.join(self.temp_dir, "migrations")
        self.backups_dir = os.path.join(self.temp_dir, "backups")
        
        self.manager = DatabaseMigrationManager(
            db_path=self.db_path,
            migrations_dir=self.migrations_dir,
            backups_dir=self.backups_dir
        )
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test manager initialization"""
        assert self.manager.db_path == self.db_path
        assert self.manager.migrations_dir == self.migrations_dir
        assert self.manager.backups_dir == self.backups_dir
        
        # Check directories were created
        assert os.path.exists(self.migrations_dir)
        assert os.path.exists(self.backups_dir)
    
    def test_migration_tracking_tables_created(self):
        """Test migration tracking tables are created"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check migration_history table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migration_history'")
            assert cursor.fetchone() is not None
            
            # Check backup_history table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='backup_history'")
            assert cursor.fetchone() is not None
    
    def test_get_current_version_initial(self):
        """Test getting current version when no migrations applied"""
        version = self.manager.get_current_version()
        assert version == "000"
    
    def test_get_current_version_after_migration(self):
        """Test getting current version after migration"""
        # Manually insert a migration record
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO migration_history (version, name, description)
                VALUES (?, ?, ?)
            ''', ("001", "Test Migration", "Test description"))
            conn.commit()
        
        version = self.manager.get_current_version()
        assert version == "001"
    
    def test_get_pending_migrations(self):
        """Test getting pending migrations"""
        # All migrations should be pending initially
        pending = self.manager.get_pending_migrations()
        assert len(pending) > 0
        
        # Verify migrations are sorted by version
        versions = [m.version for m in pending]
        assert versions == sorted(versions)
    
    def test_migration_history_empty(self):
        """Test getting migration history when empty"""
        history = self.manager.get_migration_history()
        assert history == []
    
    def test_migration_history_with_data(self):
        """Test getting migration history with data"""
        # Insert test migration record
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO migration_history 
                (version, name, description, applied_at, execution_time, rollback_available)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("001", "Test Migration", "Test description", 
                  datetime.now().isoformat(), 1.5, True))
            conn.commit()
        
        history = self.manager.get_migration_history()
        assert len(history) == 1
        
        migration_info = history[0]
        assert migration_info.version == "001"
        assert migration_info.name == "Test Migration"
        assert migration_info.applied is True
        assert migration_info.execution_time == 1.5
        assert migration_info.rollback_available is True
    
    def test_create_backup(self):
        """Test creating a backup"""
        # Create some data in the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO test_table VALUES (1, 'test')")
            conn.commit()
        
        backup_id = self.manager.create_backup(
            backup_type="test",
            compression=False
        )
        
        assert backup_id is not None
        assert backup_id.startswith("backup_")
        
        # Verify backup file exists
        backup_info = self.manager.get_backup_info(backup_id)
        assert backup_info is not None
        assert os.path.exists(backup_info.file_path)
        assert backup_info.backup_type == "test"
        assert backup_info.compression is False
    
    def test_create_compressed_backup(self):
        """Test creating a compressed backup"""
        # Create some data
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
            conn.commit()
        
        backup_id = self.manager.create_backup(
            backup_type="test",
            compression=True
        )
        
        backup_info = self.manager.get_backup_info(backup_id)
        assert backup_info.compression is True
        assert backup_info.filename.endswith('.gz')
        assert os.path.exists(backup_info.file_path)
    
    def test_list_backups(self):
        """Test listing backups"""
        # Initially no backups
        backups = self.manager.list_backups()
        assert backups == []
        
        # Create a backup
        backup_id = self.manager.create_backup(backup_type="test")
        
        # Should have one backup
        backups = self.manager.list_backups()
        assert len(backups) == 1
        assert backups[0].backup_id == backup_id
    
    def test_verify_backup_integrity(self):
        """Test backup integrity verification"""
        backup_id = self.manager.create_backup(backup_type="test")
        
        # Backup should be valid
        is_valid = self.manager.verify_backup_integrity(backup_id)
        assert is_valid is True
        
        # Corrupt the backup file
        backup_info = self.manager.get_backup_info(backup_id)
        with open(backup_info.file_path, 'wb') as f:
            f.write(b'corrupted data')
        
        # Should now be invalid
        is_valid = self.manager.verify_backup_integrity(backup_id)
        assert is_valid is False
    
    def test_delete_backup(self):
        """Test deleting a backup"""
        backup_id = self.manager.create_backup(backup_type="test")
        
        # Backup should exist
        backup_info = self.manager.get_backup_info(backup_id)
        assert backup_info is not None
        assert os.path.exists(backup_info.file_path)
        
        # Delete backup
        success = self.manager.delete_backup(backup_id)
        assert success is True
        
        # Backup should no longer exist
        backup_info = self.manager.get_backup_info(backup_id)
        assert backup_info is None
    
    def test_cleanup_old_backups(self):
        """Test cleaning up old backups"""
        # Create multiple backups
        backup_ids = []
        for i in range(5):
            backup_id = self.manager.create_backup(backup_type="test")
            backup_ids.append(backup_id)
        
        # All backups should exist
        backups = self.manager.list_backups()
        assert len(backups) == 5
        
        # Clean up keeping only 3
        deleted_count = self.manager.cleanup_old_backups(keep_days=0, keep_count=3)
        assert deleted_count == 2
        
        # Should have 3 backups remaining
        backups = self.manager.list_backups()
        assert len(backups) == 3
    
    def test_restore_backup(self):
        """Test restoring from backup"""
        # Create initial data
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO test_table VALUES (1, 'original')")
            conn.commit()
        
        # Create backup
        backup_id = self.manager.create_backup(backup_type="test", compression=False)
        
        # Modify data
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE test_table SET name = 'modified' WHERE id = 1")
            conn.commit()
        
        # Verify data was modified
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM test_table WHERE id = 1")
            assert cursor.fetchone()[0] == "modified"
        
        # Restore backup
        success = self.manager.restore_backup(backup_id, verify_integrity=False)
        assert success is True
        
        # Verify data was restored
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM test_table WHERE id = 1")
            assert cursor.fetchone()[0] == "original"
    
    def test_get_database_stats(self):
        """Test getting database statistics"""
        # Create some test data
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
            cursor.execute("INSERT INTO test_table VALUES (1, 'test')")
            conn.commit()
        
        # Create a backup
        self.manager.create_backup(backup_type="test")
        
        stats = self.manager.get_database_stats()
        
        assert "database_path" in stats
        assert "database_size_bytes" in stats
        assert "database_size_mb" in stats
        assert "current_version" in stats
        assert "total_tables" in stats
        assert "table_counts" in stats
        assert "total_backups" in stats
        assert stats["total_backups"] == 1
        assert stats["current_version"] == "000"


class TestGlobalMigrationManager:
    """Test global migration manager function"""
    
    def test_get_migration_manager_singleton(self):
        """Test migration manager singleton behavior"""
        manager1 = get_migration_manager("test1.db")
        manager2 = get_migration_manager("test1.db")
        
        # Should return same instance for same path
        assert manager1 is manager2
    
    def test_get_migration_manager_different_paths(self):
        """Test different instances for different paths"""
        manager1 = get_migration_manager("test1.db")
        manager2 = get_migration_manager("test2.db")
        
        # Should return different instances for different paths
        assert manager1 is not manager2
        assert manager1.db_path != manager2.db_path


# Mock migration for testing
class MockMigration(MigrationScript):
    """Mock migration for testing"""
    
    def __init__(self):
        super().__init__("001", "Test Migration", "Test migration description")
    
    def up(self, cursor):
        cursor.execute("CREATE TABLE test_migration (id INTEGER)")
    
    def down(self, cursor):
        cursor.execute("DROP TABLE test_migration")
    
    def validate(self, cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_migration'")
        return cursor.fetchone() is not None


@pytest.mark.unit
class TestMigrationIntegration:
    """Integration tests for migration functionality"""
    
    def setup_method(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        
        # Create manager with mock migration
        self.manager = DatabaseMigrationManager(self.db_path)
        # Replace migrations with mock
        self.manager._migrations = [MockMigration()]
    
    def teardown_method(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_full_migration_flow(self):
        """Test complete migration flow"""
        # Initially at version 000
        assert self.manager.get_current_version() == "000"
        
        # Should have one pending migration
        pending = self.manager.get_pending_migrations()
        assert len(pending) == 1
        assert pending[0].version == "001"
        
        # Run migration
        success = self.manager.migrate(create_backup=False)
        assert success is True
        
        # Should now be at version 001
        assert self.manager.get_current_version() == "001"
        
        # No pending migrations
        pending = self.manager.get_pending_migrations()
        assert len(pending) == 0
        
        # Migration should be in history
        history = self.manager.get_migration_history()
        assert len(history) == 1
        assert history[0].version == "001"
        assert history[0].applied is True
    
    def test_migration_with_backup(self):
        """Test migration with backup creation"""
        success = self.manager.migrate(create_backup=True)
        assert success is True
        
        # Should have created a backup
        backups = self.manager.list_backups()
        assert len(backups) == 1
        assert backups[0].backup_type == "pre_migration"
    
    def test_rollback_flow(self):
        """Test rollback functionality"""
        # First migrate up
        success = self.manager.migrate(create_backup=False)
        assert success is True
        assert self.manager.get_current_version() == "001"
        
        # Rollback to version 000
        success = self.manager.rollback("000", create_backup=False)
        assert success is True
        assert self.manager.get_current_version() == "000"
        
        # Migration should no longer be in history
        history = self.manager.get_migration_history()
        assert len(history) == 0