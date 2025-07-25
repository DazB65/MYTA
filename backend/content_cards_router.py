"""
Content Cards Router for CreatorMate
Contains all content cards-related API endpoints for the Content Studio feature
Uses local SQLite storage as a fallback when Supabase is not configured
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import logging
import traceback
import uuid
from typing import List, Optional, Dict, Any
import os

# Import models
from api_models import (
    ContentCardCreate, ContentCardUpdate, ContentCardStatusUpdate,
    ContentCardResponse, ContentCardsListResponse, StandardResponse,
    create_error_response, create_success_response
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/content-cards", tags=["content-cards"])

# Try to import Supabase, fall back to local storage if not available
USE_SUPABASE = False
supabase_client = None

try:
    from supabase import create_client
    supabase_url = os.getenv("SUPABASE_URL") or os.getenv("SB_URL")
    supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SB_KEY")
    
    if supabase_url and supabase_key:
        supabase_client = create_client(supabase_url, supabase_key)
        USE_SUPABASE = True
        logger.info("Using Supabase for content cards storage")
except Exception as e:
    logger.info("Supabase not configured, using local SQLite storage")

# Import local storage as fallback
from content_cards_local import get_local_content_cards_db

# Initialize Supabase client
def get_supabase_client():
    """Get configured Supabase client"""
    if USE_SUPABASE and supabase_client:
        return supabase_client
    else:
        # Return None to indicate local storage should be used
        return None

# =============================================================================
# Content Cards CRUD Endpoints
# =============================================================================

@router.get("", response_model=StandardResponse)
async def get_content_cards(
    user_id: str = Query(..., description="User ID to filter cards"),
    status: Optional[str] = Query(None, description="Filter by status"),
    include_archived: bool = Query(False, description="Include archived cards"),
    limit: int = Query(100, description="Maximum number of cards to return")
):
    """Fetch content cards for a user, optionally filtered by status"""
    try:
        logger.info(f"Fetching content cards for user: {user_id}, status: {status}")
        
        supabase = get_supabase_client()
        
        if supabase:
            # Use Supabase
            # Build query
            query = supabase.table("content_cards").select("*").eq("user_id", user_id)
            
            # Add status filter if provided
            if status:
                query = query.eq("status", status)
                
            # Add archived filter
            if not include_archived:
                query = query.eq("archived", False)
                
            # Add ordering and limit
            query = query.order("order_index", desc=False).order("created_at", desc=True).limit(limit)
            
            # Execute query
            result = query.execute()
            
            if not result.data:
                return create_success_response(
                    "No content cards found",
                    {"cards": [], "total_count": 0, "status_counts": {}}
                )
            
            cards = result.data
        else:
            # Use local SQLite storage
            local_db = get_local_content_cards_db()
            cards = local_db.get_cards(user_id, status, include_archived)
            
            if not cards:
                return create_success_response(
                    "No content cards found",
                    {"cards": [], "total_count": 0, "status_counts": {}}
                )
        
        # Continue with existing card processing logic
        
        for card_data in result.data:
            # Convert datetime strings for response
            card_response = ContentCardResponse(
                id=str(card_data["id"]),
                user_id=card_data["user_id"],
                title=card_data["title"],
                description=card_data["description"] or "",
                status=card_data["status"],
                pillars=card_data["pillars"] or [],
                due_date=card_data["due_date"],
                progress=card_data["progress"],
                archived=card_data["archived"],
                order_index=card_data["order_index"],
                created_at=card_data["created_at"],
                updated_at=card_data["updated_at"]
            )
            cards.append(card_response)
            
            # Count statuses
            card_status = card_data["status"]
            status_counts[card_status] = status_counts.get(card_status, 0) + 1
        
        response_data = ContentCardsListResponse(
            cards=cards,
            total_count=len(cards),
            status_counts=status_counts
        )
        
        return create_success_response(
            f"Retrieved {len(cards)} content cards",
            response_data.dict()
        )
        
    except Exception as e:
        logger.error(f"Error fetching content cards: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to fetch content cards")

@router.post("", response_model=StandardResponse)
async def create_content_card(card_data: ContentCardCreate):
    """Create a new content card"""
    try:
        logger.info(f"Creating content card for user: {card_data.user_id}")
        
        supabase = get_supabase_client()
        
        if supabase:
            # Use Supabase
            # Get next order index for this user and status
            order_result = supabase.table("content_cards")\
                .select("order_index")\
                .eq("user_id", card_data.user_id)\
                .eq("status", card_data.status)\
                .eq("archived", False)\
                .order("order_index", desc=True)\
                .limit(1)\
                .execute()
            
            next_order = 1000  # Default starting order
            if order_result.data:
                next_order = order_result.data[0]["order_index"] + 1000
            
            # Prepare card data for insertion
            insert_data = {
                "user_id": card_data.user_id,
                "title": card_data.title,
                "description": card_data.description,
                "status": card_data.status,
                "pillars": card_data.pillars,
                "due_date": card_data.due_date,
                "progress": card_data.progress,
                "archived": False,
                "order_index": next_order
            }
            
            # Insert into Supabase
            result = supabase.table("content_cards").insert(insert_data).execute()
            
            if not result.data:
                raise HTTPException(status_code=500, detail="Failed to create content card")
            
            created_card = result.data[0]
        else:
            # Use local SQLite storage
            local_db = get_local_content_cards_db()
            created_card = local_db.create_card(
                user_id=card_data.user_id,
                title=card_data.title,
                description=card_data.description,
                status=card_data.status,
                pillars=card_data.pillars,
                due_date=card_data.due_date,
                progress=card_data.progress
            )
        
        # Convert to response model
        card_response = ContentCardResponse(
            id=str(created_card["id"]),
            user_id=created_card["user_id"],
            title=created_card["title"],
            description=created_card["description"] or "",
            status=created_card["status"],
            pillars=created_card["pillars"] or [],
            due_date=created_card["due_date"],
            progress=created_card["progress"],
            archived=created_card["archived"],
            order_index=created_card["order_index"],
            created_at=created_card["created_at"],
            updated_at=created_card["updated_at"]
        )
        
        return create_success_response(
            "Content card created successfully",
            {"card": card_response.dict()}
        )
        
    except Exception as e:
        logger.error(f"Error creating content card: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to create content card")

@router.put("/{card_id}", response_model=StandardResponse)
async def update_content_card(card_id: str, card_data: ContentCardUpdate, user_id: str = Query(...)):
    """Update an existing content card"""
    try:
        logger.info(f"Updating content card {card_id} for user: {user_id}")
        
        supabase = get_supabase_client()
        
        # Verify card exists and belongs to user
        existing_result = supabase.table("content_cards")\
            .select("*")\
            .eq("id", card_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not existing_result.data:
            raise HTTPException(status_code=404, detail="Content card not found")
        
        # Prepare update data (only include non-None values)
        update_data = {}
        if card_data.title is not None:
            update_data["title"] = card_data.title
        if card_data.description is not None:
            update_data["description"] = card_data.description
        if card_data.status is not None:
            update_data["status"] = card_data.status
        if card_data.pillars is not None:
            update_data["pillars"] = card_data.pillars
        if card_data.due_date is not None:
            update_data["due_date"] = card_data.due_date
        if card_data.progress is not None:
            update_data["progress"] = card_data.progress
        if card_data.archived is not None:
            update_data["archived"] = card_data.archived
        if card_data.order_index is not None:
            update_data["order_index"] = card_data.order_index
        
        # Update in Supabase
        result = supabase.table("content_cards")\
            .update(update_data)\
            .eq("id", card_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update content card")
        
        updated_card = result.data[0]
        
        # Convert to response model
        card_response = ContentCardResponse(
            id=str(updated_card["id"]),
            user_id=updated_card["user_id"],
            title=updated_card["title"],
            description=updated_card["description"] or "",
            status=updated_card["status"],
            pillars=updated_card["pillars"] or [],
            due_date=updated_card["due_date"],
            progress=updated_card["progress"],
            archived=updated_card["archived"],
            order_index=updated_card["order_index"],
            created_at=updated_card["created_at"],
            updated_at=updated_card["updated_at"]
        )
        
        return create_success_response(
            "Content card updated successfully",
            {"card": card_response.dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content card: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update content card")

@router.patch("/{card_id}/status", response_model=StandardResponse)
async def update_card_status(card_id: str, status_data: ContentCardStatusUpdate):
    """Update just the status of a content card (for drag-and-drop)"""
    try:
        logger.info(f"Updating status of card {card_id} to {status_data.status}")
        
        supabase = get_supabase_client()
        
        # Verify card exists and belongs to user
        existing_result = supabase.table("content_cards")\
            .select("*")\
            .eq("id", card_id)\
            .eq("user_id", status_data.user_id)\
            .execute()
        
        if not existing_result.data:
            raise HTTPException(status_code=404, detail="Content card not found")
        
        # Prepare update data
        update_data = {"status": status_data.status}
        if status_data.order_index is not None:
            update_data["order_index"] = status_data.order_index
        
        # Update in Supabase
        result = supabase.table("content_cards")\
            .update(update_data)\
            .eq("id", card_id)\
            .eq("user_id", status_data.user_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to update card status")
        
        return create_success_response(
            f"Card status updated to {status_data.status}",
            {"card_id": card_id, "new_status": status_data.status}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating card status: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to update card status")

@router.delete("/{card_id}", response_model=StandardResponse)
async def delete_content_card(card_id: str, user_id: str = Query(...)):
    """Soft delete a content card (mark as archived)"""
    try:
        logger.info(f"Deleting content card {card_id} for user: {user_id}")
        
        supabase = get_supabase_client()
        
        # Verify card exists and belongs to user
        existing_result = supabase.table("content_cards")\
            .select("*")\
            .eq("id", card_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not existing_result.data:
            raise HTTPException(status_code=404, detail="Content card not found")
        
        # Soft delete by marking as archived
        result = supabase.table("content_cards")\
            .update({"archived": True})\
            .eq("id", card_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to delete content card")
        
        return create_success_response(
            "Content card deleted successfully",
            {"card_id": card_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content card: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to delete content card")

@router.post("/{card_id}/duplicate", response_model=StandardResponse)
async def duplicate_content_card(card_id: str, user_id: str = Query(...)):
    """Create a copy of an existing content card"""
    try:
        logger.info(f"Duplicating content card {card_id} for user: {user_id}")
        
        supabase = get_supabase_client()
        
        # Get the original card
        original_result = supabase.table("content_cards")\
            .select("*")\
            .eq("id", card_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if not original_result.data:
            raise HTTPException(status_code=404, detail="Content card not found")
        
        original_card = original_result.data[0]
        
        # Get next order index for the same status
        order_result = supabase.table("content_cards")\
            .select("order_index")\
            .eq("user_id", user_id)\
            .eq("status", original_card["status"])\
            .eq("archived", False)\
            .order("order_index", desc=True)\
            .limit(1)\
            .execute()
        
        next_order = 1000
        if order_result.data:
            next_order = order_result.data[0]["order_index"] + 1000
        
        # Prepare duplicate data
        duplicate_data = {
            "user_id": user_id,
            "title": f"{original_card['title']} (Copy)",
            "description": original_card["description"],
            "status": original_card["status"],
            "pillars": original_card["pillars"],
            "due_date": original_card["due_date"],
            "progress": original_card["progress"],
            "archived": False,
            "order_index": next_order
        }
        
        # Insert duplicate
        result = supabase.table("content_cards").insert(duplicate_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to duplicate content card")
        
        duplicated_card = result.data[0]
        
        # Convert to response model
        card_response = ContentCardResponse(
            id=str(duplicated_card["id"]),
            user_id=duplicated_card["user_id"],
            title=duplicated_card["title"],
            description=duplicated_card["description"] or "",
            status=duplicated_card["status"],
            pillars=duplicated_card["pillars"] or [],
            due_date=duplicated_card["due_date"],
            progress=duplicated_card["progress"],
            archived=duplicated_card["archived"],
            order_index=duplicated_card["order_index"],
            created_at=duplicated_card["created_at"],
            updated_at=duplicated_card["updated_at"]
        )
        
        return create_success_response(
            "Content card duplicated successfully",
            {"card": card_response.dict()}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error duplicating content card: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to duplicate content card")

# =============================================================================
# Utility Endpoints
# =============================================================================

@router.get("/stats/{user_id}", response_model=StandardResponse)
async def get_content_cards_stats(user_id: str):
    """Get statistics about content cards for a user"""
    try:
        logger.info(f"Getting content cards stats for user: {user_id}")
        
        supabase = get_supabase_client()
        
        # Get all non-archived cards for the user
        result = supabase.table("content_cards")\
            .select("status")\
            .eq("user_id", user_id)\
            .eq("archived", False)\
            .execute()
        
        # Count by status
        status_counts = {}
        total_cards = len(result.data) if result.data else 0
        
        if result.data:
            for card in result.data:
                status = card["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
        
        stats = {
            "total_cards": total_cards,
            "status_counts": status_counts,
            "active_statuses": list(status_counts.keys())
        }
        
        return create_success_response(
            "Content cards stats retrieved successfully",
            stats
        )
        
    except Exception as e:
        logger.error(f"Error getting content cards stats: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to get content cards stats")# Trigger reload
