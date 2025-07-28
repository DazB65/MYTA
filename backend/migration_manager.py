"""
Comprehensive Database Migration and Version Management System for CreatorMate
Handles schema evolution, data migration, and backup/restore operations
"""

import os
import sqlite3
import json
import shutil
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import threading
import time
import tempfile

logger = logging.getLogger(__name__)


@dataclass
class MigrationInfo:
    """Information about a database migration"""
    version: str
    name: str
    description: str
    timestamp: datetime
    applied: bool = False
    rollback_available: bool = False
    checksum: Optional[str] = None
    execution_time: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class BackupInfo:
    """Information about a database backup"""
    backup_id: str
    filename: str
    file_path: str
    size_bytes: int
    created_at: datetime
    database_version: str
    backup_type: str  # 'manual', 'automatic', 'pre_migration'
    compression: bool
    integrity_hash: str
    metadata: Dict[str, Any]


class MigrationScript:
    """Base class for database migration scripts"""
    
    def __init__(self, version: str, name: str, description: str):
        self.version = version
        self.name = name
        self.description = description
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        """Apply the migration"""
        raise NotImplementedError("Migration scripts must implement up()")
    
    def down(self, cursor: sqlite3.Cursor) -> None:
        """Rollback the migration (optional)"""
        raise NotImplementedError("Rollback not implemented for this migration")
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        """Validate the migration was applied correctly"""
        return True


class DatabaseMigrationManager:
    """Comprehensive database migration and backup management"""
    
    def __init__(self, db_path: str, migrations_dir: str = None, backups_dir: str = None):
        self.db_path = db_path
        self.migrations_dir = migrations_dir or os.path.join(os.path.dirname(__file__), "migrations")
        self.backups_dir = backups_dir or os.path.join(os.path.dirname(db_path), "backups")
        
        # Ensure directories exist
        os.makedirs(self.migrations_dir, exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)
        
        self._lock = threading.Lock()
        self._migrations: List[MigrationScript] = []
        self._load_migrations()
        self._init_migration_tracking()
    
    def _load_migrations(self) -> None:
        """Load all migration scripts from the migrations directory"""
        self._migrations = [
            # Migration 001: Add database versioning
            Migration001_InitVersioning(),
            # Migration 002: Enhance channel info table
            Migration002_EnhanceChannelInfo(),
            # Migration 003: Add analytics tables
            Migration003_AddAnalyticsTables(),
            # Migration 004: Add user preferences
            Migration004_AddUserPreferences(),
            # Migration 005: Add content scheduling
            Migration005_AddContentScheduling(),
        ]
        
        # Sort migrations by version
        self._migrations.sort(key=lambda m: m.version)
        logger.info(f"Loaded {len(self._migrations)} migration scripts")
    
    def _init_migration_tracking(self) -> None:
        """Initialize migration tracking table"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS migration_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        description TEXT,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        execution_time REAL,
                        checksum TEXT,
                        rollback_available BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Also create backup tracking table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS backup_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        backup_id TEXT UNIQUE NOT NULL,
                        filename TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        size_bytes INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        database_version TEXT,
                        backup_type TEXT DEFAULT 'manual',
                        compression BOOLEAN DEFAULT FALSE,
                        integrity_hash TEXT,
                        metadata TEXT,
                        is_valid BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                conn.commit()
                logger.info("Migration tracking tables initialized")
                
        except Exception as e:
            logger.error(f"Error initializing migration tracking: {e}")
            raise
    
    def get_current_version(self) -> str:
        """Get the current database version"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT version FROM migration_history 
                    ORDER BY applied_at DESC 
                    LIMIT 1
                ''')
                result = cursor.fetchone()
                return result[0] if result else "000"
                
        except sqlite3.OperationalError:
            # Migration table doesn't exist yet
            return "000"
        except Exception as e:
            logger.error(f"Error getting current version: {e}")
            return "000"
    
    def get_pending_migrations(self) -> List[MigrationScript]:
        """Get list of pending migrations"""
        current_version = self.get_current_version()
        return [m for m in self._migrations if m.version > current_version]
    
    def get_migration_history(self) -> List[MigrationInfo]:
        """Get history of applied migrations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT version, name, description, applied_at, execution_time, 
                           checksum, rollback_available
                    FROM migration_history 
                    ORDER BY applied_at DESC
                ''')
                
                history = []
                for row in cursor.fetchall():
                    history.append(MigrationInfo(
                        version=row[0],
                        name=row[1],
                        description=row[2],
                        timestamp=datetime.fromisoformat(row[3]),
                        applied=True,
                        execution_time=row[4],
                        checksum=row[5],
                        rollback_available=bool(row[6])
                    ))
                
                return history
                
        except Exception as e:
            logger.error(f"Error getting migration history: {e}")
            return []
    
    def migrate(self, target_version: str = None, create_backup: bool = True) -> bool:
        """Run database migrations up to target version"""
        with self._lock:
            try:
                current_version = self.get_current_version()
                logger.info(f"Current database version: {current_version}")
                
                # Get migrations to apply
                if target_version:
                    migrations_to_apply = [
                        m for m in self._migrations 
                        if current_version < m.version <= target_version
                    ]
                else:
                    migrations_to_apply = self.get_pending_migrations()
                
                if not migrations_to_apply:
                    logger.info("No migrations to apply")
                    return True
                
                logger.info(f"Applying {len(migrations_to_apply)} migrations")
                
                # Create pre-migration backup
                if create_backup:
                    backup_id = self.create_backup(
                        backup_type="pre_migration",
                        metadata={"target_version": target_version or "latest"}
                    )
                    if backup_id:
                        logger.info(f"Created pre-migration backup: {backup_id}")
                
                # Apply migrations
                for migration in migrations_to_apply:
                    success = self._apply_migration(migration)
                    if not success:
                        logger.error(f"Migration {migration.version} failed, stopping")
                        return False
                
                logger.info("All migrations applied successfully")
                return True
                
            except Exception as e:
                logger.error(f"Error during migration: {e}")
                return False
    
    def _apply_migration(self, migration: MigrationScript) -> bool:
        """Apply a single migration"""
        start_time = time.time()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                logger.info(f"Applying migration {migration.version}: {migration.name}")
                
                # Apply the migration
                migration.up(cursor)
                
                # Validate the migration
                if not migration.validate(cursor):
                    raise Exception("Migration validation failed")
                
                # Calculate execution time and checksum
                execution_time = time.time() - start_time
                checksum = self._calculate_migration_checksum(migration)
                rollback_available = hasattr(migration, 'down') and callable(migration.down)
                
                # Record in migration history
                cursor.execute('''
                    INSERT INTO migration_history 
                    (version, name, description, execution_time, checksum, rollback_available)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    migration.version,
                    migration.name,
                    migration.description,
                    execution_time,
                    checksum,
                    rollback_available
                ))
                
                conn.commit()
                logger.info(f"Migration {migration.version} applied successfully in {execution_time:.2f}s")
                return True
                
        except Exception as e:
            logger.error(f"Error applying migration {migration.version}: {e}")
            return False
    
    def rollback(self, target_version: str, create_backup: bool = True) -> bool:
        """Rollback database to a specific version"""
        with self._lock:
            try:
                current_version = self.get_current_version()
                
                if target_version >= current_version:
                    logger.warning("Target version is not older than current version")
                    return False
                
                # Create backup before rollback
                if create_backup:
                    backup_id = self.create_backup(
                        backup_type="pre_rollback",
                        metadata={"target_version": target_version}
                    )
                    logger.info(f"Created pre-rollback backup: {backup_id}")
                
                # Get migrations to rollback (in reverse order)
                migrations_to_rollback = [
                    m for m in reversed(self._migrations)
                    if target_version < m.version <= current_version
                ]
                
                # Apply rollbacks
                for migration in migrations_to_rollback:
                    success = self._rollback_migration(migration)
                    if not success:
                        logger.error(f"Rollback of {migration.version} failed")
                        return False
                
                logger.info(f"Successfully rolled back to version {target_version}")
                return True
                
            except Exception as e:
                logger.error(f"Error during rollback: {e}")
                return False
    
    def _rollback_migration(self, migration: MigrationScript) -> bool:
        """Rollback a single migration"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                logger.info(f"Rolling back migration {migration.version}: {migration.name}")
                
                # Apply rollback
                migration.down(cursor)
                
                # Remove from migration history
                cursor.execute(
                    'DELETE FROM migration_history WHERE version = ?',
                    (migration.version,)
                )
                
                conn.commit()
                logger.info(f"Migration {migration.version} rolled back successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error rolling back migration {migration.version}: {e}")
            return False
    
    def create_backup(
        self, 
        backup_type: str = "manual", 
        compression: bool = True,
        metadata: Dict[str, Any] = None
    ) -> Optional[str]:
        """Create a database backup"""
        try:
            # Generate backup ID and filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"backup_{timestamp}_{backup_type}"
            filename = f"{backup_id}.db"
            if compression:
                filename += ".gz"
            
            backup_path = os.path.join(self.backups_dir, filename)
            
            # Create the backup
            if compression:
                import gzip
                with open(self.db_path, 'rb') as src, gzip.open(backup_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
            else:
                shutil.copy2(self.db_path, backup_path)
            
            # Calculate file size and integrity hash
            size_bytes = os.path.getsize(backup_path)
            integrity_hash = self._calculate_file_hash(backup_path)
            current_version = self.get_current_version()
            
            # Record backup in database
            backup_info = BackupInfo(
                backup_id=backup_id,
                filename=filename,
                file_path=backup_path,
                size_bytes=size_bytes,
                created_at=datetime.now(),
                database_version=current_version,
                backup_type=backup_type,
                compression=compression,
                integrity_hash=integrity_hash,
                metadata=metadata or {}
            )
            
            self._record_backup(backup_info)
            
            logger.info(f"Backup created: {backup_id} ({size_bytes} bytes)")
            return backup_id
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_id: str, verify_integrity: bool = True) -> bool:
        """Restore database from a backup"""
        with self._lock:
            try:
                # Get backup info
                backup_info = self.get_backup_info(backup_id)
                if not backup_info:
                    logger.error(f"Backup {backup_id} not found")
                    return False
                
                if not os.path.exists(backup_info.file_path):
                    logger.error(f"Backup file not found: {backup_info.file_path}")
                    return False
                
                # Verify backup integrity
                if verify_integrity:
                    if not self.verify_backup_integrity(backup_id):
                        logger.error(f"Backup {backup_id} failed integrity check")
                        return False
                
                # Create backup of current state before restore
                pre_restore_backup = self.create_backup(
                    backup_type="pre_restore",
                    metadata={"restoring_from": backup_id}
                )
                
                # Restore the backup
                temp_db_path = self.db_path + ".temp"
                
                if backup_info.compression:
                    import gzip
                    with gzip.open(backup_info.file_path, 'rb') as src, open(temp_db_path, 'wb') as dst:
                        shutil.copyfileobj(src, dst)
                else:
                    shutil.copy2(backup_info.file_path, temp_db_path)
                
                # Replace current database
                shutil.move(temp_db_path, self.db_path)
                
                logger.info(f"Database restored from backup {backup_id}")
                logger.info(f"Pre-restore backup created: {pre_restore_backup}")
                return True
                
            except Exception as e:
                logger.error(f"Error restoring backup {backup_id}: {e}")
                return False
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 10) -> int:
        """Clean up old backups based on age and count"""
        try:
            backups = self.list_backups()
            if not backups:
                return 0
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda b: b.created_at, reverse=True)
            
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            deleted_count = 0
            
            # Keep the most recent backups regardless of age
            backups_to_check = backups[keep_count:]
            
            for backup in backups_to_check:
                if backup.created_at < cutoff_date:
                    if self.delete_backup(backup.backup_id):
                        deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old backups")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return 0
    
    def delete_backup(self, backup_id: str) -> bool:
        """Delete a specific backup"""
        try:
            backup_info = self.get_backup_info(backup_id)
            if not backup_info:
                return False
            
            # Remove backup file
            if os.path.exists(backup_info.file_path):
                os.remove(backup_info.file_path)
            
            # Remove from database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'DELETE FROM backup_history WHERE backup_id = ?',
                    (backup_id,)
                )
                conn.commit()
            
            logger.info(f"Backup {backup_id} deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting backup {backup_id}: {e}")
            return False
    
    def list_backups(self) -> List[BackupInfo]:
        """List all available backups"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT backup_id, filename, file_path, size_bytes, created_at,
                           database_version, backup_type, compression, integrity_hash, metadata
                    FROM backup_history 
                    ORDER BY created_at DESC
                ''')
                
                backups = []
                for row in cursor.fetchall():
                    metadata = json.loads(row[9]) if row[9] else {}
                    backups.append(BackupInfo(
                        backup_id=row[0],
                        filename=row[1],
                        file_path=row[2],
                        size_bytes=row[3],
                        created_at=datetime.fromisoformat(row[4]),
                        database_version=row[5],
                        backup_type=row[6],
                        compression=bool(row[7]),
                        integrity_hash=row[8],
                        metadata=metadata
                    ))
                
                return backups
                
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []
    
    def get_backup_info(self, backup_id: str) -> Optional[BackupInfo]:
        """Get information about a specific backup"""
        backups = self.list_backups()
        return next((b for b in backups if b.backup_id == backup_id), None)
    
    def verify_backup_integrity(self, backup_id: str) -> bool:
        """Verify the integrity of a backup"""
        try:
            backup_info = self.get_backup_info(backup_id)
            if not backup_info or not os.path.exists(backup_info.file_path):
                return False
            
            # Calculate current hash
            current_hash = self._calculate_file_hash(backup_info.file_path)
            
            # Compare with stored hash
            return current_hash == backup_info.integrity_hash
            
        except Exception as e:
            logger.error(f"Error verifying backup integrity: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get table information
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                # Get database size
                db_size = os.path.getsize(self.db_path)
                
                # Get record counts for main tables
                table_counts = {}
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        table_counts[table] = cursor.fetchone()[0]
                    except:
                        table_counts[table] = "N/A"
                
                # Get migration info
                current_version = self.get_current_version()
                pending_migrations = len(self.get_pending_migrations())
                
                # Get backup info
                backups = self.list_backups()
                total_backup_size = sum(b.size_bytes for b in backups)
                
                return {
                    "database_path": self.db_path,
                    "database_size_bytes": db_size,
                    "database_size_mb": round(db_size / (1024 * 1024), 2),
                    "current_version": current_version,
                    "pending_migrations": pending_migrations,
                    "total_tables": len(tables),
                    "table_counts": table_counts,
                    "total_backups": len(backups),
                    "total_backup_size_bytes": total_backup_size,
                    "total_backup_size_mb": round(total_backup_size / (1024 * 1024), 2),
                    "last_backup": backups[0].created_at.isoformat() if backups else None
                }
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def _record_backup(self, backup_info: BackupInfo) -> None:
        """Record backup information in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO backup_history 
                    (backup_id, filename, file_path, size_bytes, created_at, database_version,
                     backup_type, compression, integrity_hash, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    backup_info.backup_id,
                    backup_info.filename,
                    backup_info.file_path,
                    backup_info.size_bytes,
                    backup_info.created_at.isoformat(),
                    backup_info.database_version,
                    backup_info.backup_type,
                    backup_info.compression,
                    backup_info.integrity_hash,
                    json.dumps(backup_info.metadata)
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error recording backup info: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _calculate_migration_checksum(self, migration: MigrationScript) -> str:
        """Calculate checksum for a migration script"""
        content = f"{migration.version}{migration.name}{migration.description}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


# Migration Scripts
class Migration001_InitVersioning(MigrationScript):
    """Initialize database versioning system"""
    
    def __init__(self):
        super().__init__("001", "Init Versioning", "Initialize database versioning and migration tracking")
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        # Migration tracking table is created by the manager
        pass
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migration_history'")
        return cursor.fetchone() is not None


class Migration002_EnhanceChannelInfo(MigrationScript):
    """Enhance channel info table with additional fields"""
    
    def __init__(self):
        super().__init__("002", "Enhance Channel Info", "Add new fields to channel_info table")
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        # Add new columns to channel_info table
        new_columns = [
            ("goals", "TEXT DEFAULT ''"),
            ("target_audience", "TEXT DEFAULT ''"),
            ("brand_voice", "TEXT DEFAULT ''"),
            ("posting_schedule", "TEXT DEFAULT ''"),
            ("analytics_enabled", "BOOLEAN DEFAULT TRUE"),
            ("last_analytics_sync", "TIMESTAMP"),
            ("external_channel_id", "TEXT DEFAULT ''"),
            ("monetization_enabled", "BOOLEAN DEFAULT FALSE"),
            ("content_categories", "TEXT DEFAULT ''")  # JSON array
        ]
        
        for column_name, column_def in new_columns:
            try:
                cursor.execute(f"ALTER TABLE channel_info ADD COLUMN {column_name} {column_def}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" not in str(e).lower():
                    raise
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        cursor.execute("PRAGMA table_info(channel_info)")
        columns = [row[1] for row in cursor.fetchall()]
        return "goals" in columns and "target_audience" in columns


class Migration003_AddAnalyticsTables(MigrationScript):
    """Add analytics and performance tracking tables"""
    
    def __init__(self):
        super().__init__("003", "Add Analytics Tables", "Create tables for analytics and performance tracking")
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        # Video analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                video_id TEXT NOT NULL,
                title TEXT,
                published_at TIMESTAMP,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                watch_time_minutes INTEGER DEFAULT 0,
                ctr REAL DEFAULT 0,
                retention_rate REAL DEFAULT 0,
                subscriber_gain INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, video_id)
            )
        ''')
        
        # Channel performance snapshots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                snapshot_date DATE NOT NULL,
                total_subscribers INTEGER DEFAULT 0,
                total_videos INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                total_watch_time INTEGER DEFAULT 0,
                avg_ctr REAL DEFAULT 0,
                avg_retention REAL DEFAULT 0,
                monthly_revenue REAL DEFAULT 0,
                top_performing_video TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, snapshot_date)
            )
        ''')
        
        # Content performance insights
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                insight_type TEXT NOT NULL,
                content TEXT NOT NULL,
                confidence_score REAL DEFAULT 0,
                data_points TEXT,  -- JSON
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        tables = ['video_analytics', 'performance_snapshots', 'content_insights']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                return False
        return True


class Migration004_AddUserPreferences(MigrationScript):
    """Add user preferences and settings table"""
    
    def __init__(self):
        super().__init__("004", "Add User Preferences", "Add table for user preferences and settings")
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                timezone TEXT DEFAULT 'UTC',
                date_format TEXT DEFAULT 'YYYY-MM-DD',
                notifications_enabled BOOLEAN DEFAULT TRUE,
                email_notifications BOOLEAN DEFAULT TRUE,
                analytics_frequency TEXT DEFAULT 'weekly',
                dashboard_layout TEXT DEFAULT 'default',
                theme TEXT DEFAULT 'light',
                language TEXT DEFAULT 'en',
                privacy_settings TEXT DEFAULT '{}',  -- JSON
                feature_flags TEXT DEFAULT '{}',     -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_preferences'")
        return cursor.fetchone() is not None


class Migration005_AddContentScheduling(MigrationScript):
    """Add content scheduling and planning tables"""
    
    def __init__(self):
        super().__init__("005", "Add Content Scheduling", "Add tables for content scheduling and planning")
    
    def up(self, cursor: sqlite3.Cursor) -> None:
        # Content calendar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_calendar (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                content_type TEXT,
                pillar_id TEXT,
                scheduled_date DATE,
                scheduled_time TIME,
                status TEXT DEFAULT 'planned',  -- planned, in_progress, completed, cancelled
                priority INTEGER DEFAULT 1,
                tags TEXT DEFAULT '[]',  -- JSON array
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (pillar_id) REFERENCES content_pillars (id)
            )
        ''')
        
        # Content templates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_templates (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                template_type TEXT NOT NULL,  -- script, description, title, etc.
                content TEXT NOT NULL,
                placeholders TEXT DEFAULT '[]',  -- JSON array of placeholder names
                tags TEXT DEFAULT '[]',
                is_public BOOLEAN DEFAULT FALSE,
                usage_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    def validate(self, cursor: sqlite3.Cursor) -> bool:
        tables = ['content_calendar', 'content_templates']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                return False
        return True


# Global migration manager instance
_migration_manager: Optional[DatabaseMigrationManager] = None


def get_migration_manager(db_path: str = "creatormate.db") -> DatabaseMigrationManager:
    """Get or create global migration manager instance"""
    global _migration_manager
    if _migration_manager is None or _migration_manager.db_path != db_path:
        _migration_manager = DatabaseMigrationManager(db_path)
    return _migration_manager