"""
Chat Router for MYTA Real-time Chat
Handles WebSocket connections and chat API endpoints
"""

import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, Request, HTTPException

from backend.App.websocket_manager import (
    connection_manager, 
    handle_websocket_message
)
from backend.App.supabase_client import get_supabase_service
from backend.App.auth_middleware import get_current_user
from backend.App.api_models import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.websocket("/ws/{user_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, session_id: str):
    """WebSocket endpoint for real-time chat"""
    try:
        # Connect to WebSocket
        await connection_manager.connect(websocket, user_id, session_id)
        
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Handle the message
                await handle_websocket_message(websocket, user_id, session_id, message_data)
                
            except WebSocketDisconnect:
                break
            except json.JSONDecodeError:
                await connection_manager.send_to_session(user_id, session_id, {
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {e}")
                await connection_manager.send_to_session(user_id, session_id, {
                    "type": "error",
                    "message": "Internal server error",
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    
    finally:
        # Clean up connection
        connection_manager.disconnect(user_id, session_id)

@router.get("/sessions")
async def get_chat_sessions(
    limit: int = Query(20, description="Number of sessions to return"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user's chat sessions"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get sessions from database
        result = supabase.select("chat_sessions", "*", {"user_id": user_id})
        
        if result["success"]:
            sessions = result["data"]
            
            # Sort by last_message_at desc and limit
            sessions.sort(key=lambda x: x.get("last_message_at", ""), reverse=True)
            sessions = sessions[:limit]
            
            # Add online status
            for session in sessions:
                session_id = session["id"]
                session["is_active"] = any(
                    session_id in user_sessions 
                    for user_sessions in connection_manager.user_sessions.values()
                )
            
            return create_success_response("Chat sessions retrieved", {"sessions": sessions})
        else:
            return create_error_response("Failed to retrieve chat sessions", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting chat sessions: {e}")
        return create_error_response("Failed to retrieve chat sessions", str(e))

@router.post("/sessions")
async def create_chat_session(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new chat session"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        agent_id = body.get("agent_id", "1")
        title = body.get("title", f"Chat with Agent {agent_id}")
        
        # Validate agent_id
        if agent_id not in ["1", "2", "3", "4", "5"]:
            agent_id = "1"
        
        session_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "agent_id": agent_id,
            "title": title,
            "status": "active",
            "last_message_at": datetime.utcnow().isoformat(),
            "message_count": 0,
            "metadata": body.get("metadata", {})
        }
        
        supabase = get_supabase_service()
        result = supabase.insert("chat_sessions", session_data)
        
        if result["success"]:
            return create_success_response("Chat session created", {"session": result["data"][0]})
        else:
            return create_error_response("Failed to create chat session", result["error"])
            
    except Exception as e:
        logger.error(f"Error creating chat session: {e}")
        return create_error_response("Failed to create chat session", str(e))

@router.get("/sessions/{session_id}/messages")
async def get_chat_messages(
    session_id: str,
    limit: int = Query(50, description="Number of messages to return"),
    before: Optional[str] = Query(None, description="Get messages before this timestamp"),
    current_user: Dict = Depends(get_current_user)
):
    """Get messages for a chat session"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Verify session belongs to user
        session_result = supabase.select("chat_sessions", "*", {"id": session_id, "user_id": user_id})
        
        if not (session_result["success"] and session_result["data"]):
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Get messages
        filters = {"session_id": session_id, "user_id": user_id}
        result = supabase.select("chat_messages", "*", filters)
        
        if result["success"]:
            messages = result["data"]
            
            # Filter by timestamp if provided
            if before:
                try:
                    before_dt = datetime.fromisoformat(before.replace("Z", "+00:00"))
                    messages = [
                        msg for msg in messages 
                        if datetime.fromisoformat(msg["created_at"].replace("Z", "+00:00")) < before_dt
                    ]
                except:
                    pass
            
            # Sort by created_at desc and limit
            messages.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            messages = messages[:limit]
            
            # Reverse to get chronological order
            messages.reverse()
            
            return create_success_response("Chat messages retrieved", {"messages": messages})
        else:
            return create_error_response("Failed to retrieve chat messages", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat messages: {e}")
        return create_error_response("Failed to retrieve chat messages", str(e))

@router.put("/sessions/{session_id}")
async def update_chat_session(
    session_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update a chat session"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        update_data = {}
        
        if "title" in body:
            update_data["title"] = body["title"]
        
        if "status" in body:
            if body["status"] in ["active", "archived", "deleted"]:
                update_data["status"] = body["status"]
        
        if "agent_id" in body:
            if body["agent_id"] in ["1", "2", "3", "4", "5"]:
                update_data["agent_id"] = body["agent_id"]
        
        if "metadata" in body:
            update_data["metadata"] = body["metadata"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        supabase = get_supabase_service()
        result = supabase.update("chat_sessions", update_data, {"id": session_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            return create_success_response("Chat session updated", {"session": result["data"][0]})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Chat session not found")
        else:
            return create_error_response("Failed to update chat session", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating chat session: {e}")
        return create_error_response("Failed to update chat session", str(e))

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a chat session and its messages"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Delete messages first (due to foreign key constraint)
        supabase.delete("chat_messages", {"session_id": session_id, "user_id": user_id})
        
        # Delete session
        result = supabase.delete("chat_sessions", {"id": session_id, "user_id": user_id})
        
        if result["success"]:
            return create_success_response("Chat session deleted successfully")
        else:
            return create_error_response("Failed to delete chat session", result["error"])
            
    except Exception as e:
        logger.error(f"Error deleting chat session: {e}")
        return create_error_response("Failed to delete chat session", str(e))

@router.get("/status")
async def get_chat_status(current_user: Dict = Depends(get_current_user)):
    """Get chat system status and active connections"""
    try:
        user_id = current_user["id"]
        
        # Get active sessions for user
        active_sessions = connection_manager.get_active_sessions(user_id)
        is_online = connection_manager.is_user_online(user_id)
        
        # Get recent activity
        supabase = get_supabase_service()
        result = supabase.select("chat_sessions", "*", {"user_id": user_id})
        
        total_sessions = len(result["data"]) if result["success"] else 0
        
        status = {
            "is_online": is_online,
            "active_sessions": len(active_sessions),
            "total_sessions": total_sessions,
            "sessions": active_sessions,
            "server_time": datetime.utcnow().isoformat()
        }
        
        return create_success_response("Chat status retrieved", {"status": status})
        
    except Exception as e:
        logger.error(f"Error getting chat status: {e}")
        return create_error_response("Failed to retrieve chat status", str(e))

@router.post("/messages/{message_id}/edit")
async def edit_chat_message(
    message_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Edit a chat message"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        new_content = body.get("content", "").strip()
        if not new_content:
            raise HTTPException(status_code=400, detail="Message content is required")
        
        update_data = {
            "content": new_content,
            "is_edited": True,
            "edited_at": datetime.utcnow().isoformat()
        }
        
        supabase = get_supabase_service()
        result = supabase.update("chat_messages", update_data, {"id": message_id, "user_id": user_id, "role": "user"})
        
        if result["success"] and result["data"]:
            message = result["data"][0]
            
            # Notify connected sessions about the edit
            session_id = message["session_id"]
            await connection_manager.send_to_session(user_id, session_id, {
                "type": "message_edited",
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return create_success_response("Message edited successfully", {"message": message})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Message not found or cannot be edited")
        else:
            return create_error_response("Failed to edit message", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        return create_error_response("Failed to edit message", str(e))
