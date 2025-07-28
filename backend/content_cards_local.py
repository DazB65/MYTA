"""
Local SQLite storage for Content Cards
Provides a local alternative to Supabase for content cards functionality
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

class LocalContentCardsDB:
    def __init__(self, db_path: str = "creatormate.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the content cards table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content_cards (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    pillars TEXT,
                    due_date TEXT,
                    progress TEXT,
                    archived INTEGER DEFAULT 0,
                    order_index INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Content cards table initialized")
        except Exception as e:
            logger.error(f"Failed to initialize content cards database: {e}")
    
    def get_cards(self, user_id: str, status: Optional[str] = None, include_archived: bool = False):
        """Get content cards for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM content_cards WHERE user_id = ?"
            params = [user_id]
            
            if not include_archived:
                query += " AND archived = 0"
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY order_index ASC, created_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            cards = []
            for row in rows:
                card = dict(row)
                # Parse JSON fields
                if card.get('pillars'):
                    card['pillars'] = json.loads(card['pillars'])
                else:
                    card['pillars'] = []
                
                if card.get('progress'):
                    card['progress'] = json.loads(card['progress'])
                
                card['archived'] = bool(card.get('archived', 0))
                cards.append(card)
            
            conn.close()
            return cards
            
        except Exception as e:
            logger.error(f"Failed to get content cards: {e}")
            return []
    
    def create_card(self, user_id: str, title: str, description: str = "", status: str = "ideas",
                   pillars: List[Dict] = None, due_date: Optional[str] = None, 
                   progress: Optional[Dict] = None):
        """Create a new content card"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            card_id = f"card-{uuid.uuid4()}"
            now = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO content_cards 
                (id, user_id, title, description, status, pillars, due_date, progress, 
                 created_at, updated_at, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                card_id,
                user_id,
                title,
                description,
                status,
                json.dumps(pillars or []),
                due_date,
                json.dumps(progress) if progress else None,
                now,
                now,
                0
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'id': card_id,
                'user_id': user_id,
                'title': title,
                'description': description,
                'status': status,
                'pillars': pillars or [],
                'due_date': due_date,
                'progress': progress,
                'archived': False,
                'order_index': 0,
                'created_at': now,
                'updated_at': now
            }
            
        except Exception as e:
            logger.error(f"Failed to create content card: {e}")
            raise
    
    def update_card(self, card_id: str, updates: Dict[str, Any]):
        """Update a content card"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build update query
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                if key in ['pillars', 'progress'] and value is not None:
                    set_clauses.append(f"{key} = ?")
                    params.append(json.dumps(value))
                elif key == 'archived':
                    set_clauses.append(f"{key} = ?")
                    params.append(1 if value else 0)
                elif value is not None:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            set_clauses.append("updated_at = ?")
            params.append(datetime.now().isoformat())
            
            params.append(card_id)
            
            query = f"UPDATE content_cards SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            return affected > 0
            
        except Exception as e:
            logger.error(f"Failed to update content card: {e}")
            raise
    
    def delete_card(self, card_id: str):
        """Delete a content card"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM content_cards WHERE id = ?", (card_id,))
            
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            
            return affected > 0
            
        except Exception as e:
            logger.error(f"Failed to delete content card: {e}")
            raise

# Global instance
_local_db = None

def get_local_content_cards_db():
    """Get or create local content cards database"""
    global _local_db
    if _local_db is None:
        _local_db = LocalContentCardsDB()
    return _local_db