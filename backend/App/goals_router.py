"""
Goals Router for MYTA
Handles goal management operations with Supabase integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import uuid

from backend.App.supabase_client import get_supabase_service
from backend.App.auth_middleware import get_current_user
from backend.App.api_models import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/goals", tags=["goals"])

@router.get("/")
async def get_goals(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user's goals with optional filtering"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Build filters
        filters = {"user_id": user_id}
        if status:
            filters["status"] = status
        if category:
            filters["category"] = category
        
        # Get goals from Supabase
        result = supabase.select("goals", "*", filters)
        
        if result["success"]:
            goals = result["data"]
            
            # Calculate progress for each goal
            for goal in goals:
                if goal.get("target_value") and goal.get("target_value") > 0:
                    current = goal.get("current_value", 0)
                    target = goal.get("target_value")
                    goal["progress_percentage"] = min(100, round((current / target) * 100, 1))
                else:
                    goal["progress_percentage"] = 0
            
            # Sort by created_at desc
            goals.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            return create_success_response("Goals retrieved successfully", {"goals": goals})
        else:
            return create_error_response("Failed to retrieve goals", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting goals: {e}")
        return create_error_response("Failed to retrieve goals", str(e))

@router.post("/")
async def create_goal(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new goal"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Validate required fields
        if not body.get("title"):
            raise HTTPException(status_code=400, detail="Goal title is required")
        
        # Prepare goal data
        goal_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": body["title"],
            "description": body.get("description", ""),
            "target_value": body.get("target_value"),
            "current_value": body.get("current_value", 0),
            "unit": body.get("unit", ""),
            "target_date": body.get("target_date"),
            "status": body.get("status", "active"),
            "priority": body.get("priority", "medium"),
            "category": body.get("category", ""),
            "metadata": body.get("metadata", {})
        }
        
        # Validate status and priority
        valid_statuses = ["active", "completed", "paused", "cancelled"]
        valid_priorities = ["low", "medium", "high"]
        
        if goal_data["status"] not in valid_statuses:
            goal_data["status"] = "active"
        
        if goal_data["priority"] not in valid_priorities:
            goal_data["priority"] = "medium"
        
        supabase = get_supabase_service()
        result = supabase.insert("goals", goal_data)
        
        if result["success"]:
            goal = result["data"][0]
            # Calculate progress
            if goal.get("target_value") and goal.get("target_value") > 0:
                current = goal.get("current_value", 0)
                target = goal.get("target_value")
                goal["progress_percentage"] = min(100, round((current / target) * 100, 1))
            else:
                goal["progress_percentage"] = 0
            
            return create_success_response("Goal created successfully", {"goal": goal})
        else:
            return create_error_response("Failed to create goal", result["error"])
            
    except Exception as e:
        logger.error(f"Error creating goal: {e}")
        return create_error_response("Failed to create goal", str(e))

@router.get("/{goal_id}")
async def get_goal(
    goal_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get a specific goal by ID"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.select("goals", "*", {"id": goal_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            goal = result["data"][0]
            
            # Calculate progress
            if goal.get("target_value") and goal.get("target_value") > 0:
                current = goal.get("current_value", 0)
                target = goal.get("target_value")
                goal["progress_percentage"] = min(100, round((current / target) * 100, 1))
            else:
                goal["progress_percentage"] = 0
            
            return create_success_response("Goal retrieved successfully", {"goal": goal})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Goal not found")
        else:
            return create_error_response("Failed to retrieve goal", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting goal: {e}")
        return create_error_response("Failed to retrieve goal", str(e))

@router.put("/{goal_id}")
async def update_goal(
    goal_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update a goal"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Prepare update data
        update_data = {}
        
        # Only update provided fields
        if "title" in body:
            update_data["title"] = body["title"]
        if "description" in body:
            update_data["description"] = body["description"]
        if "target_value" in body:
            update_data["target_value"] = body["target_value"]
        if "current_value" in body:
            update_data["current_value"] = body["current_value"]
        if "unit" in body:
            update_data["unit"] = body["unit"]
        if "target_date" in body:
            update_data["target_date"] = body["target_date"]
        if "status" in body:
            if body["status"] in ["active", "completed", "paused", "cancelled"]:
                update_data["status"] = body["status"]
        if "priority" in body:
            if body["priority"] in ["low", "medium", "high"]:
                update_data["priority"] = body["priority"]
        if "category" in body:
            update_data["category"] = body["category"]
        if "metadata" in body:
            update_data["metadata"] = body["metadata"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        supabase = get_supabase_service()
        result = supabase.update("goals", update_data, {"id": goal_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            goal = result["data"][0]
            
            # Calculate progress
            if goal.get("target_value") and goal.get("target_value") > 0:
                current = goal.get("current_value", 0)
                target = goal.get("target_value")
                goal["progress_percentage"] = min(100, round((current / target) * 100, 1))
            else:
                goal["progress_percentage"] = 0
            
            return create_success_response("Goal updated successfully", {"goal": goal})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Goal not found")
        else:
            return create_error_response("Failed to update goal", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating goal: {e}")
        return create_error_response("Failed to update goal", str(e))

@router.delete("/{goal_id}")
async def delete_goal(
    goal_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a goal"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.delete("goals", {"id": goal_id, "user_id": user_id})
        
        if result["success"]:
            return create_success_response("Goal deleted successfully")
        else:
            return create_error_response("Failed to delete goal", result["error"])
            
    except Exception as e:
        logger.error(f"Error deleting goal: {e}")
        return create_error_response("Failed to delete goal", str(e))

@router.post("/{goal_id}/progress")
async def update_goal_progress(
    goal_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update goal progress"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        current_value = body.get("current_value")
        if current_value is None:
            raise HTTPException(status_code=400, detail="current_value is required")
        
        # Update the goal's current value
        update_data = {"current_value": current_value}
        
        supabase = get_supabase_service()
        result = supabase.update("goals", update_data, {"id": goal_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            goal = result["data"][0]
            
            # Calculate progress
            if goal.get("target_value") and goal.get("target_value") > 0:
                current = goal.get("current_value", 0)
                target = goal.get("target_value")
                goal["progress_percentage"] = min(100, round((current / target) * 100, 1))
                
                # Auto-complete if target reached
                if current >= target and goal.get("status") == "active":
                    complete_result = supabase.update("goals", {"status": "completed"}, {"id": goal_id, "user_id": user_id})
                    if complete_result["success"]:
                        goal["status"] = "completed"
            else:
                goal["progress_percentage"] = 0
            
            return create_success_response("Goal progress updated successfully", {"goal": goal})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Goal not found")
        else:
            return create_error_response("Failed to update goal progress", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        return create_error_response("Failed to update goal progress", str(e))

@router.get("/stats/summary")
async def get_goal_stats(current_user: Dict = Depends(get_current_user)):
    """Get goal statistics for the user"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get all goals for the user
        result = supabase.select("goals", "*", {"user_id": user_id})
        
        if result["success"]:
            goals = result["data"]
            
            # Calculate statistics
            total = len(goals)
            active = len([g for g in goals if g.get("status") == "active"])
            completed = len([g for g in goals if g.get("status") == "completed"])
            
            # Calculate average progress
            total_progress = 0
            goals_with_targets = 0
            
            for goal in goals:
                if goal.get("target_value") and goal.get("target_value") > 0:
                    current = goal.get("current_value", 0)
                    target = goal.get("target_value")
                    progress = min(100, (current / target) * 100)
                    total_progress += progress
                    goals_with_targets += 1
            
            avg_progress = round(total_progress / goals_with_targets, 1) if goals_with_targets > 0 else 0
            
            stats = {
                "total": total,
                "active": active,
                "completed": completed,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
                "average_progress": avg_progress
            }
            
            return create_success_response("Goal statistics retrieved", {"stats": stats})
        else:
            return create_error_response("Failed to retrieve goal statistics", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting goal stats: {e}")
        return create_error_response("Failed to retrieve goal statistics", str(e))
