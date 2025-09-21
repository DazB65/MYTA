"""
Background Jobs API Router
Provides endpoints for managing background job processing
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

from .background_job_processor import (
    get_job_processor, submit_background_job, get_job_status,
    JobPriority, JobStatus, JobResult
)
from .auth_middleware import get_current_user
from .response_models import create_success_response, create_error_response

router = APIRouter(prefix="/api/jobs", tags=["Background Jobs"])

# Request models
class JobSubmissionRequest(BaseModel):
    job_type: str
    payload: Dict[str, Any]
    priority: str = "normal"
    max_retries: int = 3
    timeout_seconds: int = 300

class BulkAnalysisRequest(BaseModel):
    video_ids: List[str]
    analysis_type: str = "performance"

class ChannelAuditRequest(BaseModel):
    channel_id: str
    audit_depth: str = "standard"

# Response models
class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    retry_count: int = 0

class JobSubmissionResponse(BaseModel):
    job_id: str
    status: str
    message: str

@router.post("/submit", response_model=JobSubmissionResponse)
async def submit_job(
    request: JobSubmissionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit a background job for processing"""
    try:
        # Validate priority
        try:
            priority = JobPriority[request.priority.upper()]
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid priority. Must be one of: {[p.name.lower() for p in JobPriority]}"
            )
        
        # Add user context to payload
        payload = request.payload.copy()
        payload['user_id'] = current_user['user_id']
        
        # Submit job
        job_id = submit_background_job(
            job_type=request.job_type,
            payload=payload,
            user_id=current_user['user_id'],
            priority=priority,
            max_retries=request.max_retries,
            timeout_seconds=request.timeout_seconds
        )
        
        return JobSubmissionResponse(
            job_id=job_id,
            status="submitted",
            message=f"Job {job_id} submitted successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit job: {str(e)}")

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status_endpoint(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get the status of a background job"""
    try:
        result = get_job_status(job_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobStatusResponse(
            job_id=result.job_id,
            status=result.status.value,
            result=result.result,
            error=result.error,
            started_at=result.started_at,
            completed_at=result.completed_at,
            duration_seconds=result.duration_seconds,
            retry_count=result.retry_count
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job status: {str(e)}")

@router.post("/cancel/{job_id}")
async def cancel_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a pending background job"""
    try:
        processor = get_job_processor()
        success = processor.cancel_job(job_id)
        
        if success:
            return create_success_response(f"Job {job_id} cancelled successfully")
        else:
            raise HTTPException(status_code=400, detail="Job cannot be cancelled (not pending)")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel job: {str(e)}")

@router.get("/stats")
async def get_processor_stats(current_user: dict = Depends(get_current_user)):
    """Get background job processor statistics"""
    try:
        processor = get_job_processor()
        stats = processor.get_stats()
        
        return create_success_response("Job processor statistics", stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

# Convenience endpoints for common job types

@router.post("/ai-analysis")
async def submit_ai_analysis_job(
    messages: List[Dict[str, str]],
    agent_id: str = "1",
    current_user: dict = Depends(get_current_user)
):
    """Submit an AI analysis job"""
    try:
        payload = {
            'messages': messages,
            'agent_id': agent_id,
            'user_id': current_user['user_id']
        }
        
        job_id = submit_background_job(
            job_type="ai_analysis",
            payload=payload,
            user_id=current_user['user_id'],
            priority=JobPriority.HIGH
        )
        
        return create_success_response(
            "AI analysis job submitted",
            {"job_id": job_id}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit AI analysis job: {str(e)}")

@router.post("/bulk-video-analysis")
async def submit_bulk_video_analysis(
    request: BulkAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit a bulk video analysis job"""
    try:
        if len(request.video_ids) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 videos per bulk analysis")
        
        payload = {
            'video_ids': request.video_ids,
            'analysis_type': request.analysis_type,
            'user_id': current_user['user_id']
        }
        
        # Estimate timeout based on number of videos
        timeout_seconds = min(len(request.video_ids) * 10, 1800)  # Max 30 minutes
        
        job_id = submit_background_job(
            job_type="bulk_video_analysis",
            payload=payload,
            user_id=current_user['user_id'],
            priority=JobPriority.NORMAL,
            timeout_seconds=timeout_seconds
        )
        
        return create_success_response(
            f"Bulk analysis job submitted for {len(request.video_ids)} videos",
            {
                "job_id": job_id,
                "estimated_duration_minutes": timeout_seconds // 60
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit bulk analysis job: {str(e)}")

@router.post("/channel-audit")
async def submit_channel_audit(
    request: ChannelAuditRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit a comprehensive channel audit job"""
    try:
        payload = {
            'channel_id': request.channel_id,
            'audit_depth': request.audit_depth,
            'user_id': current_user['user_id']
        }
        
        # Set timeout based on audit depth
        timeout_map = {
            'quick': 300,      # 5 minutes
            'standard': 900,   # 15 minutes
            'comprehensive': 1800  # 30 minutes
        }
        timeout_seconds = timeout_map.get(request.audit_depth, 900)
        
        job_id = submit_background_job(
            job_type="channel_audit",
            payload=payload,
            user_id=current_user['user_id'],
            priority=JobPriority.HIGH,
            timeout_seconds=timeout_seconds
        )
        
        return create_success_response(
            f"Channel audit job submitted ({request.audit_depth} depth)",
            {
                "job_id": job_id,
                "estimated_duration_minutes": timeout_seconds // 60
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit channel audit job: {str(e)}")

@router.get("/user-jobs")
async def get_user_jobs(
    status: Optional[str] = None,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Get jobs for the current user"""
    try:
        # This would need to be implemented in the job processor
        # to query jobs by user_id and optionally filter by status
        
        # Placeholder response
        return create_success_response(
            "User jobs retrieved",
            {
                "jobs": [],
                "total": 0,
                "message": "Job history feature coming soon"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user jobs: {str(e)}")

@router.post("/start-workers")
async def start_workers(
    num_workers: int = 4,
    current_user: dict = Depends(get_current_user)
):
    """Start background job workers (admin only)"""
    try:
        # Check if user is admin (you'd implement this check)
        if not current_user.get('is_admin', False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        processor = get_job_processor()
        processor.start_workers(num_workers)
        
        return create_success_response(f"Started {num_workers} background workers")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start workers: {str(e)}")

@router.post("/stop-workers")
async def stop_workers(current_user: dict = Depends(get_current_user)):
    """Stop background job workers (admin only)"""
    try:
        # Check if user is admin
        if not current_user.get('is_admin', False):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        processor = get_job_processor()
        processor.stop_workers()
        
        return create_success_response("Stopped background workers")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop workers: {str(e)}")
