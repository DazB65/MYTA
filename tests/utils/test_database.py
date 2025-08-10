"""
Test database utilities and cleanup functions for Vidalytics testing
"""
import asyncio
import sqlite3
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime, timedelta
import secrets
import json


class TestDatabaseManager:
    """Manages test databases and cleanup operations"""
    
    def __init__(self):
        self.temp_databases: List[str] = []
        self.active_connections: List[sqlite3.Connection] = []
    
    def create_temp_database(self, prefix: str = "test_vidalytics") -> str:
        """Create a temporary SQLite database file"""
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=".db", 
            prefix=f"{prefix}_"
        )
        temp_file.close()
        
        db_path = temp_file.name
        self.temp_databases.append(db_path)
        return db_path
    
    def get_connection(self, db_path: str) -> sqlite3.Connection:
        """Get a connection to the test database"""
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        self.active_connections.append(conn)
        return conn
    
    @contextmanager
    def database_session(self, db_path: Optional[str] = None):
        """Context manager for database sessions with automatic cleanup"""
        if db_path is None:
            db_path = self.create_temp_database()
        
        conn = self.get_connection(db_path)
        try:
            yield conn
        finally:
            conn.close()
            if conn in self.active_connections:
                self.active_connections.remove(conn)
    
    def setup_test_tables(self, conn: sqlite3.Connection):
        """Set up test database tables"""
        cursor = conn.cursor()
        
        # OAuth tokens table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS oauth_tokens (
                user_id TEXT PRIMARY KEY,
                access_token TEXT NOT NULL,
                refresh_token TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics cache table  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_cache (
                cache_key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                expires_at TEXT NOT NULL
            )
        ''')
        
        # User data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                channel_name TEXT,
                channel_id TEXT UNIQUE,
                subscriber_count INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                video_count INTEGER DEFAULT 0,
                niche TEXT,
                goals TEXT,  -- JSON array
                content_type TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                message_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                intent TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                token_usage INTEGER DEFAULT 0,
                agent_sources TEXT,  -- JSON array
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Agent performance tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_type TEXT NOT NULL,
                request_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                response_time_ms INTEGER NOT NULL,
                token_usage INTEGER NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    
    def insert_test_data(self, conn: sqlite3.Connection, data: Dict[str, List[Dict[str, Any]]]):
        """Insert test data into database tables"""
        cursor = conn.cursor()
        
        for table_name, records in data.items():
            if not records:
                continue
                
            # Get column names from first record
            columns = list(records[0].keys())
            placeholders = ','.join(['?' for _ in columns])
            
            insert_sql = f'''
                INSERT OR REPLACE INTO {table_name} 
                ({','.join(columns)}) 
                VALUES ({placeholders})
            '''
            
            # Convert records to tuples
            values = []
            for record in records:
                row_values = []
                for col in columns:
                    value = record[col]
                    # Convert lists/dicts to JSON strings
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value)
                    row_values.append(value)
                values.append(tuple(row_values))
            
            cursor.executemany(insert_sql, values)
        
        conn.commit()
    
    def cleanup_database(self, db_path: str):
        """Clean up a specific database file"""
        try:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if db_path in self.temp_databases:
                self.temp_databases.remove(db_path)
        except OSError as e:
            print(f"Warning: Could not delete database {db_path}: {e}")
    
    def cleanup_all(self):
        """Clean up all temporary databases and connections"""
        # Close active connections
        for conn in self.active_connections[:]:
            try:
                conn.close()
            except Exception:
                pass
        self.active_connections.clear()
        
        # Delete temporary database files
        for db_path in self.temp_databases[:]:
            self.cleanup_database(db_path)
    
    def __del__(self):
        """Ensure cleanup on object destruction"""
        self.cleanup_all()


class TestDataFactory:
    """Factory for creating test data sets"""
    
    @staticmethod
    def create_oauth_tokens(count: int = 3) -> List[Dict[str, Any]]:
        """Create test OAuth token records"""
        tokens = []
        for i in range(count):
            user_id = f"test-user-{i+1}"
            tokens.append({
                "user_id": user_id,
                "access_token": f"mock-access-token-{i+1}",
                "refresh_token": f"mock-refresh-token-{i+1}",
                "channel_id": f"UC_test_channel_{i+1}",
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
        return tokens
    
    @staticmethod
    def create_analytics_cache(count: int = 5) -> List[Dict[str, Any]]:
        """Create test analytics cache records"""
        cache_records = []
        for i in range(count):
            cache_key = f"cache_key_{i+1}_{secrets.token_hex(8)}"
            cache_data = {
                "health_score": 70.0 + (i * 5),
                "subscriber_growth_rate": 2.0 + (i * 0.5),
                "cached": True,
                "generated_at": datetime.now().isoformat()
            }
            
            cache_records.append({
                "cache_key": cache_key,
                "data": json.dumps(cache_data),
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
            })
        return cache_records
    
    @staticmethod
    def create_users(count: int = 3) -> List[Dict[str, Any]]:
        """Create test user records"""
        niches = ["Technology", "Gaming", "Education", "Entertainment"]
        content_types = ["Tutorial", "Review", "Entertainment", "Educational"]
        
        users = []
        for i in range(count):
            user_id = f"test-user-{i+1}"
            users.append({
                "user_id": user_id,
                "channel_name": f"Test Channel {i+1}",
                "channel_id": f"UC_test_channel_{i+1}",
                "subscriber_count": 1000 + (i * 500),
                "total_views": 50000 + (i * 10000),
                "video_count": 100 + (i * 25),
                "niche": niches[i % len(niches)],
                "goals": json.dumps(["Growth", "Monetization", "Engagement"]),
                "content_type": content_types[i % len(content_types)],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            })
        return users
    
    @staticmethod
    def create_chat_history(user_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """Create test chat history records"""
        messages = [
            ("How are my videos performing?", "content_analysis"),
            ("Who is my audience?", "audience_insights"),
            ("How can I improve my SEO?", "seo_discoverability"),
            ("What should I post next?", "content_strategy"),
            ("Help me grow my channel", "growth_strategy")
        ]
        
        history = []
        for i in range(count):
            message, intent = messages[i % len(messages)]
            history.append({
                "message_id": f"msg_{user_id}_{i+1}",
                "user_id": user_id,
                "message": f"{message} (test {i+1})",
                "response": f"Test response for {intent} query {i+1}",
                "intent": intent,
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                "token_usage": 150 + (i * 25),
                "agent_sources": json.dumps([intent])
            })
        return history
    
    @staticmethod
    def create_agent_performance(count: int = 10) -> List[Dict[str, Any]]:
        """Create test agent performance records"""
        agent_types = ["content_analysis", "audience_insights", "seo_discoverability", "content_strategy"]
        
        performance = []
        for i in range(count):
            performance.append({
                "agent_type": agent_types[i % len(agent_types)],
                "request_id": f"req_{secrets.token_hex(8)}",
                "user_id": f"test-user-{(i % 3) + 1}",
                "response_time_ms": 1000 + (i * 100),
                "token_usage": 1500 + (i * 200),
                "success": i % 10 != 9,  # 90% success rate
                "error_message": "Test error" if i % 10 == 9 else None,
                "timestamp": (datetime.now() - timedelta(minutes=i * 5)).isoformat()
            })
        return performance
    
    @staticmethod
    def create_complete_test_dataset() -> Dict[str, List[Dict[str, Any]]]:
        """Create a complete test dataset with all tables"""
        users = TestDataFactory.create_users(3)
        
        dataset = {
            "oauth_tokens": TestDataFactory.create_oauth_tokens(3),
            "analytics_cache": TestDataFactory.create_analytics_cache(8),
            "users": users,
            "agent_performance": TestDataFactory.create_agent_performance(15)
        }
        
        # Create chat history for each user
        chat_history = []
        for user in users:
            chat_history.extend(
                TestDataFactory.create_chat_history(user["user_id"], 3)
            )
        dataset["chat_history"] = chat_history
        
        return dataset


class TestCacheManager:
    """Manages test caching scenarios"""
    
    def __init__(self, db_manager: TestDatabaseManager):
        self.db_manager = db_manager
    
    def setup_cache_scenarios(self, conn: sqlite3.Connection):
        """Set up various cache scenarios for testing"""
        cursor = conn.cursor()
        
        now = datetime.now()
        
        # Fresh cache (within TTL)
        cursor.execute('''
            INSERT OR REPLACE INTO analytics_cache 
            (cache_key, data, created_at, expires_at) 
            VALUES (?, ?, ?, ?)
        ''', (
            "fresh_cache_key",
            json.dumps({"health_score": 85.0, "cached": True}),
            now.isoformat(),
            (now + timedelta(hours=1)).isoformat()
        ))
        
        # Expired cache (past TTL)
        cursor.execute('''
            INSERT OR REPLACE INTO analytics_cache 
            (cache_key, data, created_at, expires_at) 
            VALUES (?, ?, ?, ?)
        ''', (
            "expired_cache_key",
            json.dumps({"health_score": 75.0, "cached": True}),
            (now - timedelta(hours=2)).isoformat(),
            (now - timedelta(hours=1)).isoformat()
        ))
        
        # Near-expiry cache (expires soon)
        cursor.execute('''
            INSERT OR REPLACE INTO analytics_cache 
            (cache_key, data, created_at, expires_at) 
            VALUES (?, ?, ?, ?)
        ''', (
            "near_expiry_cache_key",
            json.dumps({"health_score": 80.0, "cached": True}),
            (now - timedelta(minutes=50)).isoformat(),
            (now + timedelta(minutes=10)).isoformat()
        ))
        
        conn.commit()
    
    def clear_cache(self, conn: sqlite3.Connection, pattern: Optional[str] = None):
        """Clear cache entries, optionally matching a pattern"""
        cursor = conn.cursor()
        
        if pattern:
            cursor.execute(
                "DELETE FROM analytics_cache WHERE cache_key LIKE ?",
                (f"%{pattern}%",)
            )
        else:
            cursor.execute("DELETE FROM analytics_cache")
        
        conn.commit()
    
    def get_cache_stats(self, conn: sqlite3.Connection) -> Dict[str, int]:
        """Get cache statistics"""
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        # Total cache entries
        cursor.execute("SELECT COUNT(*) FROM analytics_cache")
        total = cursor.fetchone()[0]
        
        # Active (non-expired) entries
        cursor.execute(
            "SELECT COUNT(*) FROM analytics_cache WHERE expires_at > ?",
            (now,)
        )
        active = cursor.fetchone()[0]
        
        # Expired entries
        cursor.execute(
            "SELECT COUNT(*) FROM analytics_cache WHERE expires_at <= ?",
            (now,)
        )
        expired = cursor.fetchone()[0]
        
        return {
            "total_entries": total,
            "active_entries": active,
            "expired_entries": expired,
            "cache_hit_potential": active / total if total > 0 else 0.0
        }


# Global test database manager instance
_test_db_manager = None

def get_test_db_manager() -> TestDatabaseManager:
    """Get the global test database manager instance"""
    global _test_db_manager
    if _test_db_manager is None:
        _test_db_manager = TestDatabaseManager()
    return _test_db_manager


def cleanup_test_databases():
    """Clean up all test databases - call this after test runs"""
    global _test_db_manager
    if _test_db_manager is not None:
        _test_db_manager.cleanup_all()
        _test_db_manager = None


# Pytest fixtures that can be imported
def pytest_test_database():
    """Pytest fixture for test database"""
    db_manager = get_test_db_manager()
    db_path = db_manager.create_temp_database()
    
    with db_manager.database_session(db_path) as conn:
        db_manager.setup_test_tables(conn)
        yield conn, db_path
    
    db_manager.cleanup_database(db_path)


def pytest_test_database_with_data():
    """Pytest fixture for test database with sample data"""
    db_manager = get_test_db_manager()
    db_path = db_manager.create_temp_database()
    
    with db_manager.database_session(db_path) as conn:
        db_manager.setup_test_tables(conn)
        
        # Insert test data
        test_data = TestDataFactory.create_complete_test_dataset()
        db_manager.insert_test_data(conn, test_data)
        
        yield conn, db_path
    
    db_manager.cleanup_database(db_path)