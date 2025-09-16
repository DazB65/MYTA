"""
Advanced Workflow Automation API Router
Provides endpoints for one-click workflows and automation management
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from backend.App.advanced_workflow_automation import (
    execute_one_click_workflow,
    create_automated_workflow,
    check_and_execute_automated_workflows,
    get_available_workflow_templates,
    get_automation_statistics,
    WorkflowCategory,
    AutomationTrigger
)
from backend.App.auth_middleware import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/workflow-automation", tags=["Workflow Automation"])

# Request/Response Models
class OneClickWorkflowRequest(BaseModel):
    template_id: str = Field(..., description="Workflow template identifier")
    user_id: str = Field(..., description="User identifier")
    context: Dict[str, Any] = Field(default_factory=dict, description="Execution context")
    custom_parameters: Optional[Dict[str, Any]] = Field(default=None, description="Custom parameters")

class OneClickWorkflowResponse(BaseModel):
    success: bool
    workflow_name: str
    execution_time: Optional[float] = None
    agents_involved: List[str] = []
    key_insights: List[str] = []
    recommendations: List[str] = []
    action_plan: List[str] = []
    success_metrics: List[str] = []
    expected_outcomes_achieved: List[str] = []
    workflow_id: Optional[str] = None
    execution_id: Optional[str] = None
    error: Optional[str] = None

class AutomatedWorkflowRequest(BaseModel):
    template_id: str = Field(..., description="Workflow template identifier")
    user_id: str = Field(..., description="User identifier")
    trigger_type: str = Field(..., description="Automation trigger type")
    trigger_conditions: Dict[str, Any] = Field(..., description="Trigger conditions")
    schedule: Optional[Dict[str, Any]] = Field(default=None, description="Schedule configuration")

class AutomatedWorkflowResponse(BaseModel):
    success: bool
    workflow_id: str
    template_id: str
    trigger_type: str
    status: str
    next_execution: Optional[str] = None
    message: str

@router.get("/templates")
async def get_workflow_templates(
    category: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    """Get available workflow templates"""
    try:
        workflow_category = None
        if category:
            try:
                workflow_category = WorkflowCategory(category)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        templates = get_available_workflow_templates(workflow_category)
        
        return {
            "success": True,
            "templates": templates,
            "total_count": len(templates)
        }
        
    except Exception as e:
        logger.error(f"Failed to get workflow templates: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow templates: {str(e)}")

@router.post("/execute-one-click", response_model=OneClickWorkflowResponse)
async def execute_one_click_workflow_endpoint(
    request: OneClickWorkflowRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Execute a one-click workflow template"""
    try:
        logger.info(f"Executing one-click workflow: {request.template_id} for user {request.user_id}")
        
        result = await execute_one_click_workflow(
            template_id=request.template_id,
            user_id=request.user_id,
            context=request.context,
            custom_parameters=request.custom_parameters
        )
        
        return OneClickWorkflowResponse(**result)
        
    except ValueError as e:
        logger.error(f"Invalid workflow request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to execute one-click workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")

@router.post("/create-automated", response_model=AutomatedWorkflowResponse)
async def create_automated_workflow_endpoint(
    request: AutomatedWorkflowRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Create an automated workflow"""
    try:
        logger.info(f"Creating automated workflow: {request.template_id} for user {request.user_id}")
        
        # Validate trigger type
        try:
            trigger_type = AutomationTrigger(request.trigger_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid trigger type: {request.trigger_type}")
        
        automated_workflow = await create_automated_workflow(
            template_id=request.template_id,
            user_id=request.user_id,
            trigger_type=trigger_type,
            trigger_conditions=request.trigger_conditions,
            schedule=request.schedule
        )
        
        return AutomatedWorkflowResponse(
            success=True,
            workflow_id=automated_workflow.workflow_id,
            template_id=automated_workflow.template_id,
            trigger_type=automated_workflow.trigger_type.value,
            status=automated_workflow.status,
            next_execution=automated_workflow.next_execution.isoformat() if automated_workflow.next_execution else None,
            message=f"Automated workflow created successfully"
        )
        
    except ValueError as e:
        logger.error(f"Invalid automated workflow request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create automated workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create automated workflow: {str(e)}")

@router.post("/check-triggers/{user_id}")
async def check_automation_triggers(
    user_id: str,
    current_metrics: Dict[str, Any],
    current_user: Dict = Depends(get_current_user)
):
    """Check automation triggers and execute workflows if conditions are met"""
    try:
        logger.info(f"Checking automation triggers for user {user_id}")
        
        executed_workflows = await check_and_execute_automated_workflows(user_id, current_metrics)
        
        return {
            "success": True,
            "user_id": user_id,
            "executed_workflows": executed_workflows,
            "execution_count": len(executed_workflows)
        }
        
    except Exception as e:
        logger.error(f"Failed to check automation triggers for {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to check automation triggers: {str(e)}")

@router.get("/statistics/{user_id}")
async def get_automation_statistics_endpoint(
    user_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get automation statistics for a user"""
    try:
        stats = get_automation_statistics(user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Failed to get automation statistics for {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get automation statistics: {str(e)}")

@router.get("/categories")
async def get_workflow_categories(
    current_user: Dict = Depends(get_current_user)
):
    """Get available workflow categories"""
    try:
        categories = [
            {
                "value": category.value,
                "name": category.value.replace("_", " ").title(),
                "description": f"Workflows focused on {category.value.replace('_', ' ')}"
            }
            for category in WorkflowCategory
        ]
        
        return {
            "success": True,
            "categories": categories
        }
        
    except Exception as e:
        logger.error(f"Failed to get workflow categories: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow categories: {str(e)}")

@router.get("/trigger-types")
async def get_automation_trigger_types(
    current_user: Dict = Depends(get_current_user)
):
    """Get available automation trigger types"""
    try:
        trigger_types = [
            {
                "value": trigger.value,
                "name": trigger.value.replace("_", " ").title(),
                "description": f"Trigger workflows based on {trigger.value.replace('_', ' ')}"
            }
            for trigger in AutomationTrigger
        ]
        
        return {
            "success": True,
            "trigger_types": trigger_types
        }
        
    except Exception as e:
        logger.error(f"Failed to get automation trigger types: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get automation trigger types: {str(e)}")

@router.get("/quick-actions")
async def get_quick_workflow_actions(
    current_user: Dict = Depends(get_current_user)
):
    """Get quick workflow actions for common use cases"""
    try:
        quick_actions = [
            {
                "id": "complete_video_optimization",
                "name": "Optimize My Latest Video",
                "description": "Complete analysis and optimization of your most recent video",
                "icon": "🎯",
                "estimated_time": "15 minutes",
                "complexity": "intermediate"
            },
            {
                "id": "channel_growth_strategy",
                "name": "Boost Channel Growth",
                "description": "Comprehensive strategy for accelerating channel growth",
                "icon": "📈",
                "estimated_time": "25 minutes",
                "complexity": "advanced"
            },
            {
                "id": "monetization_optimization",
                "name": "Maximize Revenue",
                "description": "Optimize all revenue streams and identify new opportunities",
                "icon": "💰",
                "estimated_time": "20 minutes",
                "complexity": "advanced"
            },
            {
                "id": "weekly_performance_review",
                "name": "Weekly Performance Check",
                "description": "Automated weekly analysis of channel performance",
                "icon": "📊",
                "estimated_time": "12 minutes",
                "complexity": "beginner"
            },
            {
                "id": "crisis_management",
                "name": "Emergency Performance Analysis",
                "description": "Rapid response for performance drops or issues",
                "icon": "🚨",
                "estimated_time": "10 minutes",
                "complexity": "expert"
            }
        ]
        
        return {
            "success": True,
            "quick_actions": quick_actions
        }
        
    except Exception as e:
        logger.error(f"Failed to get quick workflow actions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get quick workflow actions: {str(e)}")
