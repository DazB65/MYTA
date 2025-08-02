"""
Enhanced Database Management for Vidalytics
Provides connection pooling, query optimization, and monitoring
"""

import time
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import asyncpg
    ASYNCPG_AVAILABLE = True
except ImportError:
    ASYNCPG_AVAILABLE = False

try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlalchemy.pool import QueuePool
    from sqlalchemy import text, event
    from sqlalchemy.engine import Engine
    SQLALCHEMY_ASYNC_AVAILABLE = True
except ImportError:
    SQLALCHEMY_ASYNC_AVAILABLE = False

from exceptions import DatabaseError, DatabaseConnectionError
from backend.App.circuit_breaker import circuit_breaker, CircuitBreakerConfig
from logging_config import get_logger, LogCategory


logger = get_logger(__name__, LogCategory.DATABASE)


@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600
    pool_pre_ping: bool = True
    echo: bool = False
    echo_pool: bool = False
    query_timeout: int = 30
    connection_timeout: int = 10


@dataclass
class QueryStats:
    """Query statistics"""
    total_queries: int = 0
    successful_queries: int = 0
    failed_queries: int = 0
    total_time: float = 0.0
    slow_queries: int = 0
    slow_query_threshold: float = 1.0  # seconds
    
    @property
    def average_time(self) -> float:
        return self.total_time / self.total_queries if self.total_queries > 0 else 0.0
    
    @property
    def success_rate(self) -> float:
        return self.successful_queries / self.total_queries if self.total_queries > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "average_time": self.average_time,
            "success_rate": self.success_rate
        }


@dataclass
class ConnectionPoolStats:
    """Connection pool statistics"""
    pool_size: int = 0
    checked_in: int = 0
    checked_out: int = 0
    overflow: int = 0
    total_connections: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QueryMonitor:
    """Monitors database query performance"""
    
    def __init__(self, slow_query_threshold: float = 1.0):
        self.stats = QueryStats(slow_query_threshold=slow_query_threshold)
        self.slow_queries: List[Dict[str, Any]] = []
        self.max_slow_queries = 100
    
    def record_query(
        self,
        query: str,
        duration: float,
        success: bool,
        error: Optional[str] = None
    ):
        """Record query execution statistics"""
        self.stats.total_queries += 1
        self.stats.total_time += duration
        
        if success:
            self.stats.successful_queries += 1
        else:
            self.stats.failed_queries += 1
        
        if duration > self.stats.slow_query_threshold:
            self.stats.slow_queries += 1
            self._record_slow_query(query, duration, error)
    
    def _record_slow_query(self, query: str, duration: float, error: Optional[str]):
        """Record slow query for analysis"""
        slow_query = {
            "query": query[:500],  # Truncate long queries
            "duration": duration,
            "timestamp": datetime.utcnow().isoformat(),
            "error": error
        }
        
        self.slow_queries.append(slow_query)
        
        # Keep only recent slow queries
        if len(self.slow_queries) > self.max_slow_queries:
            self.slow_queries = self.slow_queries[-self.max_slow_queries:]
        
        # Log slow query
        logger.warning(
            f"Slow query detected: {duration:.3f}s",
            extra={
                "category": LogCategory.DATABASE.value,
                "metadata": {
                    "duration": duration,
                    "query_preview": query[:100],
                    "error": error
                }
            }
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get query statistics"""
        return {
            "stats": self.stats.to_dict(),
            "recent_slow_queries": self.slow_queries[-10:],  # Last 10 slow queries
            "slow_query_count": len(self.slow_queries)
        }


class EnhancedDatabase:
    """Enhanced database manager with connection pooling and monitoring"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.session_factory = None
        self.query_monitor = QueryMonitor()
        self._connected = False
    
    async def initialize(self) -> bool:
        """Initialize database connection"""
        if not SQLALCHEMY_ASYNC_AVAILABLE:
            logger.error("SQLAlchemy async not available")
            return False
        
        try:
            # Create async engine with connection pooling
            self.engine = create_async_engine(
                self.config.url,
                poolclass=QueuePool,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_timeout=self.config.pool_timeout,
                pool_recycle=self.config.pool_recycle,
                pool_pre_ping=self.config.pool_pre_ping,
                echo=self.config.echo,
                echo_pool=self.config.echo_pool,
                connect_args={
                    "command_timeout": self.config.query_timeout,
                    "server_settings": {
                        "jit": "off"  # Disable JIT for consistent performance
                    }
                } if "postgresql" in self.config.url else {}
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Test connection
            await self._test_connection()
            
            # Setup query monitoring
            self._setup_query_monitoring()
            
            self._connected = True
            logger.info("Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")
    
    async def _test_connection(self):
        """Test database connection"""
        async with self.engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    
    def _setup_query_monitoring(self):
        """Setup query monitoring events"""
        if not self.engine:
            return
        
        @event.listens_for(self.engine.sync_engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            context._query_start_time = time.time()
        
        @event.listens_for(self.engine.sync_engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            duration = time.time() - context._query_start_time
            self.query_monitor.record_query(statement, duration, True)
        
        @event.listens_for(self.engine.sync_engine, "handle_error")
        def handle_error(exception_context):
            if hasattr(exception_context, '_query_start_time'):
                duration = time.time() - exception_context._query_start_time
                self.query_monitor.record_query(
                    str(exception_context.statement),
                    duration,
                    False,
                    str(exception_context.original_exception)
                )
    
    @asynccontextmanager
    async def get_session(self):
        """Get database session with automatic cleanup"""
        if not self._connected:
            raise DatabaseConnectionError("Database not connected")
        
        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise DatabaseError(f"Database operation failed: {e}", "transaction")
        finally:
            await session.close()
    
    @circuit_breaker(
        "database",
        config=CircuitBreakerConfig(
            failure_threshold=10,
            recovery_timeout=10,
            success_threshold=5,
            timeout=30
        )
    )
    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute raw SQL query"""
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                if result.returns_rows:
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows]
                return []
            except Exception as e:
                raise DatabaseError(f"Query execution failed: {e}", "execute")
    
    @circuit_breaker("database")
    async def execute_scalar(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Execute query and return single scalar value"""
        async with self.get_session() as session:
            try:
                result = await session.execute(text(query), params or {})
                return result.scalar()
            except Exception as e:
                raise DatabaseError(f"Scalar query failed: {e}", "scalar")
    
    async def get_pool_stats(self) -> ConnectionPoolStats:
        """Get connection pool statistics"""
        if not self.engine or not hasattr(self.engine.pool, 'size'):
            return ConnectionPoolStats()
        
        pool = self.engine.pool
        return ConnectionPoolStats(
            pool_size=pool.size(),
            checked_in=pool.checkedin(),
            checked_out=pool.checkedout(),
            overflow=pool.overflow(),
            total_connections=pool.size() + pool.overflow()
        )
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get database health status"""
        try:
            start_time = time.time()
            await self._test_connection()
            response_time = time.time() - start_time
            
            pool_stats = await self.get_pool_stats()
            query_stats = self.query_monitor.get_stats()
            
            return {
                "status": "healthy",
                "response_time": response_time,
                "connected": self._connected,
                "pool": pool_stats.to_dict(),
                "queries": query_stats,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connected": False,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def cleanup(self):
        """Cleanup database connections"""
        if self.engine:
            await self.engine.dispose()
        self._connected = False
        logger.info("Database connections cleaned up")


class DatabaseManager:
    """Manages multiple database connections"""
    
    def __init__(self):
        self.databases: Dict[str, EnhancedDatabase] = {}
        self.default_db: Optional[str] = None
    
    async def add_database(
        self,
        name: str,
        config: DatabaseConfig,
        is_default: bool = False
    ) -> bool:
        """Add database connection"""
        try:
            db = EnhancedDatabase(config)
            await db.initialize()
            self.databases[name] = db
            
            if is_default or not self.default_db:
                self.default_db = name
            
            logger.info(f"Added database connection: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add database {name}: {e}")
            return False
    
    def get_database(self, name: Optional[str] = None) -> EnhancedDatabase:
        """Get database by name or default"""
        db_name = name or self.default_db
        if not db_name or db_name not in self.databases:
            raise DatabaseError(f"Database not found: {db_name}", "connection")
        return self.databases[db_name]
    
    async def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all databases"""
        health_status = {}
        for name, db in self.databases.items():
            health_status[name] = await db.get_health_status()
        return health_status
    
    async def cleanup_all(self):
        """Cleanup all database connections"""
        for db in self.databases.values():
            await db.cleanup()
        self.databases.clear()
        self.default_db = None


# Global database manager
_database_manager = DatabaseManager()


def get_database_manager() -> DatabaseManager:
    """Get global database manager"""
    return _database_manager


async def get_database(name: Optional[str] = None) -> EnhancedDatabase:
    """Get database instance"""
    return get_database_manager().get_database(name)


async def initialize_database(
    url: str,
    name: str = "default",
    **config_kwargs
) -> bool:
    """Initialize database with configuration"""
    config = DatabaseConfig(url=url, **config_kwargs)
    return await get_database_manager().add_database(name, config, is_default=True)


# Database utilities
class DatabaseUtils:
    """Database utility functions"""
    
    @staticmethod
    async def ensure_tables_exist(db: EnhancedDatabase, schema_queries: List[str]):
        """Ensure database tables exist"""
        for query in schema_queries:
            try:
                await db.execute_query(query)
            except Exception as e:
                logger.warning(f"Schema query failed (may be normal): {e}")
    
    @staticmethod
    async def get_table_stats(db: EnhancedDatabase, table_name: str) -> Dict[str, Any]:
        """Get statistics for a table"""
        try:
            # This is PostgreSQL specific - adjust for other databases
            query = """
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation,
                    most_common_vals,
                    most_common_freqs
                FROM pg_stats 
                WHERE tablename = :table_name
            """
            
            stats = await db.execute_query(query, {"table_name": table_name})
            
            # Get row count
            count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
            count_result = await db.execute_scalar(count_query)
            
            return {
                "table_name": table_name,
                "row_count": count_result,
                "column_stats": stats
            }
        except Exception as e:
            logger.warning(f"Failed to get table stats for {table_name}: {e}")
            return {"table_name": table_name, "error": str(e)}
    
    @staticmethod
    async def optimize_table(db: EnhancedDatabase, table_name: str):
        """Optimize table (database-specific)"""
        try:
            # PostgreSQL VACUUM ANALYZE
            if "postgresql" in db.config.url:
                await db.execute_query(f"VACUUM ANALYZE {table_name}")
            # Add other database optimizations as needed
            logger.info(f"Optimized table: {table_name}")
        except Exception as e:
            logger.warning(f"Failed to optimize table {table_name}: {e}")