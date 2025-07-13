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
                
                # Content pillars table for user-defined pillars
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS content_pillars (
                        id TEXT PRIMARY KEY,
                        user_id TEXT,
                        name TEXT NOT NULL,
                        icon TEXT DEFAULT '🎯',
                        color TEXT DEFAULT 'from-blue-500 to-cyan-400',
                        description TEXT DEFAULT '',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                ''')
                
                # Video-pillar allocations table for tracking which videos belong to which pillars
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS video_pillar_allocations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        video_id TEXT,
                        pillar_id TEXT,
                        allocation_type TEXT DEFAULT 'manual',
                        confidence_score REAL DEFAULT 1.0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id),
                        FOREIGN KEY (pillar_id) REFERENCES content_pillars (id),
                        UNIQUE(user_id, video_id)
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
                           monetization_status, primary_goal, notes, last_message, channel_id
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
                    "last_message": channel_row[12] if channel_row else "",
                    "channel_id": channel_row[13] if channel_row else ""
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
                    "user_id": user_id,  # Include user_id in context
                    "conversation_history": conversation_history,
                    "channel_info": channel_info
                }
                
        except Exception as e:
            logger.error(f"Error getting user context for {user_id}: {e}")
            # Return default context on error
            return {
                "user_id": user_id,  # Include user_id in error fallback too
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
                    "last_message": "",
                    "channel_id": ""
                }
            }
    
    def update_channel_info(self, user_id: str, channel_info: Dict) -> bool:
        """Update channel information for a user"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # First, try to add missing columns if they don't exist
                try:
                    cursor.execute("ALTER TABLE channel_info ADD COLUMN channel_id TEXT DEFAULT ''")
                except sqlite3.OperationalError:
                    pass  # Column already exists
                    
                try:
                    cursor.execute("ALTER TABLE channel_info ADD COLUMN total_view_count INTEGER DEFAULT 0")
                except sqlite3.OperationalError:
                    pass  # Column already exists
                    
                try:
                    cursor.execute("ALTER TABLE channel_info ADD COLUMN video_count INTEGER DEFAULT 0")
                except sqlite3.OperationalError:
                    pass  # Column already exists
                
                cursor.execute('''
                    INSERT OR REPLACE INTO channel_info (
                        user_id, name, channel_id, niche, content_type, subscriber_count, 
                        avg_view_count, total_view_count, video_count, ctr, retention, upload_frequency, 
                        video_length, monetization_status, primary_goal, notes, 
                        last_message, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    channel_info.get("name", "Unknown"),
                    channel_info.get("channel_id", ""),
                    channel_info.get("niche", "Unknown"),
                    channel_info.get("content_type", "Unknown"),
                    channel_info.get("subscriber_count", 0),
                    channel_info.get("avg_view_count", 0),
                    channel_info.get("total_view_count", 0),
                    channel_info.get("video_count", 0),
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
    
    def create_content_pillar(self, user_id: str, pillar_id: str, name: str, icon: str = "🎯", color: str = "from-blue-500 to-cyan-400", description: str = "") -> bool:
        """Create a new content pillar for a user"""
        try:
            self.create_user(user_id)  # Ensure user exists
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO content_pillars (id, user_id, name, icon, color, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (pillar_id, user_id, name, icon, color, description))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error creating content pillar for {user_id}: {e}")
            return False
    
    def get_user_content_pillars(self, user_id: str) -> List[Dict]:
        """Get all content pillars for a user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, name, icon, color, description, created_at, updated_at
                    FROM content_pillars 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                rows = cursor.fetchall()
                return [
                    {
                        "id": row[0],
                        "name": row[1],
                        "icon": row[2],
                        "color": row[3],
                        "description": row[4],
                        "created_at": row[5],
                        "updated_at": row[6]
                    }
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"Error getting content pillars for {user_id}: {e}")
            return []
    
    def update_content_pillar(self, pillar_id: str, name: str = None, icon: str = None, color: str = None, description: str = None) -> bool:
        """Update a content pillar"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                updates = []
                params = []
                
                if name is not None:
                    updates.append("name = ?")
                    params.append(name)
                if icon is not None:
                    updates.append("icon = ?")
                    params.append(icon)
                if color is not None:
                    updates.append("color = ?")
                    params.append(color)
                if description is not None:
                    updates.append("description = ?")
                    params.append(description)
                
                if not updates:
                    return True  # Nothing to update
                
                updates.append("updated_at = ?")
                params.append(datetime.now())
                params.append(pillar_id)
                
                query = f"UPDATE content_pillars SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error updating content pillar {pillar_id}: {e}")
            return False
    
    def get_content_pillar_by_id(self, pillar_id: str) -> Optional[Dict]:
        """Get a single content pillar by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, user_id, name, icon, color, description, created_at, updated_at
                    FROM content_pillars 
                    WHERE id = ?
                ''', (pillar_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "user_id": row[1],
                        "name": row[2],
                        "icon": row[3],
                        "color": row[4],
                        "description": row[5],
                        "created_at": row[6],
                        "updated_at": row[7]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting content pillar {pillar_id}: {e}")
            return None

    def delete_content_pillar(self, pillar_id: str) -> bool:
        """Delete a content pillar"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Also delete any video allocations for this pillar
                cursor.execute('DELETE FROM video_pillar_allocations WHERE pillar_id = ?', (pillar_id,))
                cursor.execute('DELETE FROM content_pillars WHERE id = ?', (pillar_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error deleting content pillar {pillar_id}: {e}")
            return False
    
    def allocate_video_to_pillar(self, user_id: str, video_id: str, pillar_id: str, allocation_type: str = "manual", confidence_score: float = 1.0) -> bool:
        """Allocate a video to a pillar"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO video_pillar_allocations 
                    (user_id, video_id, pillar_id, allocation_type, confidence_score, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, video_id, pillar_id, allocation_type, confidence_score, datetime.now()))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error allocating video {video_id} to pillar {pillar_id}: {e}")
            return False
    
    def get_videos_for_pillar(self, user_id: str, pillar_id: str) -> List[Dict]:
        """Get all videos allocated to a specific pillar"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT video_id, allocation_type, confidence_score, created_at, updated_at
                    FROM video_pillar_allocations 
                    WHERE user_id = ? AND pillar_id = ?
                    ORDER BY updated_at DESC
                ''', (user_id, pillar_id))
                
                rows = cursor.fetchall()
                return [
                    {
                        "video_id": row[0],
                        "allocation_type": row[1],
                        "confidence_score": row[2],
                        "created_at": row[3],
                        "updated_at": row[4]
                    }
                    for row in rows
                ]
                
        except Exception as e:
            logger.error(f"Error getting videos for pillar {pillar_id}: {e}")
            return []
    
    def get_pillar_for_video(self, user_id: str, video_id: str) -> Optional[Dict]:
        """Get the pillar allocation for a specific video"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT vpa.pillar_id, cp.name, cp.icon, cp.color, vpa.allocation_type, vpa.confidence_score
                    FROM video_pillar_allocations vpa
                    JOIN content_pillars cp ON vpa.pillar_id = cp.id
                    WHERE vpa.user_id = ? AND vpa.video_id = ?
                ''', (user_id, video_id))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "pillar_id": row[0],
                        "pillar_name": row[1],
                        "pillar_icon": row[2],
                        "pillar_color": row[3],
                        "allocation_type": row[4],
                        "confidence_score": row[5]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting pillar for video {video_id}: {e}")
            return None
    
    def remove_video_allocation(self, user_id: str, video_id: str) -> bool:
        """Remove video allocation from any pillar"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM video_pillar_allocations WHERE user_id = ? AND video_id = ?', (user_id, video_id))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            logger.error(f"Error removing video allocation for {video_id}: {e}")
            return False

# Global database instance
db_manager = DatabaseManager()