"""
WebSocket Manager for MYTA Real-time Chat
Handles WebSocket connections, message routing, and real-time features
"""

import json
import uuid
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
import asyncio

from backend.App.supabase_client import get_supabase_service
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.WEBSOCKET)

class ConnectionManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        # Store active connections: {user_id: {session_id: websocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        # Store user sessions: {user_id: {session_id: session_data}}
        self.user_sessions: Dict[str, Dict[str, Dict]] = {}
        # Store typing indicators: {session_id: {user_id: timestamp}}
        self.typing_indicators: Dict[str, Dict[str, datetime]] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str, session_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        
        # Initialize user connections if not exists
        if user_id not in self.active_connections:
            self.active_connections[user_id] = {}
            self.user_sessions[user_id] = {}
        
        # Store the connection
        self.active_connections[user_id][session_id] = websocket
        
        # Initialize session data
        self.user_sessions[user_id][session_id] = {
            "session_id": session_id,
            "connected_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "agent_id": "1",  # Default agent
            "status": "active"
        }
        
        logger.info(f"WebSocket connected: user={user_id}, session={session_id}")
        
        # Send connection confirmation
        await self.send_to_session(user_id, session_id, {
            "type": "connection_established",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, user_id: str, session_id: str):
        """Remove a WebSocket connection"""
        try:
            if user_id in self.active_connections:
                if session_id in self.active_connections[user_id]:
                    del self.active_connections[user_id][session_id]
                
                if session_id in self.user_sessions.get(user_id, {}):
                    del self.user_sessions[user_id][session_id]
                
                # Clean up empty user entries
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
                if user_id in self.user_sessions and not self.user_sessions[user_id]:
                    del self.user_sessions[user_id]
            
            # Clean up typing indicators
            if session_id in self.typing_indicators:
                if user_id in self.typing_indicators[session_id]:
                    del self.typing_indicators[session_id][user_id]
                if not self.typing_indicators[session_id]:
                    del self.typing_indicators[session_id]
            
            logger.info(f"WebSocket disconnected: user={user_id}, session={session_id}")
            
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
    
    async def send_to_session(self, user_id: str, session_id: str, message: Dict):
        """Send message to a specific session"""
        try:
            if (user_id in self.active_connections and 
                session_id in self.active_connections[user_id]):
                
                websocket = self.active_connections[user_id][session_id]
                await websocket.send_text(json.dumps(message))
                
                # Update last activity
                if user_id in self.user_sessions and session_id in self.user_sessions[user_id]:
                    self.user_sessions[user_id][session_id]["last_activity"] = datetime.utcnow()
                
        except Exception as e:
            logger.error(f"Error sending message to session: {e}")
            # Remove broken connection
            self.disconnect(user_id, session_id)
    
    async def send_to_user(self, user_id: str, message: Dict):
        """Send message to all sessions of a user"""
        if user_id in self.active_connections:
            for session_id in list(self.active_connections[user_id].keys()):
                await self.send_to_session(user_id, session_id, message)
    
    async def broadcast_to_session(self, session_id: str, message: Dict, exclude_user: str = None):
        """Broadcast message to all users in a session (for group chats)"""
        for user_id, sessions in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            if session_id in sessions:
                await self.send_to_session(user_id, session_id, message)
    
    def get_active_sessions(self, user_id: str) -> List[Dict]:
        """Get all active sessions for a user"""
        if user_id in self.user_sessions:
            return list(self.user_sessions[user_id].values())
        return []
    
    def is_user_online(self, user_id: str) -> bool:
        """Check if user has any active connections"""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
    
    async def handle_typing_indicator(self, user_id: str, session_id: str, is_typing: bool):
        """Handle typing indicators"""
        if session_id not in self.typing_indicators:
            self.typing_indicators[session_id] = {}
        
        if is_typing:
            self.typing_indicators[session_id][user_id] = datetime.utcnow()
        else:
            if user_id in self.typing_indicators[session_id]:
                del self.typing_indicators[session_id][user_id]
        
        # Broadcast typing status to other users in session
        typing_message = {
            "type": "typing_indicator",
            "session_id": session_id,
            "user_id": user_id,
            "is_typing": is_typing,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_to_session(session_id, typing_message, exclude_user=user_id)
    
    async def cleanup_stale_connections(self):
        """Clean up stale connections and typing indicators"""
        current_time = datetime.utcnow()
        stale_threshold = 300  # 5 minutes
        
        # Clean up stale typing indicators
        for session_id in list(self.typing_indicators.keys()):
            for user_id in list(self.typing_indicators[session_id].keys()):
                last_typing = self.typing_indicators[session_id][user_id]
                if (current_time - last_typing).seconds > 30:  # 30 seconds for typing
                    del self.typing_indicators[session_id][user_id]
            
            if not self.typing_indicators[session_id]:
                del self.typing_indicators[session_id]
        
        # Clean up stale sessions
        for user_id in list(self.user_sessions.keys()):
            for session_id in list(self.user_sessions[user_id].keys()):
                last_activity = self.user_sessions[user_id][session_id]["last_activity"]
                if (current_time - last_activity).seconds > stale_threshold:
                    logger.info(f"Cleaning up stale session: user={user_id}, session={session_id}")
                    self.disconnect(user_id, session_id)

# Global connection manager instance
connection_manager = ConnectionManager()

async def handle_websocket_message(websocket: WebSocket, user_id: str, session_id: str, message_data: Dict):
    """Handle incoming WebSocket messages"""
    try:
        message_type = message_data.get("type")
        
        if message_type == "chat_message":
            await handle_chat_message(user_id, session_id, message_data)
        
        elif message_type == "typing_start":
            await connection_manager.handle_typing_indicator(user_id, session_id, True)
        
        elif message_type == "typing_stop":
            await connection_manager.handle_typing_indicator(user_id, session_id, False)
        
        elif message_type == "agent_switch":
            await handle_agent_switch(user_id, session_id, message_data)
        
        elif message_type == "session_update":
            await handle_session_update(user_id, session_id, message_data)
        
        else:
            logger.warning(f"Unknown message type: {message_type}")
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await connection_manager.send_to_session(user_id, session_id, {
            "type": "error",
            "message": "Failed to process message",
            "timestamp": datetime.utcnow().isoformat()
        })

async def handle_chat_message(user_id: str, session_id: str, message_data: Dict):
    """Handle chat message and generate AI response"""
    try:
        content = message_data.get("content", "").strip()
        agent_id = message_data.get("agent_id", "1")
        
        if not content:
            return
        
        # Store user message in database
        supabase = get_supabase_service()
        
        user_message = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "session_id": session_id,
            "agent_id": agent_id,
            "role": "user",
            "content": content,
            "message_type": "text",
            "metadata": message_data.get("metadata", {})
        }
        
        result = supabase.insert("chat_messages", user_message)
        
        if result["success"]:
            # Send confirmation to user
            await connection_manager.send_to_session(user_id, session_id, {
                "type": "message_sent",
                "message": result["data"][0],
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Generate AI response (placeholder for now)
            await generate_ai_response(user_id, session_id, agent_id, content)
        
    except Exception as e:
        logger.error(f"Error handling chat message: {e}")

async def generate_ai_response(user_id: str, session_id: str, agent_id: str, user_message: str):
    """Generate AI response using real AI service"""
    try:
        from backend.App.ai_service import get_ai_service
        from backend.App.agent_personalities import get_agent_personality

        # Get conversation history for context
        supabase = get_supabase_service()
        history_result = supabase.select("chat_messages", "*", {
            "session_id": session_id,
            "user_id": user_id
        })

        # Build conversation context
        messages = []
        if history_result["success"]:
            # Get last 10 messages for context
            recent_messages = sorted(history_result["data"], key=lambda x: x["created_at"])[-10:]

            for msg in recent_messages:
                if msg["role"] in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Get agent memory and context
        from backend.App.agent_memory import get_agent_memory
        agent_memory = get_agent_memory()
        context = await agent_memory.get_conversation_context(user_id, session_id, agent_id)

        # Generate AI response
        ai_service = get_ai_service()

        # Send typing indicator
        await connection_manager.send_to_session(user_id, session_id, {
            "type": "agent_typing",
            "agent_id": agent_id,
            "is_typing": True,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Generate response with context
        ai_response_data = await ai_service.generate_response(
            messages=messages,
            agent_id=agent_id,
            user_id=user_id
        )

        # Stop typing indicator
        await connection_manager.send_to_session(user_id, session_id, {
            "type": "agent_typing",
            "agent_id": agent_id,
            "is_typing": False,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Get agent info
        agent_personality = get_agent_personality(agent_id)

        # Store AI response in database
        ai_message = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "session_id": session_id,
            "agent_id": agent_id,
            "role": "assistant",
            "content": ai_response_data["content"],
            "message_type": "text",
            "metadata": {
                "agent_name": agent_personality["name"],
                "provider": ai_response_data.get("provider", "unknown"),
                "model": ai_response_data.get("model", "unknown"),
                "usage": ai_response_data.get("usage", {}),
                "is_demo": ai_response_data.get("is_demo", False)
            }
        }

        result = supabase.insert("chat_messages", ai_message)

        if result["success"]:
            # Update agent memory with interaction
            await agent_memory.update_agent_memory(user_id, agent_id, {
                "user_message": user_message,
                "agent_response": ai_response_data["content"],
                "topics": agent_memory._extract_topics_from_history([{"content": user_message}]),
                "timestamp": datetime.utcnow().isoformat()
            })

            # Send AI response to user
            await connection_manager.send_to_session(user_id, session_id, {
                "type": "ai_response",
                "message": result["data"][0],
                "timestamp": datetime.utcnow().isoformat()
            })

    except Exception as e:
        logger.error(f"Error generating AI response: {e}")

        # Send error message to user
        await connection_manager.send_to_session(user_id, session_id, {
            "type": "ai_error",
            "message": "Sorry, I'm having trouble responding right now. Please try again.",
            "timestamp": datetime.utcnow().isoformat()
        })

async def handle_agent_switch(user_id: str, session_id: str, message_data: Dict):
    """Handle agent switching with memory transfer"""
    try:
        from backend.App.agent_memory import get_agent_memory

        new_agent_id = message_data.get("agent_id")

        if new_agent_id in ["1", "2", "3", "4", "5"]:
            # Get current agent
            old_agent_id = "1"  # Default
            if user_id in connection_manager.user_sessions:
                if session_id in connection_manager.user_sessions[user_id]:
                    old_agent_id = connection_manager.user_sessions[user_id][session_id].get("agent_id", "1")
                    connection_manager.user_sessions[user_id][session_id]["agent_id"] = new_agent_id

            # Handle agent handoff with memory
            agent_memory = get_agent_memory()
            handoff_result = await agent_memory.handle_agent_switch(
                user_id, session_id, old_agent_id, new_agent_id
            )

            if handoff_result["success"]:
                # Send handoff message from new agent
                from backend.App.agent_personalities import get_agent_personality
                new_agent = get_agent_personality(new_agent_id)

                # Store handoff message in database
                supabase = get_supabase_service()
                handoff_message = {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "session_id": session_id,
                    "agent_id": new_agent_id,
                    "role": "assistant",
                    "content": handoff_result["handoff_message"],
                    "message_type": "agent_switch",
                    "metadata": {
                        "agent_name": new_agent["name"],
                        "handoff_summary": handoff_result["handoff_summary"],
                        "previous_agent": old_agent_id
                    }
                }

                result = supabase.insert("chat_messages", handoff_message)

                if result["success"]:
                    # Send agent switch confirmation with handoff message
                    await connection_manager.send_to_session(user_id, session_id, {
                        "type": "agent_switched",
                        "agent_id": new_agent_id,
                        "handoff_message": result["data"][0],
                        "timestamp": datetime.utcnow().isoformat()
                    })
            else:
                # Send simple confirmation if handoff failed
                await connection_manager.send_to_session(user_id, session_id, {
                    "type": "agent_switched",
                    "agent_id": new_agent_id,
                    "timestamp": datetime.utcnow().isoformat()
                })

    except Exception as e:
        logger.error(f"Error handling agent switch: {e}")

async def handle_session_update(user_id: str, session_id: str, message_data: Dict):
    """Handle session updates"""
    try:
        updates = message_data.get("updates", {})
        
        if user_id in connection_manager.user_sessions:
            if session_id in connection_manager.user_sessions[user_id]:
                connection_manager.user_sessions[user_id][session_id].update(updates)
        
        # Send confirmation
        await connection_manager.send_to_session(user_id, session_id, {
            "type": "session_updated",
            "updates": updates,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error handling session update: {e}")
