"""
User Service for Vidalytics
Secure user management with database operations and session handling
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import contextmanager
from .auth_models import User, UserRegistration, UserLogin
from .security_config import get_security_config
from .database_security import db_encryption, audit_logger, generate_secure_id

logger = logging.getLogger(__name__)

class UserService:
    """Service for user management operations"""
    
    def __init__(self, db_path: str = "Vidalytics.db"):
        self.db_path = db_path
        self.security_config = get_security_config()
        self._init_database()
    
    def _init_database(self):
        """Initialize user tables in database"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create users table with encryption support
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    email_encrypted TEXT,
                    name TEXT NOT NULL,
                    name_encrypted TEXT,
                    password_hash TEXT NOT NULL,
                    is_verified BOOLEAN DEFAULT FALSE,
                    subscription_tier TEXT DEFAULT 'free',
                    youtube_connected BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    verification_token TEXT,
                    reset_token TEXT,
                    reset_token_expires TIMESTAMP
                )
            """)

            # Migration: Add email column if it doesn't exist (for existing databases)
            try:
                cursor.execute("SELECT email FROM users LIMIT 1")
            except sqlite3.OperationalError:
                # Email column doesn't exist, add it
                logger.info("Migrating database: Adding email column")
                cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
                cursor.execute("ALTER TABLE users ADD COLUMN email_encrypted TEXT")
                # Update existing records with placeholder email
                cursor.execute("UPDATE users SET email = id || '@migrated.local' WHERE email IS NULL")
            
            # Create user sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            
            # Create audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions (session_token)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions (user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON user_audit_log (user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON user_audit_log (timestamp)")
            
            conn.commit()
            logger.info("User database tables initialized successfully")
    
    @contextmanager
    def _get_db_connection(self):
        """Get database connection with proper error handling"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def create_user(self, registration: UserRegistration, ip_address: str = None,
                   user_agent: str = None) -> User:
        """Create a new user account with enhanced security"""
        try:
            # Check if user already exists
            if self.get_user_by_email(registration.email):
                raise ValueError("User with this email already exists")

            # Generate secure user ID
            secure_user_id = generate_secure_id()

            # Create user object with secure ID
            user = User.create_user(
                email=registration.email,
                name=registration.name,
                password=registration.password
            )
            user.id = secure_user_id

            # Encrypt sensitive data
            encrypted_email = db_encryption.encrypt(user.email)
            encrypted_name = db_encryption.encrypt(user.name)

            # Save to database with encrypted fields
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (
                        id, email, email_encrypted, name, name_encrypted,
                        password_hash, is_verified, subscription_tier,
                        youtube_connected, created_at, verification_token
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user.id, user.email, encrypted_email, user.name, encrypted_name,
                    user.password_hash, user.is_verified, user.subscription_tier,
                    user.youtube_connected, user.created_at, user.verification_token
                ))
                conn.commit()

            # Log user creation with audit trail
            audit_logger.log_action(
                action="user_created",
                user_id=user.id,
                table_name="users",
                record_id=user.id,
                new_values={"email": user.email, "name": user.name},
                ip_address=ip_address,
                user_agent=user_agent,
                severity="INFO"
            )

            # Log security event
            audit_logger.log_security_event(
                event_type="user_registration",
                severity="INFO",
                description=f"New user registered: {user.email}",
                user_id=user.id,
                ip_address=ip_address,
                user_agent=user_agent
            )

            logger.info(f"User created successfully: {user.email}")
            return user

        except Exception as e:
            # Log failed user creation
            audit_logger.log_security_event(
                event_type="user_registration_failed",
                severity="WARNING",
                description=f"Failed user registration attempt: {registration.email}",
                ip_address=ip_address,
                user_agent=user_agent,
                details={"error": str(e)}
            )
            logger.error(f"Failed to create user: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")
            raise
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_user(row)
                return None
                
        except Exception as e:
            logger.error(f"Failed to get user by ID: {e}")
            raise
    
    def authenticate_user(self, login: UserLogin, ip_address: str = None,
                         user_agent: str = None) -> Optional[User]:
        """Authenticate user with email and password with enhanced security logging"""
        try:
            user = self.get_user_by_email(login.email)
            if not user:
                # Log failed login attempt
                audit_logger.log_security_event(
                    event_type="login_failed",
                    severity="WARNING",
                    description=f"Login attempt for non-existent user: {login.email}",
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"reason": "user_not_found", "email": login.email}
                )
                return None

            if not user.verify_password(login.password):
                # Log failed password attempt
                audit_logger.log_security_event(
                    event_type="login_failed",
                    severity="WARNING",
                    description=f"Invalid password attempt for user: {login.email}",
                    user_id=user.id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    details={"reason": "invalid_password", "email": login.email}
                )
                return None

            # Update last login
            old_last_login = user.last_login
            user.last_login = datetime.utcnow()
            self.update_user(user)

            # Log successful authentication
            audit_logger.log_action(
                action="user_login",
                user_id=user.id,
                table_name="users",
                record_id=user.id,
                old_values={"last_login": old_last_login.isoformat() if old_last_login else None},
                new_values={"last_login": user.last_login.isoformat()},
                ip_address=ip_address,
                user_agent=user_agent,
                severity="INFO"
            )

            # Log data access
            audit_logger.log_data_access(
                user_id=user.id,
                table_name="users",
                operation="login",
                sensitive_data=True,
                ip_address=ip_address
            )

            logger.info(f"User authenticated successfully: {user.email}")
            return user

        except Exception as e:
            # Log authentication error
            audit_logger.log_security_event(
                event_type="authentication_error",
                severity="ERROR",
                description=f"Authentication system error for: {login.email}",
                ip_address=ip_address,
                user_agent=user_agent,
                details={"error": str(e)}
            )
            logger.error(f"Failed to authenticate user: {e}")
            raise
    
    def update_user(self, user: User):
        """Update user in database"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET
                        name = ?, password_hash = ?, is_verified = ?,
                        subscription_tier = ?, youtube_connected = ?,
                        last_login = ?, verification_token = ?,
                        reset_token = ?, reset_token_expires = ?
                    WHERE id = ?
                """, (
                    user.name, user.password_hash, user.is_verified,
                    user.subscription_tier, user.youtube_connected,
                    user.last_login, user.verification_token,
                    user.reset_token, user.reset_token_expires, user.id
                ))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise
    
    def _row_to_user(self, row) -> User:
        """Convert database row to User object"""
        return User(
            user_id=row['id'],
            email=row['email'],
            name=row['name'],
            password_hash=row['password_hash'],
            is_verified=bool(row['is_verified']),
            subscription_tier=row['subscription_tier'],
            youtube_connected=bool(row['youtube_connected']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            last_login=datetime.fromisoformat(row['last_login']) if row['last_login'] else None,
            verification_token=row['verification_token'],
            reset_token=row['reset_token'],
            reset_token_expires=datetime.fromisoformat(row['reset_token_expires']) if row['reset_token_expires'] else None
        )
    
    def _log_user_action(self, user_id: Optional[str], action: str, details: dict, 
                        ip_address: str = None, user_agent: str = None):
        """Log user action for audit trail"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_audit_log (user_id, action, details, ip_address, user_agent)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, action, str(details), ip_address, user_agent))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log user action: {e}")

# Global user service instance
user_service = UserService()
