"""
Intelligent Agent Workflows API Router
Provides endpoints for creating and managing intelligent multi-agent workflows
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from .intelligent_agent_workflows import (
    create_intelligent_workflow, 
    execute_intelligent_workflow, 
    get_workflow_status,
    workflow_engine
)
from .auth_middleware import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/intelligent-workflows", tags=["Intelligent Workflows"])

# Request/Response Models
class WorkflowRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    request_message: str = Field(..., description="User's request message")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

class WorkflowResponse(BaseModel):
    success: bool
    workflow_id: str
    status: str
    message: str
    estimated_completion: Optional[str] = None

class WorkflowExecutionRequest(BaseModel):
    workflow_id: str = Field(..., description="Workflow identifier to execute")

class WorkflowExecutionResponse(BaseModel):
    success: bool
    workflow_id: str
    status: str
    results: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None

class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    current_stage: int
    total_stages: int
    completed_tasks: int
    total_tasks: int
    estimated_completion: str
    active_tasks: List[str]

@router.post("/create", response_model=WorkflowResponse)
async def create_workflow(
    request: WorkflowRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Create a new intelligent workflow for complex multi-agent tasks"""
    try:
        logger.info(f"Creating intelligent workflow for user {request.user_id}")
        
        # Create the workflow
        workflow = await create_intelligent_workflow(
            user_id=request.user_id,
            user_request=request.request_message,
            context=request.context
        )
        
        logger.info(f"✅ Workflow created successfully: {workflow.workflow_id}")
        
        return WorkflowResponse(
            success=True,
            workflow_id=workflow.workflow_id,
            status=workflow.status,
            message=f"Intelligent workflow created with {len(workflow.decomposed_tasks)} tasks",
            estimated_completion=workflow.estimated_completion.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")

@router.post("/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(
    request: WorkflowExecutionRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Execute an intelligent workflow"""
    try:
        logger.info(f"Executing workflow: {request.workflow_id}")
        
        # Execute the workflow
        result = await execute_intelligent_workflow(request.workflow_id)
        
        if result.get("success", False):
            logger.info(f"✅ Workflow executed successfully: {request.workflow_id}")
            
            return WorkflowExecutionResponse(
                success=True,
                workflow_id=request.workflow_id,
                status="completed",
                results=result.get("results"),
                execution_time=result.get("execution_time")
            )
        else:
            logger.error(f"❌ Workflow execution failed: {request.workflow_id}")
            
            return WorkflowExecutionResponse(
                success=False,
                workflow_id=request.workflow_id,
                status="failed",
                error=result.get("error", "Unknown error")
            )
        
    except Exception as e:
        logger.error(f"Failed to execute workflow {request.workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")

@router.get("/status/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status_endpoint(
    workflow_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Get the current status of a workflow"""
    try:
        status = get_workflow_status(workflow_id)
        
        if not status:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
        return WorkflowStatusResponse(**status)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow status for {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow status: {str(e)}")

@router.post("/create-and-execute", response_model=WorkflowExecutionResponse)
async def create_and_execute_workflow(
    request: WorkflowRequest,
    current_user: Dict = Depends(get_current_user)
):
    """Create and immediately execute an intelligent workflow (one-step process)"""
    try:
        logger.info(f"Creating and executing workflow for user {request.user_id}")
        
        # Create the workflow
        workflow = await create_intelligent_workflow(
            user_id=request.user_id,
            user_request=request.request_message,
            context=request.context
        )
        
        logger.info(f"✅ Workflow created: {workflow.workflow_id}, now executing...")
        
        # Execute the workflow immediately
        result = await execute_intelligent_workflow(workflow.workflow_id)
        
        if result.get("success", False):
            logger.info(f"✅ Workflow completed successfully: {workflow.workflow_id}")
            
            return WorkflowExecutionResponse(
                success=True,
                workflow_id=workflow.workflow_id,
                status="completed",
                results=result.get("results"),
                execution_time=result.get("execution_time")
            )
        else:
            logger.error(f"❌ Workflow execution failed: {workflow.workflow_id}")
            
            return WorkflowExecutionResponse(
                success=False,
                workflow_id=workflow.workflow_id,
                status="failed",
                error=result.get("error", "Unknown error")
            )
        
    except Exception as e:
        logger.error(f"Failed to create and execute workflow: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create and execute workflow: {str(e)}")

@router.get("/templates")
async def get_workflow_templates(
    current_user: Dict = Depends(get_current_user)
):
    """Get available workflow templates"""
    try:
        templates = workflow_engine.workflow_templates
        
        # Format templates for API response
        formatted_templates = {}
        for template_id, template in templates.items():
            formatted_templates[template_id] = {
                "name": template["name"],
                "description": template["description"],
                "complexity": template["complexity"].value,
                "task_count": len(template["template_tasks"]),
                "estimated_agents": len(set(
                    agent for task in template["template_tasks"] 
                    for agent in task["required_agents"]
                ))
            }
        
        return {
            "success": True,
            "templates": formatted_templates
        }
        
    except Exception as e:
        logger.error(f"Failed to get workflow templates: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workflow templates: {str(e)}")

@router.get("/active")
async def get_active_workflows(
    current_user: Dict = Depends(get_current_user)
):
    """Get all active workflows"""
    try:
        active_workflows = []
        
        for workflow_id, workflow in workflow_engine.active_workflows.items():
            active_workflows.append({
                "workflow_id": workflow_id,
                "user_id": workflow.user_id,
                "status": workflow.status,
                "original_request": workflow.original_request,
                "start_time": workflow.start_time.isoformat(),
                "current_stage": workflow.current_stage,
                "total_stages": len(workflow.execution_plan),
                "completed_tasks": len(workflow.completed_tasks),
                "total_tasks": len(workflow.decomposed_tasks)
            })
        
        return {
            "success": True,
            "active_workflows": active_workflows,
            "total_count": len(active_workflows)
        }
        
    except Exception as e:
        logger.error(f"Failed to get active workflows: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get active workflows: {str(e)}")

@router.delete("/{workflow_id}")
async def cancel_workflow(
    workflow_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """Cancel an active workflow"""
    try:
        if workflow_id in workflow_engine.active_workflows:
            workflow = workflow_engine.active_workflows[workflow_id]
            workflow.status = "cancelled"
            
            logger.info(f"✅ Workflow cancelled: {workflow_id}")
            
            return {
                "success": True,
                "message": f"Workflow {workflow_id} cancelled successfully"
            }
        else:
            raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel workflow: {str(e)}")
