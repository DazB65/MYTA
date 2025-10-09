"""
Notes Router for MYTA
Handles note management operations with Supabase integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import uuid

from .supabase_client import get_supabase_service
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("/")
async def get_notes(
    limit: int = Query(50, description="Number of notes to return"),
    search: Optional[str] = Query(None, description="Search in note content"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user's notes with optional filtering"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get notes from Supabase
        result = supabase.select("notes", "*", {"user_id": user_id})
        
        if result["success"]:
            notes = result["data"]
            
            # Apply search filter
            if search:
                search_lower = search.lower()
                notes = [note for note in notes if search_lower in note.get("content", "").lower()]
            
            # Apply tags filter
            if tags:
                tag_list = [tag.strip() for tag in tags.split(",")]
                notes = [note for note in notes 
                        if any(tag in note.get("tags", []) for tag in tag_list)]
            
            # Sort by created_at desc and limit
            notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            notes = notes[:limit]
            
            return create_success_response("Notes retrieved successfully", {"notes": notes})
        else:
            return create_error_response("Failed to retrieve notes", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting notes: {e}")
        return create_error_response("Failed to retrieve notes", str(e))

@router.post("/")
async def create_note(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new note"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Validate required fields
        content = body.get("content", "").strip()
        if not content:
            raise HTTPException(status_code=400, detail="Note content is required")
        
        # Prepare note data
        note_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "content": content,
            "tags": body.get("tags", []),
            "metadata": body.get("metadata", {})
        }
        
        supabase = get_supabase_service()
        result = supabase.insert("notes", note_data)
        
        if result["success"]:
            return create_success_response("Note created successfully", {"note": result["data"][0]})
        else:
            return create_error_response("Failed to create note", result["error"])
            
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        return create_error_response("Failed to create note", str(e))

@router.get("/{note_id}")
async def get_note(
    note_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get a specific note by ID"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.select("notes", "*", {"id": note_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            return create_success_response("Note retrieved successfully", {"note": result["data"][0]})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Note not found")
        else:
            return create_error_response("Failed to retrieve note", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting note: {e}")
        return create_error_response("Failed to retrieve note", str(e))

@router.put("/{note_id}")
async def update_note(
    note_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update a note"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Prepare update data
        update_data = {}
        
        # Only update provided fields
        if "content" in body:
            content = body["content"].strip()
            if not content:
                raise HTTPException(status_code=400, detail="Note content cannot be empty")
            update_data["content"] = content
        
        if "tags" in body:
            update_data["tags"] = body["tags"]
        
        if "metadata" in body:
            update_data["metadata"] = body["metadata"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        supabase = get_supabase_service()
        result = supabase.update("notes", update_data, {"id": note_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            return create_success_response("Note updated successfully", {"note": result["data"][0]})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Note not found")
        else:
            return create_error_response("Failed to update note", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating note: {e}")
        return create_error_response("Failed to update note", str(e))

@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a note"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.delete("notes", {"id": note_id, "user_id": user_id})
        
        if result["success"]:
            return create_success_response("Note deleted successfully")
        else:
            return create_error_response("Failed to delete note", result["error"])
            
    except Exception as e:
        logger.error(f"Error deleting note: {e}")
        return create_error_response("Failed to delete note", str(e))

@router.get("/search/content")
async def search_notes(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, description="Number of results to return"),
    current_user: Dict = Depends(get_current_user)
):
    """Search notes by content"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get all notes for the user
        result = supabase.select("notes", "*", {"user_id": user_id})
        
        if result["success"]:
            notes = result["data"]
            
            # Perform case-insensitive search
            search_query = q.lower()
            matching_notes = []
            
            for note in notes:
                content = note.get("content", "").lower()
                if search_query in content:
                    # Add search relevance score (simple word count)
                    note["relevance_score"] = content.count(search_query)
                    matching_notes.append(note)
            
            # Sort by relevance score (descending) then by created_at (descending)
            matching_notes.sort(key=lambda x: (x.get("relevance_score", 0), x.get("created_at", "")), reverse=True)
            matching_notes = matching_notes[:limit]
            
            # Remove relevance score from response
            for note in matching_notes:
                note.pop("relevance_score", None)
            
            return create_success_response(
                f"Found {len(matching_notes)} notes matching '{q}'",
                {"notes": matching_notes, "query": q}
            )
        else:
            return create_error_response("Failed to search notes", result["error"])
            
    except Exception as e:
        logger.error(f"Error searching notes: {e}")
        return create_error_response("Failed to search notes", str(e))

@router.get("/tags/list")
async def get_note_tags(current_user: Dict = Depends(get_current_user)):
    """Get all unique tags used in user's notes"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get all notes for the user
        result = supabase.select("notes", "tags", {"user_id": user_id})
        
        if result["success"]:
            notes = result["data"]
            
            # Collect all unique tags
            all_tags = set()
            for note in notes:
                tags = note.get("tags", [])
                if isinstance(tags, list):
                    all_tags.update(tags)
            
            # Convert to sorted list
            unique_tags = sorted(list(all_tags))
            
            return create_success_response("Note tags retrieved successfully", {"tags": unique_tags})
        else:
            return create_error_response("Failed to retrieve note tags", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting note tags: {e}")
        return create_error_response("Failed to retrieve note tags", str(e))

@router.post("/bulk-delete")
async def bulk_delete_notes(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Bulk delete multiple notes"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        note_ids = body.get("note_ids", [])
        if not note_ids:
            raise HTTPException(status_code=400, detail="No note IDs provided")
        
        supabase = get_supabase_service()
        deleted_count = 0
        
        for note_id in note_ids:
            result = supabase.delete("notes", {"id": note_id, "user_id": user_id})
            if result["success"]:
                deleted_count += 1
        
        return create_success_response(
            f"Bulk delete completed. {deleted_count} notes deleted.",
            {"deleted_count": deleted_count, "total_requested": len(note_ids)}
        )
        
    except Exception as e:
        logger.error(f"Error in bulk delete: {e}")
        return create_error_response("Failed to perform bulk delete", str(e))

@router.get("/stats/summary")
async def get_note_stats(current_user: Dict = Depends(get_current_user)):
    """Get note statistics for the user"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get all notes for the user
        result = supabase.select("notes", "*", {"user_id": user_id})
        
        if result["success"]:
            notes = result["data"]
            
            # Calculate statistics
            total = len(notes)
            
            # Count unique tags
            all_tags = set()
            total_words = 0
            
            for note in notes:
                # Count tags
                tags = note.get("tags", [])
                if isinstance(tags, list):
                    all_tags.update(tags)
                
                # Count words
                content = note.get("content", "")
                words = len(content.split()) if content else 0
                total_words += words
            
            # Calculate recent activity (notes created in last 7 days)
            from datetime import datetime, timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_notes = 0
            
            for note in notes:
                created_at = note.get("created_at")
                if created_at:
                    try:
                        note_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                        if note_date >= week_ago:
                            recent_notes += 1
                    except:
                        pass
            
            stats = {
                "total": total,
                "unique_tags": len(all_tags),
                "total_words": total_words,
                "average_words_per_note": round(total_words / total, 1) if total > 0 else 0,
                "recent_notes_7_days": recent_notes
            }
            
            return create_success_response("Note statistics retrieved", {"stats": stats})
        else:
            return create_error_response("Failed to retrieve note statistics", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting note stats: {e}")
        return create_error_response("Failed to retrieve note statistics", str(e))
