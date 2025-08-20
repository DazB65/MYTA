"""
Comprehensive Logging Configuration for Vidalytics
Provides structured logging, performance monitoring, and observability
"""

import sys
import json
import logging
import logging.handlers
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pathlib import Path
from contextvars import ContextVar
import threading
import queue
import time
from dataclasses import dataclass, asdict
from enum import Enum

from backend.App.config import get_settings


class LogLevel(Enum):
    """Log level enumeration"""
    CRITICAL = "CRITICAL"
    ERROR = "ERROR" 
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogCategory(Enum):
    """Log category enumeration for better organization"""
    SECURITY = "security"
    AUTHENTICATION = "auth"
    API = "api"
    AGENT = "agent"
    DATABASE = "database"
    BACKUP = "backup"
    MIGRATION = "migration"
    PERFORMANCE = "performance"
    USER_ACTION = "user_action"
    SYSTEM = "system"
    ERROR = "error"
    AUDIT = "audit"
    CACHE = "cache"
    WEBSOCKET = "websocket"
    PAYMENT = "payment"
    NOTIFICATIONS = "notifications"
    ANALYTICS = "analytics"
    SCHEDULER = "scheduler"


# Context variables for request tracking
request_id_context: ContextVar[str] = ContextVar('request_id', default='')
user_id_context: ContextVar[str] = ContextVar('user_id', default='')
session_id_context: ContextVar[str] = ContextVar('session_id', default='')


@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: str
    category: str
    message: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    module: Optional[str] = None
    function: Optional[str] = None
    line_number: Optional[int] = None
    duration_ms: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    stack_trace: Optional[str] = None


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured JSON logging"""
    
    def __init__(self, include_trace: bool = True):
        super().__init__()
        self.include_trace = include_trace
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        # Extract context information
        request_id = getattr(record, 'request_id', None) or request_id_context.get('')
        user_id = getattr(record, 'user_id', None) or user_id_context.get('')
        session_id = getattr(record, 'session_id', None) or session_id_context.get('')
        
        # Build log entry
        log_entry = LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            level=record.levelname,
            category=getattr(record, 'category', LogCategory.SYSTEM.value),
            message=record.getMessage(),
            request_id=request_id if request_id else None,
            user_id=user_id if user_id else None,
            session_id=session_id if session_id else None,
            module=record.module,
            function=record.funcName,
            line_number=record.lineno,
            duration_ms=getattr(record, 'duration_ms', None),
            metadata=getattr(record, 'metadata', None)
        )
        
        # Add stack trace for errors if configured
        if self.include_trace and record.exc_info:
            log_entry.stack_trace = self.formatException(record.exc_info)
        
        # Convert to JSON
        log_dict = {k: v for k, v in asdict(log_entry).items() if v is not None}
        return json.dumps(log_dict, ensure_ascii=False)


class ColoredConsoleFormatter(logging.Formatter):
    """Colored console formatter for development"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format with colors for console output"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Get context info
        request_id = getattr(record, 'request_id', None) or request_id_context.get('')
        user_id = getattr(record, 'user_id', None) or user_id_context.get('')
        category = getattr(record, 'category', 'system')
        
        # Build formatted message
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        context_info = []
        if request_id:
            context_info.append(f"req:{request_id[:8]}")
        if user_id:
            context_info.append(f"user:{user_id[:8]}")
        
        context_str = f"[{','.join(context_info)}]" if context_info else ""
        
        formatted = (
            f"{color}{timestamp} {record.levelname:8}{reset} "
            f"{category:12} {record.module:15}.{record.funcName:15} "
            f"{context_str:20} {record.getMessage()}"
        )
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


class PerformanceLogger:
    """Logger for performance monitoring and metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger('performance')
        self._metrics_queue = queue.Queue()
        self._metrics_thread = None
        self._running = False
    
    def start_metrics_collection(self):
        """Start background metrics collection"""
        if self._running:
            return
        
        self._running = True
        self._metrics_thread = threading.Thread(target=self._process_metrics, daemon=True)
        self._metrics_thread.start()
    
    def stop_metrics_collection(self):
        """Stop background metrics collection"""
        self._running = False
        if self._metrics_thread:
            self._metrics_thread.join(timeout=5)
    
    def log_request_metrics(self, method: str, path: str, status_code: int, 
                          duration_ms: float, request_size: int = 0, 
                          response_size: int = 0, user_id: str = None):
        """Log HTTP request metrics"""
        metrics = {
            'type': 'http_request',
            'method': method,
            'path': path,
            'status_code': status_code,
            'duration_ms': duration_ms,
            'request_size_bytes': request_size,
            'response_size_bytes': response_size,
            'user_id': user_id
        }
        
        self.logger.info(
            f"HTTP {method} {path} {status_code} {duration_ms:.1f}ms",
            extra={
                'category': LogCategory.PERFORMANCE.value,
                'duration_ms': duration_ms,
                'metadata': metrics
            }
        )
        
        # Queue for background processing
        self._metrics_queue.put(metrics)
    
    def log_agent_metrics(self, agent_type: str, operation: str, duration_ms: float,
                         token_usage: Dict[str, int] = None, success: bool = True,
                         user_id: str = None):
        """Log AI agent performance metrics"""
        metrics = {
            'type': 'agent_operation',
            'agent_type': agent_type,
            'operation': operation,
            'duration_ms': duration_ms,
            'success': success,
            'token_usage': token_usage or {},
            'user_id': user_id
        }
        
        self.logger.info(
            f"Agent {agent_type} {operation} {'✓' if success else '✗'} {duration_ms:.1f}ms",
            extra={
                'category': LogCategory.AGENT.value,
                'duration_ms': duration_ms,
                'metadata': metrics
            }
        )
        
        self._metrics_queue.put(metrics)
    
    def log_database_metrics(self, operation: str, table: str, duration_ms: float,
                           rows_affected: int = 0, success: bool = True):
        """Log database operation metrics"""
        metrics = {
            'type': 'database_operation',
            'operation': operation,
            'table': table,
            'duration_ms': duration_ms,
            'rows_affected': rows_affected,
            'success': success
        }
        
        self.logger.info(
            f"DB {operation} {table} {rows_affected} rows {duration_ms:.1f}ms",
            extra={
                'category': LogCategory.DATABASE.value,
                'duration_ms': duration_ms,
                'metadata': metrics
            }
        )
        
        self._metrics_queue.put(metrics)
    
    def _process_metrics(self):
        """Background thread to process metrics"""
        while self._running:
            try:
                # Process metrics in batches
                metrics_batch = []
                deadline = time.time() + 10  # 10 second batch window
                
                while time.time() < deadline and len(metrics_batch) < 100:
                    try:
                        metric = self._metrics_queue.get(timeout=1)
                        metrics_batch.append(metric)
                    except queue.Empty:
                        break
                
                if metrics_batch:
                    self._store_metrics_batch(metrics_batch)
                
            except Exception as e:
                self.logger.error(f"Error processing metrics: {e}")
    
    def _store_metrics_batch(self, metrics: List[Dict[str, Any]]):
        """Store metrics batch (implement storage logic here)"""
        # For now, just log the batch size
        # In production, you might store to database, send to monitoring service, etc.
        pass


class AuditLogger:
    """Logger for security and compliance audit events"""
    
    def __init__(self):
        self.logger = logging.getLogger('audit')
    
    def log_authentication(self, user_id: str, action: str, success: bool, 
                          ip_address: str = None, user_agent: str = None,
                          additional_info: Dict[str, Any] = None):
        """Log authentication events"""
        metadata = {
            'action': action,
            'success': success,
            'ip_address': ip_address,
            'user_agent': user_agent
        }
        if additional_info:
            metadata.update(additional_info)
        
        self.logger.info(
            f"Auth {action} {'✓' if success else '✗'} user:{user_id}",
            extra={
                'category': LogCategory.AUTHENTICATION.value,
                'user_id': user_id,
                'metadata': metadata
            }
        )
    
    def log_data_access(self, user_id: str, resource: str, action: str,
                       success: bool, additional_info: Dict[str, Any] = None):
        """Log data access events"""
        metadata = {
            'resource': resource,
            'action': action,
            'success': success
        }
        if additional_info:
            metadata.update(additional_info)
        
        self.logger.info(
            f"Data access {action} {resource} {'✓' if success else '✗'} user:{user_id}",
            extra={
                'category': LogCategory.AUDIT.value,
                'user_id': user_id,
                'metadata': metadata
            }
        )
    
    def log_security_event(self, event_type: str, severity: str, description: str,
                          user_id: str = None, ip_address: str = None,
                          additional_info: Dict[str, Any] = None):
        """Log security events"""
        metadata = {
            'event_type': event_type,
            'severity': severity,
            'ip_address': ip_address
        }
        if additional_info:
            metadata.update(additional_info)
        
        level = getattr(logging, severity.upper(), logging.WARNING)
        
        self.logger.log(
            level,
            f"Security {event_type} {description}",
            extra={
                'category': LogCategory.SECURITY.value,
                'user_id': user_id,
                'metadata': metadata
            }
        )


class LoggingManager:
    """Central logging manager for Vidalytics"""
    
    def __init__(self):
        self.settings = get_settings()
        self.performance_logger = PerformanceLogger()
        self.audit_logger = AuditLogger()
        self._configured = False
        self._log_dir = None
    
    def configure_logging(self) -> None:
        """Configure logging system based on environment"""
        if self._configured:
            return
        
        # Create logs directory
        self._log_dir = Path("../logs")
        self._log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self._get_log_level())
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        if self.settings.is_development():
            console_handler.setFormatter(ColoredConsoleFormatter())
        else:
            console_handler.setFormatter(StructuredFormatter())
        
        console_handler.setLevel(self._get_log_level())
        root_logger.addHandler(console_handler)
        
        # Add file handler for persistent logging
        if not self.settings.is_development():
            file_handler = self._create_file_handler('application.log')
            file_handler.setFormatter(StructuredFormatter())
            root_logger.addHandler(file_handler)
        
        # Configure specific loggers
        self._configure_specialized_loggers()
        
        # Start performance metrics collection
        self.performance_logger.start_metrics_collection()
        
        self._configured = True
        
        # Log configuration completion
        logging.getLogger(__name__).info(
            f"Logging configured for {self.settings.environment} environment",
            extra={'category': LogCategory.SYSTEM.value}
        )
    
    def _get_log_level(self) -> int:
        """Get appropriate log level for environment"""
        if self.settings.is_development():
            return logging.DEBUG
        elif self.settings.is_staging():
            return logging.INFO
        else:  # Production
            return logging.WARNING
    
    def _create_file_handler(self, filename: str) -> logging.Handler:
        """Create rotating file handler"""
        file_path = self._log_dir / filename
        
        # Use rotating file handler to prevent log files from growing too large
        handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=50 * 1024 * 1024,  # 50MB
            backupCount=10,
            encoding='utf-8'
        )
        
        return handler
    
    def _configure_specialized_loggers(self):
        """Configure specialized loggers for different categories"""
        
        # Security logger - always log to separate file
        security_logger = logging.getLogger('security')
        security_handler = self._create_file_handler('security.log')
        security_handler.setFormatter(StructuredFormatter())
        security_logger.addHandler(security_handler)
        security_logger.setLevel(logging.INFO)
        
        # Audit logger - always log to separate file
        audit_logger = logging.getLogger('audit')
        audit_handler = self._create_file_handler('audit.log')
        audit_handler.setFormatter(StructuredFormatter())
        audit_logger.addHandler(audit_handler)
        audit_logger.setLevel(logging.INFO)
        
        # Performance logger
        performance_logger = logging.getLogger('performance')
        performance_handler = self._create_file_handler('performance.log')
        performance_handler.setFormatter(StructuredFormatter())
        performance_logger.addHandler(performance_handler)
        performance_logger.setLevel(logging.INFO)
        
        # Error logger - capture all errors in separate file
        error_logger = logging.getLogger('errors')
        error_handler = self._create_file_handler('errors.log')
        error_handler.setFormatter(StructuredFormatter(include_trace=True))
        error_logger.addHandler(error_handler)
        error_logger.setLevel(logging.ERROR)
        
        # Agent logger for AI operations
        agent_logger = logging.getLogger('agents')
        agent_handler = self._create_file_handler('agents.log')
        agent_handler.setFormatter(StructuredFormatter())
        agent_logger.addHandler(agent_handler)
        agent_logger.setLevel(logging.INFO)
    
    def set_request_context(self, request_id: str, user_id: str = None, session_id: str = None):
        """Set request context for current thread"""
        request_id_context.set(request_id)
        if user_id:
            user_id_context.set(user_id)
        if session_id:
            session_id_context.set(session_id)
    
    def clear_request_context(self):
        """Clear request context"""
        request_id_context.set('')
        user_id_context.set('')
        session_id_context.set('')
    
    def get_performance_logger(self) -> PerformanceLogger:
        """Get performance logger instance"""
        return self.performance_logger
    
    def get_audit_logger(self) -> AuditLogger:
        """Get audit logger instance"""
        return self.audit_logger
    
    def shutdown(self):
        """Shutdown logging system"""
        self.performance_logger.stop_metrics_collection()
        
        # Flush all handlers
        for handler in logging.getLogger().handlers:
            handler.flush()
            if hasattr(handler, 'close'):
                handler.close()


# Context manager for timing operations
class TimedOperation:
    """Context manager for timing operations with automatic logging"""
    
    def __init__(self, operation_name: str, category: LogCategory = LogCategory.PERFORMANCE,
                 logger: logging.Logger = None, log_level: int = logging.INFO):
        self.operation_name = operation_name
        self.category = category
        self.logger = logger or logging.getLogger(__name__)
        self.log_level = log_level
        self.start_time = None
        self.duration_ms = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration_ms = (time.time() - self.start_time) * 1000
        
        if exc_type is None:
            self.logger.log(
                self.log_level,
                f"{self.operation_name} completed in {self.duration_ms:.1f}ms",
                extra={
                    'category': self.category.value,
                    'duration_ms': self.duration_ms
                }
            )
        else:
            self.logger.error(
                f"{self.operation_name} failed after {self.duration_ms:.1f}ms: {exc_val}",
                extra={
                    'category': self.category.value,
                    'duration_ms': self.duration_ms
                },
                exc_info=True
            )


# Decorator for automatic performance logging
def log_performance(operation_name: str = None, category: LogCategory = LogCategory.PERFORMANCE):
    """Decorator to automatically log function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"
            logger = logging.getLogger(func.__module__)
            
            with TimedOperation(name, category, logger):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Global logging manager instance
_logging_manager: Optional[LoggingManager] = None


def get_logging_manager() -> LoggingManager:
    """Get or create global logging manager"""
    global _logging_manager
    if _logging_manager is None:
        _logging_manager = LoggingManager()
        _logging_manager.configure_logging()
    return _logging_manager


def get_logger(name: str, category: LogCategory = LogCategory.SYSTEM) -> logging.Logger:
    """Get logger with category context"""
    logger = logging.getLogger(name)
    
    # Add category to all log records from this logger
    original_makeRecord = logger.makeRecord
    
    def makeRecord(*args, **kwargs):
        record = original_makeRecord(*args, **kwargs)
        if not hasattr(record, 'category'):
            record.category = category.value
        return record
    
    logger.makeRecord = makeRecord
    return logger


# Convenience functions
def log_security_event(event_type: str, description: str, severity: str = "WARNING", **kwargs):
    """Log security event"""
    get_logging_manager().get_audit_logger().log_security_event(
        event_type, severity, description, **kwargs
    )


def log_user_action(user_id: str, action: str, resource: str, success: bool = True, **kwargs):
    """Log user action for audit trail"""
    get_logging_manager().get_audit_logger().log_data_access(
        user_id, resource, action, success, kwargs
    )


def log_performance_metrics(operation_type: str, **metrics):
    """Log performance metrics"""
    logger = get_logging_manager().get_performance_logger()
    
    if operation_type == 'http_request':
        logger.log_request_metrics(**metrics)
    elif operation_type == 'agent_operation':
        logger.log_agent_metrics(**metrics)
    elif operation_type == 'database_operation':
        logger.log_database_metrics(**metrics)


# Initialize logging when module is imported
try:
    get_logging_manager()
except Exception as e:
    # Fallback to basic logging if configuration fails
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger(__name__).error(f"Failed to configure advanced logging: {e}")