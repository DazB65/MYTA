"""
Tasks Router for MYTA
Handles task management operations with Supabase integration
"""

from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import Dict, List, Optional, Any
import json
from datetime import datetime, timedelta
import uuid

from backend.App.supabase_client import get_supabase_service
from backend.App.auth_middleware import get_current_user
from backend.App.response_utils import create_success_response, create_error_response
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
async def get_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    limit: int = Query(50, description="Number of tasks to return"),
    current_user: Dict = Depends(get_current_user)
):
    """Get user's tasks with optional filtering"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Build filters
        filters = {"user_id": user_id}
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        
        # Get tasks from Supabase
        result = supabase.select("tasks", "*", filters)
        
        if result["success"]:
            tasks = result["data"]
            
            # Sort by created_at desc and limit
            tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            tasks = tasks[:limit]
            
            return create_success_response("Tasks retrieved successfully", {"tasks": tasks})
        else:
            return create_error_response("Failed to retrieve tasks", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return create_error_response("Failed to retrieve tasks", str(e))

@router.post("/")
async def create_task(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new task"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        # Validate required fields
        if not body.get("title"):
            raise HTTPException(status_code=400, detail="Task title is required")
        
        # Prepare task data
        task_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "title": body["title"],
            "description": body.get("description", ""),
            "priority": body.get("priority", "medium"),
            "status": body.get("status", "pending"),
            "due_date": body.get("due_date"),
            "tags": body.get("tags", []),
            "metadata": body.get("metadata", {})
        }
        
        # Validate priority and status
        valid_priorities = ["low", "medium", "high", "urgent"]
        valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
        
        if task_data["priority"] not in valid_priorities:
            task_data["priority"] = "medium"
        
        if task_data["status"] not in valid_statuses:
            task_data["status"] = "pending"
        
        supabase = get_supabase_service()
        result = supabase.insert("tasks", task_data)
        
        if result["success"]:
            return create_success_response("Task created successfully", {"task": result["data"][0]})
        else:
            return create_error_response("Failed to create task", result["error"])
            
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return create_error_response("Failed to create task", str(e))

@router.get("/{task_id}")
async def get_task(
    task_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get a specific task by ID"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.select("tasks", "*", {"id": task_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            return create_success_response("Task retrieved successfully", {"task": result["data"][0]})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            return create_error_response("Failed to retrieve task", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task: {e}")
        return create_error_response("Failed to retrieve task", str(e))

@router.put("/{task_id}")
async def update_task(
    task_id: str,
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Update a task"""
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
        if "priority" in body:
            if body["priority"] in ["low", "medium", "high", "urgent"]:
                update_data["priority"] = body["priority"]
        if "status" in body:
            if body["status"] in ["pending", "in_progress", "completed", "cancelled"]:
                update_data["status"] = body["status"]
                # Set completed_at if status is completed
                if body["status"] == "completed":
                    update_data["completed_at"] = datetime.utcnow().isoformat()
                elif body["status"] != "completed":
                    update_data["completed_at"] = None
        if "due_date" in body:
            update_data["due_date"] = body["due_date"]
        if "tags" in body:
            update_data["tags"] = body["tags"]
        if "metadata" in body:
            update_data["metadata"] = body["metadata"]
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        supabase = get_supabase_service()
        result = supabase.update("tasks", update_data, {"id": task_id, "user_id": user_id})
        
        if result["success"] and result["data"]:
            return create_success_response("Task updated successfully", {"task": result["data"][0]})
        elif result["success"]:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            return create_error_response("Failed to update task", result["error"])
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return create_error_response("Failed to update task", str(e))

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Delete a task"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        result = supabase.delete("tasks", {"id": task_id, "user_id": user_id})
        
        if result["success"]:
            return create_success_response("Task deleted successfully")
        else:
            return create_error_response("Failed to delete task", result["error"])
            
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return create_error_response("Failed to delete task", str(e))

@router.get("/stats/summary")
async def get_task_stats(current_user: Dict = Depends(get_current_user)):
    """Get task statistics for the user"""
    try:
        user_id = current_user["id"]
        supabase = get_supabase_service()
        
        # Get all tasks for the user
        result = supabase.select("tasks", "*", {"user_id": user_id})
        
        if result["success"]:
            tasks = result["data"]
            
            # Calculate statistics
            total = len(tasks)
            completed = len([t for t in tasks if t.get("status") == "completed"])
            pending = len([t for t in tasks if t.get("status") == "pending"])
            in_progress = len([t for t in tasks if t.get("status") == "in_progress"])
            
            # Calculate overdue tasks
            now = datetime.utcnow()
            overdue = 0
            due_today = 0
            
            for task in tasks:
                if task.get("due_date") and task.get("status") != "completed":
                    due_date = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
                    if due_date.date() < now.date():
                        overdue += 1
                    elif due_date.date() == now.date():
                        due_today += 1
            
            stats = {
                "total": total,
                "completed": completed,
                "pending": pending,
                "in_progress": in_progress,
                "overdue": overdue,
                "due_today": due_today,
                "completion_rate": round((completed / total * 100) if total > 0 else 0, 1)
            }
            
            return create_success_response("Task statistics retrieved", {"stats": stats})
        else:
            return create_error_response("Failed to retrieve task statistics", result["error"])
            
    except Exception as e:
        logger.error(f"Error getting task stats: {e}")
        return create_error_response("Failed to retrieve task statistics", str(e))

@router.post("/bulk")
async def bulk_update_tasks(
    request: Request,
    current_user: Dict = Depends(get_current_user)
):
    """Bulk update multiple tasks"""
    try:
        user_id = current_user["id"]
        body = await request.json()
        
        task_updates = body.get("tasks", [])
        if not task_updates:
            raise HTTPException(status_code=400, detail="No tasks provided for update")
        
        supabase = get_supabase_service()
        updated_tasks = []
        
        for task_update in task_updates:
            task_id = task_update.get("id")
            updates = task_update.get("updates", {})
            
            if not task_id or not updates:
                continue
            
            # Add completed_at if status is being set to completed
            if updates.get("status") == "completed":
                updates["completed_at"] = datetime.utcnow().isoformat()
            elif updates.get("status") and updates["status"] != "completed":
                updates["completed_at"] = None
            
            result = supabase.update("tasks", updates, {"id": task_id, "user_id": user_id})
            
            if result["success"] and result["data"]:
                updated_tasks.extend(result["data"])
        
        return create_success_response(
            f"Bulk update completed. {len(updated_tasks)} tasks updated.",
            {"updated_tasks": updated_tasks}
        )
        
    except Exception as e:
        logger.error(f"Error in bulk update: {e}")
        return create_error_response("Failed to perform bulk update", str(e))
