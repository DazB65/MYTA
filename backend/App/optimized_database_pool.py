"""
Optimized Database Connection Pool for SQLite
Provides connection pooling, query optimization, and performance monitoring
"""

import sqlite3
import threading
import time
import logging
from typing import Dict, Any, Optional, List, ContextManager
from contextlib import contextmanager
from dataclasses import dataclass
from queue import Queue, Empty
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class PoolConfig:
    """Configuration for database connection pool"""
    db_path: str = "Vidalytics.db"
    pool_size: int = 10
    max_pool_size: int = 20
    timeout: int = 30
    check_same_thread: bool = False
    journal_mode: str = "WAL"  # Write-Ahead Logging
    synchronous: str = "NORMAL"
    cache_size: int = -64000  # 64MB cache
    temp_store: str = "MEMORY"
    mmap_size: int = 268435456  # 256MB memory-mapped I/O
    busy_timeout: int = 30000  # 30 seconds
    
@dataclass
class QueryStats:
    """Query performance statistics"""
    total_queries: int = 0
    total_time: float = 0.0
    slow_queries: int = 0
    failed_queries: int = 0
    avg_time: float = 0.0
    
    def update(self, duration: float, success: bool = True):
        """Update statistics with new query"""
        self.total_queries += 1
        self.total_time += duration
        self.avg_time = self.total_time / self.total_queries
        
        if duration > 1.0:  # Slow query threshold: 1 second
            self.slow_queries += 1
            
        if not success:
            self.failed_queries += 1

class PooledConnection:
    """Wrapper for pooled database connection"""
    
    def __init__(self, connection: sqlite3.Connection, pool: 'DatabasePool'):
        self.connection = connection
        self.pool = pool
        self.created_at = time.time()
        self.last_used = time.time()
        self.in_use = False
        
    def execute(self, query: str, params: tuple = None) -> sqlite3.Cursor:
        """Execute query with performance tracking"""
        start_time = time.time()
        try:
            self.last_used = time.time()
            cursor = self.connection.execute(query, params or ())
            duration = time.time() - start_time
            self.pool.stats.update(duration, True)
            
            if duration > 1.0:
                logger.warning(f"Slow query ({duration:.2f}s): {query[:100]}...")
                
            return cursor
        except Exception as e:
            duration = time.time() - start_time
            self.pool.stats.update(duration, False)
            logger.error(f"Query failed ({duration:.2f}s): {query[:100]}... Error: {e}")
            raise
            
    def executemany(self, query: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """Execute multiple queries with performance tracking"""
        start_time = time.time()
        try:
            self.last_used = time.time()
            cursor = self.connection.executemany(query, params_list)
            duration = time.time() - start_time
            self.pool.stats.update(duration, True)
            return cursor
        except Exception as e:
            duration = time.time() - start_time
            self.pool.stats.update(duration, False)
            logger.error(f"Batch query failed ({duration:.2f}s): {query[:100]}... Error: {e}")
            raise
            
    def commit(self):
        """Commit transaction"""
        self.connection.commit()
        
    def rollback(self):
        """Rollback transaction"""
        self.connection.rollback()
        
    def close(self):
        """Return connection to pool"""
        self.in_use = False
        self.pool._return_connection(self)

class DatabasePool:
    """SQLite connection pool with performance optimization"""
    
    def __init__(self, config: PoolConfig):
        self.config = config
        self.stats = QueryStats()
        self._pool: Queue = Queue(maxsize=config.max_pool_size)
        self._all_connections: List[PooledConnection] = []
        self._lock = threading.Lock()
        self._initialized = False
        
    def initialize(self):
        """Initialize the connection pool"""
        if self._initialized:
            return
            
        logger.info(f"Initializing database pool with {self.config.pool_size} connections")
        
        # Create initial connections
        for _ in range(self.config.pool_size):
            conn = self._create_connection()
            pooled_conn = PooledConnection(conn, self)
            self._pool.put(pooled_conn)
            self._all_connections.append(pooled_conn)
            
        self._initialized = True
        logger.info(f"Database pool initialized with {len(self._all_connections)} connections")
        
    def _create_connection(self) -> sqlite3.Connection:
        """Create optimized SQLite connection"""
        conn = sqlite3.connect(
            self.config.db_path,
            timeout=self.config.timeout,
            check_same_thread=self.config.check_same_thread
        )
        
        # Apply performance optimizations
        conn.execute(f"PRAGMA journal_mode = {self.config.journal_mode}")
        conn.execute(f"PRAGMA synchronous = {self.config.synchronous}")
        conn.execute(f"PRAGMA cache_size = {self.config.cache_size}")
        conn.execute(f"PRAGMA temp_store = {self.config.temp_store}")
        conn.execute(f"PRAGMA mmap_size = {self.config.mmap_size}")
        conn.execute(f"PRAGMA busy_timeout = {self.config.busy_timeout}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA optimize")  # Query planner optimization
        
        # Set row factory for dict-like access
        conn.row_factory = sqlite3.Row
        
        return conn
        
    @contextmanager
    def get_connection(self) -> ContextManager[PooledConnection]:
        """Get connection from pool with automatic return"""
        if not self._initialized:
            self.initialize()
            
        connection = None
        try:
            # Try to get connection from pool
            try:
                connection = self._pool.get(timeout=self.config.timeout)
                connection.in_use = True
                yield connection
            except Empty:
                # Pool exhausted, create temporary connection if under max
                with self._lock:
                    if len(self._all_connections) < self.config.max_pool_size:
                        conn = self._create_connection()
                        connection = PooledConnection(conn, self)
                        connection.in_use = True
                        self._all_connections.append(connection)
                        logger.info(f"Created additional connection (total: {len(self._all_connections)})")
                        yield connection
                    else:
                        raise Exception("Database pool exhausted and max size reached")
                        
        finally:
            if connection:
                connection.close()
                
    def _return_connection(self, connection: PooledConnection):
        """Return connection to pool"""
        if not connection.in_use:
            return
            
        connection.in_use = False
        
        # Check if connection is still healthy
        try:
            connection.connection.execute("SELECT 1")
            self._pool.put(connection)
        except Exception as e:
            logger.warning(f"Removing unhealthy connection: {e}")
            self._remove_connection(connection)
            
    def _remove_connection(self, connection: PooledConnection):
        """Remove connection from pool"""
        with self._lock:
            if connection in self._all_connections:
                self._all_connections.remove(connection)
                try:
                    connection.connection.close()
                except:
                    pass
                    
    def get_stats(self) -> Dict[str, Any]:
        """Get pool statistics"""
        with self._lock:
            active_connections = sum(1 for conn in self._all_connections if conn.in_use)
            
        return {
            "total_connections": len(self._all_connections),
            "active_connections": active_connections,
            "available_connections": self._pool.qsize(),
            "query_stats": {
                "total_queries": self.stats.total_queries,
                "avg_time_ms": round(self.stats.avg_time * 1000, 2),
                "slow_queries": self.stats.slow_queries,
                "failed_queries": self.stats.failed_queries,
                "success_rate": round((self.stats.total_queries - self.stats.failed_queries) / max(self.stats.total_queries, 1) * 100, 2)
            }
        }
        
    def cleanup_idle_connections(self, max_idle_time: int = 300):
        """Remove idle connections (older than max_idle_time seconds)"""
        current_time = time.time()
        to_remove = []
        
        with self._lock:
            for conn in self._all_connections:
                if not conn.in_use and (current_time - conn.last_used) > max_idle_time:
                    to_remove.append(conn)
                    
        for conn in to_remove:
            self._remove_connection(conn)
            logger.info(f"Removed idle connection (idle for {current_time - conn.last_used:.1f}s)")
            
    def close_all(self):
        """Close all connections"""
        with self._lock:
            for conn in self._all_connections:
                try:
                    conn.connection.close()
                except:
                    pass
            self._all_connections.clear()
            
        # Clear the queue
        while not self._pool.empty():
            try:
                self._pool.get_nowait()
            except Empty:
                break
                
        logger.info("All database connections closed")

# Global pool instance
_db_pool: Optional[DatabasePool] = None

def get_database_pool() -> DatabasePool:
    """Get or create global database pool"""
    global _db_pool
    if _db_pool is None:
        config = PoolConfig()
        _db_pool = DatabasePool(config)
    return _db_pool

@contextmanager
def get_db_connection():
    """Get database connection from pool"""
    pool = get_database_pool()
    with pool.get_connection() as conn:
        yield conn

def get_pool_stats() -> Dict[str, Any]:
    """Get database pool statistics"""
    pool = get_database_pool()
    return pool.get_stats()

def cleanup_idle_connections():
    """Cleanup idle database connections"""
    pool = get_database_pool()
    pool.cleanup_idle_connections()

def close_database_pool():
    """Close database pool - call on app shutdown"""
    global _db_pool
    if _db_pool:
        _db_pool.close_all()
        _db_pool = None
