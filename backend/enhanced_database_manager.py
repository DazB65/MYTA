"""
Enhanced Database Manager for Vidalytics
Improved SQLite database operations with proper error handling, connection pooling, and transactions
"""

import sqlite3
import json
import logging
import threading
import time
from contextlib import contextmanager
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import queue

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base exception class for database errors"""
    pass

class ConnectionPoolError(DatabaseError):
    """Exception raised when connection pool operations fail"""
    pass

class TransactionError(DatabaseError):
    """Exception raised when transaction operations fail"""
    pass

class DataIntegrityError(DatabaseError):
    """Exception raised when data integrity constraints are violated"""
    pass

@dataclass
class ConnectionConfig:
    """Configuration for database connections"""
    db_path: str = "Vidalytics.db"
    pool_size: int = 10
    timeout: int = 30
    check_same_thread: bool = False
    journal_mode: str = "WAL"  # Write-Ahead Logging for better concurrency
    synchronous: str = "NORMAL"
    cache_size: int = -64000  # 64MB cache

class ConnectionPool:
    """Thread-safe connection pool for SQLite"""
    
    def __init__(self, config: ConnectionConfig):
        self.config = config
        self._pool = queue.Queue(maxsize=config.pool_size)
        self._created_connections = 0
        self._lock = threading.Lock()
        self._closed = False
        
        # Pre-populate the pool
        self._initialize_pool()
        
    def _initialize_pool(self):
        """Initialize the connection pool with connections"""
        for _ in range(self.config.pool_size):
            try:
                conn = self._create_connection()
                self._pool.put(conn, block=False)
            except queue.Full:
                break
            except Exception as e:
                logger.error(f"Failed to initialize connection pool: {e}")
                raise ConnectionPoolError(f"Pool initialization failed: {e}")
    
    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection with optimal settings"""
        try:
            conn = sqlite3.connect(
                self.config.db_path,
                timeout=self.config.timeout,
                check_same_thread=self.config.check_same_thread
            )
            
            # Configure connection for optimal performance
            conn.execute(f"PRAGMA journal_mode = {self.config.journal_mode}")
            conn.execute(f"PRAGMA synchronous = {self.config.synchronous}")
            conn.execute(f"PRAGMA cache_size = {self.config.cache_size}")
            conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
            conn.execute("PRAGMA temp_store = MEMORY")  # Store temp tables in memory
            
            # Set row factory for dict-like access
            conn.row_factory = sqlite3.Row
            
            with self._lock:
                self._created_connections += 1
                
            logger.debug(f"Created new database connection (total: {self._created_connections})")
            return conn
            
        except sqlite3.Error as e:
            logger.error(f"Failed to create database connection: {e}")
            raise ConnectionPoolError(f"Connection creation failed: {e}")
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool with proper cleanup"""
        if self._closed:
            raise ConnectionPoolError("Connection pool is closed")
            
        conn = None
        try:
            # Try to get from pool first
            try:
                conn = self._pool.get(block=True, timeout=5)
            except queue.Empty:
                # Pool exhausted, create new connection
                logger.warning("Connection pool exhausted, creating new connection")
                conn = self._create_connection()
            
            # Verify connection is still valid
            try:
                conn.execute("SELECT 1").fetchone()
            except sqlite3.Error:
                # Connection is stale, create new one
                logger.warning("Stale connection detected, creating new one")
                try:
                    conn.close()
                except:
                    pass
                conn = self._create_connection()
            
            yield conn
            
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise DatabaseError(f"Connection error: {e}")
        finally:
            if conn and not self._closed:
                # Return connection to pool
                try:
                    self._pool.put(conn, block=False)
                except queue.Full:
                    # Pool is full, close the connection
                    try:
                        conn.close()
                    except:
                        pass
    
    def close(self):
        """Close all connections in the pool"""
        self._closed = True
        
        while not self._pool.empty():
            try:
                conn = self._pool.get(block=False)
                conn.close()
            except (queue.Empty, sqlite3.Error):
                break
        
        logger.info(f"Closed connection pool with {self._created_connections} total connections")

class EnhancedDatabaseManager:
    """Enhanced database manager with proper error handling and connection pooling"""
    
    def __init__(self, config: Optional[ConnectionConfig] = None):
        self.config = config or ConnectionConfig()
        self.pool = ConnectionPool(self.config)
        self._initialized = False
        self._lock = threading.Lock()
        
        # Initialize database schema
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables and proper error handling"""
        if self._initialized:
            return
            
        with self._lock:
            if self._initialized:
                return
                
            try:
                with self.pool.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Begin transaction
                    cursor.execute("BEGIN TRANSACTION")
                    
                    try:
                        # Users table
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                id TEXT PRIMARY KEY,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        ''')
                        
                        # Channel info table with comprehensive error handling
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS channel_info (
                                user_id TEXT PRIMARY KEY,
                                name TEXT DEFAULT 'Unknown',
                                channel_id TEXT DEFAULT '',
                                niche TEXT DEFAULT 'Unknown',
                                content_type TEXT DEFAULT 'Unknown',
                                subscriber_count INTEGER DEFAULT 0 CHECK (subscriber_count >= 0),
                                avg_view_count INTEGER DEFAULT 0 CHECK (avg_view_count >= 0),
                                total_view_count INTEGER DEFAULT 0 CHECK (total_view_count >= 0),
                                video_count INTEGER DEFAULT 0 CHECK (video_count >= 0),
                                ctr REAL DEFAULT 0 CHECK (ctr >= 0 AND ctr <= 100),
                                retention REAL DEFAULT 0 CHECK (retention >= 0 AND retention <= 100),
                                upload_frequency TEXT DEFAULT 'Unknown',
                                video_length TEXT DEFAULT 'Unknown',
                                monetization_status TEXT DEFAULT 'Unknown',
                                primary_goal TEXT DEFAULT 'Unknown',
                                notes TEXT DEFAULT '',
                                last_message TEXT DEFAULT '',
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            )
                        ''')
                        
                        # Add missing columns safely
                        self._add_missing_columns(cursor)
                        
                        # Conversation history table
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS conversation_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id TEXT NOT NULL,
                                role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
                                content TEXT NOT NULL,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            )
                        ''')
                        
                        # Insights table
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS insights (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id TEXT NOT NULL,
                                title TEXT NOT NULL,
                                content TEXT NOT NULL,
                                type TEXT DEFAULT 'general' CHECK (type IN ('general', 'performance', 'growth', 'monetization')),
                                priority INTEGER DEFAULT 1 CHECK (priority BETWEEN 1 AND 5),
                                is_read BOOLEAN DEFAULT FALSE,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                            )
                        ''')
                        
                        # Content pillars table
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS content_pillars (
                                id TEXT PRIMARY KEY,
                                user_id TEXT NOT NULL,
                                name TEXT NOT NULL,
                                icon TEXT DEFAULT '🎯',
                                color TEXT DEFAULT 'from-blue-500 to-cyan-400',
                                description TEXT DEFAULT '',
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                UNIQUE(user_id, name)
                            )
                        ''')
                        
                        # Video-pillar allocations table
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS video_pillar_allocations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id TEXT NOT NULL,
                                video_id TEXT NOT NULL,
                                pillar_id TEXT NOT NULL,
                                allocation_type TEXT DEFAULT 'manual' CHECK (allocation_type IN ('manual', 'auto', 'ai')),
                                confidence_score REAL DEFAULT 1.0 CHECK (confidence_score BETWEEN 0 AND 1),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                                FOREIGN KEY (pillar_id) REFERENCES content_pillars (id) ON DELETE CASCADE,
                                UNIQUE(user_id, video_id)
                            )
                        ''')
                        
                        # Create indexes for better performance
                        self._create_indexes(cursor)
                        
                        # Commit transaction
                        cursor.execute("COMMIT")
                        
                        self._initialized = True
                        logger.info("Enhanced database initialized successfully")
                        
                    except Exception as e:
                        cursor.execute("ROLLBACK")
                        raise
                        
            except sqlite3.Error as e:
                logger.error(f"Database initialization failed: {e}")
                raise DatabaseError(f"Database initialization failed: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during database initialization: {e}")
                raise DatabaseError(f"Database initialization failed: {e}")
    
    def _add_missing_columns(self, cursor: sqlite3.Cursor):
        """Safely add missing columns to existing tables"""
        columns_to_add = [
            ("channel_info", "channel_id", "TEXT DEFAULT ''"),
            ("channel_info", "total_view_count", "INTEGER DEFAULT 0"),
            ("channel_info", "video_count", "INTEGER DEFAULT 0")
        ]
        
        for table, column, definition in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
                logger.debug(f"Added column {column} to table {table}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    continue  # Column already exists
                else:
                    logger.warning(f"Failed to add column {column} to {table}: {e}")
    
    def _create_indexes(self, cursor: sqlite3.Cursor):
        """Create database indexes for better performance"""
        indexes = [
            ("idx_channel_info_user_id", "channel_info", ["user_id"]),
            ("idx_conversation_history_user_id", "conversation_history", ["user_id"]),
            ("idx_conversation_history_timestamp", "conversation_history", ["timestamp"]),
            ("idx_insights_user_id", "insights", ["user_id"]),
            ("idx_insights_type", "insights", ["type"]),
            ("idx_content_pillars_user_id", "content_pillars", ["user_id"]),
            ("idx_video_pillar_allocations_user_id", "video_pillar_allocations", ["user_id"]),
            ("idx_video_pillar_allocations_pillar_id", "video_pillar_allocations", ["pillar_id"])
        ]
        
        for index_name, table, columns in indexes:
            try:
                column_list = ", ".join(columns)
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({column_list})")
                logger.debug(f"Created index {index_name}")
            except sqlite3.Error as e:
                logger.warning(f"Failed to create index {index_name}: {e}")
    
    @contextmanager
    def transaction(self):
        """Context manager for database transactions with proper error handling"""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("BEGIN TRANSACTION")
                yield cursor
                cursor.execute("COMMIT")
                logger.debug("Transaction committed successfully")
            except Exception as e:
                cursor.execute("ROLLBACK")
                logger.error(f"Transaction rolled back due to error: {e}")
                raise TransactionError(f"Transaction failed: {e}")
    
    def create_user(self, user_id: str) -> bool:
        """Create a new user with proper error handling"""
        if not user_id or not user_id.strip():
            raise DataIntegrityError("User ID cannot be empty")
        
        try:
            with self.transaction() as cursor:
                cursor.execute('''
                    INSERT OR IGNORE INTO users (id) VALUES (?)
                ''', (user_id.strip(),))
                
                affected_rows = cursor.rowcount
                if affected_rows > 0:
                    logger.info(f"Created new user: {user_id}")
                    return True
                else:
                    logger.debug(f"User already exists: {user_id}")
                    return False
                    
        except sqlite3.Error as e:
            logger.error(f"Failed to create user {user_id}: {e}")
            raise DatabaseError(f"Failed to create user: {e}")
    
    def update_channel_info(self, user_id: str, channel_data: Dict[str, Any]) -> bool:
        """Update channel information with comprehensive error handling and validation"""
        if not user_id or not user_id.strip():
            raise DataIntegrityError("User ID cannot be empty")
        
        if not channel_data:
            raise DataIntegrityError("Channel data cannot be empty")
        
        # Validate numeric fields
        numeric_fields = {
            'subscriber_count': (0, float('inf')),
            'avg_view_count': (0, float('inf')),
            'total_view_count': (0, float('inf')),
            'video_count': (0, float('inf')),
            'ctr': (0, 100),
            'retention': (0, 100)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in channel_data:
                try:
                    value = float(channel_data[field])
                    if not (min_val <= value <= max_val):
                        raise DataIntegrityError(f"{field} must be between {min_val} and {max_val}")
                    channel_data[field] = value
                except (ValueError, TypeError):
                    logger.warning(f"Invalid {field} value: {channel_data[field]}, setting to 0")
                    channel_data[field] = 0
        
        try:
            # Ensure user exists first
            self.create_user(user_id)
            
            with self.transaction() as cursor:
                # Build dynamic update query
                set_clauses = []
                values = []
                
                valid_columns = [
                    'name', 'channel_id', 'niche', 'content_type', 'subscriber_count',
                    'avg_view_count', 'total_view_count', 'video_count', 'ctr', 'retention',
                    'upload_frequency', 'video_length', 'monetization_status', 'primary_goal', 'notes'
                ]
                
                for column in valid_columns:
                    if column in channel_data:
                        set_clauses.append(f"{column} = ?")
                        values.append(channel_data[column])
                
                if set_clauses:
                    set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                    values.append(user_id)
                    
                    query = f'''
                        INSERT OR REPLACE INTO channel_info 
                        (user_id, {', '.join(valid_columns)}, updated_at)
                        VALUES ({', '.join(['?' for _ in range(len(valid_columns) + 2)])})
                    '''
                    
                    # Prepare values for insert
                    insert_values = [user_id]
                    for column in valid_columns:
                        insert_values.append(channel_data.get(column, ''))
                    insert_values.append(datetime.now().isoformat())
                    
                    cursor.execute(query, insert_values)
                    
                    logger.info(f"Updated channel info for user: {user_id}")
                    return True
                else:
                    logger.warning(f"No valid channel data provided for user: {user_id}")
                    return False
                    
        except sqlite3.IntegrityError as e:
            logger.error(f"Data integrity error updating channel info for {user_id}: {e}")
            raise DataIntegrityError(f"Data integrity violation: {e}")
        except sqlite3.Error as e:
            logger.error(f"Database error updating channel info for {user_id}: {e}")
            raise DatabaseError(f"Failed to update channel info: {e}")
    
    def get_channel_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get channel information with proper error handling"""
        if not user_id or not user_id.strip():
            raise DataIntegrityError("User ID cannot be empty")
        
        try:
            with self.pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM channel_info WHERE user_id = ?
                ''', (user_id.strip(),))
                
                result = cursor.fetchone()
                if result:
                    return dict(result)
                else:
                    logger.debug(f"No channel info found for user: {user_id}")
                    return None
                    
        except sqlite3.Error as e:
            logger.error(f"Failed to get channel info for {user_id}: {e}")
            raise DatabaseError(f"Failed to retrieve channel info: {e}")
    
    def close(self):
        """Close the database connection pool"""
        try:
            self.pool.close()
            logger.info("Database manager closed successfully")
        except Exception as e:
            logger.error(f"Error closing database manager: {e}")

# Global database manager instance
_db_manager: Optional[EnhancedDatabaseManager] = None

def get_enhanced_db_manager() -> EnhancedDatabaseManager:
    """Get or create enhanced database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = EnhancedDatabaseManager()
    return _db_manager

def get_db_connection():
    """Get database connection from the enhanced connection pool"""
    return get_enhanced_db_manager().pool.get_connection()

# Backward compatibility functions
def create_user(user_id: str) -> bool:
    """Backward compatibility wrapper"""
    return get_enhanced_db_manager().create_user(user_id)

def update_channel_info(user_id: str, channel_data: Dict[str, Any]) -> bool:
    """Backward compatibility wrapper"""
    return get_enhanced_db_manager().update_channel_info(user_id, channel_data)

def get_channel_info(user_id: str) -> Optional[Dict[str, Any]]:
    """Backward compatibility wrapper"""
    return get_enhanced_db_manager().get_channel_info(user_id)