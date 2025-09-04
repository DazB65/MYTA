"""
Database Security Utilities for Vidalytics
Handles encryption, audit logging, and secure data operations
"""

import os
import logging
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import sqlite3
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class DatabaseEncryption:
    """Handles encryption/decryption of sensitive database fields"""
    
    def __init__(self):
        self._fernet = None
        self._initialize_encryption()
    
    def _initialize_encryption(self):
        """Initialize encryption with key from environment or generate new one"""
        encryption_key = os.getenv('DATABASE_ENCRYPTION_KEY')
        
        if not encryption_key:
            # Generate a new key for development
            encryption_key = Fernet.generate_key().decode()
            logger.warning("No DATABASE_ENCRYPTION_KEY found. Generated temporary key for development.")
            logger.warning("Set DATABASE_ENCRYPTION_KEY environment variable for production.")
        
        try:
            # If it's a base64 key, use it directly
            self._fernet = Fernet(encryption_key.encode())
        except Exception:
            # If it's a password, derive a key from it
            password = encryption_key.encode()
            salt = os.getenv('ENCRYPTION_SALT', 'vidalytics_salt_2024').encode()
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            self._fernet = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        if not data:
            return data
        
        try:
            encrypted = self._fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return encrypted_data
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._fernet.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def hash_sensitive_data(self, data: str, salt: Optional[str] = None) -> str:
        """Create a one-way hash of sensitive data for searching"""
        if not salt:
            salt = os.getenv('DATA_HASH_SALT', 'vidalytics_hash_salt_2024')
        
        combined = f"{data}{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()

class AuditLogger:
    """Comprehensive audit logging for database operations"""
    
    def __init__(self, db_path: str = "Vidalytics.db"):
        self.db_path = db_path
        self._init_audit_tables()
    
    def _init_audit_tables(self):
        """Initialize audit logging tables"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create comprehensive audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT,
                    session_id TEXT,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id TEXT,
                    old_values TEXT,
                    new_values TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    request_id TEXT,
                    severity TEXT DEFAULT 'INFO',
                    success BOOLEAN DEFAULT TRUE,
                    error_message TEXT,
                    additional_data TEXT
                )
            """)
            
            # Create security events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    user_id TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    description TEXT,
                    details TEXT,
                    resolved BOOLEAN DEFAULT FALSE,
                    resolved_at TIMESTAMP,
                    resolved_by TEXT
                )
            """)
            
            # Create data access log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_access_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    record_count INTEGER DEFAULT 1,
                    sensitive_data_accessed BOOLEAN DEFAULT FALSE,
                    ip_address TEXT,
                    session_id TEXT
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log (timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log (user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log (action)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_security_events_type ON security_events (event_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_access_user ON data_access_log (user_id)")
            
            conn.commit()
    
    @contextmanager
    def _get_db_connection(self):
        """Get database connection with proper error handling"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def log_action(self, action: str, user_id: Optional[str] = None, 
                   table_name: Optional[str] = None, record_id: Optional[str] = None,
                   old_values: Optional[Dict] = None, new_values: Optional[Dict] = None,
                   ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                   session_id: Optional[str] = None, request_id: Optional[str] = None,
                   severity: str = 'INFO', success: bool = True, 
                   error_message: Optional[str] = None, 
                   additional_data: Optional[Dict] = None):
        """Log an audit event"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO audit_log (
                        user_id, session_id, action, table_name, record_id,
                        old_values, new_values, ip_address, user_agent, request_id,
                        severity, success, error_message, additional_data
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, session_id, action, table_name, record_id,
                    str(old_values) if old_values else None,
                    str(new_values) if new_values else None,
                    ip_address, user_agent, request_id, severity, success,
                    error_message, str(additional_data) if additional_data else None
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
    
    def log_security_event(self, event_type: str, severity: str, description: str,
                          user_id: Optional[str] = None, ip_address: Optional[str] = None,
                          user_agent: Optional[str] = None, details: Optional[Dict] = None):
        """Log a security event"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO security_events (
                        event_type, severity, user_id, ip_address, user_agent,
                        description, details
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    event_type, severity, user_id, ip_address, user_agent,
                    description, str(details) if details else None
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    def log_data_access(self, user_id: str, table_name: str, operation: str,
                       record_count: int = 1, sensitive_data: bool = False,
                       ip_address: Optional[str] = None, session_id: Optional[str] = None):
        """Log data access for compliance"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO data_access_log (
                        user_id, table_name, operation, record_count,
                        sensitive_data_accessed, ip_address, session_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, table_name, operation, record_count,
                    sensitive_data, ip_address, session_id
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log data access: {e}")
    
    def get_user_activity(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get user activity for the specified period"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM audit_log 
                    WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                    ORDER BY timestamp DESC
                """.format(days), (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get user activity: {e}")
            return []
    
    def cleanup_old_logs(self, retention_days: int = 90):
        """Clean up old audit logs based on retention policy"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Clean up old audit logs
                cursor.execute("""
                    DELETE FROM audit_log 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(retention_days))
                
                # Clean up old security events (keep resolved ones longer)
                cursor.execute("""
                    DELETE FROM security_events 
                    WHERE timestamp < datetime('now', '-{} days') AND resolved = TRUE
                """.format(retention_days * 2))
                
                # Clean up old data access logs
                cursor.execute("""
                    DELETE FROM data_access_log 
                    WHERE timestamp < datetime('now', '-{} days')
                """.format(retention_days))
                
                conn.commit()
                logger.info(f"Cleaned up audit logs older than {retention_days} days")
        except Exception as e:
            logger.error(f"Failed to cleanup old logs: {e}")

def generate_secure_id() -> str:
    """Generate a cryptographically secure ID"""
    return secrets.token_urlsafe(16)

def hash_for_lookup(data: str) -> str:
    """Create a hash suitable for database lookups while preserving privacy"""
    salt = os.getenv('LOOKUP_HASH_SALT', 'vidalytics_lookup_2024')
    combined = f"{data}{salt}"
    return hashlib.sha256(combined.encode()).hexdigest()

# Global instances
db_encryption = DatabaseEncryption()
audit_logger = AuditLogger()
