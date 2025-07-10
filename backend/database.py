"""
Database module for CreatorMate
Handles SQLite database operations for user context and channel information
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "creatormate.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Channel info table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS channel_info (
                        user_id TEXT PRIMARY KEY,
                        name TEXT DEFAULT 'Unknown',
                        niche TEXT DEFAULT 'Unknown',
                        content_type TEXT DEFAULT 'Unknown',
                        subscriber_count INTEGER DEFAULT 0,
                        avg_view_count INTEGER DEFAULT 0,
                        ctr REAL DEFAULT 0,
                        retention REAL DEFAULT 0,
                        upload_frequency TEXT DEFAULT 'Unknown',
                        video_length TEXT DEFAULT 'Unknown',
                        monetization_status TEXT DEFAULT 'Unknown',
                        primary_goal TEXT DEFAULT 'Unknown',
                        notes TEXT DEFAULT '',
                        last_message TEXT DEFAULT '',
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Conversation history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversation_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        role TEXT,
                        content TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Insights table for dynamic insights
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS insights (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        title TEXT,
                        content TEXT,
                        type TEXT,
                        priority INTEGER DEFAULT 1,
                        is_read BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def create_user(self, user_id: str) -> bool:
        """Create a new user if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO users (id) VALUES (?)
                ''', (user_id,))
                
                # Create default channel info
                cursor.execute('''
                    INSERT OR IGNORE INTO channel_info (user_id) VALUES (?)
                ''', (user_id,))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {e}")
            return False
    
    def get_user_context(self, user_id: str) -> Dict:
        """Get complete user context including channel info and conversation history"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get channel info
                cursor.execute('''
                    SELECT name, niche, content_type, subscriber_count, avg_view_count,
                           ctr, retention, upload_frequency, video_length, 
                           monetization_status, primary_goal, notes, last_message
                    FROM channel_info WHERE user_id = ?
                ''', (user_id,))
                
                channel_row = cursor.fetchone()
                channel_info = {
                    "name": channel_row[0] if channel_row else "Unknown",
                    "niche": channel_row[1] if channel_row else "Unknown",
                    "content_type": channel_row[2] if channel_row else "Unknown",
                    "subscriber_count": channel_row[3] if channel_row else 0,
                    "avg_view_count": channel_row[4] if channel_row else 0,
                    "ctr": channel_row[5] if channel_row else 0,
                    "retention": channel_row[6] if channel_row else 0,
                    "upload_frequency": channel_row[7] if channel_row else "Unknown",
                    "video_length": channel_row[8] if channel_row else "Unknown",
                    "monetization_status": channel_row[9] if channel_row else "Unknown",
                    "primary_goal": channel_row[10] if channel_row else "Unknown",
                    "notes": channel_row[11] if channel_row else "",
                    "last_message": channel_row[12] if channel_row else ""
                }
                
                # Get conversation history (last 10 messages)
                cursor.execute('''
                    SELECT role, content FROM conversation_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 10
                ''', (user_id,))
                
                conversation_rows = cursor.fetchall()
                conversation_history = [
                    {"role": row[0], "content": row[1]} 
                    for row in reversed(conversation_rows)
                ]
                
                return {
                    "conversation_history": conversation_history,
                    "channel_info": channel_info
                }
                
        except Exception as e:
            logger.error(f"Error getting user context for {user_id}: {e}")
            # Return default context on error
            return {
                "conversation_history": [],
                "channel_info": {
                    "name": "Unknown",
                    "niche": "Unknown",
                    "content_type": "Unknown",
                    "subscriber_count": 0,
                    "avg_view_count": 0,
                    "ctr": 0,
                    "retention": 0,
                    "upload_frequency": "Unknown",
                    "video_length": "Unknown",
                    "monetization_status": "Unknown",
                    "primary_goal": "Unknown",
                    "notes": "",
                    "last_message": ""
                }
            }
    
    def update_channel_info(self, user_id: str, channel_info: Dict) -> bool:
        """Update channel information for a user"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO channel_info (
                        user_id, name, niche, content_type, subscriber_count, 
                        avg_view_count, ctr, retention, upload_frequency, 
                        video_length, monetization_status, primary_goal, notes, 
                        last_message, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    channel_info.get("name", "Unknown"),
                    channel_info.get("niche", "Unknown"),
                    channel_info.get("content_type", "Unknown"),
                    channel_info.get("subscriber_count", 0),
                    channel_info.get("avg_view_count", 0),
                    channel_info.get("ctr", 0),
                    channel_info.get("retention", 0),
                    channel_info.get("upload_frequency", "Unknown"),
                    channel_info.get("video_length", "Unknown"),
                    channel_info.get("monetization_status", "Unknown"),
                    channel_info.get("primary_goal", "Unknown"),
                    channel_info.get("notes", ""),
                    channel_info.get("last_message", ""),
                    datetime.now()
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error updating channel info for {user_id}: {e}")
            return False
    
    def add_conversation_message(self, user_id: str, role: str, content: str) -> bool:
        """Add a message to conversation history"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversation_history (user_id, role, content)
                    VALUES (?, ?, ?)
                ''', (user_id, role, content))
                
                # Keep only last 20 messages per user
                cursor.execute('''
                    DELETE FROM conversation_history 
                    WHERE user_id = ? AND id NOT IN (
                        SELECT id FROM conversation_history 
                        WHERE user_id = ? 
                        ORDER BY timestamp DESC 
                        LIMIT 20
                    )
                ''', (user_id, user_id))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding conversation message for {user_id}: {e}")
            return False
    
    def create_insight(self, user_id: str, title: str, content: str, insight_type: str = "general", priority: int = 1) -> bool:
        """Create a new insight for a user"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO insights (user_id, title, content, type, priority)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, title, content, insight_type, priority))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error creating insight for {user_id}: {e}")
            return False
    
    def get_user_insights(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get insights for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, title, content, type, priority, is_read, created_at
                    FROM insights 
                    WHERE user_id = ? 
                    ORDER BY priority DESC, created_at DESC 
                    LIMIT ?
                ''', (user_id, limit))
                
                rows = cursor.fetchall()
                return [
                    {
                        "id": row[0],
                        "title": row[1],
                        "content": row[2],
                        "type": row[3],
                        "priority": row[4],
                        "is_read": bool(row[5]),
                        "created_at": row[6]
                    }
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"Error getting insights for {user_id}: {e}")
            return []

# Global database instance
db_manager = DatabaseManager()